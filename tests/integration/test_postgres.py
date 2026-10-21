"""Native PostgreSQL/PostGIS acceptance; opt in with a dedicated sandbox DSN."""

import json
import os
import subprocess
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(src))


def test_unmigrated_postgres_namespace_fails_at_startup():
    dsn = os.environ.get("UNITESIS_TEST_POSTGRES_DSN")
    if not dsn:
        pytest.skip("dedicated PostgreSQL sandbox DSN not supplied")
    from unitesis_adapters.postgres_repository import PostgresRepository
    from unitesis_adapters.sql_repository import RepositoryIntegrityError

    with pytest.raises(RepositoryIntegrityError, match="migration"):
        PostgresRepository(dsn, namespace="missing_" + uuid.uuid4().hex[:12])


@pytest.mark.parametrize("fixture", ["radial_feeder_6bus.json", "mv_lv_transformers.json"])
def test_native_postgres_reread_append_only_and_atomic_jobs(fixture):
    dsn = os.environ.get("UNITESIS_TEST_POSTGRES_DSN")
    if not dsn:
        pytest.skip("dedicated PostgreSQL sandbox DSN not supplied")
    psycopg = pytest.importorskip("psycopg")
    from unitesis_adapters.neutral_json import ingest_file
    from unitesis_adapters.postgres_repository import PostgresJobRepository, PostgresRepository
    from unitesis_application.study import solve_and_compare
    from unitesis_simulation import NewtonRaphsonEngine

    namespace = "acceptance_" + uuid.uuid4().hex[:12]
    repo = PostgresRepository(dsn, namespace=namespace, initialize=True)
    imported = ingest_file(ROOT / "fixtures/networks" / fixture)
    snapshot = imported.require_snapshot()
    sha = repo.save_snapshot(snapshot, imported.manifest)
    assert repo.save_snapshot(snapshot, imported.manifest) == sha
    assert PostgresRepository(dsn, namespace=namespace).load_snapshot(sha).content_sha256 == sha
    result = solve_and_compare(snapshot, "base", candidate=NewtonRaphsonEngine())
    key = repo.save_result(result["candidate"])
    assert repo.get_result(key)["status"] == "computed"
    assert repo.list_snapshots()[0]["snapshot_sha256"] == sha
    assert len(repo.results_for_snapshot(sha)) == 1
    with psycopg.connect(dsn) as conn, pytest.raises(psycopg.Error):
        from psycopg import sql

        conn.execute(sql.SQL("DELETE FROM {}.electrical_snapshot").format(
            sql.Identifier(namespace)))
    jobs = [PostgresJobRepository(dsn, namespace=namespace) for _ in range(2)]
    jobs[0].enqueue("study", "study", {"snapshot_sha256": sha})
    with ThreadPoolExecutor(2) as pool:
        assert sorted(pool.map(lambda r: r.claim("study"), jobs)) == [False, True]
    jobs[0].finish("study", {"result_sha256": [key]})
    assert jobs[1].get("study")["status"] == "finished"
    with pytest.raises(ValueError):
        jobs[1].finish("study", {})


def test_api_queue_and_independent_postgres_worker(tmp_path, monkeypatch):
    dsn = os.environ.get("UNITESIS_TEST_POSTGRES_DSN")
    if not dsn:
        pytest.skip("dedicated PostgreSQL sandbox DSN not supplied")
    from unitesis_adapters.postgres_repository import PostgresRepository

    sys.path.insert(0, str(ROOT / "apps/control-api/src"))
    from fastapi.testclient import TestClient
    from unitesis_api.main import create_app

    namespace = "worker_" + uuid.uuid4().hex[:12]
    PostgresRepository(dsn, namespace=namespace, initialize=True)
    monkeypatch.setenv("UNITESIS_LOCAL_ONLY", "1")
    monkeypatch.delenv("UNITESIS_CREDENTIALS_FILE", raising=False)
    monkeypatch.setenv("UNITESIS_POSTGRES_DSN", dsn)
    monkeypatch.setenv("UNITESIS_POSTGRES_NAMESPACE", namespace)
    monkeypatch.setenv("UNITESIS_EXECUTION_MODE", "worker")
    with TestClient(create_app(tmp_path / "unused.sqlite")) as client:
        body = json.loads((ROOT / "fixtures/networks/radial_feeder_6bus.json").read_text())
        sha = client.post("/api/v1/snapshots", json=body).json()["snapshot_sha256"]
        response = client.post("/api/v1/studies", json={"snapshot_sha256": sha})
        assert response.status_code == 202
        job_id = response.json()["job_id"]
        assert client.get(f"/api/v1/jobs/{job_id}").json()["status"] == "queued"
    process = subprocess.run([sys.executable, str(ROOT / "scripts/unitesis.py"),
        "postgres-worker", "--namespace", namespace, "--job-id", job_id],
        capture_output=True, text=True, timeout=60)
    assert process.returncode == 0, "worker failed (credentials omitted)"
    assert json.loads(process.stdout)["comparison"] == "passed"
    with TestClient(create_app(tmp_path / "unused.sqlite")) as client:
        done = client.get(f"/api/v1/jobs/{job_id}").json()
        assert done["status"] == "finished"
        assert done["comparison"] == "passed"
        assert len(done["result_sha256"]) == 2
