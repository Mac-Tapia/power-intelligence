"""VNR-GIS SQL Server backups: read-only restore, schema recovery and table export (spec 001).

VNR-GIS is the information system Osinergmin distributes to every distribution concession
for the Valor Nuevo de Reemplazo (Ley de Concesiones Electricas, art. 77; Guia VNR, Res.
232-2017-OS/CD), so this adapter targets the *VNRGIS schema version*, not a company.

Access goes through ``sqlcmd`` with Windows authentication on the local instance; no extra
Python driver is required. Rules (AC-001-U02): a restore always creates a **new** database,
refuses to touch an existing one, verifies the backup first, records the backup SHA-256 and
header, and sets the database READ_ONLY. Queries are SELECT-only.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SEP = "\x1f"                      # unit separator: never part of VNR text values
_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]{2,100}$")
_DEFAULT_SQLCMD = (r"C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn"
                   r"\sqlcmd.exe")


class VnrSqlError(RuntimeError):
    """The backup, the instance or a query cannot be used safely."""


def sha256_file(path: Path, chunk: int = 1 << 22) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        while block := fh.read(chunk):
            h.update(block)
    return h.hexdigest()


@dataclass
class SqlcmdClient:
    """Thin wrapper over ``sqlcmd``; ``runner`` is injectable for tests."""

    instance: str = r"lpc:.\SQLEXPRESS"
    sqlcmd: str = field(default_factory=lambda: shutil.which("sqlcmd") or _DEFAULT_SQLCMD)
    runner: Any = None

    def run(self, sql: str, database: str = "master") -> list[list[str]]:
        args = [self.sqlcmd, "-S", self.instance, "-E", "-C", "-d", database, "-b",
                "-W", "-h", "-1", "-s", SEP, "-Q", "SET NOCOUNT ON; " + sql]
        if self.runner is not None:
            out = self.runner(args)
        else:
            proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                                  errors="replace", check=False)
            if proc.returncode != 0:
                raise VnrSqlError((proc.stdout + proc.stderr).strip()[:800])
            out = proc.stdout
        return [line.split(SEP) for line in out.splitlines() if line.strip()]

    def run_with_headers(self, sql: str, database: str = "master") -> list[dict[str, str]]:
        """Result sets whose column set depends on the server version, mapped by name."""
        args = [self.sqlcmd, "-S", self.instance, "-E", "-C", "-d", database, "-b",
                "-W", "-s", SEP, "-Q", "SET NOCOUNT ON; " + sql]
        if self.runner is not None:
            out = self.runner(args)
        else:
            proc = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                                  errors="replace", check=False)
            if proc.returncode != 0:
                raise VnrSqlError((proc.stdout + proc.stderr).strip()[:800])
            out = proc.stdout
        lines = [ln for ln in out.splitlines() if ln.strip()]
        if len(lines) < 2:
            return []
        header = lines[0].split(SEP)
        return [dict(zip(header, ln.split(SEP), strict=False)) for ln in lines[2:]]

    @staticmethod
    def literal(text: str) -> str:
        return "N'" + text.replace("'", "''") + "'"


def database_exists(client: SqlcmdClient, name: str) -> bool:
    return bool(client.run(f"SELECT name FROM sys.databases WHERE name = {client.literal(name)}"))


def backup_header(client: SqlcmdClient, bak: Path) -> dict[str, str]:
    keep = ("DatabaseName", "BackupFinishDate", "CompatibilityLevel", "Collation",
            "SoftwareVersionMajor", "BackupType", "DatabaseVersion")
    rows = client.run_with_headers(f"RESTORE HEADERONLY FROM DISK = {client.literal(str(bak))}")
    if not rows:
        raise VnrSqlError(f"no backup set in {bak}")
    return {k: rows[0].get(k) for k in keep}


def _file_list(client: SqlcmdClient, bak: Path) -> list[tuple[str, str]]:
    rows = client.run_with_headers(
        f"RESTORE FILELISTONLY FROM DISK = {client.literal(str(bak))}")
    return [(r["LogicalName"], r["Type"]) for r in rows]


def restore_readonly(client: SqlcmdClient, bak: str | Path, database: str,
                     data_dir: str | Path) -> dict[str, Any]:
    """Restore ``bak`` into the NEW database ``database`` and set it READ_ONLY."""
    bak = Path(bak)
    if not _NAME.match(database):
        raise VnrSqlError("database name must be alphanumeric/underscore (3-100 chars)")
    if "'" in str(bak) or not bak.is_file():
        raise VnrSqlError(f"backup not found or unsafe path: {bak}")
    if database_exists(client, database):
        raise VnrSqlError(f"database {database} already exists; restores never overwrite")
    digest = sha256_file(bak)
    header = backup_header(client, bak)
    client.run(f"RESTORE VERIFYONLY FROM DISK = {client.literal(str(bak))}")
    moves = []
    for logical, kind in _file_list(client, bak):
        ext = "mdf" if kind == "D" else "ldf"
        target = Path(data_dir) / f"{database}_{logical}.{ext}"
        moves.append(f"MOVE {client.literal(logical)} TO {client.literal(str(target))}")
    client.run(f"RESTORE DATABASE [{database}] FROM DISK = {client.literal(str(bak))} "
               f"WITH {', '.join(moves)}, RECOVERY")
    client.run(f"ALTER DATABASE [{database}] SET READ_ONLY WITH NO_WAIT")
    ro = client.run(f"SELECT is_read_only FROM sys.databases WHERE name = "
                    f"{client.literal(database)}")
    return {"schema": "unitesis.vnrgis-restore/1", "backup_file": bak.name,
            "backup_sha256": digest, "backup_header": header, "database": database,
            "read_only": bool(ro and ro[0][0] == "1"), "verified": True}


def schema_profile(client: SqlcmdClient, database: str) -> dict[str, Any]:
    """Tables, row counts, columns and types, primary and foreign keys (no record values)."""
    tables = client.run(
        "SELECT s.name + '.' + t.name, SUM(p.rows) FROM sys.tables t "
        "JOIN sys.schemas s ON s.schema_id = t.schema_id "
        "JOIN sys.partitions p ON p.object_id = t.object_id AND p.index_id IN (0, 1) "
        "GROUP BY s.name, t.name ORDER BY s.name, t.name", database)
    cols = client.run(
        "SELECT TABLE_SCHEMA + '.' + TABLE_NAME, COLUMN_NAME, DATA_TYPE, "
        "ISNULL(CAST(CHARACTER_MAXIMUM_LENGTH AS varchar(12)), ''), IS_NULLABLE "
        "FROM INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION",
        database)
    pks = client.run(
        "SELECT ku.TABLE_SCHEMA + '.' + ku.TABLE_NAME, ku.COLUMN_NAME "
        "FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE ku "
        "ON tc.CONSTRAINT_NAME = ku.CONSTRAINT_NAME WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY'",
        database)
    fks = client.run(
        "SELECT OBJECT_SCHEMA_NAME(f.parent_object_id) + '.' + OBJECT_NAME(f.parent_object_id), "
        "COL_NAME(fc.parent_object_id, fc.parent_column_id), "
        "OBJECT_SCHEMA_NAME(f.referenced_object_id) + '.' + OBJECT_NAME(f.referenced_object_id), "
        "COL_NAME(fc.referenced_object_id, fc.referenced_column_id) "
        "FROM sys.foreign_keys f JOIN sys.foreign_key_columns fc "
        "ON f.object_id = fc.constraint_object_id", database)
    out: dict[str, Any] = {"schema": "unitesis.sql-schema-profile/1", "database": database,
                           "tables": {}}
    for name, rows in tables:
        out["tables"][name] = {"rows": int(rows or 0), "columns": [], "primary_key": [],
                               "foreign_keys": []}
    for t, col, typ, length, nullable in cols:
        if t in out["tables"]:
            out["tables"][t]["columns"].append(
                {"name": col, "type": typ + (f"({length})" if length else ""),
                 "nullable": nullable == "YES"})
    for t, col in pks:
        if t in out["tables"]:
            out["tables"][t]["primary_key"].append(col)
    for t, col, ref, ref_col in fks:
        if t in out["tables"]:
            out["tables"][t]["foreign_keys"].append(
                {"column": col, "references": f"{ref}.{ref_col}"})
    return out


def select_rows(client: SqlcmdClient, database: str, table: str, columns: list[str],
                where: str = "") -> list[dict[str, str | None]]:
    """SELECT-only export of named columns; ``NULL`` becomes ``None``."""
    if not re.match(r"^[A-Za-z0-9_]+\.[A-Za-z0-9_]+$", table) or not all(
            re.match(r"^[A-Za-z0-9_]+$", c) for c in columns):
        raise VnrSqlError("table and column names must be plain identifiers")
    if where and any(k in where.upper() for k in (";", "INSERT", "UPDATE", "DELETE", "DROP",
                                                   "ALTER", "EXEC")):
        raise VnrSqlError("only a plain WHERE filter is allowed")
    schema, name = table.split(".")
    sql = (f"SELECT {', '.join(f'[{c}]' for c in columns)} FROM [{schema}].[{name}]"
           + (f" WHERE {where}" if where else ""))
    rows = client.run(sql, database)
    return [{c: (None if v == "NULL" else v) for c, v in zip(columns, r, strict=False)}
            for r in rows]
