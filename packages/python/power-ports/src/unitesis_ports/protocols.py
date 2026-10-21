"""Typed protocols consumed by ``unitesis_application`` and implemented by adapters."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from unitesis_domain import ElectricalSnapshot, StudyRequest, StudyResult


class EngineUnavailable(RuntimeError):
    """The solver runtime/licence is absent; callers must report ``unavailable``."""


@runtime_checkable
class PowerFlowEngine(Protocol):
    name: str

    def version(self) -> str: ...

    def solve(self, snapshot: ElectricalSnapshot, request: StudyRequest) -> StudyResult: ...


@runtime_checkable
class SurrogateEngine(Protocol):
    """Fast approximate power flow (spec 029). Screens only; never certifies (ADR-0002)."""

    name: str

    def version(self) -> str: ...

    def predict_vm(self, snapshot: ElectricalSnapshot, p_node: Any, q_node: Any) -> Any:
        """Voltage magnitudes (scenarios x electrical nodes, slack first) for node loads."""


@runtime_checkable
class SnapshotRepository(Protocol):
    def save_snapshot(self, snapshot: ElectricalSnapshot, manifest: dict[str, Any]) -> str: ...

    def load_snapshot(self, snapshot_sha256: str) -> ElectricalSnapshot: ...


@runtime_checkable
class StudyRepository(Protocol):
    def save_result(self, result: StudyResult, evidence_path: str | None) -> str: ...

    def get_result(self, result_sha256: str) -> dict[str, Any]: ...


@runtime_checkable
class EvidenceStore(Protocol):
    def publish(self, run_id: str, documents: dict[str, Any]) -> Path: ...

    def verify(self, run_dir: Path) -> dict[str, Any]: ...


@runtime_checkable
class DatasetRepository(Protocol):
    def save_dataset(self, manifest: dict[str, Any]) -> str: ...

    def get_dataset(self, dataset_sha256: str) -> dict[str, Any]: ...


@runtime_checkable
class JobRepository(Protocol):
    def enqueue(self, job_id: str, kind: str, request: dict[str, Any]) -> dict[str, Any]: ...
    def get(self, job_id: str) -> dict[str, Any]: ...
    def claim(self, job_id: str) -> bool: ...
    def finish(self, job_id: str, outcome: dict[str, Any]) -> dict[str, Any]: ...
    def fail(self, job_id: str, error_code: str) -> dict[str, Any]: ...
    def recover_interrupted(self) -> int: ...
    def close(self) -> None: ...
