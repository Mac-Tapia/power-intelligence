"""Offline, read-only reader for Access ``.mdb`` study databases (spec 001, T001-U05).

Uses the Jet OLE DB provider that ships with Windows through the 32-bit PowerShell host
(the Jet driver is 32-bit only), so no Python package is installed and no CYME program is
executed (ADR-0010). The database is opened with ``Mode=Read`` and ``Share Deny None``:
nothing is ever written. Output is structure (tables, columns, row counts) or a UTF-8 CSV
export of one table, for REA profiling (ADR-0012) and for readers built on top.
"""

from __future__ import annotations

import csv
import io
import os
import re
import subprocess
from pathlib import Path
from typing import Any

POWERSHELL32 = Path(os.environ.get("SYSTEMROOT", r"C:\Windows")) / \
    r"SysWOW64\WindowsPowerShell\v1.0\powershell.exe"
_TABLE = re.compile(r"^[\w\- ]{1,64}$")

_CONNECT = (
    "$cs = 'Provider=Microsoft.Jet.OLEDB.4.0;Data Source=' + $env:UNITESIS_MDB + "
    "';Mode=Read;Jet OLEDB:Database Locking Mode=0;';"
    "$c = New-Object System.Data.OleDb.OleDbConnection $cs; $c.Open();"
)
_SCHEMA = _CONNECT + (
    "$t = $c.GetOleDbSchemaTable([System.Data.OleDb.OleDbSchemaGuid]::Tables, $null);"
    "foreach ($r in $t.Rows) { if ($r.TABLE_TYPE -eq 'TABLE') {"
    " $n = $r.TABLE_NAME; $cmd = $c.CreateCommand();"
    " $cmd.CommandText = 'SELECT COUNT(*) FROM [' + $n + ']'; $k = $cmd.ExecuteScalar();"
    " $cols = $c.GetOleDbSchemaTable([System.Data.OleDb.OleDbSchemaGuid]::Columns,"
    " @($null, $null, $n, $null));"
    " $cl = ($cols.Rows | Sort-Object ORDINAL_POSITION | ForEach-Object {"
    " $_.COLUMN_NAME + ':' + $_.DATA_TYPE }) -join ';';"
    " [Console]::Out.WriteLine($n + [char]31 + $k + [char]31 + $cl) } }; $c.Close()"
)
_EXPORT = _CONNECT + (
    "$cmd = $c.CreateCommand();"
    " $cmd.CommandText = 'SELECT * FROM [' + $env:UNITESIS_TABLE + ']';"
    "$rd = $cmd.ExecuteReader(); $h = @(); for ($i = 0; $i -lt $rd.FieldCount; $i++) {"
    " $h += $rd.GetName($i) }; [Console]::Out.WriteLine(($h -join [char]31));"
    "while ($rd.Read()) { $v = @(); for ($i = 0; $i -lt $rd.FieldCount; $i++) {"
    " if ($rd.IsDBNull($i)) { $v += [char]30 } else {"
    " $v += ([string]$rd.GetValue($i)).Replace([string][char]10, ' ')"
    ".Replace([string][char]13, ' ') } };"
    " [Console]::Out.WriteLine(($v -join [char]31)) }; $rd.Close(); $c.Close()"
)


class MdbError(RuntimeError):
    """The database cannot be opened read-only or the request is unsafe."""


def _run(script: str, mdb: Path, table: str | None = None, runner=None) -> str:
    mdb = Path(mdb)
    if not mdb.is_file():
        raise MdbError(f"database not found: {mdb}")
    env = dict(os.environ, UNITESIS_MDB=str(mdb.resolve()))
    if table is not None:
        if not _TABLE.match(table):
            raise MdbError("table names must be plain identifiers")
        env["UNITESIS_TABLE"] = table
    args = [str(POWERSHELL32), "-NoProfile", "-NonInteractive", "-Command",
            "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; " + script]
    if runner is not None:
        return runner(args, env)
    proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env, check=False)
    if proc.returncode != 0 or "Exception" in proc.stderr:
        raise MdbError((proc.stderr or proc.stdout).strip()[:800])
    return proc.stdout


def _lines(text: str) -> list[str]:
    """Split on newlines only: ``str.splitlines`` would also split on the NULL marker."""
    return [ln.rstrip("\r") for ln in text.split("\n") if ln.strip("\r")]


def schema(mdb: str | Path, runner=None) -> dict[str, Any]:
    """Tables with row counts and ``column:oledb_type`` lists (no record values)."""
    out: dict[str, Any] = {"schema": "unitesis.mdb-schema-profile/1", "file": Path(mdb).name,
                           "tables": {}}
    for line in _lines(_run(_SCHEMA, Path(mdb), runner=runner)):
        parts = line.split("\x1f")
        if len(parts) == 3:
            name, rows, cols = parts
            out["tables"][name] = {"rows": int(rows),
                                   "columns": [c.split(":")[0] for c in cols.split(";") if c]}
    return out


def read_table(mdb: str | Path, table: str, runner=None) -> list[dict[str, str | None]]:
    """All rows of one table as strings (``None`` for NULL); read-only."""
    text = _run(_EXPORT, Path(mdb), table, runner=runner)
    lines = _lines(text)
    if not lines:
        return []
    header = lines[0].split("\x1f")
    rows = []
    for line in lines[1:]:
        values = line.split("\x1f")
        rows.append({h: (None if v == "\x1e" else v) for h, v in zip(header, values, strict=False)})
    return rows


def to_csv(rows: list[dict[str, Any]]) -> str:
    buf = io.StringIO()
    if rows:
        writer = csv.DictWriter(buf, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return buf.getvalue()
