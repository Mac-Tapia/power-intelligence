"""Ingestion quarantine, SQL repository, evidence read-back and custody (specs 001/004)."""

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.neutral_json import (  # noqa: E402
    IngestionError,
    build_snapshot,
    ingest_file,
    parse_payload,
    snapshot_to_payload,
)
from unitesis_adapters.sql_repository import (  # noqa: E402
    RepositoryIntegrityError,
    SqliteRepository,
)
from unitesis_domain import StudyRequest  # noqa: E402
from unitesis_evidence import (  # noqa: E402
    CustodyBlockedError,
    EvidenceError,
    discover_inputs,
    publish_evidence,
    read_evidence,
    write_inventory,
)
from unitesis_simulation import RadialBFSEngine  # noqa: E402

FEEDER = ROOT / "fixtures/networks/radial_feeder_6bus.json"


def payload():
    return json.loads(FEEDER.read_text(encoding="utf-8"))


class IngestionTests(unittest.TestCase):
    def test_valid_source_validates_with_manifest(self):
        res = ingest_file(FEEDER)
        self.assertEqual(res.state, "model_validated")
        self.assertEqual(res.manifest["snapshot_sha256"], res.snapshot.content_sha256)
        self.assertEqual(len(res.manifest["source_sha256"]), 64)

    def test_missing_parameter_is_quarantined_not_imputed(self):
        data = payload()
        del data["network"]["lines"][1]["r_ohm_per_km"]
        res = build_snapshot(parse_payload(json.dumps(data).encode()), "t")
        self.assertEqual(res.state, "quarantined")
        self.assertIsNone(res.snapshot)
        self.assertEqual((res.quarantine[0].element_id, res.quarantine[0].field),
                         ("L12", "r_ohm_per_km"))
        with self.assertRaises(IngestionError):
            res.require_snapshot()

    def test_all_bad_records_are_reported_together(self):
        data = payload()
        data["network"]["loads"][0]["p_mw"] = "1.0"
        del data["network"]["switches"][0]["closed"]
        data["network"]["buses"][0]["crs_x"] = 1
        res = build_snapshot(parse_payload(json.dumps(data).encode()), "t")
        self.assertEqual({q.element_id for q in res.quarantine}, {"C1", "S2", "SE"})

    def test_parse_rejections(self):
        good = FEEDER.read_text(encoding="utf-8")
        cases = {
            "duplicate key": good.replace('"source_id"', '"source_id": "x", "source_id"', 1),
            "nan constant": good.replace('"p_mw": 0.8', '"p_mw": NaN'),
            "units": good.replace('"kA"', '"A"'),
            "schema": good.replace("unitesis.network-input/1", "other/1"),
        }
        for name, text in cases.items():
            with self.subTest(name), self.assertRaises(IngestionError):
                parse_payload(text.encode())

    def test_export_roundtrip_preserves_identity(self):
        snap = ingest_file(FEEDER).require_snapshot()
        again = build_snapshot(snapshot_to_payload(snap, "export"), "rt").require_snapshot()
        self.assertEqual(again.content_sha256, snap.content_sha256)


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.repo = SqliteRepository(":memory:")
        self.ing = ingest_file(FEEDER)
        self.snap = self.ing.require_snapshot()

    def test_snapshot_roundtrip_and_idempotence(self):
        key = self.repo.save_snapshot(self.snap, self.ing.manifest)
        self.assertEqual(self.repo.save_snapshot(self.snap, self.ing.manifest), key)
        self.assertEqual(self.repo.load_snapshot(key).content_sha256, key)

    def test_result_roundtrip(self):
        self.repo.save_snapshot(self.snap, self.ing.manifest)
        res = RadialBFSEngine().solve(self.snap, StudyRequest(self.snap.content_sha256, "b", "e"))
        key = self.repo.save_result(res, "evidence.json")
        self.assertEqual(self.repo.get_result(key)["status"], "computed")
        self.assertEqual(len(self.repo.results_for_snapshot(self.snap.content_sha256)), 1)

    def test_tampering_detected(self):
        key = self.repo.save_snapshot(self.snap, self.ing.manifest)
        # bypass the append-only trigger only to simulate external corruption
        self.repo._db.execute("DROP TRIGGER snapshot_no_update")
        self.repo._db.execute("UPDATE electrical_snapshot SET canonical = replace(canonical, "
                              "'0.8', '0.9') WHERE snapshot_sha256 = ?", (key,))
        with self.assertRaises(RepositoryIntegrityError):
            self.repo.load_snapshot(key)

    def test_append_only(self):
        key = self.repo.save_snapshot(self.snap, self.ing.manifest)
        with self.assertRaises(sqlite3.DatabaseError):
            self.repo._db.execute("DELETE FROM electrical_snapshot WHERE snapshot_sha256=?", (key,))

    def test_quarantine_persisted(self):
        data = payload()
        del data["network"]["lines"][0]["x_ohm_per_km"]
        res = build_snapshot(parse_payload(json.dumps(data).encode()), "t")
        res.manifest["source_sha256"] = "a" * 64
        self.repo.save_source(res.manifest, res.quarantine)
        self.assertEqual(self.repo.quarantine_for("a" * 64)[0]["field"], "x_ohm_per_km")


class EvidenceAndCustodyTests(unittest.TestCase):
    def test_publish_reread_and_detect_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ev.json"
            publish_evidence(path, {"a": 1, "b": [1.5, "x"]})
            self.assertEqual(read_evidence(path), {"a": 1, "b": [1.5, "x"]})
            path.write_text(path.read_text().replace('"a":1', '"a":2'), encoding="utf-8")
            with self.assertRaises(EvidenceError):
                read_evidence(path)

    def test_nonfinite_evidence_refused(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(ValueError):
            publish_evidence(Path(tmp) / "x.json", {"v": float("nan")})

    def test_custody_states_and_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.csv").write_text("t,v\n1,2\n", encoding="utf-8")
            (root / "copy.csv").write_text("t,v\n1,2\n", encoding="utf-8")
            (root / "fake.xlsx").write_text("not a zip", encoding="utf-8")
            (root / "notes.md").write_text("# info", encoding="utf-8")
            inv = discover_inputs([root], expected=[root / "missing.csv"])
            states = {Path(e.path).name: e.state for e in inv.entries}
            self.assertEqual(states, {"a.csv": "SUPPORTED", "copy.csv": "DUPLICATE",
                                      "fake.xlsx": "QUARANTINED", "notes.md": "DOCUMENTATION"})
            self.assertFalse(inv.accepted)
            with self.assertRaises(CustodyBlockedError):
                inv.require_accepted()
            out = write_inventory(inv, root / "out")
            self.assertEqual(out["summary"]["total"], 4)


if __name__ == "__main__":
    unittest.main()
