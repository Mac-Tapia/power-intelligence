"""Use case: authorized time series -> cleaned supervised dataset -> verified manifest."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from unitesis_evidence.store import publish_evidence
from unitesis_ports import DatasetRepository
from unitesis_sciml.datasets import DatasetSpec, build_dataset, write_dataset


def build_forecast_dataset(source: str | Path, out_dir: str | Path, spec: DatasetSpec,
                           repository: DatasetRepository | None = None) -> dict[str, Any]:
    splits, manifest = build_dataset(source, spec)
    out = write_dataset(splits, manifest, out_dir)
    manifest["files"] = {name: f"{name}.csv" for name in splits}
    verified = publish_evidence(out / "manifest.json", manifest)
    if repository is not None:
        repository.save_dataset(verified)
    return verified
