"""HTTP telemetry must be useful while omitting credentials and raw URL identifiers."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(src))
sys.path.insert(0, str(ROOT / "apps/control-api/src"))


def test_structured_audit_omits_request_data_and_includes_trace(monkeypatch, caplog):
    from fastapi.testclient import TestClient
    from unitesis_api.main import create_app

    monkeypatch.setenv("UNITESIS_LOCAL_ONLY", "1")
    monkeypatch.delenv("UNITESIS_CREDENTIALS_FILE", raising=False)
    caplog.set_level("INFO", logger="unitesis.audit")
    with TestClient(create_app(":memory:")) as client:
        response = client.get("/api/v1/private-customer?token=private-token",
                              headers={"Authorization": "Bearer private-credential"})
        assert response.status_code == 404
        assert len(response.headers["x-request-id"]) == 32
        metrics = client.get("/api/v1/metrics").json()
        assert metrics["requests"] >= 1
    events = [json.loads(r.message) for r in caplog.records if r.name == "unitesis.audit"]
    assert any(e["status"] == 404 and e["resource"] == "other" for e in events)
    assert "private-" not in json.dumps(events)
