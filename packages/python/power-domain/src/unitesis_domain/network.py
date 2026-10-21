"""Neutral electrical model and ``ElectricalSnapshot`` v2 (spec 006; CONTRACTS-AND-EVIDENCE).

Semantics adapted from ``flujos/solvers/base.py`` and ``grid-bridge/domain/elements.py``
but rewritten on the standard library: no Pydantic, no solver imports.

The v2 content hash covers every electrically relevant field (connections, states,
P/Q, impedances, lengths, voltages, frequency) and is invariant to record order.
Provenance (source id, files, CRS) lives in the ``SourceManifest`` and is *not* part
of the electrical identity, so two sources describing the same network hash equal.
"""

from __future__ import annotations

from dataclasses import MISSING, dataclass, field, fields
from hashlib import sha256
from json import dumps
from typing import Any

from .units import require_bool, require_finite, require_non_negative, require_positive

SNAPSHOT_SCHEMA = "unitesis.electrical-snapshot/v2"
SNAPSHOT_SCHEMA_V3 = "unitesis.electrical-snapshot/v3"   # v2 + transformers (superset)
SNAPSHOT_SCHEMA_V4 = "unitesis.electrical-snapshot/v4"   # v3 + phase-frame data (superset)
SUPPORTED_SCHEMAS = (SNAPSHOT_SCHEMA, SNAPSHOT_SCHEMA_V3, SNAPSHOT_SCHEMA_V4)

# Phase-frame vocabulary (spec 008-C). Phase sets are written in A-B-C order.
PHASE_SETS = ("A", "B", "C", "AB", "AC", "BC", "ABC")
LOAD_MODELS = ("constant_power", "constant_impedance", "constant_current")
CONNECTIONS = ("wye", "delta")
VECTOR_GROUPS = ("YNyn0",)   # phase-frame transformer connections implemented so far

# Optional v4 fields and their defaults: omitted from the canonical form when default,
# so v2/v3 snapshots keep their identity hash.
_V4_DEFAULTS: dict[str, object] = {
    "phases": "ABC", "z_phase_ohm_per_km": None, "b_phase_us_per_km": None,
    "connection": "wye", "model": "constant_power", "phase_p_mw": None, "phase_q_mvar": None,
    "vector_group": None,
}


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


def _require_phases(value: object, name: str) -> str:
    if value not in PHASE_SETS:
        raise SnapshotError(f"{name} must be one of {', '.join(PHASE_SETS)}, got {value!r}")
    return str(value)


def delta_branches(phases: str) -> tuple[str, ...]:
    """Phase pairs of a delta connection: ABC -> AB, BC, CA; AB/BC -> itself; AC -> CA."""
    if len(phases) == 3:
        return ("AB", "BC", "CA")
    if len(phases) == 2:
        return ("CA",) if phases == "AC" else (phases,)
    raise SnapshotError(f"a delta connection needs at least two phases, got {phases!r}")


def _float_vector(value: object, n: int, name: str) -> tuple[float, ...]:
    if not isinstance(value, (list, tuple)) or len(value) != n:
        raise SnapshotError(f"{name} must have {n} values")
    return tuple(float(require_finite(v, name)) for v in value)


def _phase_matrix(value: object, n: int, name: str, complex_entries: bool) -> tuple:
    """Validate a symmetric n x n matrix; complex entries are [re, im] pairs."""
    if not isinstance(value, (list, tuple)) or len(value) != n:
        raise SnapshotError(f"{name} must be a {n}x{n} matrix")
    rows = []
    for row in value:
        if not isinstance(row, (list, tuple)) or len(row) != n:
            raise SnapshotError(f"{name} must be a {n}x{n} matrix")
        if complex_entries:
            cells = []
            for cell in row:
                if not isinstance(cell, (list, tuple)) or len(cell) != 2:
                    raise SnapshotError(f"{name} entries must be [re, im] pairs")
                cells.append((float(require_finite(cell[0], name)),
                              float(require_finite(cell[1], name))))
            rows.append(tuple(cells))
        else:
            rows.append(tuple(float(require_finite(c, name)) for c in row))
    for i in range(n):
        for j in range(i + 1, n):
            if rows[i][j] != rows[j][i]:
                raise SnapshotError(f"{name} must be symmetric")
        diag = rows[i][i]
        if complex_entries and (diag[0] < 0 or diag[1] <= 0):
            raise SnapshotError(f"{name}: self impedance needs r >= 0 and x > 0")
    return tuple(rows)


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
    # Phase frame (008-C). r/x stay the positive-sequence equivalent used by balanced engines.
    phases: str = "ABC"
    z_phase_ohm_per_km: tuple | None = None    # len(phases)^2 [re, im], Kron-reduced
    b_phase_us_per_km: tuple | None = None     # shunt susceptance matrix, microsiemens/km

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
        n = len(_require_phases(self.phases, f"{self.line_id}.phases"))
        if self.z_phase_ohm_per_km is not None:
            object.__setattr__(self, "z_phase_ohm_per_km", _phase_matrix(
                self.z_phase_ohm_per_km, n, f"{self.line_id}.z_phase_ohm_per_km", True))
        if self.b_phase_us_per_km is not None:
            object.__setattr__(self, "b_phase_us_per_km", _phase_matrix(
                self.b_phase_us_per_km, n, f"{self.line_id}.b_phase_us_per_km", False))
        if self.phases != "ABC" and self.z_phase_ohm_per_km is None:
            raise SnapshotError(f"{self.line_id}: a {self.phases} line needs z_phase_ohm_per_km")

    @property
    def z_ohm(self) -> complex:
        return complex(self.r_ohm_per_km, self.x_ohm_per_km) * self.length_km

    @property
    def is_phase_frame(self) -> bool:
        return (self.phases != "ABC" or self.z_phase_ohm_per_km is not None
                or self.b_phase_us_per_km is not None)


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
    # Phase frame (008-C): P/Q are totals at nominal voltage; ``model`` gives the voltage
    # dependence (ZIP). Per-element values follow ``phases`` (wye) or ``delta_branches``.
    phases: str = "ABC"
    connection: str = "wye"
    model: str = "constant_power"
    phase_p_mw: tuple[float, ...] | None = None
    phase_q_mvar: tuple[float, ...] | None = None

    def __post_init__(self) -> None:
        lid = _require_id(self.load_id, "load_id")
        _require_id(self.bus, f"{lid}.bus")
        require_finite(self.p_mw, f"{lid}.p_mw")
        require_finite(self.q_mvar, f"{lid}.q_mvar")
        require_bool(self.in_service, f"{lid}.in_service")
        _as_floats(self, "p_mw", "q_mvar")
        _require_phases(self.phases, f"{lid}.phases")
        if self.connection not in CONNECTIONS:
            raise SnapshotError(f"{lid}.connection must be one of {', '.join(CONNECTIONS)}")
        if self.model not in LOAD_MODELS:
            raise SnapshotError(f"{lid}.model must be one of {', '.join(LOAD_MODELS)}")
        n = len(self.elements)
        if (self.phase_p_mw is None) != (self.phase_q_mvar is None):
            raise SnapshotError(f"{lid}: phase_p_mw and phase_q_mvar go together")
        if self.phase_p_mw is not None:
            p = _float_vector(self.phase_p_mw, n, f"{lid}.phase_p_mw")
            q = _float_vector(self.phase_q_mvar, n, f"{lid}.phase_q_mvar")
            for total, parts, label in ((self.p_mw, p, "p_mw"), (self.q_mvar, q, "q_mvar")):
                if abs(sum(parts) - total) > 1e-9 * max(1.0, abs(total)):
                    raise SnapshotError(f"{lid}: {label} must equal the sum of its phases")
            object.__setattr__(self, "phase_p_mw", p)
            object.__setattr__(self, "phase_q_mvar", q)

    @property
    def elements(self) -> tuple[str, ...]:
        """Wye: the phases (A, B, ...); delta: the phase pairs (AB, BC, CA)."""
        return tuple(self.phases) if self.connection == "wye" else delta_branches(self.phases)

    def element_powers(self) -> tuple[tuple[str, complex], ...]:
        """Nominal complex power (MVA) per element; equal split when not given per phase."""
        if self.phase_p_mw is None:
            share = complex(self.p_mw, self.q_mvar) / len(self.elements)
            return tuple((e, share) for e in self.elements)
        return tuple((e, complex(p, q)) for e, p, q in
                     zip(self.elements, self.phase_p_mw, self.phase_q_mvar, strict=True))

    @property
    def is_phase_frame(self) -> bool:
        return any(getattr(self, f) != _V4_DEFAULTS[f] for f in
                   ("phases", "connection", "model", "phase_p_mw", "phase_q_mvar"))


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
    """Two-winding transformer, balanced positive sequence (spec 008-B2).

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
    vector_group: str | None = None   # winding connection, required by the phase frame (008-C)

    def __post_init__(self) -> None:
        tid = _require_id(self.transformer_id, "transformer_id")
        if self.vector_group is not None and self.vector_group not in VECTOR_GROUPS:
            raise SnapshotError(f"{tid}: vector_group {self.vector_group!r} not implemented; "
                                f"supported: {', '.join(VECTOR_GROUPS)}")
        if self.vector_group == "YNyn0" and self.shift_degree != 0:
            raise SnapshotError(f"{tid}: YNyn0 has no phase shift")
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
class VoltageRegulator:
    """Step-voltage regulator, one single-phase unit per phase, wye connected (spec 008-C).

    Ideal ratio per phase: ``V_to = (1 + tap * step_percent / 100) * V_from``; currents
    transform with the conjugate ratio (lossless). Taps are fixed (manual control);
    automatic line-drop compensation is outside the current scope.
    """

    regulator_id: str
    from_bus: str
    to_bus: str
    phases: str
    tap_positions: tuple[int, ...]
    step_percent: float
    in_service: bool = True

    def __post_init__(self) -> None:
        rid = _require_id(self.regulator_id, "regulator_id")
        _require_id(self.from_bus, f"{rid}.from_bus")
        _require_id(self.to_bus, f"{rid}.to_bus")
        if self.from_bus == self.to_bus:
            raise SnapshotError(f"{rid}: self-loop")
        n = len(_require_phases(self.phases, f"{rid}.phases"))
        taps = self.tap_positions
        if not isinstance(taps, (list, tuple)) or len(taps) != n or any(
                isinstance(t, bool) or not isinstance(t, int) for t in taps):
            raise SnapshotError(f"{rid}: tap_positions must be {n} integers")
        object.__setattr__(self, "tap_positions", tuple(taps))
        step = require_positive(self.step_percent, f"{rid}.step_percent")
        for t in taps:
            if not 0.8 <= 1 + t * step / 100 <= 1.2:
                raise SnapshotError(f"{rid}: regulator ratio outside [0.8, 1.2]")
        require_bool(self.in_service, f"{rid}.in_service")
        _as_floats(self, "step_percent")

    def ratios(self) -> tuple[tuple[str, float], ...]:
        return tuple((ph, 1 + t * self.step_percent / 100)
                     for ph, t in zip(self.phases, self.tap_positions, strict=True))


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
    regulators: tuple[VoltageRegulator, ...] = ()

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
                     + [t.transformer_id for t in self.transformers]
                     + [r.regulator_id for r in self.regulators], "branch")
        self._unique([ld.load_id for ld in self.loads], "load")
        self._unique([s.bus for s in self.slacks], "slack bus")
        known = set(bus_ids)
        refs = [s.bus for s in self.slacks] + [ld.bus for ld in self.loads]
        for br in (*self.lines, *self.switches, *self.regulators):
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
        transformers the form is v3 = v2 + ``transformers``; with phase-frame data it is
        v4 = v3 + optional phase fields + ``regulators``. Phase fields at their default
        are omitted, so adding the v4 vocabulary changed no existing hash.
        """
        def value(v: Any) -> Any:
            return [value(x) for x in v] if isinstance(v, tuple) else v

        def omitted(it: Any, f: str) -> bool:
            # only optional v4 fields (declared with that default) at their default value
            default = next((d.default for d in fields(it) if d.name == f), MISSING)
            return (f in _V4_DEFAULTS and default == _V4_DEFAULTS[f]
                    and getattr(it, f) == default)

        def rows(items: tuple[Any, ...], key: str) -> list[dict[str, Any]]:
            out = [{f: value(getattr(it, f)) for f in it.__slots__ if not omitted(it, f)}
                   for it in items]
            return sorted(out, key=lambda r: r[key])

        v4 = bool(self.regulators) or bool(self.phase_frame_elements()) or any(
            t.vector_group is not None for t in self.transformers)
        schema = (SNAPSHOT_SCHEMA_V4 if v4 else
                  SNAPSHOT_SCHEMA_V3 if self.transformers else SNAPSHOT_SCHEMA)
        canon = {
            "schema": schema,
            "frequency_hz": float(self.frequency_hz),
            "buses": rows(self.buses, "bus_id"),
            "lines": rows(self.lines, "line_id"),
            "switches": rows(self.switches, "switch_id"),
            "loads": rows(self.loads, "load_id"),
            "slacks": rows(self.slacks, "bus"),
        }
        if self.transformers:
            canon["transformers"] = rows(self.transformers, "transformer_id")
        if self.regulators:
            canon["regulators"] = rows(self.regulators, "regulator_id")
        return canon

    def phase_frame_elements(self) -> tuple[str, ...]:
        """Ids that only a phase-frame engine can represent (balanced engines reject them)."""
        ids = [ln.line_id for ln in self.lines if ln.is_phase_frame]
        ids += [ld.load_id for ld in self.loads if ld.is_phase_frame]
        ids += [r.regulator_id for r in self.regulators]
        return tuple(sorted(ids))

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
            regulators=tuple(VoltageRegulator(**r) for r in data.get("regulators", [])),
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
