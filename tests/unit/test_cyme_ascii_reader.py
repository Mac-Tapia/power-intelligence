"""Offline CYME ASCII reader (spec 001, T010): explicit rules, quarantine, real-network run."""

import json
import math
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.cyme_ascii import (  # noqa: E402
    CymeFormatError,
    ReaderRules,
    parse_sections,
    read_export,
)
from unitesis_adapters.neutral_json import ingest_file  # noqa: E402
from unitesis_application.network_import import cyme_rules_for, import_cyme_export  # noqa: E402
from unitesis_config import CaseError, load_case  # noqa: E402
from unitesis_domain import StudyRequest  # noqa: E402
from unitesis_simulation import NewtonRaphsonEngine  # noqa: E402

FIX = ROOT / "fixtures/networks/cyme-ascii"
FILES = (FIX / "RED_synthetic.txt", FIX / "CARGA_synthetic.txt", FIX / "BD_Equipo_synthetic.txt")
RULES = ReaderRules(60.0, 10.0)
ARCHIVE = os.environ.get("UNITESIS_ARCHIVE_ROOT",
                         "D:/Proyectos/PowerIntelligence_archivo_2026-10-20/consolidacion")
REAL = Path(ARCHIVE) / "flujos/outputs/jobs/79efed5d-8204-416b-acdb-7ee75da3509d/inputs"


def by_id(results):
    return {r.network_id: r for r in results}


class SyntheticExportTests(unittest.TestCase):
    def setUp(self):
        self.res = by_id(read_export(*FILES, RULES))

    def test_valid_feeder_with_declared_rules(self):
        ok = self.res["NET_OK"]
        self.assertEqual(ok.state, "model_validated")
        snap = ok.snapshot
        self.assertEqual({b.nominal_kv for b in snap.buses}, {22.9})
        self.assertEqual(snap.slacks[0].bus, "N_OK0")
        line = next(ln for ln in snap.lines if ln.line_id == "S_OK1")
        self.assertEqual((line.length_km, line.r_ohm_per_km, line.max_current_ka),
                         (1.0, 0.6755, 0.195))
        self.assertEqual([s.switch_id for s in snap.switches], ["S_OK2"])      # DEFAULT 1.5 m
        self.assertFalse(next(ln for ln in snap.lines if ln.line_id == "S_OK4").in_service)
        load = next(ld for ld in snap.loads if ld.load_id == "D1")
        self.assertEqual(load.bus, "N_OK1")                                   # section ToNode
        self.assertAlmostEqual(load.q_mvar, 0.4 * math.tan(math.acos(0.95)))
        self.assertEqual(ok.load_attributes["D3"]["connected_kva"], 250.0)
        counts = ok.manifest["record_counts"]
        self.assertEqual((counts["ideal_connectors"], counts["open_devices"]), (1, 1))
        self.assertEqual(ok.manifest["parameter_quality"]["loads_without_kw"], 1)
        self.assertEqual(len(ok.manifest["files"]["network"]["sha256"]), 64)

    def test_every_rejection_is_kept_with_its_reason(self):
        bad = self.res["NET_BAD"]
        self.assertEqual(bad.state, "quarantined")
        self.assertIsNone(bad.snapshot)
        reasons = {(q.element_id, q.field): q.reason for q in bad.quarantine}
        self.assertIn("not in equipment catalogue", reasons[("S_BAD1", "LineCableID")])
        self.assertIn("DEFAULT conductor over 30.0 m", reasons[("S_BAD3", "LineCableID")])
        self.assertIn("non three-phase", reasons[("NET_BAD", "Phase")])
        self.assertIn("unsupported value type", reasons[("DB3", "ValueType")])

    def test_positive_sequence_approximation_only_when_declared(self):
        rules = ReaderRules(60.0, 40.0, allow_positive_sequence_approximation=True)
        bad = by_id(read_export(*FILES, rules))["NET_BAD"]
        fields = {q.field for q in bad.quarantine}
        self.assertNotIn("Phase", fields)               # approximation accepted explicitly
        self.assertIn("LineCableID", fields)            # missing catalogue still blocks
        self.assertTrue(bad.manifest["parameter_quality"]["positive_sequence_approximation"])

    def test_imported_feeder_solves(self):
        snap = self.res["NET_OK"].snapshot
        res = NewtonRaphsonEngine().solve(
            snap, StudyRequest(snap.content_sha256, "s", "unitesis-newton-raphson"))
        self.assertEqual(res.status, "computed")
        self.assertIn("bus:N_OK4", res.excluded_elements)

    def test_rules_and_format_are_validated(self):
        with self.assertRaises(ValueError):
            ReaderRules(55.0, 10.0)
        with self.assertRaises(ValueError):
            ReaderRules(60.0, 500.0)
        with tempfile.TemporaryDirectory() as tmp:
            broken = Path(tmp) / "RED.txt"
            broken.write_text("[SECTION]\nS1,A,B,ABC\n", encoding="latin-1")
            with self.assertRaises(CymeFormatError):
                parse_sections(broken)

    def test_deterministic_snapshot_identity(self):
        again = by_id(read_export(*FILES, RULES))["NET_OK"].snapshot
        self.assertEqual(again.content_sha256, self.res["NET_OK"].snapshot.content_sha256)


class ImportUseCaseTests(unittest.TestCase):
    def test_case_rules_drive_import_and_output_reingests(self):
        case = load_case(ROOT / "config/cases/pe-ica-electrodunas.json")
        self.assertEqual(cyme_rules_for(case).default_connector_max_m, 10.0)
        with tempfile.TemporaryDirectory() as tmp:
            report = import_cyme_export(case, *FILES, tmp)
            self.assertEqual(report["summary"], {"model_validated": 1, "quarantined": 1})
            row = next(r for r in report["feeders"] if r["state"] == "model_validated")
            snap = ingest_file(Path(tmp) / row["snapshot_file"]).require_snapshot()
            self.assertEqual(snap.content_sha256, row["snapshot_sha256"])
            payload = json.loads((Path(tmp) / row["snapshot_file"]).read_text(encoding="utf-8"))
            self.assertIn("pe-ica-electrodunas", payload["provenance"])

    def test_geometry_is_separate_and_shares_electrical_ids(self):
        case = load_case(ROOT / "config/cases/pe-ica-electrodunas.json")
        with tempfile.TemporaryDirectory() as tmp:
            report = import_cyme_export(case, *FILES, tmp)
            row = next(r for r in report["feeders"] if r["state"] == "model_validated")
            geo = json.loads((Path(tmp) / row["geometry_file"]).read_text(encoding="utf-8"))
            snap = ingest_file(Path(tmp) / row["snapshot_file"]).require_snapshot()
        self.assertEqual(geo["crs"], case.crs)
        self.assertFalse(geo["crs_verified"])
        section_ids = {f["id"] for f in geo["features"] if f["properties"]["kind"] == "section"}
        branch_ids = {ln.line_id for ln in snap.lines} | {s.switch_id for s in snap.switches}
        self.assertEqual(section_ids, branch_ids)
        node_ids = {f["id"] for f in geo["features"] if f["properties"]["kind"] == "node"}
        self.assertEqual(node_ids, {b.bus_id for b in snap.buses})
        self.assertEqual(geo["extent"], [0.0, 0.0, 300.0, 50.0])
        self.assertEqual(snap.content_sha256, row["snapshot_sha256"])   # geometry not in identity

    def test_case_without_rules_is_rejected(self):
        case = load_case(ROOT / "config/cases/pe-ica-electrodunas.json")
        bare = type(case)(**{**{f: getattr(case, f) for f in case.__dataclass_fields__},
                             "import_rules": {}})
        with self.assertRaises(CaseError):
            cyme_rules_for(bare)


@unittest.skipUnless(REAL.is_dir(), "real Electro Dunas CYME export not available")
class RealNetworkTests(unittest.TestCase):
    def test_real_export_imports_and_every_validated_feeder_converges(self):
        results = read_export(REAL / "RED_030826.txt", REAL / "CARGA_030826.txt",
                              REAL / "BD_Equipo_V261124 (1).txt", RULES)
        validated = [r for r in results if r.snapshot is not None]
        self.assertEqual(len(results), 93)
        self.assertGreaterEqual(len(validated), 44)
        engine = NewtonRaphsonEngine()
        statuses = {engine.solve(r.snapshot, StudyRequest(r.snapshot.content_sha256, "base",
                                                          engine.name)).status
                    for r in validated}
        self.assertEqual(statuses, {"computed"})


if __name__ == "__main__":
    unittest.main()
