"""Phase impedance and shunt admittance of distribution lines (spec 008-C).

Own implementation of the methods in W. H. Kersting, *Distribution System Modeling and
Analysis* (ch. 4-5), the formulation behind the IEEE PES radial test feeders (E-04):

* overhead series impedance: modified Carson equations plus Kron reduction of the
  grounded neutrals;
* overhead shunt admittance: potential coefficients with conductor images;
* underground concentric-neutral cables: equivalent neutral conductor (GMR_cn, r/k) and
  the radial-field capacitance of each cable.

SI units: metres, ohm/km, microsiemens/km. Earth resistivity and frequency are explicit
arguments; there are no hidden defaults. The coefficients reproduce Kersting's
``0.00158836 f`` and ``0.00202237 f (ln(1/GMR) + 7.6786 + 0.5 ln(rho/f))`` ohm/mile forms.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

EPS0 = 8.8541878128e-12          # F/m
_FT_PER_M = 1 / 0.3048


@dataclass(frozen=True, slots=True)
class OverheadConductor:
    label: str                   # "A", "B", "C" (phases) or "N..." (grounded neutral)
    r_ohm_per_km: float
    gmr_m: float
    diameter_m: float
    height_m: float              # above earth, for the image method


@dataclass(frozen=True, slots=True)
class ConcentricNeutralCable:
    label: str                   # phase served by this cable
    r_ohm_per_km: float          # phase conductor
    gmr_m: float
    diameter_m: float            # phase conductor
    outer_diameter_m: float      # over the neutral strands
    strand_r_ohm_per_km: float
    strand_gmr_m: float
    strand_diameter_m: float
    strands: int
    insulation_permittivity: float


def _carson(f_hz: float, rho_ohm_m: float) -> tuple[float, float, float]:
    """(real term, imaginary coefficient, earth constant) per km, distances in metres."""
    real = math.pi ** 2 * 1e-4 * f_hz
    imag = 4 * math.pi * 1e-4 * f_hz
    const = 7.6786 + 0.5 * math.log(rho_ohm_m / f_hz) - math.log(_FT_PER_M)
    return real, imag, const


def _kron(m: np.ndarray, n_phase: int) -> np.ndarray:
    if m.shape[0] == n_phase:
        return m
    a, b = m[:n_phase, :n_phase], m[:n_phase, n_phase:]
    c, d = m[n_phase:, :n_phase], m[n_phase:, n_phase:]
    return a - b @ np.linalg.solve(d, c)


def _ordered(labels: list[str]) -> list[int]:
    """Phases first (A, B, C order), then neutrals."""
    phases = sorted((i for i, lb in enumerate(labels) if lb in "ABC" and len(lb) == 1),
                    key=lambda i: labels[i])
    return phases + [i for i in range(len(labels)) if i not in phases]


def overhead_phase_impedance(conductors: list[OverheadConductor],
                             distance_m: dict[frozenset[str], float], *,
                             frequency_hz: float, earth_resistivity_ohm_m: float
                             ) -> tuple[str, np.ndarray]:
    """Kron-reduced series impedance (ohm/km) of the phase conductors, in A-B-C order."""
    order = _ordered([c.label for c in conductors])
    cs = [conductors[i] for i in order]
    real, imag, const = _carson(frequency_hz, earth_resistivity_ohm_m)
    n = len(cs)
    z = np.empty((n, n), dtype=complex)
    for i, ci in enumerate(cs):
        for j, cj in enumerate(cs):
            if i == j:
                z[i, i] = ci.r_ohm_per_km + real + 1j * imag * (math.log(1 / ci.gmr_m) + const)
            else:
                d = distance_m[frozenset((ci.label, cj.label))]
                z[i, j] = real + 1j * imag * (math.log(1 / d) + const)
    n_ph = sum(1 for c in cs if c.label in ("A", "B", "C"))
    return "".join(c.label for c in cs[:n_ph]), _kron(z, n_ph)


def overhead_shunt_susceptance(conductors: list[OverheadConductor],
                               distance_m: dict[frozenset[str], float], *,
                               frequency_hz: float) -> tuple[str, np.ndarray]:
    """Shunt susceptance matrix (microsiemens/km) from Kron-reduced potential coefficients."""
    order = _ordered([c.label for c in conductors])
    cs = [conductors[i] for i in order]
    n = len(cs)
    p = np.empty((n, n))
    k = 1 / (2 * math.pi * EPS0)                     # m/F
    for i, ci in enumerate(cs):
        for j, cj in enumerate(cs):
            if i == j:
                p[i, i] = k * math.log(2 * ci.height_m / (ci.diameter_m / 2))
            else:
                d = distance_m[frozenset((ci.label, cj.label))]
                s = math.sqrt(d * d + 4 * ci.height_m * cj.height_m)
                p[i, j] = k * math.log(s / d)
    n_ph = sum(1 for c in cs if c.label in ("A", "B", "C"))
    c_f_per_m = np.linalg.inv(_kron(p, n_ph))
    b = 2 * math.pi * frequency_hz * c_f_per_m * 1e3 * 1e6   # microsiemens/km
    return "".join(c.label for c in cs[:n_ph]), b


def concentric_neutral_impedance(cables: list[ConcentricNeutralCable],
                                 distance_m: dict[frozenset[str], float], *,
                                 frequency_hz: float, earth_resistivity_ohm_m: float
                                 ) -> tuple[str, np.ndarray]:
    """Series impedance (ohm/km) of concentric-neutral cables, Kersting section 4.3.

    Each cable adds an equivalent neutral ``CN<phase>`` with ``GMR_cn = (GMR_s k R^(k-1))^(1/k)``
    and ``r_s / k``; ``R`` is the radius of the strand circle. Phase-to-other-neutral
    distances use ``(D^k - R^k)^(1/k)``.
    """
    cables = sorted(cables, key=lambda c: c.label)
    real, imag, const = _carson(frequency_hz, earth_resistivity_ohm_m)
    labels: list[str] = [c.label for c in cables] + [f"CN{c.label}" for c in cables]
    radius: dict[str, float] = {}
    gmr: dict[str, float] = {}
    res: dict[str, float] = {}
    for c in cables:
        k = c.strands
        big_r = (c.outer_diameter_m - c.strand_diameter_m) / 2
        radius[c.label] = big_r
        gmr[c.label], res[c.label] = c.gmr_m, c.r_ohm_per_km
        gmr[f"CN{c.label}"] = (c.strand_gmr_m * k * big_r ** (k - 1)) ** (1 / k)
        res[f"CN{c.label}"] = c.strand_r_ohm_per_km / k

    def dist(a: str, b: str) -> float:
        pa, pb = a.removeprefix("CN"), b.removeprefix("CN")
        if pa == pb and a != b:                       # phase to its own neutral
            return radius[pa]
        d = distance_m[frozenset((pa, pb))]
        cn_of = pb if b.startswith("CN") and not a.startswith("CN") else (
            pa if a.startswith("CN") and not b.startswith("CN") else None)
        if cn_of is not None:                         # phase to another cable's neutral
            k = next(c.strands for c in cables if c.label == cn_of)
            return (d ** k - radius[cn_of] ** k) ** (1 / k)
        return d

    n = len(labels)
    z = np.empty((n, n), dtype=complex)
    for i, a in enumerate(labels):
        for j, b in enumerate(labels):
            if i == j:
                z[i, i] = res[a] + real + 1j * imag * (math.log(1 / gmr[a]) + const)
            else:
                z[i, j] = real + 1j * imag * (math.log(1 / dist(a, b)) + const)
    return "".join(c.label for c in cables), _kron(z, len(cables))


def concentric_neutral_susceptance(cables: list[ConcentricNeutralCable], *,
                                   frequency_hz: float) -> tuple[str, np.ndarray]:
    """Diagonal shunt susceptance (microsiemens/km): the neutral screens each phase."""
    cables = sorted(cables, key=lambda c: c.label)
    b = np.zeros((len(cables), len(cables)))
    for i, c in enumerate(cables):
        k = c.strands
        big_r = (c.outer_diameter_m - c.strand_diameter_m) / 2
        denom = (math.log(big_r / (c.diameter_m / 2))
                 - math.log(k * (c.strand_diameter_m / 2) / big_r) / k)
        cap = 2 * math.pi * EPS0 * c.insulation_permittivity / denom      # F/m
        b[i, i] = 2 * math.pi * frequency_hz * cap * 1e3 * 1e6
    return "".join(c.label for c in cables), b


def as_snapshot_matrices(z: np.ndarray, b: np.ndarray | None) -> tuple[list, list | None]:
    """Symmetric JSON-ready matrices for ``Line.z_phase_ohm_per_km`` / ``b_phase_us_per_km``."""
    zs = (z + z.T) / 2
    zj = [[[float(zs[i, j].real), float(zs[i, j].imag)] for j in range(len(zs))]
          for i in range(len(zs))]
    if b is None:
        return zj, None
    bs = (b + b.T) / 2
    return zj, [[float(bs[i, j]) for j in range(len(bs))] for i in range(len(bs))]


def positive_sequence(z: np.ndarray) -> complex:
    """Positive-sequence equivalent: z_s - z_m for three phases, the self term otherwise."""
    n = len(z)
    if n < 3:
        return complex(z[0, 0])
    zs = np.trace(z) / n
    zm = (z.sum() - np.trace(z)) / (n * (n - 1))
    return complex(zs - zm)
