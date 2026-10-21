"""SQLite repository implementing Snapshot/Study/Dataset ports (stdlib ``sqlite3``).

Same content-addressed, append-only model as ``infra/db/postgres/0001_core.sql``.
Re-inserting an identical record is idempotent; a different payload under an existing
digest is an integrity error (it can only mean corruption or a hashing bug).
On read, snapshots are rebuilt and their digest recomputed before being returned.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from unitesis_domain import ElectricalSnapshot, QuarantineRecord, StudyResult

_SCHEMA = """
CREATE TABLE IF NOT EXISTS source_manifest (
    source_sha256 TEXT PRIMARY KEY, source_id TEXT NOT NULL, manifest TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS electrical_snapshot (
    snapshot_sha256 TEXT PRIMARY KEY, source_sha256 TEXT REFERENCES source_manifest,
    name TEXT, canonical TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS quarantine_record (
    id INTEGER PRIMARY KEY, source_sha256 TEXT NOT NULL REFERENCES source_manifest,
    element_id TEXT NOT NULL, field TEXT NOT NULL, reason TEXT NOT NULL,
    source_ref TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS study_result (
    result_sha256 TEXT PRIMARY KEY, request_sha256 TEXT NOT NULL,
    snapshot_sha256 TEXT NOT NULL REFERENCES electrical_snapshot,
    scenario_id TEXT NOT NULL, engine TEXT NOT NULL, engine_version TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('computed','failed','unavailable')),
    payload TEXT NOT NULL, evidence_path TEXT);
CREATE TABLE IF NOT EXISTS forecast_dataset (
    dataset_sha256 TEXT PRIMARY KEY, source_sha256 TEXT NOT NULL, manifest TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS snapshot_no_update BEFORE UPDATE ON electrical_snapshot
    BEGIN SELECT RAISE(ABORT, 'append-only'); END;
CREATE TRIGGER IF NOT EXISTS snapshot_no_delete BEFORE DELETE ON electrical_snapshot
    BEGIN SELECT RAISE(ABORT, 'append-only'); END;
CREATE TRIGGER IF NOT EXISTS result_no_update BEFORE UPDATE ON study_result
    BEGIN SELECT RAISE(ABORT, 'append-only'); END;
CREATE TRIGGER IF NOT EXISTS result_no_delete BEFORE DELETE ON study_result
    BEGIN SELECT RAISE(ABORT, 'append-only'); END;
"""


class RepositoryIntegrityError(RuntimeError):
    pass


def _dump(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)


class SqliteRepository:
    def __init__(self, path: str | Path = ":memory:") -> None:
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(str(path), check_same_thread=False)
        self._db.execute("PRAGMA foreign_keys = ON")
        self._db.executescript(_SCHEMA)

    def close(self) -> None:
        self._db.close()

    def _insert_once(self, table: str, key_col: str, key: str, row: dict[str, Any],
                     compare_col: str) -> None:
        cur = self._db.execute(f"SELECT {compare_col} FROM {table} WHERE {key_col} = ?", (key,))
        existing = cur.fetchone()
        if existing is not None:
            if existing[0] != row[compare_col]:
                raise RepositoryIntegrityError(f"{table}: different content under digest {key}")
            return
        cols = ", ".join(row)
        marks = ", ".join("?" for _ in row)
        with self._db:
            self._db.execute(f"INSERT INTO {table} ({cols}) VALUES ({marks})", tuple(row.values()))

    # --- SnapshotRepository ------------------------------------------------------------
    def save_source(self, manifest: dict[str, Any],
                    quarantine: list[QuarantineRecord] | None = None) -> str:
        key = manifest["source_sha256"]
        self._insert_once("source_manifest", "source_sha256", key,
                          {"source_sha256": key, "source_id": manifest["source_id"],
                           "manifest": _dump(manifest)}, "manifest")
        exists = self._db.execute("SELECT COUNT(*) FROM quarantine_record WHERE source_sha256=?",
                                  (key,)).fetchone()[0]
        if quarantine and not exists:
            with self._db:
                self._db.executemany(
                    "INSERT INTO quarantine_record (source_sha256, element_id, field, reason, "
                    "source_ref) VALUES (?,?,?,?,?)",
                    [(key, q.element_id, q.field, q.reason, q.source_ref) for q in quarantine])
        return key

    def save_snapshot(self, snapshot: ElectricalSnapshot, manifest: dict[str, Any]) -> str:
        source = self.save_source(manifest) if "source_sha256" in manifest else None
        key = snapshot.content_sha256
        self._insert_once("electrical_snapshot", "snapshot_sha256", key,
                          {"snapshot_sha256": key, "source_sha256": source,
                           "name": snapshot.name, "canonical": _dump(snapshot.canonical())},
                          "canonical")
        return key

    def list_snapshots(self) -> list[dict[str, Any]]:
        cur = self._db.execute("SELECT snapshot_sha256, name, source_sha256 FROM "
                               "electrical_snapshot ORDER BY rowid")
        return [dict(zip(("snapshot_sha256", "name", "source_sha256"), r, strict=True))
                for r in cur.fetchall()]

    def load_snapshot(self, snapshot_sha256: str) -> ElectricalSnapshot:
        row = self._db.execute("SELECT canonical, name FROM electrical_snapshot "
                               "WHERE snapshot_sha256 = ?", (snapshot_sha256,)).fetchone()
        if row is None:
            raise KeyError(snapshot_sha256)
        snapshot = ElectricalSnapshot.from_canonical(json.loads(row[0]), name=row[1] or "")
        if snapshot.content_sha256 != snapshot_sha256:
            raise RepositoryIntegrityError("stored snapshot does not match its digest")
        return snapshot

    def quarantine_for(self, source_sha256: str) -> list[dict[str, str]]:
        cur = self._db.execute("SELECT element_id, field, reason, source_ref FROM "
                               "quarantine_record WHERE source_sha256 = ? ORDER BY id",
                               (source_sha256,))
        return [dict(zip(("element_id", "field", "reason", "source_ref"), r, strict=True))
                for r in cur.fetchall()]

    # --- StudyRepository ---------------------------------------------------------------
    def save_result(self, result: StudyResult, evidence_path: str | None = None) -> str:
        key = result.result_sha256
        self._insert_once("study_result", "result_sha256", key, {
            "result_sha256": key, "request_sha256": result.request_sha256,
            "snapshot_sha256": result.snapshot_sha256, "scenario_id": result.scenario_id,
            "engine": result.engine, "engine_version": result.engine_version,
            "status": result.status, "payload": _dump(result.as_dict()),
            "evidence_path": evidence_path}, "payload")
        return key

    def get_result(self, result_sha256: str) -> dict[str, Any]:
        row = self._db.execute("SELECT payload, evidence_path FROM study_result "
                               "WHERE result_sha256 = ?", (result_sha256,)).fetchone()
        if row is None:
            raise KeyError(result_sha256)
        return json.loads(row[0]) | {"evidence_path": row[1]}

    def results_for_snapshot(self, snapshot_sha256: str) -> list[dict[str, str]]:
        cur = self._db.execute("SELECT result_sha256, scenario_id, engine, status FROM "
                               "study_result WHERE snapshot_sha256 = ? ORDER BY rowid",
                               (snapshot_sha256,))
        return [dict(zip(("result_sha256", "scenario_id", "engine", "status"), r, strict=True))
                for r in cur.fetchall()]

    # --- DatasetRepository -------------------------------------------------------------
    def save_dataset(self, manifest: dict[str, Any]) -> str:
        key = manifest["dataset_sha256"]
        self._insert_once("forecast_dataset", "dataset_sha256", key, {
            "dataset_sha256": key, "source_sha256": manifest["source"]["source_sha256"],
            "manifest": _dump(manifest)}, "manifest")
        return key

    def get_dataset(self, dataset_sha256: str) -> dict[str, Any]:
        row = self._db.execute("SELECT manifest FROM forecast_dataset WHERE dataset_sha256 = ?",
                               (dataset_sha256,)).fetchone()
        if row is None:
            raise KeyError(dataset_sha256)
        return json.loads(row[0])
