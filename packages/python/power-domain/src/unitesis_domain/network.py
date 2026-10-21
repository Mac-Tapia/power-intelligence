"""Neutral electrical model and ``ElectricalSnapshot`` v2 (spec 004; CONTRACTS-AND-EVIDENCE).

Semantics adapted from ``flujos/solvers/base.py`` and ``grid-bridge/domain/elements.py``
but rewritten on the standard library: no Pydantic, no solver imports.

The v2 content hash covers every electrically relevant field (connections, states,
P/Q, impedances, lengths, voltages, frequency) and is invariant to record order.
Provenance (source id, files, CRS) lives in the ``SourceManifest`` and is *not* part
of the electrical identity, so two sources describing the same network hash equal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from json import dumps
from typing import Any

from .units import require_bool, require_finite, require_non_negative, require_positive

SNAPSHOT_SCHEMA = "unitesis.electrical-snapshot/v2"
SNAPSHOT_SCHEMA_V3 = "unitesis.electrical-snapshot/v3"   # v2 + transformers (superset)
SUPPORTED_SCHEMAS = (SNAPSHOT_SCHEMA, SNAPSHOT_SCHEMA_V3)


class SnapshotError(ValueError):
    """The electrical snapshot violates a structural invariant."""


def _require_id(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SnapshotError(f"{name} must be a non-empty string")
    return value


def _as_floats(obj: object, *names: str) -> None:
    """Store numeric fields as float so 1 and 1.0 give the same identity (JSON round trips)."""
    for name in names:
        value = getattr(obj, name)
        if value is not None:
            object.__setattr__(obj, name, float(value))


@dataclass(frozen=True, slots=True)
class Bus:
    bus_id: str
    nominal_kv: float

    def __post_init__(self) -> None:
        _require_id(self.bus_id, "bus_id")
        kv = require_positive(self.nominal_kv, f"{self.bus_id}.nominal_kv")
        if kv >= 2000:
            raise SnapshotError(f"{self.bus_id}: nominal_kv {kv} outside physical range")
        _as_floats(self, "nominal_kv")


@dataclass(frozen=True, slots=True)
class Line:
    line_id: str
    from_bus: str
    to_bus: str
    length_km: float
    r_ohm_per_km: float
    x_ohm_per_km: float
    max_current_ka: float | None = None
    in_service: bool = True

    def __post_init__(self) -> None:
        _require_id(self.line_id, "line_id")
        _require_id(self.from_bus, f"{self.line_id}.from_bus")
        _require_id(self.to_bus, f"{self.line_id}.to_bus")
        if self.from_bus == self.to_bus:
            raise SnapshotError(f"{self.line_id}: self-loop")
        require_positive(self.length_km, f"{self.line_id}.length_km")
        r = require_non_negative(self.r_ohm_per_km, f"{self.line_id}.r_ohm_per_km")
        x = require_non_negative(self.x_ohm_per_km, f"{self.line_id}.x_ohm_per_km")
        if r + x == 0:
            raise SnapshotError(f"{self.line_id}: zero series impedance")
        if self.max_current_ka is not None:
            require_positive(self.max_current_ka, f"{self.line_id}.max_current_ka")
        require_bool(self.in_service, f"{self.line_id}.in_service")
        _as_floats(self, "length_km", "r_ohm_per_km", "x_ohm_per_km", "max_current_ka")

    @property
    def z_ohm(self) -> complex:
        return complex(self.r_ohm_per_km, self.x_ohm_per_km) * self.length_km


@dataclass(frozen=True, slots=True)
class Switch:
    switch_id: str
    from_bus: str
    to_bus: str
    closed: bool

    def __post_init__(self) -> None:
        _require_id(self.switch_id, "switch_id")
        _require_id(self.from_bus, f"{self.switch_id}.from_bus")
        _require_id(self.to_bus, f"{self.switch_id}.to_bus")
        if self.from_bus == self.to_bus:
            raise SnapshotError(f"{self.switch_id}: self-loop")
        require_bool(self.closed, f"{self.switch_id}.closed")


@dataclass(frozen=True, slots=True)
class Load:
    load_id: str
    bus: str
    p_mw: float
    q_mvar: float
    in_service: bool = True

    def __post_init__(self) -> None:
        _require_id(self.load_id, "load_id")
        _require_id(self.bus, f"{self.load_id}.bus")
        require_finite(self.p_mw, f"{self.load_id}.p_mw")
        require_finite(self.q_mvar, f"{self.load_id}.q_mvar")
        require_bool(self.in_service, f"{self.load_id}.in_service")
        _as_floats(self, "p_mw", "q_mvar")


@dataclass(frozen=True, slots=True)
class Slack:
    bus: str
    vm_pu: float = 1.0
    angle_deg: float = 0.0

    def __post_init__(self) -> None:
        _require_id(self.bus, "slack.bus")
        vm = require_positive(self.vm_pu, "slack.vm_pu")
        if not 0.5 <= vm <= 1.5:
            raise SnapshotError(f"slack vm_pu {vm} outside [0.5, 1.5]")
        require_finite(self.angle_deg, "slack.angle_deg")
        _as_floats(self, "vm_pu", "angle_deg")


@dataclass(frozen=True, slots=True)
class Transformer:
    """Two-winding transformer, balanced positive sequence (spec 004-B2).

    Series impedance from the short-circuit test (``vk_percent``, ``vkr_percent`` on
    ``sn_mva``); rated voltages may differ from the bus nominal voltages (off-nominal
    ratio). Tap on the HV side: ratio factor ``1 + tap_pos * tap_step_percent / 100``.
    ``shift_degree`` is the vector-group phase shift (LV lags HV by this angle).
    The magnetising branch is outside the current scope and is not modelled.
    """

    transformer_id: str
    hv_bus: str
    lv_bus: str
    sn_mva: float
    vn_hv_kv: float
    vn_lv_kv: float
    vk_percent: float
    vkr_percent: float
    tap_pos: int = 0
    tap_step_percent: float = 0.0
    shift_degree: float = 0.0
    in_service: bool = True

    def __post_init__(self) -> None:
        tid = _require_id(self.transformer_id, "transformer_id")
        _require_id(self.hv_bus, f"{tid}.hv_bus")
        _require_id(self.lv_bus, f"{tid}.lv_bus")
        if self.hv_bus == self.lv_bus:
            raise SnapshotError(f"{tid}: self-loop")
        require_positive(self.sn_mva, f"{tid}.sn_mva")
        hv = require_positive(self.vn_hv_kv, f"{tid}.vn_hv_kv")
        lv = require_positive(self.vn_lv_kv, f"{tid}.vn_lv_kv")
        if hv < lv:
            raise SnapshotError(f"{tid}: vn_hv_kv must be >= vn_lv_kv")
        vk = require_positive(self.vk_percent, f"{tid}.vk_percent")
        vkr = require_non_negative(self.vkr_percent, f"{tid}.vkr_percent")
        if vkr > vk or vk > 50:
            raise SnapshotError(f"{tid}: need 0 <= vkr_percent <= vk_percent <= 50")
        if isinstance(self.tap_pos, bool) or not isinstance(self.tap_pos, int):
            raise SnapshotError(f"{tid}: tap_pos must be an integer")
        step = require_finite(self.tap_step_percent, f"{tid}.tap_step_percent")
        if not 0.5 <= 1 + self.tap_pos * step / 100 <= 1.5:
            raise SnapshotError(f"{tid}: tap ratio outside [0.5, 1.5]")
        require_finite(self.shift_degree, f"{tid}.shift_degree")
        require_bool(self.in_service, f"{tid}.in_service")
        _as_floats(self, "sn_mva", "vn_hv_kv", "vn_lv_kv", "vk_percent", "vkr_percent",
                   "tap_step_percent", "shift_degree")


@dataclass(frozen=True, slots=True)
class ElectricalSnapshot:
    """Immutable, validated network content. Construction fails closed."""

    frequency_hz: float
    buses: tuple[Bus, ...]
    lines: tuple[Line, ...] = ()
    switches: tuple[Switch, ...] = ()
    loads: tuple[Load, ...] = ()
    slacks: tuple[Slack, ...] = ()
    name: str = field(default="", compare=False)
    transformers: tuple[Transformer, ...] = ()

    def __post_init__(self) -> None:
        freq = require_positive(self.frequency_hz, "frequency_hz")
        if freq not in (50.0, 60.0):
            raise SnapshotError(f"frequency_hz must be 50 or 60, got {freq}")
        _as_floats(self, "frequency_hz")
        if not self.buses:
            raise SnapshotError("at least one bus is required")
        if not self.slacks:
            raise SnapshotError("at least one slack (external grid) is required")
        bus_ids = [b.bus_id for b in self.buses]
        self._unique(bus_ids, "bus")
        self._unique([ln.line_id for ln in self.lines] + [s.switch_id for s in self.switches]
                     + [t.transformer_id for t in self.transformers], "branch")
        self._unique([ld.load_id for ld in self.loads], "load")
        self._unique([s.bus for s in self.slacks], "slack bus")
        known = set(bus_ids)
        refs = [s.bus for s in self.slacks] + [ld.bus for ld in self.loads]
        for br in (*self.lines, *self.switches):
            refs += [br.from_bus, br.to_bus]
        for tr in self.transformers:
            refs += [tr.hv_bus, tr.lv_bus]
        missing = sorted(set(refs) - known)
        if missing:
            raise SnapshotError(f"unknown bus references: {', '.join(missing)}")

    @staticmethod
    def _unique(ids: list[str], label: str) -> None:
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        if dupes:
            raise SnapshotError(f"duplicate {label} ids: {', '.join(dupes)}")

    def bus(self, bus_id: str) -> Bus:
        for b in self.buses:
            if b.bus_id == bus_id:
                return b
        raise KeyError(bus_id)

    def canonical(self) -> dict[str, Any]:
        """Order-independent canonical form; the basis of the identity hash.

        Snapshots without transformers keep the exact v2 form (unchanged hashes); with
        transformers the form is v3 = v2 + ``transformers``.
        """
        def rows(items: tuple[Any, ...], key: str) -> list[dict[str, Any]]:
            out = [{f: getattr(it, f) for f in it.__slots__} for it in items]
            return sorted(out, key=lambda r: r[key])

        canon = {
            "schema": SNAPSHOT_SCHEMA_V3 if self.transformers else SNAPSHOT_SCHEMA,
            "frequency_hz": float(self.frequency_hz),
            "buses": rows(self.buses, "bus_id"),
            "lines": rows(self.lines, "line_id"),
            "switches": rows(self.switches, "switch_id"),
            "loads": rows(self.loads, "load_id"),
            "slacks": rows(self.slacks, "bus"),
        }
        if self.transformers:
            canon["transformers"] = rows(self.transformers, "transformer_id")
        return canon

    @property
    def content_sha256(self) -> str:
        payload = dumps(self.canonical(), sort_keys=True, separators=(",", ":"), allow_nan=False)
        return sha256(payload.encode("utf-8")).hexdigest()

    @classmethod
    def from_canonical(cls, data: dict[str, Any], name: str = "") -> ElectricalSnapshot:
        if data.get("schema") not in SUPPORTED_SCHEMAS:
            raise SnapshotError(f"unsupported snapshot schema {data.get('schema')!r}")
        return cls(
            frequency_hz=data["frequency_hz"],
            buses=tuple(Bus(**r) for r in data["buses"]),
            lines=tuple(Line(**r) for r in data.get("lines", [])),
            switches=tuple(Switch(**r) for r in data.get("switches", [])),
            loads=tuple(Load(**r) for r in data.get("loads", [])),
            slacks=tuple(Slack(**r) for r in data["slacks"]),
            transformers=tuple(Transformer(**r) for r in data.get("transformers", [])),
            name=name,
        )


@dataclass(frozen=True, slots=True)
class QuarantineRecord:
    """A source field that could not be accepted; never silently imputed."""

    element_id: str
    field: str
    reason: str
    source_ref: str

    def as_dict(self) -> dict[str, str]:
        return {"element_id": self.element_id, "field": self.field,
                "reason": self.reason, "source_ref": self.source_ref}
