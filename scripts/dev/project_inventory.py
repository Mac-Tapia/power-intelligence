"""Spec 000: deterministic ownership inventory; never deletes or imports product code."""

from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Any

SKIP = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
        ".ruff_cache", ".mypy_cache", ".worktrees", ".playwright-mcp"}
PACKAGES = {
    "domain": ["004"], "ports": ["000", "004"], "adapters": ["001", "009"],
    "application": ["002", "005", "009"], "config": ["029"],
    "economics": ["005", "022"], "evidence": ["004"], "simulation": ["004"],
    "topology": ["003", "004"], "optimization": ["005"], "sciml": ["006", "029"],
    "marl": ["007"], "agents": ["008"], "graph": ["010"], "p2p": ["011"],
    "ledger": ["012"], "market": ["013"], "graphrag": ["014"],
    "regulation": ["020", "021", "022", "026", "027"],
}
ROOT_FILES = {"README.md", "AGENTS.md", "Makefile", "pyproject.toml", ".editorconfig",
              ".env.example", ".gitattributes", ".gitignore", ".mcp.json.example"}


def _secret(path: Path) -> bool:
    return (any(part in {"secrets", "credentials"} for part in path.parts)
            or (path.name.startswith(".env") and not path.name.endswith(".example"))
            or path.suffix.lower() in {".key", ".pem"}
            or path.name == ".mcp.json")


def _ownership(name: str) -> tuple[str | None, list[str], str]:
    parts = Path(name).parts
    if len(parts) >= 3 and parts[:2] == ("packages", "python"):
        key = parts[2].removeprefix("power-")
        return (parts[2], PACKAGES[key], "runtime") if key in PACKAGES else (None, [], "unknown")
    if name.startswith("apps/workstation-web/"):
        return "workstation-web", ["003", "009"], "application"
    if name.startswith("apps/control-api/"):
        return "control-api", ["009"], "application"
    if len(parts) > 1 and parts[0] == "specs" and parts[1][:3].isdigit():
        return "specification", [parts[1][:3]], "governance"
    if parts[0] in {".agents", ".cursor", "connectors", "tools"}:
        return "agent-governance", ["015"], "configuration"
    if parts[0] in {"docs", "tests", "scripts", "config", "contracts", "fixtures",
                    "benchmarks", "datasets", "templates", "infra", "requirements",
                    ".github", ".specify", ".vscode", "specs"} or name in ROOT_FILES:
        return parts[0] if len(parts) > 1 else "repository", ["000"], "support"
    return None, [], "unknown"


def build_inventory(root: Path) -> dict[str, Any]:
    root = root.resolve(strict=True)
    proc = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                          capture_output=True, check=True)
    tracked = set(proc.stdout.decode("utf-8").split("\0")) - {""}
    files: list[dict[str, Any]] = []
    imports: dict[str, list[str]] = defaultdict(list)
    local = {"files": 0, "bytes": 0}
    for parent, dirs, names in os.walk(root, followlinks=False):
        base = Path(parent)
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not _secret(Path(d)))
        links = [d for d in dirs if (base / d).is_symlink() or (base / d).is_junction()]
        dirs[:] = [d for d in dirs if d not in links]
        for name in sorted(names + links):
            path = base / name
            rel = path.relative_to(root)
            if _secret(rel):
                continue
            # Never reveal local source/evidence names, including directory names.
            if rel.parts[0] == "local-data":
                if path.is_file() and not path.is_symlink():
                    local["files"] += 1
                    local["bytes"] += path.stat().st_size
                continue
            owner, specs, role = _ownership(rel.as_posix())
            row = {"path": rel.as_posix(), "owner": owner, "spec_ids": specs,
                   "role": role, "tracked": rel.as_posix() in tracked}
            if path.is_symlink() or path.is_junction():
                row["kind"] = "symlink"
            else:
                data = path.read_bytes()
                row.update(kind="file", bytes=len(data), sha256=sha256(data).hexdigest())
                if path.suffix == ".py":
                    tree = ast.parse(data, filename=rel.as_posix())
                    for node in ast.walk(tree):
                        modules = ([a.name for a in node.names] if isinstance(node, ast.Import)
                                   else [node.module or ""] if isinstance(node, ast.ImportFrom)
                                   else [])
                        for module in modules:
                            if module.startswith("unitesis_"):
                                imports[module.split(".")[0]].append(rel.as_posix())
            files.append(row)
    specs_present = {p.name[:3] for p in (root / "specs").glob("*/spec.md")
                     for p in [p.parent]}
    missing = sorted({s for f in files for s in f["spec_ids"]} - specs_present)
    return {"schema": "unitesis.project-inventory/1", "files": sorted(files,
            key=lambda r: r["path"]), "local_data_summary": local,
            "importers": {k: sorted(set(v)) for k, v in sorted(imports.items())},
            "roles": dict(sorted(Counter(f["role"] for f in files).items())),
            "problems": {"unowned_files": sorted(f["path"] for f in files if not f["owner"]),
                         "missing_specs": missing,
                         "missing_tracked_files": sorted(p for p in tracked
                             if not (root / p).exists() and not (root / p).is_symlink())},
            "interpretation": "Ownership is traceability, not functional acceptance. "
                              "A missing static consumer does not prove a file is unused."}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    temp: Path | None = None
    try:
        root = args.root.resolve(strict=True)
        output = args.output if args.output.is_absolute() else root / args.output
        # Reject links before resolution, including an existing target link.
        if any(p.is_symlink() or p.is_junction() for p in [output, *output.parents]):
            raise ValueError("linked output paths are forbidden")
        output = output.resolve()
        if not output.is_relative_to(root / "local-data"):
            raise ValueError("output must be under project local-data")
        report = build_inventory(root)
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent,
                                         delete=False) as handle:
            temp = Path(handle.name)
            json.dump(report, handle, indent=2, ensure_ascii=False, allow_nan=False)
        os.replace(temp, output)
        reread = json.loads(output.read_text(encoding="utf-8"))
        if reread != report:
            raise ValueError("inventory reread mismatch")
        print(json.dumps({"files": len(report["files"]), "problems": report["problems"]}))
        return 1 if any(report["problems"].values()) else 0
    except (OSError, ValueError, SyntaxError, subprocess.CalledProcessError) as exc:
        print(f"Inventory unavailable: {type(exc).__name__}", file=sys.stderr)
        return 2
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
