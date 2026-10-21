"""CYME ASCII in the phase frame (spec 008-C3, REA findings of ADR-0012).

A synthetic feeder with a single-phase lateral is appended to copies of the synthetic
export: phase matrices come from the catalogue sequence values, load phases from the
recovered bitmask, the load connection from the case-declared code map. Every mismatch
goes to quarantine.
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.cyme_ascii import ReaderRules, phases_from_code, read_export  # noqa: E402
from unitesis_domain import StudyRequest  # noqa: E402
from unitesis_simulation import NewtonRaphsonEngine, ThreePhaseEngine  # noqa: E402

FIX = ROOT / "fixtures/networks/cyme-ascii"
FEEDER = """FORMAT_SECTION=SectionID,FromNodeID,ToNodeID,Phase
FEEDER=NET_PH,N_PH0,1,2026,,,1.0
S_PH1,N_PH0,N_PH1,ABC
S_PH2,N_PH1,N_PH2,A
S_PH3,N_PH1,N_PH3,ABC
"""
CONFIG = "S_PH1,AA05003D,1000,1\nS_PH2,AA05003D,800,1\nS_PH3,AA05003D,600,1\n"
SOURCE = "SRC_PH,DEV_SRC_PH,N_PH0,NET_PH,22.9\n"
LOADS = "S_PH2,DPH2,SPOT,0,1\nS_PH3,DPH3,SPOT,0,1\n"
CUSTOMERS = ("S_PH2,DPH2,SPOT,CPH2,Otro,0,0,2026,,1,1,2,{a},120.0,0.95,160.0,100.0,3,0.0\n"
             "S_PH3,DPH3,SPOT,CPH3,Otro,0,0,2026,,1,1,2,7,300.0,0.95,400.0,100.0,5,0.0\n")


def insert_after(text: str, marker: str, block: str) -> str:
    head, sep, tail = text.partition(marker)
    line_end = tail.index("\n") + 1
    return head + sep + tail[:line_end] + block + tail[line_end:]


def export(tmp: Path, lateral_code: str = "1") -> tuple[Path, Path, Path]:
    red = (FIX / "RED_synthetic.txt").read_text(encoding="latin-1")
    red = insert_after(red, "FORMAT_SOURCE=", SOURCE)
    red = red.replace("[LINE CONFIGURATION]", FEEDER + "\n[LINE CONFIGURATION]", 1)
    red = insert_after(red, "FORMAT_LINECONFIGURATION=", CONFIG)
    carga = (FIX / "CARGA_synthetic.txt").read_text(encoding="latin-1")
    carga = insert_after(carga, "FORMAT_LOADS=", LOADS)
    carga = insert_after(carga, "FORMAT_CUSTOMERLOADS=", CUSTOMERS.format(a=lateral_code))
    (tmp / "RED.txt").write_text(red, encoding="latin-1")
    (tmp / "CARGA.txt").write_text(carga, encoding="latin-1")
    shutil.copy(FIX / "BD_Equipo_synthetic.txt", tmp / "BD.txt")
    return tmp / "RED.txt", tmp / "CARGA.txt", tmp / "BD.txt"


PHASE_RULES = ReaderRules(60.0, 10.0, phase_frame_from_sequence=True,
                          load_connection_codes=(("0", "wye"),))


class CymePhaseFrameTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def feeder(self, rules=PHASE_RULES, code="1"):
        return {r.network_id: r for r in read_export(*export(self.dir, code), rules)}["NET_PH"]

    def test_bitmask_decoding(self):
        self.assertEqual([phases_from_code(c) for c in ("1", "3", "5", "6", "7")],
                         ["A", "AB", "AC", "BC", "ABC"])
        self.assertIsNone(phases_from_code("8"))
        self.assertIsNone(phases_from_code("x"))

    def test_without_the_rule_the_feeder_stays_quarantined(self):
        imp = self.feeder(ReaderRules(60.0, 10.0))
        self.assertEqual(imp.state, "quarantined")

    def test_phase_frame_feeder_validates_and_solves(self):
        imp = self.feeder()
        self.assertEqual(imp.state, "model_validated", [q.as_dict() for q in imp.quarantine])
        snap = imp.snapshot
        lateral = next(ln for ln in snap.lines if ln.line_id == "S_PH2")
        self.assertEqual(lateral.phases, "A")
        self.assertEqual(len(lateral.z_phase_ohm_per_km), 1)
        load = next(ld for ld in snap.loads if ld.load_id == "DPH2")
        self.assertEqual((load.phases, load.connection), ("A", "wye"))
        self.assertTrue(imp.manifest["phase_frame"])
        self.assertTrue(any("bitmask" in i for i in imp.manifest["interpretations"]))
        res = ThreePhaseEngine().solve(snap, StudyRequest(snap.content_sha256, "s", "3ph"))
        self.assertEqual(res.status, "computed", res.messages)
        flows = {f.phase: f.i_from_a for f in res.flows if f.branch_id == "S_PH2"}
        self.assertEqual(set(flows), {"A"})
        nr = NewtonRaphsonEngine().solve(snap, StudyRequest(snap.content_sha256, "s", "nr"))
        self.assertEqual(nr.status, "failed")            # balanced engine refuses phase data

    def test_load_phase_outside_its_section_is_quarantined(self):
        imp = self.feeder(code="2")                       # B load on an A-only lateral
        self.assertEqual(imp.state, "quarantined")
        self.assertTrue(any(q.element_id == "DPH2" for q in imp.quarantine))

    def test_undeclared_connection_code_is_quarantined(self):
        imp = self.feeder(ReaderRules(60.0, 10.0, phase_frame_from_sequence=True))
        self.assertEqual(imp.state, "quarantined")
        self.assertTrue(any(q.field == "Connection" for q in imp.quarantine))

    def test_three_phase_feeders_keep_their_balanced_snapshot(self):
        plain = {r.network_id: r for r in read_export(*export(self.dir), ReaderRules(60.0, 10.0))}
        phase = {r.network_id: r for r in read_export(*export(self.dir), PHASE_RULES)}
        self.assertEqual(plain["NET_OK"].snapshot.content_sha256,
                         phase["NET_OK"].snapshot.content_sha256)


if __name__ == "__main__":
    unittest.main()
