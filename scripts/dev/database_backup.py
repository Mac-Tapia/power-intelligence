"""Spec 004 local recovery: verified SQLite copies, published without overwriting."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import tempfile
from contextlib import closing
from hashlib import sha256
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TABLES = {"electrical_snapshot", "study_result", "source_manifest", "study_job"}
TRIGGERS = {"snapshot_no_update", "snapshot_no_delete", "result_no_update",
            "result_no_delete", "job_terminal_no_update", "job_no_delete"}


def _no_links(path: Path) -> None:
    if any(p.is_symlink() or p.is_junction() for p in [path, *path.parents]):
        raise ValueError("linked database paths are forbidden")


def _validate(db: sqlite3.Connection) -> dict[str, int]:
    if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
        raise ValueError("database integrity check failed")
    if db.execute("PRAGMA foreign_key_check").fetchone() is not None:
        raise ValueError("database foreign key check failed")
    tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    triggers = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='trigger'")}
    if not tables >= TABLES or not triggers >= TRIGGERS:
        raise ValueError("not a durable UNITESIS database")
    return {table: db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in sorted(TABLES)}


def backup_database(source: Path, destination: Path) -> dict[str, Any]:
    source, destination = Path(source).absolute(), Path(destination).absolute()
    _no_links(source)
    _no_links(destination)
    if not source.is_file():
        raise ValueError("source database is missing")
    if destination.exists() or destination == source:
        raise ValueError("destination must be a new database")
    temporary: Path | None = None
    try:
        with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)) as src:
            _validate(src)
            destination.parent.mkdir(parents=True, exist_ok=True)
            fd, name = tempfile.mkstemp(prefix=".unitesis-backup-", dir=destination.parent)
            os.close(fd)
            temporary = Path(name)
            with closing(sqlite3.connect(temporary)) as copy:
                src.backup(copy)
                counts = _validate(copy)
        digest = sha256(temporary.read_bytes()).hexdigest()
        # Same-directory link is atomic and fails if another writer created the target.
        # os.replace would silently overwrite an existing active database.
        os.link(temporary, destination)
        reread = sha256(destination.read_bytes()).hexdigest()
        if reread != digest:
            raise ValueError("backup reread digest mismatch")
        return {"schema": "unitesis.database-backup/1", "status": "reread_verified",
                "sha256": digest, "bytes": destination.stat().st_size, "counts": counts}
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def restore_database(source: Path, destination: Path) -> dict[str, Any]:
    return backup_database(source, destination)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["backup", "restore"])
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        _no_links(args.destination.absolute())
        if not args.destination.resolve().is_relative_to(ROOT / "local-data"):
            raise ValueError("destination must be under project local-data")
        action = backup_database if args.operation == "backup" else restore_database
        print(json.dumps(action(args.source, args.destination)))
        return 0
    except (OSError, ValueError, sqlite3.Error) as exc:
        print(f"Database recovery rejected: {type(exc).__name__}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
