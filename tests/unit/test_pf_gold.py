"""Gold promotion validates authorization, split identity and bytes, not just a label."""

import sys
from dataclasses import replace
from hashlib import sha256
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(src))


def test_real_candidate_without_temporal_split_cannot_be_gold(tmp_path):
    from unitesis_application.pf_dataset import promote_pf_dataset
    from unitesis_config import load_case

    case = load_case(ROOT / "config/cases/pe-ica-electrodunas.json")
    data = ROOT / "local-data/datasets/pf-scenarios-pe-ica-electrodunas"
    if not data.is_dir():
        pytest.skip("local authorized candidate is not distributed in Git")
    with pytest.raises(ValueError):
        promote_pf_dataset(replace(case, authorized=False), data, tmp_path / "denied.json")
    # AC-035-D04 and AC-029-S01 require dates and temporal gaps in addition to feeder split.
    with pytest.raises(ValueError, match="temporal"):
        promote_pf_dataset(case, data, tmp_path / "gold.json")


def gold_fixture(tmp_path):
    from unitesis_config import load_case
    from unitesis_evidence import publish_evidence

    case = replace(load_case(ROOT / "config/cases/pe-ica-electrodunas.json"),
                   case_id="xy-test-grid", source_ids=("unit-source",))
    raw = tmp_path / "raw.bin"
    raw.write_bytes(b"unit fixture raw bytes")
    rows, blocks = [], {}
    for i, split in enumerate(("train", "valid", "test")):
        instant = f"2024-01-{1+i*3:02d}T00:00:00+00:00"
        path = tmp_path / f"{split}.npz"
        np.savez(path, vm_pu=np.ones((1, 1)), va_deg=np.zeros((1, 1)),
                 p_mw=np.zeros((1, 1)), q_mvar=np.zeros((1, 1)),
                 label_residual_pu=np.zeros(1), timestamp_utc=np.array([instant]))
        rows.append({"network_id": split, "snapshot_sha256": str(i) * 64, "split": split,
                     "file": path.name, "sha256": sha256(path.read_bytes()).hexdigest(), "kept": 1})
        blocks[split] = {"start": instant, "end": instant}
    manifest = {"schema": "unitesis.pf-scenarios/1", "case_id": case.case_id,
        "dataset_id": "unit-fixture", "totals": {"kept": 3, "contrast_failed": 0,
            "contrast_unavailable": 0, "contrast_passed": 1}, "feeders": rows,
        "silver_rules": [], "code_tree_sha256": "a" * 64, "limitations": ["unit fixture only"],
        "column_origin": {k: "scenario" for k in ("p_mw", "q_mvar", "vm_pu", "va_deg")},
        "source_files": [{"file": "raw.bin", "source_id": "unit-source",
            "case_id": case.case_id, "role": "application_case",
            "sha256": sha256(raw.read_bytes()).hexdigest()}],
        "temporal_split": {"interval_seconds": 900, "max_lag_steps": 96,
            "horizon_steps": 1, "partitions": blocks}}
    publish_evidence(tmp_path / "manifest.json", manifest)
    return case, manifest


@pytest.mark.parametrize("defect", ["method_reference", "raw_tamper", "empty",
                                    "registry_reference", "overwrite"])
def test_gold_blocks_wrong_provenance_and_empty_partitions(tmp_path, defect):
    from unitesis_application.pf_dataset import promote_pf_dataset
    from unitesis_evidence import publish_evidence

    case, manifest = gold_fixture(tmp_path)
    registry = {"sources": [{"source_id": "unit-source", "case_id": case.case_id,
                              "role": "application_case"}]}
    output = tmp_path / "gold.json"
    if defect == "method_reference":
        manifest["source_files"][0].update(role="method_reference", case_id=None)
    elif defect == "raw_tamper":
        (tmp_path / "raw.bin").write_bytes(b"tampered")
    elif defect == "registry_reference":
        registry["sources"][0]["role"] = "method_reference"
    elif defect == "overwrite":
        output = tmp_path / "manifest.json"
    else:
        manifest["totals"]["kept"] = 0
        for row in manifest["feeders"]:
            row["kept"] = 0
            path = tmp_path / row["file"]
            np.savez(path, vm_pu=np.ones((0, 1)), va_deg=np.zeros((0, 1)),
                p_mw=np.zeros((0, 1)), q_mvar=np.zeros((0, 1)), label_residual_pu=np.zeros(0),
                timestamp_utc=np.array([], dtype=str))
            row["sha256"] = sha256(path.read_bytes()).hexdigest()
    publish_evidence(tmp_path / "manifest.json", manifest)
    with pytest.raises(ValueError):
        promote_pf_dataset(case, tmp_path, output, source_registry=registry)


def test_gold_accepts_complete_unit_fixture(tmp_path):
    from unitesis_application.pf_dataset import promote_pf_dataset

    case, _ = gold_fixture(tmp_path)
    registry = {"sources": [{"source_id": "unit-source", "case_id": case.case_id,
                              "role": "application_case"}]}
    assert promote_pf_dataset(case, tmp_path, tmp_path / "gold.json",
                              source_registry=registry)["samples"] == 3
