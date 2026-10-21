"""StudyRequest / StudyResult contracts (spec 008; CONTRACTS-AND-EVIDENCE).

Source, model, request and result carry distinct hashes. Execution time is never part
of an identity. A result's status is explicit; success is never inferred from
``converged`` alone, an HTTP code or ``bool(value)``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
from json import dumps
from typing import Any, Literal

from .units import require_finite, require_positive

StudyStatus = Literal["computed", "failed", "unavailable"]
STUDY_REQUEST_SCHEMA = "unitesis.study-request/v1"
STUDY_RESULT_SCHEMA = "unitesis.study-result/v1"


def _digest(payload: dict[str, Any]) -> str:
    return sha256(dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True, slots=True)
class SolverSettings:
    tolerance_pu: float = 1e-8  # MVA mismatch (BASE_MVA = 1); pandapower default
    max_iterations: int = 100

    def __post_init__(self) -> None:
        tol = require_positive(self.tolerance_pu, "tolerance_pu")
        if tol >= 1e-2:
            raise ValueError("tolerance_pu too loose for an engineering study")
        if isinstance(self.max_iterations, bool) or not isinstance(self.max_iterations, int):
            raise ValueError("max_iterations must be int")
        if not 1 <= self.max_iterations <= 10_000:
            raise ValueError("max_iterations out of range")


@dataclass(frozen=True, slots=True)
class ComparisonTolerances:
    """Initial per-case tolerances from CONTRACTS-AND-EVIDENCE; never relaxed automatically."""

    voltage_pu: float = 1e-6
    angle_deg: float = 1e-4
    losses_mw: float = 1e-6
    current_a_abs: float = 1e-3
    current_rel: float = 1e-4
    balance_mva: float = 1e-6

    def __post_init__(self) -> None:
        for name in self.__slots__:
            require_positive(getattr(self, name), f"tolerance.{name}")


@dataclass(frozen=True, slots=True)
class StudyRequest:
    snapshot_sha256: str
    scenario_id: str
    engine: str
    settings: SolverSettings = field(default_factory=SolverSettings)

    def __post_init__(self) -> None:
        if len(self.snapshot_sha256) != 64:
            raise ValueError("snapshot_sha256 must be a SHA-256 hex digest")
        if not self.scenario_id.strip() or not self.engine.strip():
            raise ValueError("scenario_id and engine are required")

    def as_dict(self) -> dict[str, Any]:
        return {"schema": STUDY_REQUEST_SCHEMA, "snapshot_sha256": self.snapshot_sha256,
                "scenario_id": self.scenario_id, "engine": self.engine,
                "settings": asdict(self.settings)}

    @property
    def request_sha256(self) -> str:
        return _digest(self.as_dict())


@dataclass(frozen=True, slots=True)
class BusResult:
    bus_id: str
    vm_pu: float
    va_deg: float

    def __post_init__(self) -> None:
        require_finite(self.vm_pu, f"{self.bus_id}.vm_pu")
        require_finite(self.va_deg, f"{self.bus_id}.va_deg")


@dataclass(frozen=True, slots=True)
class BranchResult:
    branch_id: str
    from_bus: str
    to_bus: str
    i_ka: float
    p_from_mw: float
    q_from_mvar: float
    p_loss_mw: float
    q_loss_mvar: float
    loading_percent: float | None = None

    def __post_init__(self) -> None:
        for name in ("i_ka", "p_from_mw", "q_from_mvar", "p_loss_mw", "q_loss_mvar"):
            require_finite(getattr(self, name), f"{self.branch_id}.{name}")
        if self.loading_percent is not None:
            require_finite(self.loading_percent, f"{self.branch_id}.loading_percent")


@dataclass(frozen=True, slots=True)
class StudyResult:
    request_sha256: str
    snapshot_sha256: str
    scenario_id: str
    engine: str
    engine_version: str
    status: StudyStatus
    converged: bool = False
    iterations: int = 0
    residual_pu: float | None = None
    buses: tuple[BusResult, ...] = ()
    branches: tuple[BranchResult, ...] = ()
    slack_p_mw: float | None = None
    slack_q_mvar: float | None = None
    total_load_p_mw: float | None = None
    total_load_q_mvar: float | None = None
    total_loss_p_mw: float | None = None
    total_loss_q_mvar: float | None = None
    excluded_elements: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in ("computed", "failed", "unavailable"):
            raise ValueError(f"invalid status {self.status!r}")
        if self.status == "computed" and (not self.converged or not self.buses):
            raise ValueError("a computed result requires convergence and bus results")

    @property
    def balance_mismatch_mva(self) -> float | None:
        """|S_slack - S_load - S_loss| — physical balance, not an iteration step."""
        vals = (self.slack_p_mw, self.slack_q_mvar, self.total_load_p_mw,
                self.total_load_q_mvar, self.total_loss_p_mw, self.total_loss_q_mvar)
        if any(v is None for v in vals):
            return None
        sp, sq, lp, lq, xp, xq = vals  # type: ignore[misc]
        return abs(complex(sp - lp - xp, sq - lq - xq))

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["schema"] = STUDY_RESULT_SCHEMA
        data["balance_mismatch_mva"] = self.balance_mismatch_mva
        return data

    @property
    def result_sha256(self) -> str:
        return _digest(self.as_dict())


UNBALANCED_RESULT_SCHEMA = "unitesis.unbalanced-study-result/v1"


@dataclass(frozen=True, slots=True)
class PhaseVoltage:
    """Line-to-neutral voltage of one phase; ``vm_pu`` on the bus nominal kV / sqrt(3)."""

    bus_id: str
    phase: str
    vm_pu: float
    va_deg: float

    def __post_init__(self) -> None:
        if self.phase not in ("A", "B", "C"):
            raise ValueError(f"{self.bus_id}: invalid phase {self.phase!r}")
        require_finite(self.vm_pu, f"{self.bus_id}.{self.phase}.vm_pu")
        require_finite(self.va_deg, f"{self.bus_id}.{self.phase}.va_deg")


@dataclass(frozen=True, slots=True)
class PhaseBranchFlow:
    """Current and power entering a branch at its from-side, per phase."""

    branch_id: str
    from_bus: str
    to_bus: str
    phase: str
    i_from_a: float
    i_to_a: float
    p_from_mw: float
    q_from_mvar: float
    loading_percent: float | None = None

    def __post_init__(self) -> None:
        for name in ("i_from_a", "i_to_a", "p_from_mw", "q_from_mvar"):
            require_finite(getattr(self, name), f"{self.branch_id}.{self.phase}.{name}")


@dataclass(frozen=True, slots=True)
class BranchLoss:
    branch_id: str
    p_loss_mw: float
    q_loss_mvar: float


@dataclass(frozen=True, slots=True)
class VoltageUnbalance:
    """IEC voltage unbalance factor |V2| / |V1| of a three-phase bus, in percent."""

    bus_id: str
    vuf_percent: float


@dataclass(frozen=True, slots=True)
class UnbalancedStudyResult:
    """Phase-frame power flow result (spec 008-C); separate from the balanced contract."""

    request_sha256: str
    snapshot_sha256: str
    scenario_id: str
    engine: str
    engine_version: str
    status: StudyStatus
    converged: bool = False
    iterations: int = 0
    residual_mva: float | None = None          # max nodal power mismatch at the solution
    voltages: tuple[PhaseVoltage, ...] = ()
    flows: tuple[PhaseBranchFlow, ...] = ()
    losses: tuple[BranchLoss, ...] = ()
    unbalance: tuple[VoltageUnbalance, ...] = ()
    slack_p_mw: float | None = None
    slack_q_mvar: float | None = None
    total_load_p_mw: float | None = None
    total_load_q_mvar: float | None = None
    total_loss_p_mw: float | None = None
    total_loss_q_mvar: float | None = None
    excluded_elements: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in ("computed", "failed", "unavailable"):
            raise ValueError(f"invalid status {self.status!r}")
        if self.status == "computed" and (not self.converged or not self.voltages):
            raise ValueError("a computed result requires convergence and phase voltages")

    @property
    def balance_mismatch_mva(self) -> float | None:
        """|S_slack - S_load - S_loss| with the loss summed over branches."""
        vals = (self.slack_p_mw, self.slack_q_mvar, self.total_load_p_mw,
                self.total_load_q_mvar, self.total_loss_p_mw, self.total_loss_q_mvar)
        if any(v is None for v in vals):
            return None
        sp, sq, lp, lq, xp, xq = vals  # type: ignore[misc]
        return abs(complex(sp - lp - xp, sq - lq - xq))

    def voltage(self, bus_id: str, phase: str) -> PhaseVoltage:
        for v in self.voltages:
            if v.bus_id == bus_id and v.phase == phase:
                return v
        raise KeyError((bus_id, phase))

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["schema"] = UNBALANCED_RESULT_SCHEMA
        data["balance_mismatch_mva"] = self.balance_mismatch_mva
        return data

    @property
    def result_sha256(self) -> str:
        return _digest(self.as_dict())
