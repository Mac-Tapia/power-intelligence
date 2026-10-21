"""Integral platform: techno-economic alternatives, unified CLI, control-api v0.2 and UI."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))
sys.path.insert(0, str(ROOT / "apps/control-api/src"))

from unitesis_adapters.neutral_json import ingest_file  # noqa: E402
from unitesis_application.alternatives import evaluate_conductor_alternatives  # noqa: E402
from unitesis_economics import load_basis  # noqa: E402
from unitesis_evidence import read_evidence  # noqa: E402
from unitesis_optimization import SizingCriteria, load_catalog  # noqa: E402
from unitesis_ports import EngineUnavailable  # noqa: E402
from unitesis_simulation import RadialBFSEngine  # noqa: E402

CLI = ROOT / "scripts/unitesis.py"
FEEDER = ROOT / "fixtures/networks/radial_feeder_6bus.json"
CATALOG = ROOT / "config/catalogs/conductors/aaac6201_nexans_reference.json"
BASIS = ROOT / "fixtures/economics/conductor_alternatives_synthetic.json"
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


class _Unavailable:
    name = "absent-reference"

    def version(self):
        return "n/a"

    def solve(self, snapshot, request):
        raise EngineUnavailable("reference runtime not installed")


class _SecondBFS(RadialBFSEngine):
    """Same equations under another identity: stands in for an independent reference."""

    name = "second-bfs-reference"


class _Biased(RadialBFSEngine):
    """Reference that disagrees with the candidate: comparison must fail."""

    name = "biased-reference"

    def solve(self, snapshot, request):
        res = super().solve(snapshot, request)
        return replace(res, buses=tuple(replace(b, vm_pu=b.vm_pu * 0.99) for b in res.buses))


def cli(*args):
    return subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True,
                          text=True, timeout=300, check=False)


class AlternativesUseCaseTests(unittest.TestCase):
    def setUp(self):
        self.snap = ingest_file(FEEDER).require_snapshot()
        self.catalog = load_catalog(CATALOG)
        self.criteria = SizingCriteria(75.0, 1.2)
        self.basis = load_basis(BASIS)

    def evaluate(self, **kw):
        return evaluate_conductor_alternatives(self.snap, "L13", self.catalog, self.criteria,
                                               self.basis, **kw)

    def test_unavailable_reference_never_ranks(self):
        report = self.evaluate(reference=_Unavailable())
        self.assertEqual(report["ranking"], [])
        self.assertIsNone(report["recommended"])
        self.assertTrue(all(a["independent_check"] in ("unavailable", "not_run")
                            for a in report["alternatives"]))
        self.assertFalse(report["technical_acceptance"])

    def test_failed_comparison_is_not_feasible(self):
        report = self.evaluate(reference=_Biased())
        self.assertEqual(report["ranking"], [])
        self.assertTrue(all(a["technical_feasible"] is False for a in report["alternatives"]))

    def test_unpriced_alternatives_are_reported_not_ranked(self):
        self.basis = replace(self.basis, conductor_cost_per_km=(("nexans-aaac6201-70-19",
                                                                 11500.0),))
        report = self.evaluate(reference=_SecondBFS())
        self.assertEqual([r["alternative_id"] for r in report["ranking"]],
                         ["nexans-aaac6201-70-19"])
        unpriced = [a for a in report["alternatives"] if "unpriced_reason" in a]
        self.assertEqual(len(unpriced), 3)

    def test_source_snapshot_untouched(self):
        before = self.snap.content_sha256
        self.evaluate(reference=_SecondBFS())
        self.assertEqual(self.snap.content_sha256, before)

    @unittest.skipUnless(HAS_PP, "pandapower required")
    def test_ranking_by_npv_with_independent_check(self):
        report = self.evaluate()
        npv = [r["npv_total_cost"] for r in report["ranking"]]
        self.assertEqual(npv, sorted(npv))
        self.assertEqual(report["recommended"], report["ranking"][0]["alternative_id"])
        self.assertTrue(all(a["independent_check"] == "passed" for a in report["alternatives"]
                            if a["technical_feasible"]))


class UnifiedCliTests(unittest.TestCase):
    @unittest.skipUnless(HAS_PP, "pandapower required")
    def test_study_alternatives_and_verify(self):
        with tempfile.TemporaryDirectory() as tmp:
            ev = Path(tmp) / "base.json"
            proc = cli("study", "--input", FEEDER, "--output", ev)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(cli("verify-evidence", ev).returncode, 0)
            alt = Path(tmp) / "alt.json"
            proc = cli("alternatives", "--input", FEEDER, "--output", alt, "--line", "L13",
                       "--catalog", CATALOG, "--basis", BASIS, "--temperature-c", "75",
                       "--gmd-m", "1.2")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = read_evidence(alt)
            self.assertEqual(payload["schema"], "unitesis.alternatives-evidence/1")
            self.assertIsNotNone(payload["recommended"])

    @unittest.skipUnless(HAS_PP, "pandapower required")
    def test_criteria_precedence_flag_over_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "nl.json"
            base = ("new-load", "--input", FEEDER, "--output", out, "--load-id", "NL",
                    "--bus", "B3", "--p-mw", "0.5", "--q-mvar", "0.1", "--case",
                    "pe-ica-electrodunas")
            self.assertEqual(cli(*base).returncode, 0)
            crit = read_evidence(out)["request"]["criteria"]
            self.assertTrue(crit["source"].startswith("case:pe-ica-electrodunas"))
            self.assertEqual(cli(*base, "--v-min-pu", "0.97").returncode, 0)
            crit = read_evidence(out)["request"]["criteria"]
            self.assertEqual(crit["v_min_pu"], 0.97)
            self.assertIn("explicit override", crit["source"])

    def test_corrupt_evidence_exit_6(self):
        with tempfile.TemporaryDirectory() as tmp:
            ev = Path(tmp) / "ev.json"
            ev.write_text(json.dumps({"schema": "power-intelligence.evidence/1",
                                      "payload_sha256": "0" * 64, "payload": {"a": 1}}),
                          encoding="utf-8")
            self.assertEqual(cli("verify-evidence", ev).returncode, 6)

    def test_invalid_basis_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "basis.json"
            data = json.loads(BASIS.read_text(encoding="utf-8"))
            del data["discount_rate"]
            bad.write_text(json.dumps(data), encoding="utf-8")
            proc = cli("alternatives", "--input", FEEDER, "--output", Path(tmp) / "a.json",
                       "--line", "L13", "--catalog", CATALOG, "--basis", bad,
                       "--temperature-c", "75", "--gmd-m", "1.2")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("discount_rate", proc.stderr)

    def test_serve_refuses_non_local_bind(self):
        proc = cli("serve", "--host", "0.0.0.0")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("localhost", proc.stderr)


@unittest.skipUnless(HAS_API and HAS_PP, "fastapi/httpx/pandapower required")
class ControlApiV02Tests(unittest.TestCase):
    def setUp(self):
        os.environ["UNITESIS_LOCAL_ONLY"] = "1"
        from fastapi.testclient import TestClient
        from unitesis_api.main import create_app
        self.client = TestClient(create_app(":memory:"))
        self.sha = self.client.post("/api/v1/snapshots", json=json.loads(
            FEEDER.read_text(encoding="utf-8"))).json()["snapshot_sha256"]

    def test_catalog_examples_and_snapshot_listing(self):
        cats = self.client.get("/api/v1/catalogs/conductors").json()
        self.assertEqual(cats[0]["catalog_id"], "aaac6201_nexans_reference")
        self.assertIn("radial_feeder_6bus", self.client.get("/api/v1/examples").json())
        self.assertEqual(self.client.get("/api/v1/examples/../../AGENTS").status_code, 404)
        listed = self.client.get("/api/v1/snapshots").json()
        self.assertEqual([s["snapshot_sha256"] for s in listed], [self.sha])

    def test_alternatives_job(self):
        body = {"snapshot_sha256": self.sha, "line_id": "L13",
                "catalog_id": "aaac6201_nexans_reference", "operating_temperature_c": 75,
                "phase_gmd_m": 1.2,
                "economic_basis": self.client.get("/api/v1/economic-basis/example").json()}
        job = self.client.post("/api/v1/studies/conductor-alternatives", json=body).json()
        done = self.client.get(f"/api/v1/jobs/{job['job_id']}").json()
        self.assertEqual(done["status"], "finished", done)
        self.assertEqual(done["kind"], "alternatives")
        self.assertIsNotNone(done["report"]["recommended"])

    def test_alternatives_rejects_bad_basis_and_catalog(self):
        body = {"snapshot_sha256": self.sha, "line_id": "L13",
                "catalog_id": "aaac6201_nexans_reference", "operating_temperature_c": 75,
                "phase_gmd_m": 1.2, "economic_basis": {"schema": "unitesis.economic-basis/1"}}
        self.assertEqual(self.client.post("/api/v1/studies/conductor-alternatives",
                                          json=body).status_code, 422)
        body["catalog_id"] = "missing"
        self.assertEqual(self.client.post("/api/v1/studies/conductor-alternatives",
                                          json=body).status_code, 404)

    def test_workstation_ui_is_served(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn("UNITESIS Workstation", page.text)
        self.assertEqual(self.client.get("/app.js").status_code, 200)


if __name__ == "__main__":
    unittest.main()
