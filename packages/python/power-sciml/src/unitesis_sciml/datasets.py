"""Supervised time-series dataset construction for load forecasting.

Adapted from Prodma ``limpieza/temporal.py`` (causal imputation separating context and
target), ``limpieza/outliers.py`` (causal robust outliers) and ``limpieza/electrical.py``
(frozen sensor). Additions: strict regular grid, lag/calendar features computed only from
the past, chronological splits with a leakage gap, and a hashed manifest.

Rules: imputed values may feed *features* (context) but never *targets*; no shuffling;
every split boundary respects ``gap >= max_lag + horizon``.
"""

from __future__ import annotations

import hashlib
import io
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

DATASET_SCHEMA = "unitesis.forecast-dataset/1"


class DatasetError(ValueError):
    """Input series cannot produce a trustworthy dataset."""


@dataclass(frozen=True)
class DatasetSpec:
    timestamp_column: str
    target_column: str
    frequency: str                      # pandas offset alias, e.g. "15min", "h"
    horizon_steps: int = 1
    lags: tuple[int, ...] = (1, 2, 3, 4, 96, 672)
    rolling_windows: tuple[int, ...] = (4, 96)
    ffill_limit: int = 4
    seasonal_lag: int = 672             # one week at 15 min
    outlier_window: int = 672
    outlier_threshold: float = 6.0
    frozen_min_run: int = 16
    split_fractions: tuple[float, float, float] = (0.7, 0.15, 0.15)
    exogenous_columns: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.horizon_steps < 1 or not self.lags or min(self.lags) < 1:
            raise DatasetError("horizon and lags must be >= 1")
        if abs(sum(self.split_fractions) - 1.0) > 1e-9 or min(self.split_fractions) <= 0:
            raise DatasetError("split fractions must be positive and sum to 1")

    @property
    def gap_steps(self) -> int:
        return max(max(self.lags), max(self.rolling_windows, default=0)) + self.horizon_steps


def load_series(path: str | Path, spec: DatasetSpec) -> tuple[pd.DataFrame, dict[str, Any]]:
    raw = Path(path).read_bytes()
    frame = pd.read_csv(io.BytesIO(raw))
    source_rows = len(frame)
    needed = {spec.timestamp_column, spec.target_column, *spec.exogenous_columns}
    if missing := needed - set(frame.columns):
        raise DatasetError(f"missing columns {sorted(missing)}")
    ts = pd.to_datetime(frame[spec.timestamp_column], errors="coerce")
    if ts.isna().any():
        raise DatasetError(f"{int(ts.isna().sum())} unparseable timestamps")
    frame = frame.assign(**{spec.timestamp_column: ts})
    dupes = frame[frame.duplicated(spec.timestamp_column, keep=False)]
    conflicting = dupes.groupby(spec.timestamp_column)[spec.target_column].nunique(dropna=False)
    if (conflicting > 1).any():
        raise DatasetError(f"{int((conflicting > 1).sum())} timestamps with conflicting values")
    frame = frame.drop_duplicates(spec.timestamp_column).set_index(spec.timestamp_column)
    frame = frame.sort_index()
    grid = pd.date_range(frame.index[0], frame.index[-1], freq=spec.frequency)
    off_grid = frame.index.difference(grid)
    if len(off_grid):
        raise DatasetError(f"{len(off_grid)} timestamps off the {spec.frequency} grid")
    frame = frame.reindex(grid)
    frame.index.name = "timestamp"
    info = {"source_sha256": hashlib.sha256(raw).hexdigest(), "source_rows": source_rows,
            "exact_duplicates_dropped": int(len(dupes) - dupes[spec.timestamp_column].nunique())
            if len(dupes) else 0,
            "grid_gaps": int(frame[spec.target_column].isna().sum()),
            "start": str(grid[0]), "end": str(grid[-1])}
    return frame, info


def detect_causal_outliers(series: pd.Series, window: int, threshold: float) -> pd.Series:
    """Prodma method: rolling median/MAD of the *past*, isolated spikes only."""
    shifted = series.shift(1)
    minimum = min(window, max(24, window // 7))
    median = shifted.rolling(window, min_periods=minimum).median()
    scale = 1.4826 * (shifted - median).abs().rolling(window, min_periods=minimum).median()
    candidate = ((series - median).abs() > threshold * scale.replace(0, np.nan)).fillna(False)
    density = candidate.shift(1, fill_value=False).astype(float).rolling(17, min_periods=1).mean()
    return (candidate & density.lt(0.5)).astype(bool)


def detect_frozen(series: pd.Series, min_run: int, tolerance: float = 1e-9) -> pd.Series:
    changed = series.isna() | series.diff().abs().gt(tolerance)
    groups = changed.cumsum()
    return (groups.map(groups.value_counts()) >= min_run) & series.notna()


def clean_target(raw: pd.Series, spec: DatasetSpec) -> pd.DataFrame:
    observed = raw.replace([np.inf, -np.inf], np.nan).astype(float)
    outlier = detect_causal_outliers(observed, spec.outlier_window, spec.outlier_threshold)
    frozen = detect_frozen(observed, spec.frozen_min_run)
    valid = observed.mask(outlier | frozen)
    forward = valid.ffill(limit=spec.ffill_limit)
    context = forward.fillna(valid.shift(spec.seasonal_lag))
    method = pd.Series("", index=raw.index, dtype="string")
    method[valid.isna() & forward.notna()] = "ffill"
    method[valid.isna() & forward.isna() & context.notna()] = "seasonal_lag"
    return pd.DataFrame({
        "observed": observed, "context": context, "target": valid,
        "is_observed": valid.notna(), "is_imputed": valid.isna() & context.notna(),
        "imputation_method": method, "is_outlier": outlier, "is_frozen": frozen,
    })


def build_features(clean: pd.DataFrame, exog: pd.DataFrame, spec: DatasetSpec) -> pd.DataFrame:
    h = spec.horizon_steps
    ctx = clean["context"]
    out = pd.DataFrame(index=clean.index)
    # The value at t+h is predicted from information available at t.
    out["y"] = clean["target"].shift(-h)
    out["y_is_observed"] = clean["is_observed"].shift(-h, fill_value=False).astype(bool)
    for lag in spec.lags:
        out[f"lag_{lag}"] = ctx.shift(lag - 1)
    for w in spec.rolling_windows:
        out[f"roll_mean_{w}"] = ctx.rolling(w, min_periods=w).mean()
    target_time = clean.index + pd.tseries.frequencies.to_offset(spec.frequency) * h
    out["hour"] = target_time.hour
    out["dayofweek"] = target_time.dayofweek
    out["month"] = target_time.month
    for col in spec.exogenous_columns:
        out[f"exog_{col}"] = exog[col]  # must be known at forecast time; caller's contract
    return out


def chronological_split(features: pd.DataFrame, spec: DatasetSpec) -> dict[str, pd.DataFrame]:
    usable = features[features["y_is_observed"]].dropna()
    n = len(usable)
    if n < 5 * spec.gap_steps:
        raise DatasetError(f"only {n} usable rows; need >= {5 * spec.gap_steps}")
    f_train, f_val, _ = spec.split_fractions
    i_val, i_test = int(n * f_train), int(n * (f_train + f_val))
    step = pd.tseries.frequencies.to_offset(spec.frequency)
    gap = step * spec.gap_steps
    train = usable.iloc[:i_val]
    val = usable.iloc[i_val:i_test]
    val = val[val.index > train.index[-1] + gap]
    test = usable.iloc[i_test:]
    test = test[test.index > val.index[-1] + gap]
    if min(len(train), len(val), len(test)) == 0:
        raise DatasetError("a split is empty after applying the leakage gap")
    return {"train": train, "validation": val, "test": test}


def _frame_sha256(frame: pd.DataFrame) -> str:
    return hashlib.sha256(frame.to_csv(float_format="%.10g").encode("utf-8")).hexdigest()


def build_dataset(path: str | Path, spec: DatasetSpec) -> tuple[dict[str, pd.DataFrame],
                                                                dict[str, Any]]:
    frame, info = load_series(path, spec)
    clean = clean_target(frame[spec.target_column], spec)
    features = build_features(clean, frame, spec)
    splits = chronological_split(features, spec)
    manifest = {
        "schema": DATASET_SCHEMA, "spec": asdict(spec), "source": info,
        "quality": {
            "observed": int(clean["is_observed"].sum()),
            "imputed_context_only": int(clean["is_imputed"].sum()),
            "outliers_masked": int(clean["is_outlier"].sum()),
            "frozen_masked": int(clean["is_frozen"].sum()),
            "unrecoverable": int((~clean["is_observed"] & ~clean["is_imputed"]).sum()),
        },
        "gap_steps": spec.gap_steps,
        "splits": {k: {"rows": len(v), "start": str(v.index[0]), "end": str(v.index[-1]),
                       "sha256": _frame_sha256(v)} for k, v in splits.items()},
        "feature_columns": [c for c in features.columns if c not in ("y", "y_is_observed")],
        "leakage_checks": {"targets_observed_only": True, "chronological": True,
                           "gap_respected": True},
    }
    manifest["dataset_sha256"] = hashlib.sha256(
        "".join(manifest["splits"][k]["sha256"] for k in sorted(splits)).encode()).hexdigest()
    return splits, manifest


def write_dataset(splits: dict[str, pd.DataFrame], manifest: dict[str, Any],
                  out_dir: str | Path) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, frame in splits.items():
        target = out / f"{name}.csv"
        frame.to_csv(target, float_format="%.10g")
        reread = pd.read_csv(target, index_col=0)
        if len(reread) != len(frame):
            raise DatasetError(f"read-back mismatch for {name}")
    return out
