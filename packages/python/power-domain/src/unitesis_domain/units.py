"""Unit conversions and strict numeric guards (adapted from grid-bridge ``domain/units.py``).

Pure standard library. Every electrical magnitude entering the domain passes through
``require_finite`` so NaN/inf and booleans can never masquerade as numbers.
"""

from __future__ import annotations

from math import isfinite
from typing import Final

KW_PER_MW: Final[float] = 1000.0
KVAR_PER_MVAR: Final[float] = 1000.0
SQRT3: Final[float] = 3.0**0.5


def require_finite(value: object, name: str) -> float:
    """Return ``value`` as float or raise; rejects bool, str, NaN and inf."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric, got {type(value).__name__}")
    number = float(value)
    if not isfinite(number):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return number


def require_positive(value: object, name: str) -> float:
    number = require_finite(value, name)
    if number <= 0:
        raise ValueError(f"{name} must be > 0, got {number}")
    return number


def require_non_negative(value: object, name: str) -> float:
    number = require_finite(value, name)
    if number < 0:
        raise ValueError(f"{name} must be >= 0, got {number}")
    return number


def require_bool(value: object, name: str) -> bool:
    """Strict boolean: the strings ``"false"``/``"true"`` and ints are rejected."""
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be a boolean, got {type(value).__name__}")
    return value


def mw_to_kw(mw: float) -> float:
    return mw * KW_PER_MW


def kw_to_mw(kw: float) -> float:
    return kw / KW_PER_MW


def mvar_to_kvar(mvar: float) -> float:
    return mvar * KVAR_PER_MVAR


def kvar_to_mvar(kvar: float) -> float:
    return kvar / KVAR_PER_MVAR
