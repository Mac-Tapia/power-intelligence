"""Read-only Access reader (spec 001, T001-U05) with a scripted 32-bit PowerShell host."""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.access_mdb import MdbError, read_table, schema, to_csv  # noqa: E402

US, RS = "\x1f", "\x1e"


class ScriptedPowerShell:
    def __init__(self, out):
        self.out = out
        self.calls = []

    def __call__(self, args, env):
        self.calls.append((args, env))
        return self.out


class AccessMdbTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.mdb = Path(self.tmp.name) / "study.mdb"
        self.mdb.write_bytes(b"jet")

    def tearDown(self):
        self.tmp.cleanup()

    def test_schema_opens_read_only_and_parses_structure(self):
        ps = ScriptedPowerShell(f"CYMSECTION{US}3{US}SectionId:130;Phase:130\n")
        out = schema(self.mdb, runner=ps)
        self.assertEqual(out["tables"]["CYMSECTION"], {"rows": 3,
                                                       "columns": ["SectionId", "Phase"]})
        args, env = ps.calls[0]
        self.assertIn("SysWOW64", args[0])
        self.assertIn("Mode=Read", args[-1])
        self.assertEqual(env["UNITESIS_MDB"], str(self.mdb.resolve()))

    def test_read_table_maps_null_and_rejects_unsafe_names(self):
        ps = ScriptedPowerShell(f"SectionId{US}Phase\nS1{US}ABC\nS2{US}{RS}\n")
        rows = read_table(self.mdb, "CYMSECTION", runner=ps)
        self.assertEqual(rows, [{"SectionId": "S1", "Phase": "ABC"},
                                {"SectionId": "S2", "Phase": None}])
        self.assertIn("SectionId,Phase", to_csv(rows))
        with self.assertRaises(MdbError):
            read_table(self.mdb, "CYMSECTION]; DROP TABLE x", runner=ps)
        with self.assertRaises(MdbError):
            schema(Path(self.tmp.name) / "missing.mdb", runner=ps)


if __name__ == "__main__":
    unittest.main()
