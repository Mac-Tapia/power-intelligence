"""Spec 004 recovery for an explicitly named local UNITESIS sandbox container.

Never targets a remote DSN or overwrites a database; a failed restore leaves the new
database for diagnosis instead of deleting it or claiming it is ready.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
from hashlib import file_digest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _check(container: str, database: str, namespace: str = "unitesis") -> None:
    if not re.fullmatch(r"unitesis-[a-z0-9_-]+", container):
        raise ValueError("explicit UNITESIS sandbox container required")
    if not all(re.fullmatch(r"[a-z][a-z0-9_]{0,62}", s) for s in (database, namespace)):
        raise ValueError("invalid database/schema identifier")


def _file(path: Path) -> Path:
    path = path.absolute()
    if any(p.is_symlink() or p.is_junction() for p in [path, *path.parents]):
        raise ValueError("linked backup path forbidden")
    return path


def backup_namespace(container: str, database: str, namespace: str, output: Path) -> dict:
    _check(container, database, namespace)
    output = _file(Path(output))
    if output.exists():
        raise ValueError("new backup destination required")
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=output.parent, prefix=".pg-backup-")
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as handle:
            result = subprocess.run(["docker", "exec", container, "pg_dump", "-U", "postgres",
                "--no-password", "--format=custom", "--no-owner", "--no-privileges",
                "--dbname", database, "--schema", namespace], stdout=handle,
                stderr=subprocess.PIPE, timeout=180)
            handle.flush()
            os.fsync(handle.fileno())
        if result.returncode or not temporary.stat().st_size:
            raise RuntimeError("native pg_dump failed")
        with temporary.open("rb") as handle:
            checksum = file_digest(handle, "sha256").hexdigest()
        os.link(temporary, output)
        with output.open("rb") as handle:
            if file_digest(handle, "sha256").hexdigest() != checksum:
                raise RuntimeError("backup reread failed")
        return {"status": "reread_verified", "sha256": checksum,
                "bytes": output.stat().st_size, "namespace": namespace}
    finally:
        temporary.unlink(missing_ok=True)


def restore_namespace(container: str, new_database: str, source: Path) -> dict:
    _check(container, new_database)
    if not new_database.startswith("unitesis_restore_"):
        raise ValueError("restore destination must be a new unitesis_restore_ database")
    source = _file(Path(source))
    if not source.is_file() or source.stat().st_size == 0:
        raise ValueError("backup source missing")
    commands = [["docker", "exec", container, "createdb", "-U", "postgres", new_database],
        ["docker", "exec", container, "psql", "-U", "postgres", "-v", "ON_ERROR_STOP=1",
         "-d", new_database, "-c", "CREATE EXTENSION IF NOT EXISTS postgis"]]
    for command in commands:
        result = subprocess.run(command, capture_output=True, timeout=60)
        if result.returncode:
            raise RuntimeError("restore target could not be created; existing databases preserved")
    with source.open("rb") as handle:
        result = subprocess.run(["docker", "exec", "-i", container, "pg_restore", "-U",
            "postgres", "--exit-on-error", "--single-transaction", "--no-owner",
            "--no-privileges", "--dbname", new_database], stdin=handle,
            capture_output=True, timeout=180)
    if result.returncode:
        raise RuntimeError("native restore failed; new database retained for diagnosis")
    return {"status": "restored_requires_application_reread", "database": new_database}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["backup", "restore"])
    parser.add_argument("--container", required=True)
    parser.add_argument("--database", required=True)
    parser.add_argument("--namespace", default="unitesis")
    parser.add_argument("--file", type=Path, required=True)
    args = parser.parse_args()
    path = _file(args.file)
    if not path.resolve().is_relative_to(ROOT / "local-data"):
        raise ValueError("backup artifact must be under local-data")
    report = (backup_namespace(args.container, args.database, args.namespace, path)
              if args.operation == "backup" else restore_namespace(
                  args.container, args.database, path))
    print(json.dumps(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
