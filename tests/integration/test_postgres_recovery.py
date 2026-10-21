"""Native pg_dump/pg_restore recovery into a new sandbox database."""

import os
import sys
import uuid
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/dev"))
for src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(src))


def test_pg_dump_restore_preserves_effective_engine_results(tmp_path):
    dsn = os.environ.get("UNITESIS_TEST_POSTGRES_DSN")
    container = os.environ.get("UNITESIS_TEST_POSTGRES_CONTAINER")
    if not dsn or not container:
        pytest.skip("explicit local PostgreSQL container sandbox not supplied")
    from postgres_backup import backup_namespace, restore_namespace
    from psycopg.conninfo import conninfo_to_dict, make_conninfo
    from unitesis_adapters.neutral_json import ingest_file
    from unitesis_adapters.postgres_repository import PostgresRepository
    from unitesis_application.study import solve_and_compare

    namespace = "recovery_" + uuid.uuid4().hex[:10]
    repo = PostgresRepository(dsn, namespace=namespace, initialize=True)
    source = ingest_file(ROOT / "fixtures/networks/radial_feeder_6bus.json")
    snap = source.require_snapshot()
    sha = repo.save_snapshot(snap, source.manifest)
    key = repo.save_result(solve_and_compare(snap, "backup")["candidate"])
    artifact = tmp_path / "backup.dump"
    report = backup_namespace(container, conninfo_to_dict(dsn)["dbname"], namespace, artifact)
    assert report["bytes"] > 0
    restored_db = "unitesis_restore_" + uuid.uuid4().hex[:10]
    restore_namespace(container, restored_db, artifact)
    restored = PostgresRepository(make_conninfo(dsn, dbname=restored_db), namespace=namespace)
    assert restored.load_snapshot(sha).content_sha256 == sha
    assert restored.get_result(key)["status"] == "computed"
    with pytest.raises((ValueError, FileExistsError)):
        backup_namespace(container, conninfo_to_dict(dsn)["dbname"], namespace, artifact)
