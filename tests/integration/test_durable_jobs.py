"""Real studies and jobs remain available across API lifetimes."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(src))
sys.path.insert(0, str(ROOT / "apps/control-api/src"))

from fastapi.testclient import TestClient
from unitesis_api.main import create_app

FEEDER = ROOT / "fixtures/networks/radial_feeder_6bus.json"


def test_integer_voltage_json_runs_after_sqlite_reread(tmp_path, monkeypatch):
    """JSON.stringify serializes 1.0 as 1; the solver must accept either representation."""
    monkeypatch.setenv("UNITESIS_LOCAL_ONLY", "1")
    body = json.loads(FEEDER.read_text())
    for slack in body["network"]["slacks"]:
        slack["vm_pu"] = 1
    with TestClient(create_app(tmp_path / "integer.sqlite")) as client:
        sha = client.post("/api/v1/snapshots", json=body).json()["snapshot_sha256"]
        job = client.post("/api/v1/studies", json={"snapshot_sha256": sha}).json()
        done = client.get(f"/api/v1/jobs/{job['job_id']}").json()
        assert done["status"] == "finished", done
        assert done["comparison"] == "passed"


@pytest.mark.parametrize("kind", ["study", "new_load", "alternatives"])
def test_jobs_survive_restart(tmp_path, monkeypatch, kind):
    monkeypatch.setenv("UNITESIS_LOCAL_ONLY", "1")
    db = tmp_path / "api.sqlite"
    with TestClient(create_app(db)) as client:
        sha = client.post("/api/v1/snapshots", json=json.loads(FEEDER.read_text())).json()[
            "snapshot_sha256"]
        body = {"snapshot_sha256": sha}
        endpoint = "/api/v1/studies"
        if kind == "new_load":
            endpoint += "/new-load"
            body.update(load_id="NL", bus="B3", p_mw=0.5, q_mvar=0.2)
        elif kind == "alternatives":
            endpoint += "/conductor-alternatives"
            body.update(line_id="L13", catalog_id="aaac6201_nexans_reference",
                        operating_temperature_c=75, phase_gmd_m=1.2,
                        economic_basis=json.loads((ROOT / "fixtures/economics/"
                            "conductor_alternatives_synthetic.json").read_text()))
        response = client.post(endpoint, json=body)
        assert response.status_code == 202, response.text
        job_id = response.json()["job_id"]
        done = client.get(f"/api/v1/jobs/{job_id}").json()
        assert done["status"] == "finished", done
    with TestClient(create_app(db)) as reopened:
        reread = reopened.get(f"/api/v1/jobs/{job_id}")
        assert reread.status_code == 200
        assert reread.json() == done
        if kind != "alternatives":
            assert done["comparison"] == "passed"
            assert len(done["result_sha256"]) == 2
            for digest in done["result_sha256"]:
                assert reopened.get(f"/api/v1/results/{digest}").json()["status"] == "computed"
        else:
            assert done["request"]["economic_basis"] == body["economic_basis"]
            assert len(done["request"]["catalog_sha256"]) == 64
        assert reopened.get("/api/v1/jobs/unknown").status_code == 404


def test_interrupted_and_queued_jobs_on_restart(tmp_path, monkeypatch):
    from unitesis_adapters.job_repository import SqliteJobRepository

    monkeypatch.setenv("UNITESIS_LOCAL_ONLY", "1")
    db = tmp_path / "api.sqlite"
    jobs = SqliteJobRepository(db)
    jobs.enqueue("running", "study", {})
    jobs.enqueue("queued", "study", {})
    jobs.claim("running")
    jobs.close()
    with TestClient(create_app(db)) as client:
        failed = client.get("/api/v1/jobs/running").json()
        assert failed["status"] == "failed"
        assert failed["error_code"] == "interrupted"
        assert client.get("/api/v1/jobs/queued").json()["status"] == "queued"


def test_nonfinite_input_is_rejected_without_echoing_private_request(monkeypatch):
    monkeypatch.setenv("UNITESIS_LOCAL_ONLY", "1")
    with TestClient(create_app(":memory:"), raise_server_exceptions=False) as client:
        body = {"snapshot_sha256": "a" * 64, "load_id": "private-customer",
                "bus": "B3", "p_mw": float("inf"), "q_mvar": 0}
        response = client.post("/api/v1/studies/new-load", content=json.dumps(body),
                               headers={"content-type": "application/json"})
        assert response.status_code == 422
        assert "private-customer" not in response.text
        assert "Infinity" not in response.text
