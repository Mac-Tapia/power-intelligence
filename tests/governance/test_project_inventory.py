"""Inventory must expose unowned product files without disclosing private data."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/dev"))


def test_inventory_ownership_privacy_and_repeatability(tmp_path):
    from project_inventory import build_inventory

    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    for name, content in {
        "apps/workstation-web/public/view.js": "export const label = 'voltage';",
        "scripts/example.py": "from unitesis_domain import ElectricalSnapshot\n",
        ".env": "TOKEN=private-value",
        "local-data/customer-name/private.csv": "private-value",
        "loose.bin": "unowned",
    }.items():
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    report = build_inventory(tmp_path)
    rows = {r["path"]: r for r in report["files"]}
    assert rows["apps/workstation-web/public/view.js"]["spec_ids"] == ["003", "009"]
    assert rows["loose.bin"]["owner"] is None
    assert "loose.bin" in report["problems"]["unowned_files"]
    assert report["importers"]["unitesis_domain"] == ["scripts/example.py"]
    assert "private-value" not in json.dumps(report)
    assert "customer-name" not in json.dumps(report)
    assert ".env" not in rows
    assert report["files"] == build_inventory(tmp_path)["files"]


def test_output_must_stay_in_local_data(tmp_path):
    from project_inventory import main

    assert main(["--root", str(ROOT), "--output", str(tmp_path / "out.json")]) == 2
    assert not (tmp_path / "out.json").exists()


def test_symlink_not_followed(tmp_path):
    from project_inventory import build_inventory

    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    outside = tmp_path.parent / "private-target.txt"
    outside.write_text("private-value")
    try:
        (tmp_path / "external").symlink_to(outside)
    except OSError:
        pytest.skip("No symlink rights")
    row = next(r for r in build_inventory(tmp_path)["files"] if r["path"] == "external")
    assert row["kind"] == "symlink"
    assert "sha256" not in row


def test_actual_project_has_no_unowned_files_or_missing_specs():
    from project_inventory import build_inventory

    report = build_inventory(ROOT)
    assert report["problems"] == {"unowned_files": [], "missing_specs": [],
                                  "missing_tracked_files": []}
