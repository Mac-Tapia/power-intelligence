"""Authentication and cross-tenant denial against real independent databases."""

import hashlib
import json
import secrets
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(src))
sys.path.insert(0, str(ROOT / "apps/control-api/src"))
from fastapi.testclient import TestClient
from unitesis_api.main import create_app


def setup_auth(tmp_path, monkeypatch):
    tokens = {name: secrets.token_urlsafe(32) for name in ["alpha", "beta", "reader", "expired"]}
    grants = [{"token_sha256": hashlib.sha256(token.encode()).hexdigest(),
               "tenant_id": "beta" if name == "beta" else "alpha", "subject": name,
               "role": "reader" if name == "reader" else "engineer",
               "expires_at": int(time.time()) + (-10 if name == "expired" else 3600)}
              for name, token in tokens.items()]
    path = tmp_path / "credentials.json"
    path.write_text(json.dumps({"schema": "unitesis.credentials/1", "grants": grants}))
    monkeypatch.setenv("UNITESIS_LOCAL_ONLY", "1")
    monkeypatch.setenv("UNITESIS_CREDENTIALS_FILE", str(path))
    return tokens, path


def test_roles_and_tenant_data_isolation(tmp_path, monkeypatch):
    tokens, _ = setup_auth(tmp_path, monkeypatch)
    headers = lambda name: {"Authorization": "Bearer " + tokens[name]}  # noqa: E731
    with TestClient(create_app(tmp_path / "base.sqlite")) as client:
        assert client.get("/api/v1/snapshots").status_code == 401
        assert client.get("/api/v1/snapshots", headers=headers("expired")).status_code == 401
        payload = json.loads((ROOT / "fixtures/networks/radial_feeder_6bus.json").read_text())
        assert client.post("/api/v1/snapshots", json=payload,
                           headers=headers("reader")).status_code == 403
        imported = client.post("/api/v1/snapshots", json=payload, headers=headers("alpha"))
        assert imported.status_code == 201
        sha = imported.json()["snapshot_sha256"]
        assert len(client.get("/api/v1/snapshots", headers=headers("reader")).json()) == 1
        assert client.get("/api/v1/snapshots", headers=headers("beta")).json() == []
        assert client.get(f"/api/v1/snapshots/{sha}", headers=headers("beta")).status_code == 404
        job = client.post("/api/v1/studies", json={"snapshot_sha256": sha},
                          headers=headers("alpha")).json()
        path = f"/api/v1/jobs/{job['job_id']}"
        assert client.get(path, headers=headers("beta")).status_code == 404
        done = client.get(path, headers=headers("alpha")).json()
        assert done["comparison"] == "passed"
        for digest in done["result_sha256"]:
            assert client.get(f"/api/v1/results/{digest}",
                              headers=headers("beta")).status_code == 404


def test_invalid_tenant_config_fails_before_creating_stores(tmp_path, monkeypatch):
    _, path = setup_auth(tmp_path, monkeypatch)
    data = json.loads(path.read_text())
    data["grants"][0]["tenant_id"] = "../outside"
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        create_app(tmp_path / "base.sqlite")
    assert not (tmp_path / "base.tenants").exists()
