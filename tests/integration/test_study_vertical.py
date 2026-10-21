"""Study vertical end to end: unified CLI exit codes, new-load scenario, evidence, control-api."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))
sys.path.insert(0, str(ROOT / "apps/control-api/src"))

from unitesis_evidence import read_evidence  # noqa: E402

CLI = ROOT / "scripts/unitesis.py"
FEEDER = ROOT / "fixtures/networks/radial_feeder_6bus.json"
try:
    import pandapower  # noqa: F401
    HAS_PP = True
except Exception:
    HAS_PP = False
try:
    import fastapi  # noqa: F401
    import httpx  # noqa: F401
    HAS_API = True
except Exception:
    HAS_API = False


def run_cli(*args):
    return subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True,
                          text=True, timeout=180, check=False)


class CliTests(unittest.TestCase):
    @unittest.skipUnless(HAS_PP, "pandapower required for the independent reference")
    def test_full_vertical_passes_and_evidence_rereads(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "ev.json"
            proc = run_cli("study", "--input", FEEDER, "--output", out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            ev = read_evidence(out)
            self.assertEqual(ev["comparison"]["status"], "passed")
            self.assertFalse(ev["technical_acceptance"])
            self.assertEqual(ev["snapshot_sha256"], ev["source_manifest"]["snapshot_sha256"])

    def test_quarantined_input_exit_2(self):
        data = json.loads(FEEDER.read_text(encoding="utf-8"))
        del data["network"]["lines"][0]["length_km"]
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "bad.json"
            src.write_text(json.dumps(data), encoding="utf-8")
            proc = run_cli("study", "--input", src, "--output", Path(tmp) / "ev.json")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("length_km", proc.stderr)
            self.assertFalse((Path(tmp) / "ev.json").exists())

    @unittest.skipUnless(HAS_PP, "pandapower required")
    def test_new_load_scenario_does_not_touch_source(self):
        before = FEEDER.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "nl.json"
            proc = run_cli("new-load", "--input", FEEDER, "--output", out, "--load-id", "NL1",
                           "--bus", "B3", "--p-mw", "6.0", "--q-mvar", "2.0")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            ev = read_evidence(out)
            self.assertNotEqual(ev["before"]["snapshot_sha256"], ev["after"]["snapshot_sha256"])
            self.assertEqual(ev["screening"], "violations")  # 6 MW at B3 overloads L13
            self.assertLess(ev["after"]["summary"]["min_vm_pu"],
                            ev["before"]["summary"]["min_vm_pu"])
        self.assertEqual(FEEDER.read_bytes(), before)


@unittest.skipUnless(HAS_API and HAS_PP, "fastapi/httpx/pandapower required")
class ControlApiTests(unittest.TestCase):
    def setUp(self):
        os.environ["UNITESIS_LOCAL_ONLY"] = "1"
        from fastapi.testclient import TestClient
        from unitesis_api.main import create_app
        self.client = TestClient(create_app(":memory:"))

    def test_import_study_and_fetch_results(self):
        payload = json.loads(FEEDER.read_text(encoding="utf-8"))
        r = self.client.post("/api/v1/snapshots", json=payload)
        self.assertEqual(r.status_code, 201, r.text)
        sha = r.json()["snapshot_sha256"]
        job = self.client.post("/api/v1/studies", json={"snapshot_sha256": sha}).json()
        done = self.client.get(f"/api/v1/jobs/{job['job_id']}").json()
        self.assertEqual(done["status"], "finished", done)
        self.assertEqual(done["comparison"], "passed")
        res = self.client.get(f"/api/v1/results/{done['result_sha256'][0]}").json()
        self.assertEqual(res["status"], "computed")
        self.assertEqual(len(self.client.get(f"/api/v1/snapshots/{sha}").json()["results"]), 2)

    def test_quarantined_upload_is_422_with_reasons(self):
        payload = json.loads(FEEDER.read_text(encoding="utf-8"))
        del payload["network"]["loads"][0]["q_mvar"]
        r = self.client.post("/api/v1/snapshots", json=payload)
        self.assertEqual(r.status_code, 422)
        self.assertEqual(r.json()["detail"]["quarantine"][0]["field"], "q_mvar")

    def test_unknown_snapshot_404_and_new_load_job(self):
        self.assertEqual(self.client.post("/api/v1/studies",
                                          json={"snapshot_sha256": "0" * 64}).status_code, 404)
        sha = self.client.post("/api/v1/snapshots", json=json.loads(
            FEEDER.read_text(encoding="utf-8"))).json()["snapshot_sha256"]
        job = self.client.post("/api/v1/studies/new-load", json={
            "snapshot_sha256": sha, "load_id": "NL", "bus": "B2", "p_mw": 0.5,
            "q_mvar": 0.1}).json()
        done = self.client.get(f"/api/v1/jobs/{job['job_id']}").json()
        self.assertEqual(done["status"], "finished", done)
        self.assertNotEqual(done["scenario_snapshot_sha256"], sha)

    def test_refuses_to_start_without_local_flag(self):
        from unitesis_api.main import create_app
        os.environ.pop("UNITESIS_LOCAL_ONLY")
        with self.assertRaises(RuntimeError):
            create_app(":memory:")


if __name__ == "__main__":
    unittest.main()
