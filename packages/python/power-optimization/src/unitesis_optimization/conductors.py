"""Traceable conductor catalog and positive-sequence parameters.

Adapted from SelecCablesAAAC ``aaac_pf/conductors.py``. Differences from the donor:
no silent defaults (alpha, temperature limit and source must be in the catalog), no
legacy section-only lookup, and the GMR approximation is reported explicitly.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from unitesis_domain.units import require_finite, require_positive

GMR_ROUND_STRANDED_FACTOR = 0.7788  # GMR ~ 0.7788 r, declared assumption when no datasheet GMR
_REQUIRED = ("id", "material", "section_mm2", "diameter_mm", "r20_ohm_km", "ampacity_a",
             "alpha20_per_c", "max_continuous_temperature_c")


@dataclass(frozen=True, slots=True)
class Conductor:
    conductor_id: str
    material: str
    section_mm2: float
    diameter_mm: float
    r20_ohm_km: float
    ampacity_a: float
    alpha20_per_c: float
    max_temperature_c: float
    gmr_mm: float | None = None
    datasheet_reference: str = ""

    def __post_init__(self) -> None:
        for name in ("section_mm2", "diameter_mm", "r20_ohm_km", "ampacity_a", "alpha20_per_c"):
            require_positive(getattr(self, name), f"{self.conductor_id}.{name}")
        require_finite(self.max_temperature_c, f"{self.conductor_id}.max_temperature_c")
        if self.gmr_mm is not None:
            require_positive(self.gmr_mm, f"{self.conductor_id}.gmr_mm")

    def resistance_ohm_km(self, temperature_c: float) -> float:
        """R(T) = R20 (1 + alpha (T - 20))."""
        require_finite(temperature_c, "temperature_c")
        return self.r20_ohm_km * (1.0 + self.alpha20_per_c * (temperature_c - 20.0))

    def reactance_ohm_km(self, phase_gmd_m: float, frequency_hz: float) -> tuple[float, str]:
        """Positive-sequence X for transposed 3-phase geometry, plus the GMR basis used."""
        require_positive(phase_gmd_m, "phase_gmd_m")
        require_positive(frequency_hz, "frequency_hz")
        if self.gmr_mm is not None:
            gmr_m, basis = self.gmr_mm / 1000.0, "datasheet_gmr"
        else:
            gmr_m = GMR_ROUND_STRANDED_FACTOR * self.diameter_mm / 2000.0
            basis = "assumed_gmr_0.7788r"
        if phase_gmd_m <= gmr_m:
            raise ValueError("phase_gmd_m must exceed conductor GMR")
        return 2.0 * math.pi * frequency_hz * 2e-4 * math.log(phase_gmd_m / gmr_m), basis


@dataclass(frozen=True, slots=True)
class ConductorCatalog:
    name: str
    source_url: str
    source_note: str
    sha256: str
    conductors: tuple[Conductor, ...]

    def by_id(self, conductor_id: str) -> Conductor:
        for c in self.conductors:
            if c.conductor_id == conductor_id:
                return c
        raise KeyError(conductor_id)

    def ordered_by_section(self) -> list[Conductor]:
        return sorted(self.conductors, key=lambda c: (c.section_mm2, c.conductor_id))


def load_catalog(path: str | Path) -> ConductorCatalog:
    raw = Path(path).read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    if not payload.get("source_url") and not payload.get("source_note"):
        raise ValueError("catalog must declare its source (source_url or source_note)")
    rows = payload.get("conductors")
    if not isinstance(rows, list) or not rows:
        raise ValueError("catalog requires a non-empty 'conductors' array")
    conductors = []
    for i, row in enumerate(rows):
        missing = [f for f in _REQUIRED if f not in row]
        if missing:
            raise ValueError(f"conductors[{i}] missing {missing}; values are never defaulted")
        conductors.append(Conductor(
            conductor_id=row["id"], material=row["material"],
            section_mm2=row["section_mm2"], diameter_mm=row["diameter_mm"],
            r20_ohm_km=row["r20_ohm_km"], ampacity_a=row["ampacity_a"],
            alpha20_per_c=row["alpha20_per_c"],
            max_temperature_c=row["max_continuous_temperature_c"],
            gmr_mm=row.get("gmr_mm"), datasheet_reference=row.get("datasheet_reference", "")))
    ids = [c.conductor_id for c in conductors]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate conductor ids in catalog")
    return ConductorCatalog(payload.get("name", Path(path).stem), payload.get("source_url", ""),
                            payload.get("source_note", ""), sha256(raw).hexdigest(),
                            tuple(conductors))
