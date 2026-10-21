"""Spec 004 local profile: SQLite jobs with atomic claims and immutable terminals."""

from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS study_job (
    job_id TEXT PRIMARY KEY, kind TEXT NOT NULL, request TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('queued','running','finished','failed')),
    outcome TEXT NOT NULL DEFAULT '{}');
CREATE TRIGGER IF NOT EXISTS job_terminal_no_update BEFORE UPDATE ON study_job
WHEN OLD.status IN ('finished','failed')
BEGIN SELECT RAISE(ABORT, 'terminal job is immutable'); END;
CREATE TRIGGER IF NOT EXISTS job_no_delete BEFORE DELETE ON study_job
BEGIN SELECT RAISE(ABORT, 'job deletion forbidden'); END;
"""
RESERVED = {"job_id", "kind", "request", "status"}
ERROR_CODES = {"interrupted", "execution_failed"}


def _dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


class SqliteJobRepository:
    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = str(path)
        self._lock = threading.RLock()
        self._closed = False
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._memory = (sqlite3.connect(":memory:", check_same_thread=False)
                        if self.path == ":memory:" else None)
        with self._connection() as db:
            db.executescript(SCHEMA)

    @contextmanager
    def _connection(self):
        with self._lock:
            if self._closed:
                raise RuntimeError("repository is closed")
            db = self._memory or sqlite3.connect(self.path, timeout=30)
            try:
                with db:
                    yield db
            finally:
                if self._memory is None:
                    db.close()

    def close(self) -> None:
        with self._lock:
            if self._memory is not None and not self._closed:
                self._memory.close()
            self._closed = True

    def enqueue(self, job_id: str, kind: str, request: dict[str, Any]) -> dict[str, Any]:
        if not job_id or kind not in {"study", "new_load", "alternatives"}:
            raise ValueError("invalid job identity or kind")
        payload = _dump(request)
        with self._connection() as db:
            db.execute("INSERT OR IGNORE INTO study_job(job_id,kind,request,status) "
                       "VALUES(?,?,?,'queued')", (job_id, kind, payload))
            row = db.execute("SELECT kind,request FROM study_job WHERE job_id=?",
                             (job_id,)).fetchone()
            if row != (kind, payload):
                raise ValueError("job identity conflicts with stored request")
        return self.get(job_id)

    def get(self, job_id: str) -> dict[str, Any]:
        with self._connection() as db:
            row = db.execute("SELECT kind,request,status,outcome FROM study_job WHERE job_id=?",
                             (job_id,)).fetchone()
        if row is None:
            raise KeyError(job_id)
        return {"job_id": job_id, "kind": row[0], "request": json.loads(row[1]),
                "status": row[2], **json.loads(row[3])}

    def claim(self, job_id: str) -> bool:
        with self._connection() as db:
            return db.execute("UPDATE study_job SET status='running' "
                              "WHERE job_id=? AND status='queued'", (job_id,)).rowcount == 1

    def _terminal(self, job_id: str, status: str, outcome: dict[str, Any]) -> dict[str, Any]:
        if RESERVED & outcome.keys():
            raise ValueError("reserved job fields in outcome")
        payload = _dump(outcome)
        with self._connection() as db:
            changed = db.execute("UPDATE study_job SET status=?,outcome=? "
                                 "WHERE job_id=? AND status='running'",
                                 (status, payload, job_id)).rowcount
            if changed != 1:
                raise ValueError("job is not running")
        return self.get(job_id)

    def finish(self, job_id: str, outcome: dict[str, Any]) -> dict[str, Any]:
        return self._terminal(job_id, "finished", outcome)

    def fail(self, job_id: str, error_code: str) -> dict[str, Any]:
        if error_code not in ERROR_CODES:
            raise ValueError("unsupported public error code")
        return self._terminal(job_id, "failed", {"error_code": error_code})

    def recover_interrupted(self) -> int:
        """Single API process only: invoke once before serving, never during execution."""
        with self._connection() as db:
            return db.execute("UPDATE study_job SET status='failed',outcome=? "
                              "WHERE status='running'",
                              (_dump({"error_code": "interrupted"}),)).rowcount
