"""Measured demand: bronze -> silver rules, physical checks, typical profiles, baselines (016).

Silver rules are declared, never guessed: the column map names each source column's
quantity and unit, and the timestamp convention says whether a stamp closes or opens its
interval. Physical consistency (``|S|^2 ~ P^2 + Q^2`` per row) is measured and reported,
not repaired. Typical profiles are built from the *training* period only, so they can be
used as a forecast baseline on later data without leakage. Baselines are the yardstick any
learned forecaster must beat on the same split (spec 016, AC-016 baselines medibles).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

DAYTYPES = ("weekday", "saturday", "sunday")
QUANTITIES = ("kw", "kvar", "kva")


@dataclass(frozen=True)
class SilverRules:
    """Declared interpretation of one measured sheet.

    ``columns`` maps a source header to ``(series_id, quantity)`` with quantity in
    ``QUANTITIES``; ``interval_ending`` means a stamp labels the interval that ends there.
    """

    timestamp_header: str
    columns: tuple[tuple[str, str, str], ...]          # (header, series_id, quantity)
    frequency: str
    timezone: str
    interval_ending: bool

    def __post_init__(self) -> None:
        if not self.columns:
            raise ValueError("at least one measured column is required")
        for header, series_id, quantity in self.columns:
            if quantity not in QUANTITIES or not series_id or not header:
                raise ValueError(f"invalid column rule {(header, series_id, quantity)}")


def silver_from_rows(rows: list[list[dict[str, Any]]], rules: SilverRules
                     ) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Bronze cell rows (first row = headers) -> regular-grid silver frame + quality report.

    Columns of the frame are ``<series_id>_<quantity>``; the index is interval *start* in the
    case timezone. Rows with unparsable stamps or non-numeric values are counted, not fixed.
    """
    headers = [str(c.get("value", "")).replace("\n", " ").strip() for c in rows[0]]
    norm = {h.replace("\n", " ").strip(): i for i, h in enumerate(headers)}
    if rules.timestamp_header not in norm:
        raise ValueError(f"timestamp column {rules.timestamp_header!r} not in headers")
    missing = [h for h, *_ in rules.columns if h not in norm]
    if missing:
        raise ValueError(f"declared columns not in source headers: {missing}")
    ts_i = norm[rules.timestamp_header]
    stamps, data, bad_rows = [], {f"{s}_{q}": [] for _, s, q in rules.columns}, 0
    for row in rows[1:]:
        cell = row[ts_i] if ts_i < len(row) else {}
        try:
            stamp = pd.Timestamp(cell.get("value"))
        except (TypeError, ValueError):
            bad_rows += 1
            continue
        if pd.isna(stamp):
            bad_rows += 1
            continue
        stamps.append(stamp)
        for header, s, q in rules.columns:
            c = row[norm[header]] if norm[header] < len(row) else {}
            v = c.get("value")
            data[f"{s}_{q}"].append(float(v) if isinstance(v, (int, float)) else np.nan)
    frame = pd.DataFrame(data, index=pd.DatetimeIndex(stamps))
    step = pd.tseries.frequencies.to_offset(rules.frequency)
    if rules.interval_ending:
        frame.index = frame.index - step
    duplicated = frame.index.duplicated(keep=False)
    conflicting = 0
    if duplicated.any():
        dup = frame[duplicated]
        conflicting = int((dup.groupby(level=0).nunique(dropna=False) > 1).any(axis=1).sum())
    frame = frame[~frame.index.duplicated(keep="first")].sort_index()
    grid = pd.date_range(frame.index[0], frame.index[-1], freq=rules.frequency)
    off_grid = int(len(frame.index.difference(grid)))
    frame = frame.reindex(grid)
    frame.index = frame.index.tz_localize(rules.timezone)
    frame.index.name = "interval_start"
    report = {"source_rows": len(rows) - 1, "unparsable_rows": bad_rows,
              "duplicate_stamps": int(duplicated.sum()), "conflicting_duplicates": conflicting,
              "off_grid_stamps": off_grid, "grid_intervals": len(grid),
              "missing_per_column": {c: int(frame[c].isna().sum()) for c in frame.columns},
              "negative_per_column": {c: int((frame[c] < 0).sum()) for c in frame.columns},
              "start": str(frame.index[0]), "end": str(frame.index[-1])}
    return frame, report


def apparent_power_consistency(kw: pd.Series, kvar: pd.Series, kva: pd.Series,
                               tolerance: float = 0.02) -> dict[str, Any]:
    """Share of rows where |S| and sqrt(P^2+Q^2) agree within ``tolerance`` (relative)."""
    mask = kw.notna() & kvar.notna() & kva.notna() & (kva.abs() > 0)
    if not mask.any():
        return {"rows_checked": 0}
    rel = ((np.hypot(kw[mask], kvar[mask]) - kva[mask]).abs() / kva[mask].abs())
    return {"rows_checked": int(mask.sum()), "tolerance": tolerance,
            "share_consistent": float((rel <= tolerance).mean()),
            "p99_relative_gap": float(rel.quantile(0.99))}


def daytype(index: pd.DatetimeIndex) -> np.ndarray:
    dow = index.dayofweek
    return np.where(dow < 5, "weekday", np.where(dow == 5, "saturday", "sunday"))


def typical_profiles(series: pd.Series, *, min_days: int = 4) -> dict[str, Any]:
    """Mean normalised day per (month, daytype) from the given (training) series.

    Each day is divided by its own peak, so profiles are shapes in p.u.; cells with fewer
    than ``min_days`` complete days are reported as missing, never interpolated.
    """
    s = series.dropna()
    steps = int(pd.Timedelta("1D") / pd.tseries.frequencies.to_offset(pd.infer_freq(
        series.index[:200]) or "15min"))
    frame = pd.DataFrame({"v": s, "date": s.index.date, "slot": [
        (t.hour * 60 + t.minute) * steps // 1440 for t in s.index]})
    pivot = frame.pivot_table(index="date", columns="slot", values="v", aggfunc="mean")
    pivot = pivot[pivot.notna().sum(axis=1) == steps]           # complete days only
    days = pd.DatetimeIndex(pd.to_datetime(pivot.index))
    peak = pivot.max(axis=1).replace(0, np.nan)
    shape = pivot.div(peak, axis=0)
    out: dict[str, Any] = {"steps_per_day": steps, "profiles": {}, "missing_cells": []}
    for month in range(1, 13):
        for dt in DAYTYPES:
            sel = (days.month == month) & (daytype(days) == dt)
            if sel.sum() < min_days:
                out["missing_cells"].append(f"{month:02d}-{dt}")
                continue
            out["profiles"][f"{month:02d}-{dt}"] = {
                "days": int(sel.sum()),
                "shape_pu": [round(float(x), 6) for x in shape[sel].mean(axis=0)],
                "mean_daily_peak": float(peak[sel].mean())}
    return out


def _errors(actual: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    m = np.isfinite(actual) & np.isfinite(pred)
    a, p = actual[m], pred[m]
    mae = float(np.mean(np.abs(a - p)))
    return {"points": int(m.sum()), "mae": mae, "rmse": float(np.sqrt(np.mean((a - p) ** 2))),
            "nmae_percent": float(100 * mae / np.mean(np.abs(a))) if len(a) else float("nan")}


def baseline_forecasts(series: pd.Series, train_end: pd.Timestamp, test_start: pd.Timestamp,
                       profiles: dict[str, Any]) -> dict[str, Any]:
    """Day-ahead baselines on ``[test_start, end]`` using only information up to each day.

    * ``seasonal_naive_week``: value one week earlier;
    * ``profile_x_recent_peak``: training shape of (month, daytype) times the mean daily
      peak of the previous 7 days (known at forecast time).
    """
    steps = profiles["steps_per_day"]
    test = series[series.index >= test_start]
    week = steps * 7
    naive = series.shift(week).reindex(test.index)
    daily_peak = series.resample("1D").max()
    recent_peak = daily_peak.shift(1).rolling(7, min_periods=5).mean()
    pred = []
    for t in test.index:
        key = f"{t.month:02d}-{daytype(pd.DatetimeIndex([t]))[0]}"
        prof = profiles["profiles"].get(key)
        rp = recent_peak.get(t.normalize(), np.nan)
        slot = (t.hour * 60 + t.minute) * steps // 1440
        pred.append(prof["shape_pu"][slot] * rp if prof and np.isfinite(rp) else np.nan)
    actual = test.to_numpy(dtype=float)
    return {"test_start": str(test_start), "test_end": str(test.index[-1]),
            "train_end": str(train_end),
            "seasonal_naive_week": _errors(actual, naive.to_numpy(dtype=float)),
            "profile_x_recent_peak": _errors(actual, np.array(pred, dtype=float))}
