"""Read-only networks router (spec 003): imported feeders and source geometry."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))
sys.path.insert(0, str(ROOT / "apps/control-api/src"))

from unitesis_application.network_import import import_cyme_export  # noqa: E402
from unitesis_config import load_case  # noqa: E402

FIX = ROOT / "fixtures/networks/cyme-ascii"
FILES = (FIX / "RED_synthetic.txt", FIX / "CARGA_synthetic.txt", FIX / "BD_Equipo_synthetic.txt")
try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    HAS_API = True
except Exception:
    HAS_API = False


@unittest.skipUnless(HAS_API, "fastapi/httpx required")
class NetworksRouterTests(unittest.TestCase):
    def setUp(self):
        from unitesis_api.networks import create_networks_router
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        case = load_case(ROOT / "config/cases/pe-ica-electrodunas.json")
        import_cyme_export(case, *FILES, root / case.case_id)
        app = FastAPI()
        app.include_router(create_networks_router(root))
        self.client = TestClient(app)
        self.root = root

    def tearDown(self):
        self.tmp.cleanup()

    def test_lists_cases_and_feeders_without_customer_attributes(self):
        cases = self.client.get("/api/v1/networks").json()
        self.assertEqual(cases[0]["case_id"], "pe-ica-electrodunas")
        feeders = self.client.get("/api/v1/networks/pe-ica-electrodunas/feeders").json()
        self.assertEqual({f["network_id"]: f["state"] for f in feeders},
                         {"NET_OK": "model_validated", "NET_BAD": "quarantined"})
        self.assertNotIn("load_attributes", json.dumps(feeders))

    def test_feeder_payload_and_geometry(self):
        base = "/api/v1/networks/pe-ica-electrodunas/feeders/NET_OK"
        payload = self.client.get(base).json()
        self.assertEqual(payload["schema"], "unitesis.network-input/1")
        geo = self.client.get(base + "/geometry").json()
        self.assertEqual(geo["crs"], "EPSG:32718")
        ids = {f["id"] for f in geo["features"]}
        self.assertIn("S_OK1", ids)

    def test_unknown_quarantined_and_traversal_are_404(self):
        for path in ("/api/v1/networks/pe-ica-electrodunas/feeders/NET_BAD",
                     "/api/v1/networks/pe-ica-electrodunas/feeders/NOPE/geometry",
                     "/api/v1/networks/..%2F..%2Fconfig/feeders",
                     "/api/v1/networks/other-case/feeders"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)

    def test_tampered_report_is_rejected(self):
        report = self.root / "pe-ica-electrodunas" / "import_report.json"
        data = json.loads(report.read_text(encoding="utf-8"))
        data["payload"]["summary"]["model_validated"] = 99
        report.write_text(json.dumps(data), encoding="utf-8")
        self.assertEqual(self.client.get("/api/v1/networks/pe-ica-electrodunas/feeders")
                         .status_code, 409)


if __name__ == "__main__":
    unittest.main()
