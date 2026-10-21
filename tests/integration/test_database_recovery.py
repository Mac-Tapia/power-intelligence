"""A restored database must serve real job results and retain append-only protection."""

import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/dev"))
for src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(src))
sys.path.insert(0, str(ROOT / "apps/control-api/src"))


def test_backup_restore_serves_study_and_protects_snapshot(tmp_path, monkeypatch):
    from database_backup import backup_database, restore_database
    from fastapi.testclient import TestClient
    from unitesis_api.main import create_app

    monkeypatch.setenv("UNITESIS_LOCAL_ONLY", "1")
    source = tmp_path / "api.sqlite"
    with TestClient(create_app(source)) as client:
        sha = client.post("/api/v1/snapshots", json=json.loads((ROOT / "fixtures/networks/"
                "radial_feeder_6bus.json").read_text())).json()["snapshot_sha256"]
        job = client.post("/api/v1/studies", json={"snapshot_sha256": sha}).json()
        result = client.get(f"/api/v1/jobs/{job['job_id']}").json()
    backup, restored = tmp_path / "backup.sqlite", tmp_path / "restored.sqlite"
    report = backup_database(source, backup)
    assert report["counts"]["study_result"] == 2
    assert report["counts"]["study_job"] == 1
    assert len(report["sha256"]) == 64
    assert restore_database(backup, restored)["counts"] == report["counts"]
    with TestClient(create_app(restored)) as client:
        assert client.get(f"/api/v1/jobs/{job['job_id']}").json() == result
        assert client.get(f"/api/v1/snapshots/{sha}").json()["snapshot_sha256"] == sha
        for digest in result["result_sha256"]:
            assert client.get(f"/api/v1/results/{digest}").json()["status"] == "computed"
    with sqlite3.connect(restored) as db, pytest.raises(sqlite3.IntegrityError):
        db.execute("DELETE FROM electrical_snapshot")


def test_bad_inputs_do_not_create_or_overwrite_destination(tmp_path):
    from database_backup import backup_database, restore_database

    destination = tmp_path / "out.sqlite"
    with pytest.raises((ValueError, OSError)):
        backup_database(tmp_path / "missing.sqlite", destination)
    assert not destination.exists()
    bad = tmp_path / "bad.sqlite"
    bad.write_bytes(b"corrupt database")
    with pytest.raises((ValueError, sqlite3.DatabaseError)):
        restore_database(bad, destination)
    assert not destination.exists()
    with sqlite3.connect(tmp_path / "foreign.sqlite") as db:
        db.execute("CREATE TABLE unrelated(x)")
    with pytest.raises(ValueError):
        backup_database(tmp_path / "foreign.sqlite", destination)
    destination.write_bytes(b"preserve original")
    with pytest.raises((ValueError, OSError)):
        restore_database(bad, destination)
    assert destination.read_bytes() == b"preserve original"


def test_backup_cli_rejects_external_destination(tmp_path):
    from database_backup import main

    assert main(["backup", "--source", str(tmp_path / "in.sqlite"),
                 "--destination", str(tmp_path / "out.sqlite")]) == 2
