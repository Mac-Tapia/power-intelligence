"""Strict neutral JSON ingestion -> ``ElectricalSnapshot`` + ``SourceManifest`` + quarantine.

States (CONTRACTS-AND-EVIDENCE): ``parsed -> quarantined | model_validated``.
Every required field is explicit in the source; nothing is defaulted. Records that fail
are kept in the quarantine with field, reason and source reference, and block the
snapshot (fail closed).
Custody pattern (SHA-256 of original bytes, parser version) adapted from Prodma
``custody/inventory.py``; duplicate-key and non-finite rejection from the earlier
reconciliation draft of this module.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Any, Literal

from unitesis_domain import (
    Bus,
    ElectricalSnapshot,
    Line,
    Load,
    QuarantineRecord,
    Slack,
    SnapshotError,
    Switch,
)

INPUT_SCHEMA = "unitesis.network-input/1"
MANIFEST_SCHEMA = "unitesis.source-manifest/1"
PARSER = "unitesis-neutral-json/0.2.0"
UNITS = {
    "voltage": "kV",
    "length": "km",
    "impedance": "ohm/km",
    "power": "MW/MVAr",
    "current": "kA",
    "frequency": "Hz",
}

_SPECS: dict[str, tuple[type, tuple[str, ...], tuple[str, ...], str]] = {
    # collection: (type, required fields, optional fields, id field)
    "buses": (Bus, ("bus_id", "nominal_kv"), (), "bus_id"),
    "lines": (
        Line,
        (
            "line_id",
            "from_bus",
            "to_bus",
            "length_km",
            "r_ohm_per_km",
            "x_ohm_per_km",
            "in_service",
        ),
        ("max_current_ka",),
        "line_id",
    ),
    "switches": (Switch, ("switch_id", "from_bus", "to_bus", "closed"), (), "switch_id"),
    "loads": (Load, ("load_id", "bus", "p_mw", "q_mvar", "in_service"), (), "load_id"),
    "slacks": (Slack, ("bus", "vm_pu", "angle_deg"), (), "bus"),
}


class IngestionError(ValueError):
    """The source cannot be parsed at all (schema, encoding, duplicate keys)."""


@dataclass
class IngestionResult:
    state: Literal["quarantined", "model_validated"]
    manifest: dict[str, Any]
    quarantine: list[QuarantineRecord] = field(default_factory=list)
    snapshot: ElectricalSnapshot | None = None

    def require_snapshot(self) -> ElectricalSnapshot:
        if self.snapshot is None:
            reasons = "; ".join(f"{q.element_id}.{q.field}: {q.reason}" for q in self.quarantine)
            raise IngestionError(f"source quarantined, calculation blocked: {reasons}")
        return self.snapshot


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise IngestionError(f"duplicate JSON key {key!r}")
        out[key] = value
    return out


def _reject_constant(value: str) -> Any:
    raise IngestionError(f"non-finite JSON constant {value}")


def parse_payload(raw: bytes) -> dict[str, Any]:
    try:
        payload = json.loads(
            raw.decode("utf-8-sig"),
            object_pairs_hook=_no_duplicates,
            parse_constant=_reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise IngestionError(f"unreadable JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise IngestionError("top-level JSON object required")
    if payload.get("schema") != INPUT_SCHEMA:
        raise IngestionError(f"unsupported schema {payload.get('schema')!r}")
    if payload.get("units") != UNITS:
        raise IngestionError(f"units must be declared exactly as {UNITS}")
    allowed = {"schema", "source_id", "units", "network", "crs", "authorization", "provenance"}
    if extra := set(payload) - allowed:
        raise IngestionError(f"unknown top-level fields: {sorted(extra)}")
    if not isinstance(payload.get("source_id"), str) or not payload["source_id"].strip():
        raise IngestionError("source_id required")
    if "provenance" in payload and (not isinstance(payload["provenance"], str)
                                    or not payload["provenance"].strip()):
        raise IngestionError("provenance must be a non-empty string when present")
    if not isinstance(payload.get("network"), dict):
        raise IngestionError("network object required")
    return payload


def build_snapshot(payload: dict[str, Any], source_ref: str) -> IngestionResult:
    net = payload["network"]
    quarantine: list[QuarantineRecord] = []
    built: dict[str, list[Any]] = {}
    for coll, (cls, required, optional, id_field) in _SPECS.items():
        rows = net.get(coll, [] if coll in ("switches", "loads") else None)
        if not isinstance(rows, list):
            quarantine.append(QuarantineRecord("network", coll, "array required", source_ref))
            continue
        built[coll] = []
        for i, row in enumerate(rows):
            ref = f"{source_ref}#/network/{coll}/{i}"
            elem = f"{coll}[{i}]"
            if isinstance(row, dict):
                elem = str(row.get(id_field, elem))
            if not isinstance(row, dict):
                quarantine.append(QuarantineRecord(elem, "*", "object required", ref))
                continue
            missing = [f for f in required if f not in row]
            unknown = sorted(set(row) - set(required) - set(optional))
            for f in missing:
                quarantine.append(QuarantineRecord(elem, f, "missing in source; not imputed", ref))
            for f in unknown:
                quarantine.append(QuarantineRecord(elem, f, "unsupported field", ref))
            if missing or unknown:
                continue
            try:
                built[coll].append(cls(**row))
            except (ValueError, TypeError) as exc:
                quarantine.append(QuarantineRecord(elem, "*", str(exc), ref))
    if "frequency_hz" not in net:
        quarantine.append(QuarantineRecord("network", "frequency_hz", "missing", source_ref))

    counts = {c: len(net.get(c, []) or []) for c in _SPECS if isinstance(net.get(c, []), list)}
    manifest: dict[str, Any] = {
        "schema": MANIFEST_SCHEMA,
        "source_id": payload["source_id"],
        "parser": PARSER,
        "units": UNITS,
        "crs": payload.get("crs"),
        "geometry": "not_ingested",
        "authorization": payload.get("authorization", "not_declared"),
        "provenance": payload.get("provenance"),
        "record_counts": counts,
        "quarantined_fields": len(quarantine),
        "parameter_quality": "explicit_source_values_unverified",
    }
    if quarantine:
        return IngestionResult("quarantined", manifest, quarantine)
    try:
        snapshot = ElectricalSnapshot(
            frequency_hz=net["frequency_hz"],
            buses=tuple(built["buses"]),
            lines=tuple(built["lines"]),
            switches=tuple(built["switches"]),
            loads=tuple(built["loads"]),
            slacks=tuple(built["slacks"]),
            name=payload["source_id"],
        )
    except (SnapshotError, ValueError) as exc:
        quarantine.append(QuarantineRecord("network", "*", str(exc), source_ref))
        return IngestionResult("quarantined", manifest, quarantine)
    manifest["snapshot_sha256"] = snapshot.content_sha256
    return IngestionResult("model_validated", manifest, [], snapshot)


def ingest_file(path: str | Path) -> IngestionResult:
    source = Path(path)
    raw = source.read_bytes()
    payload = parse_payload(raw)
    result = build_snapshot(payload, source.name)
    result.manifest.update(
        file_name=source.name, source_sha256=sha256(raw).hexdigest(), size_bytes=len(raw)
    )
    return result


def snapshot_to_payload(snapshot: ElectricalSnapshot, source_id: str, *,
                        provenance: str | None = None,
                        authorization: str | None = None) -> dict[str, Any]:
    """Inverse mapping, used to export imported feeders and cloned scenarios."""
    canon = snapshot.canonical()
    network = {k: canon[k] for k in ("buses", "lines", "switches", "loads", "slacks")}
    network["frequency_hz"] = canon["frequency_hz"]
    payload: dict[str, Any] = {"schema": INPUT_SCHEMA, "source_id": source_id, "units": UNITS,
                               "network": network}
    if provenance:
        payload["provenance"] = provenance
    if authorization:
        payload["authorization"] = authorization
    return payload
