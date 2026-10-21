"""Small, dependency-free domain invariants, not a power-flow implementation."""

from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from json import dumps
from typing import Literal

Phase = Literal["A", "B", "C", "N"]

@dataclass(frozen=True, slots=True)
class Equipment:
    equipment_id: str
    kind: str
    nominal_kv: float

    def __post_init__(self) -> None:
        if not self.equipment_id.strip() or not self.kind.strip():
            raise ValueError("Stable equipment ID and kind are required")
        if not 0 < self.nominal_kv < 2000:
            raise ValueError("Nominal voltage must be physically positive (kV)")

@dataclass(frozen=True, slots=True)
class NetworkSnapshot:
    source_id: str
    equipment: tuple[Equipment, ...]

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id is mandatory for provenance")
        ids = [e.equipment_id for e in self.equipment]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate equipment IDs in network snapshot")

    @property
    def content_sha256(self) -> str:
        canonical = {
            "source_id": self.source_id,
            "equipment": sorted(
                [dict(equipment_id=e.equipment_id,kind=e.kind,nominal_kv=e.nominal_kv)
                 for e in self.equipment],
                key=lambda item: item["equipment_id"],
            ),
        }
        return sha256(dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
