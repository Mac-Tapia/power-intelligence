"""VNR-GIS SQL adapter safety rules (AC-001-U02) with a scripted ``sqlcmd`` (no server)."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))

from unitesis_adapters.vnrgis_sql import (  # noqa: E402
    SEP,
    SqlcmdClient,
    VnrSqlError,
    restore_readonly,
    select_rows,
)


class ScriptedSqlcmd:
    """Answers sqlcmd calls by keyword and records every statement sent."""

    def __init__(self, existing=()):
        self.existing = set(existing)
        self.sent = []

    def __call__(self, args):
        sql = args[args.index("-Q") + 1]
        self.sent.append(sql)
        if "FROM sys.databases WHERE name =" in sql and "is_read_only" not in sql:
            name = sql.split("N'")[1].split("'")[0]
            return name + "\n" if name in self.existing else ""
        if "RESTORE HEADERONLY" in sql:
            return SEP.join(["DatabaseName", "BackupType"]) + "\n--\nVNR_X" + SEP + "1\n"
        if "RESTORE FILELISTONLY" in sql:
            return (SEP.join(["LogicalName", "Type"]) + "\n--\n" + "vnr_dat" + SEP + "D\n"
                    + "vnr_log" + SEP + "L\n")
        if "is_read_only" in sql:
            return "1\n"
        if sql.startswith("SET NOCOUNT ON; SELECT [CodSalidaMT]"):
            return "AL104" + SEP + "NULL\n"
        return ""


class VnrSqlTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.bak = Path(self.tmp.name) / "VNR.bak"
        self.bak.write_bytes(b"backup bytes")

    def tearDown(self):
        self.tmp.cleanup()

    def test_restore_creates_new_read_only_database_after_verification(self):
        script = ScriptedSqlcmd()
        out = restore_readonly(SqlcmdClient(runner=script), self.bak, "UNITESIS_RO_TEST",
                               self.tmp.name)
        self.assertTrue(out["read_only"])
        self.assertEqual(len(out["backup_sha256"]), 64)
        order = [s for s in script.sent if "RESTORE VERIFYONLY" in s or "RESTORE DATABASE" in s
                 or "SET READ_ONLY" in s]
        self.assertTrue(order[0].count("VERIFYONLY") and "READ_ONLY" in order[-1])
        restore = next(s for s in script.sent if "RESTORE DATABASE" in s)
        self.assertIn("MOVE N'vnr_dat'", restore)
        self.assertIn(os.path.join(self.tmp.name, "UNITESIS_RO_TEST_vnr_log.ldf"), restore)

    def test_existing_database_is_never_overwritten(self):
        script = ScriptedSqlcmd(existing={"IGEA_VNR_PRUEBA"})
        with self.assertRaises(VnrSqlError):
            restore_readonly(SqlcmdClient(runner=script), self.bak, "IGEA_VNR_PRUEBA",
                             self.tmp.name)
        self.assertFalse(any("RESTORE DATABASE" in s for s in script.sent))

    def test_unsafe_names_and_filters_are_rejected(self):
        client = SqlcmdClient(runner=ScriptedSqlcmd())
        with self.assertRaises(VnrSqlError):
            restore_readonly(client, self.bak, "bad;name", self.tmp.name)
        with self.assertRaises(VnrSqlError):
            select_rows(client, "DB", "dbo.mtSalida", ["CodSalidaMT"], where="1=1; DROP TABLE x")
        with self.assertRaises(VnrSqlError):
            select_rows(client, "DB", "dbo.mt Salida", ["CodSalidaMT"])

    def test_select_maps_null(self):
        rows = select_rows(SqlcmdClient(runner=ScriptedSqlcmd()), "DB", "dbo.mtSalida",
                           ["CodSalidaMT", "CodTenNomi"])
        self.assertEqual(rows, [{"CodSalidaMT": "AL104", "CodTenNomi": None}])


if __name__ == "__main__":
    unittest.main()
