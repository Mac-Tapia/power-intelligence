"""Source-data quality gates for training datasets (forecasting, MADRL, LLM evaluation).

Each check returns a plain report with a ``status`` and the numbers behind it, so an audit
can be re-run and compared. Checks never repair data: a failing source is quarantined or
rebuilt from its raw origin with an explicit, recorded transformation.

Defects these gates were written for (review 2026-10-20, spec 035):

* ``forecast_leakage``: "predicted" columns equal to the future actual value (an oracle).
* ``monthly_split_consistency``: a total column shifted k months against its components.
* ``positional_time_index``: date/time columns corrupted (e.g. Excel serial times) while
  the row order still encodes a regular grid.
* ``real_coverage``: files whose name claims a long period but whose rows are mostly
  empty or zero.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np
import pandas as pd

ORACLE_THRESHOLD = 0.99
CONSISTENT_THRESHOLD = 0.95


def _finite_pair(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.isfinite(a) & np.isfinite(b)


def forecast_leakage(actual: Sequence[float], predicted: Sequence[float], horizon: int,
                     *, rtol: float = 1e-9) -> dict[str, Any]:
    """Compare a ``predicted_h`` column with the actual series at t and at t+h.

    ``oracle`` means the column reproduces the future actual value: any controller
    trained on it sees the future and its reported performance is optimistic.
    """
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    a = np.asarray(actual, dtype=float)
    p = np.asarray(predicted, dtype=float)
    if a.shape != p.shape or len(a) <= horizon:
        raise ValueError("actual and predicted must have equal length > horizon")
    same_now = _finite_pair(a, p)
    eq_now = float(np.isclose(p[same_now], a[same_now], rtol=rtol, atol=0.0).mean())
    fa, fp = a[horizon:], p[:-horizon]
    ok = _finite_pair(fa, fp)
    eq_future = float(np.isclose(fp[ok], fa[ok], rtol=rtol, atol=0.0).mean())
    if eq_future >= ORACLE_THRESHOLD:
        status = "oracle"
    elif eq_now >= ORACLE_THRESHOLD:
        status = "persistence"
    else:
        status = "forecast"
    return {"check": "forecast_leakage", "horizon": horizon, "status": status,
            "equal_to_current": eq_now, "equal_to_future": eq_future}


def monthly_split_consistency(peak: Sequence[float], offpeak: Sequence[float],
                              total: Sequence[float], *, max_lag: int = 12,
                              rel_tol: float = 0.01) -> dict[str, Any]:
    """Check ``peak + offpeak == total`` and find a constant row shift if there is one.

    ``shifted`` reports the lag k for which total[t + k] matches the components of t; it
    is evidence for a correction, not the correction itself.
    """
    s = np.asarray(peak, dtype=float) + np.asarray(offpeak, dtype=float)
    t = np.asarray(total, dtype=float)
    if s.shape != t.shape or len(s) < 3:
        raise ValueError("peak, offpeak and total must have equal length >= 3")
    scores: dict[int, float] = {}
    for k in range(0, min(max_lag, len(s) - 2) + 1):
        a, b = s[: len(s) - k], t[k:]
        ok = _finite_pair(a, b) & (b > 0) & (a > 0)
        scores[k] = float((np.abs(a[ok] - b[ok]) / b[ok] < rel_tol).mean()) if ok.any() else 0.0
    best = max(scores, key=lambda k: (scores[k], -k))
    if scores[0] >= CONSISTENT_THRESHOLD:
        status = "consistent"
    elif scores[best] >= CONSISTENT_THRESHOLD:
        status = "shifted"
    else:
        status = "inconsistent"
    return {"check": "monthly_split_consistency", "status": status, "match_lag0": scores[0],
            "best_lag": best, "match_best_lag": scores[best], "rows": int(len(s))}


def positional_time_index(dates: Sequence[Any], *, start: str, freq: str,
                          dayfirst: bool = False) -> dict[str, Any]:
    """Test a regular index built from row position against the recorded timestamps.

    * Full timestamps (date and time present): every parseable value must equal the
      positional index exactly -> ``regular``.
    * Date-only or corrupted times: parseable calendar days must agree with the position
      and the rows must fill whole days -> ``reconstructable`` (time rebuilt by position).
    Anything else is ``rejected``: a missing or extra row shifts every later label.
    """
    n = len(dates)
    index = pd.date_range(start=start, periods=n, freq=freq)
    parsed = pd.to_datetime(pd.Series(list(dates), dtype="object").astype(str),
                            errors="coerce", dayfirst=dayfirst, format="mixed")
    mask = parsed.notna().to_numpy()
    valid = parsed[mask]
    full_timestamps = bool(mask.all()) and bool((valid != valid.dt.normalize()).any())
    if full_timestamps:
        agree = valid.to_numpy() == index.to_numpy()
    elif mask.any():
        agree = valid.dt.normalize().to_numpy() == index[mask].normalize().to_numpy()
    else:
        agree = np.array([])
    steps_per_day = pd.Timedelta("1D") / pd.Timedelta(freq)
    whole_days = float(n / steps_per_day).is_integer()
    agreement = float(agree.mean()) if agree.size else 0.0
    if full_timestamps and agreement == 1.0:
        status = "regular"
    elif not full_timestamps and agree.size and agreement == 1.0 and whole_days:
        status = "reconstructable"
    else:
        status = "rejected"
    return {"check": "positional_time_index", "status": status, "rows": n,
            "parseable_dates": int(mask.sum()), "full_timestamps": full_timestamps,
            "agreement": agreement, "whole_days": whole_days,
            "start": str(index[0]) if n else None, "end": str(index[-1]) if n else None}


def real_coverage(values: Sequence[float], *, claimed_rows: int | None = None) -> dict[str, Any]:
    """Fraction of rows with a finite, non-zero value (zeros used as filler count as empty)."""
    v = np.asarray(pd.to_numeric(pd.Series(values), errors="coerce"), dtype=float)
    real = int((np.isfinite(v) & (v != 0)).sum())
    denominator = claimed_rows if claimed_rows is not None else len(v)
    frac = real / denominator if denominator else 0.0
    if frac >= CONSISTENT_THRESHOLD:
        status = "adequate"
    else:
        status = "sparse" if frac >= 0.5 else "mostly_empty"
    return {"check": "real_coverage", "status": status, "real_rows": real,
            "denominator_rows": int(denominator), "fraction": frac}
