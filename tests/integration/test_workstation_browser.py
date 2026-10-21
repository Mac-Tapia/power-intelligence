"""Headless browser acceptance against a running authenticated localhost API."""

import hashlib
import json
import secrets
import socket
import sys
import threading
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(src))
sys.path.insert(0, str(ROOT / "apps/control-api/src"))


def test_authenticated_ui_runs_and_logs_out(tmp_path, monkeypatch):
    uvicorn = pytest.importorskip("uvicorn")
    pytest.importorskip("playwright")
    from playwright.sync_api import expect, sync_playwright
    from unitesis_api.main import create_app

    token = secrets.token_urlsafe(32)
    path = tmp_path / "credentials.json"
    path.write_text(json.dumps({"schema": "unitesis.credentials/1", "grants": [{
        "token_sha256": hashlib.sha256(token.encode()).hexdigest(), "tenant_id": "test",
        "subject": "browser", "role": "engineer", "expires_at": int(time.time()) + 600}]}))
    monkeypatch.setenv("UNITESIS_LOCAL_ONLY", "1")
    monkeypatch.setenv("UNITESIS_CREDENTIALS_FILE", str(path))
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(create_app(tmp_path / "api.sqlite"),
        host="127.0.0.1", port=port, log_level="error", access_log=False))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 15
        while not server.started and time.monotonic() < deadline:
            time.sleep(0.05)
        assert server.started
        with sync_playwright() as playwright:
            if not Path(playwright.chromium.executable_path).is_file():
                pytest.skip("Chromium not installed in this environment")
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            events = []
            page.on("pageerror", lambda error: events.append(str(error)))
            page.on("response", lambda response: events.append(
                f"{response.status} {response.url.split('/api/v1/')[-1]}"))
            page.goto(f"http://127.0.0.1:{port}")
            expect(page.locator("#access-msg")).to_contain_text("Ingrese una credencial")
            page.locator("#access-token").fill(token)
            page.locator("#connect-access").click()
            expect(page.locator("#access-msg")).to_contain_text("Sesión autenticada")
            assert page.evaluate("localStorage.length + sessionStorage.length") == 0
            page.locator("#example").select_option("radial_feeder_6bus")
            page.locator("#load-example").click()
            expect(page.locator("#run-flow")).to_be_enabled()
            page.locator("#run-flow").click()
            try:
                expect(page.locator("#flow-out")).to_contain_text("passed", timeout=30000)
            except AssertionError:
                (tmp_path / "browser-events.json").write_text(json.dumps(events), encoding="utf-8")
                raise
            page.locator("#disconnect-access").click()
            expect(page.locator("#access-msg")).to_contain_text("Ingrese una credencial")
            browser.close()
    finally:
        server.should_exit = True
        thread.join(timeout=15)
        assert not thread.is_alive()
