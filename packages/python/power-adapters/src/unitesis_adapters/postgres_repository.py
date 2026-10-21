"""Spec 004 native PostgreSQL ports, append-only identities and atomic job claims.

Initialization is an explicit sandbox/migration operation, never an implicit
fallback from a failed database connection. DSNs must stay outside repository/logs.
"""

from __future__ import annotations

import json
import re
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from unitesis_domain import ElectricalSnapshot

from .job_repository import ERROR_CODES, RESERVED
from .sql_repository import RepositoryIntegrityError

ROOT = Path(__file__).resolve().parents[5]


def _json(value):
    # Also reject non-finite values before sending to the database.
    json.dumps(value, allow_nan=False)
    return Jsonb(value)


class PostgresRepository:
    def __init__(self, dsn: str, *, namespace: str = "unitesis", initialize: bool = False):
        if not re.fullmatch(r"[a-z][a-z0-9_]{0,62}", namespace):
            raise ValueError("invalid database namespace")
        self._dsn, self.namespace = dsn, namespace
        if initialize:
            with psycopg.connect(dsn) as conn:
                for name in ("0001_core.sql", "0002_jobs.sql", "0003_snapshot_v3.sql"):
                    script = (ROOT / "infra/db/postgres" / name).read_text(encoding="utf-8")
                    # namespace is validated before interpolation; SQL contains no user data.
                    if name == "0001_core.sql":
                        script = script.replace("CREATE SCHEMA IF NOT EXISTS unitesis;",
                                                f"CREATE SCHEMA IF NOT EXISTS {namespace};")
                        script = script.replace("SET search_path = unitesis, public;",
                                                f"SET search_path = {namespace}, public;")
                    conn.execute(script)
        with psycopg.connect(dsn) as conn:
            for table in ("source_manifest", "electrical_snapshot", "study_result", "study_job"):
                if conn.execute("SELECT to_regclass(%s)",
                                (f"{namespace}.{table}",)).fetchone()[0] is None:
                    raise RepositoryIntegrityError("required PostgreSQL migration is missing")

    @contextmanager
    def _connection(self):
        with psycopg.connect(self._dsn, row_factory=dict_row) as conn:
            conn.execute(sql.SQL("SET LOCAL search_path TO {}, public").format(
                sql.Identifier(self.namespace)))
            yield conn

    def close(self) -> None:
        """Connections are scoped to each operation and already closed."""

    def _once(self, table: str, key_column: str, values: dict[str, Any], compare: str):
        key = values[key_column]
        with self._connection() as conn:
            columns = list(values)
            conn.execute(sql.SQL("INSERT INTO {} ({}) VALUES ({}) ON CONFLICT DO NOTHING").format(
                sql.Identifier(table), sql.SQL(",").join(map(sql.Identifier, columns)),
                sql.SQL(",").join(sql.Placeholder() for _ in columns)), tuple(values.values()))
            row = conn.execute(sql.SQL("SELECT {} FROM {} WHERE {}=%s").format(
                sql.Identifier(compare), sql.Identifier(table), sql.Identifier(key_column)),
                (key,)).fetchone()
            expected = (json.loads(json.dumps(values[compare].obj, allow_nan=False))
                        if isinstance(values[compare], Jsonb) else values[compare])
            if row[compare] != expected:
                raise RepositoryIntegrityError("different payload under stored digest")
        return key

    def save_source(self, manifest, quarantine=None):
        key = self._once("source_manifest", "source_sha256", {
            "source_sha256": manifest["source_sha256"], "source_id": manifest["source_id"],
            "parser": manifest["parser"], "manifest": _json(manifest)}, "manifest")
        if quarantine:
            with self._connection() as conn:
                for record in quarantine:
                    conn.execute("INSERT INTO quarantine_record (source_sha256,element_id,field,"
                                 "reason,source_ref) SELECT %s,%s,%s,%s,%s WHERE NOT EXISTS "
                                 "(SELECT 1 FROM quarantine_record WHERE source_sha256=%s "
                                 "AND element_id=%s AND field=%s AND reason=%s AND source_ref=%s)",
                                 (key, record.element_id, record.field, record.reason,
                                  record.source_ref) * 2)
        return key

    def save_snapshot(self, snapshot, manifest):
        source = self.save_source(manifest) if "source_sha256" in manifest else None
        return self._once("electrical_snapshot", "snapshot_sha256", {
            "snapshot_sha256": snapshot.content_sha256,
            "schema_version": snapshot.canonical()["schema"], "source_sha256": source,
            "name": snapshot.name, "canonical": _json(snapshot.canonical())}, "canonical")

    def list_snapshots(self):
        with self._connection() as conn:
            result = conn.execute("SELECT snapshot_sha256,name,source_sha256 FROM "
                                  "electrical_snapshot ORDER BY created_at,snapshot_sha256")
            return result.fetchall()

    def load_snapshot(self, digest):
        with self._connection() as conn:
            row = conn.execute("SELECT canonical,name FROM electrical_snapshot "
                               "WHERE snapshot_sha256=%s", (digest,)).fetchone()
        if row is None:
            raise KeyError(digest)
        snapshot = ElectricalSnapshot.from_canonical(row["canonical"], name=row["name"] or "")
        if snapshot.content_sha256 != digest:
            raise RepositoryIntegrityError("stored snapshot digest mismatch")
        return snapshot

    def save_result(self, result, evidence_path=None):
        return self._once("study_result", "result_sha256", {
            "result_sha256": result.result_sha256, "request_sha256": result.request_sha256,
            "snapshot_sha256": result.snapshot_sha256, "scenario_id": result.scenario_id,
            "engine": result.engine, "engine_version": result.engine_version,
            "status": result.status, "payload": _json(result.as_dict()),
            "evidence_path": evidence_path}, "payload")

    def get_result(self, digest):
        with self._connection() as conn:
            row = conn.execute("SELECT payload,evidence_path FROM study_result "
                               "WHERE result_sha256=%s", (digest,)).fetchone()
        if row is None:
            raise KeyError(digest)
        return row["payload"] | {"evidence_path": row["evidence_path"]}

    def results_for_snapshot(self, digest):
        with self._connection() as conn:
            return conn.execute("SELECT result_sha256,scenario_id,engine,status FROM study_result "
                                "WHERE snapshot_sha256=%s ORDER BY created_at,result_sha256",
                                (digest,)).fetchall()


class PostgresJobRepository(PostgresRepository):
    def enqueue(self, job_id, kind, request):
        if not job_id or kind not in {"study", "new_load", "alternatives"}:
            raise ValueError("invalid job identity or kind")
        with self._connection() as conn:
            conn.execute("INSERT INTO study_job(job_id,kind,request,status) "
                         "VALUES(%s,%s,%s,'queued') ON CONFLICT DO NOTHING",
                         (job_id, kind, _json(request)))
            row = conn.execute("SELECT kind,request FROM study_job WHERE job_id=%s",
                               (job_id,)).fetchone()
            if row != {"kind": kind, "request": request}:
                raise ValueError("job identity conflicts with stored request")
        return self.get(job_id)

    def get(self, job_id):
        with self._connection() as conn:
            row = conn.execute("SELECT job_id,kind,request,status,outcome FROM study_job "
                               "WHERE job_id=%s", (job_id,)).fetchone()
        if row is None:
            raise KeyError(job_id)
        outcome = row.pop("outcome")
        return row | outcome

    def claim(self, job_id):
        with self._connection() as conn:
            return conn.execute("UPDATE study_job SET status='running' "
                                "WHERE job_id=%s AND status='queued'", (job_id,)).rowcount == 1

    def _terminal(self, job_id, status, outcome):
        if RESERVED & outcome.keys():
            raise ValueError("reserved job outcome fields")
        with self._connection() as conn:
            changed = conn.execute("UPDATE study_job SET status=%s,outcome=%s "
                                   "WHERE job_id=%s AND status='running'",
                                   (status, _json(outcome), job_id)).rowcount
            if changed != 1:
                raise ValueError("job is not running")
        return self.get(job_id)

    def finish(self, job_id, outcome):
        return self._terminal(job_id, "finished", outcome)

    def fail(self, job_id, error_code):
        if error_code not in ERROR_CODES:
            raise ValueError("unsupported error code")
        return self._terminal(job_id, "failed", {"error_code": error_code})

    def recover_interrupted(self):
        raise RuntimeError("PostgreSQL recovery requires explicit worker coordination")
