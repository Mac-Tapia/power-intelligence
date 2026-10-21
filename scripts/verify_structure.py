"""Structural contract of the repository (stdlib + the stdlib-only power-config package).

Checks: required governance files, FEATURE-MAP <-> specs/ in both directions, application
cases valid and consistent with regulatory profiles and data sources, and the cleanliness
rules (no placeholder folders, no versioned/historical documents, no data artifacts).
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages/python/power-config/src"))

from unitesis_config import CaseError, check_consistency, list_cases, load_case  # noqa: E402

SKIP = {
    ".git",
    ".venv",
    "local-data",
    ".ruff_cache",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    ".playwright-mcp",
}
REQUIRED = [
    "README.md",
    "AGENTS.md",
    ".specify/memory/constitution.md",
    ".github/workflows/ci.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "requirements/dev.txt",
    "docs/architecture/ARCHITECTURE-INTEGRAL.md",
    "docs/architecture/MODULE-BOUNDARIES.md",
    "docs/architecture/CONTRACTS-AND-EVIDENCE.md",
    "docs/traceability/FEATURE-MAP.md",
    "docs/traceability/contribution-registry.json",
    "docs/development/SDD-WORKTREE-GUIDE.md",
    "config/datasets/sources.v2.json",
    "config/cases/_template.json",
    "scripts/unitesis.py",
    "scripts/dev/worktree.py",
    "apps/control-api/src/unitesis_api/main.py",
    "tests/security/test_no_proprietary_engines.py",
    # agent governance (spec 015)
    ".cursor/mcp.json",
    ".cursor/worktrees.json",
    "connectors/registry.json",
    "tools/mcp/unitesis_server.py",
    "docs/agents/AGENT-ROLES.md",
    "scripts/agents/validate_agent_setup.py",
]
FORBIDDEN_DATA = (
    "*.mdb",
    "*.accdb",
    "*.bak",
    "*.dgs",
    "*.pfd",
    "*.sxst",
    "*.parquet",
    "*.pt",
    "*.pth",
    "*.ckpt",
    "*.xlsx",
    "*.xls",
    "*.xlsb",
)
VERSIONED_DOC = re.compile(r"(^|[_-])V\d+(\.\d+)?([_.-]|$)", re.IGNORECASE)
problems: list[str] = []


def walk_files():
    for path in ROOT.rglob("*"):
        if not set(path.relative_to(ROOT).parts) & SKIP and path.is_file():
            yield path


problems += [f"missing required file: {r}" for r in REQUIRED if not (ROOT / r).is_file()]

# FEATURE-MAP <-> specs/
feature_map = (ROOT / "docs/traceability/FEATURE-MAP.md").read_text(encoding="utf-8")
mapped: set[str] = set()
for line in feature_map.splitlines():
    cell = line.split("|")[1].strip() if line.startswith("|") and line.count("|") > 2 else ""
    if m := re.fullmatch(r"(\d{3})[–-](\d{3})", cell):
        mapped |= {f"{i:03d}" for i in range(int(m[1]), int(m[2]) + 1)}
    elif re.fullmatch(r"\d{3}", cell):
        mapped.add(cell)
spec_dirs = {p.name[:3]: p for p in (ROOT / "specs").iterdir() if p.is_dir()}
spec_names = [p.name for p in (ROOT / "specs").iterdir() if p.is_dir()]
problems += [
    f"spec ID {i} used by more than one folder"
    for i in sorted({n[:3] for n in spec_names if sum(m[:3] == n[:3] for m in spec_names) > 1})
]
problems += [
    f"FEATURE-MAP lists {i} but specs/ has no folder" for i in sorted(mapped - set(spec_dirs))
]
problems += [
    f"specs/{spec_dirs[i].name} missing from FEATURE-MAP" for i in sorted(set(spec_dirs) - mapped)
]
for folder in sorted(spec_dirs.values()):
    for name in ("spec.md", "tasks.md"):
        if not (folder / name).is_file():
            problems.append(f"specs/{folder.name}/{name} missing")

# Application cases <-> regulatory profiles <-> data sources
registry = json.loads((ROOT / "config/datasets/sources.v2.json").read_text(encoding="utf-8"))
cases = list_cases(ROOT / "config/cases")
if not cases:
    problems.append("no application case in config/cases")
for case_id, path in cases.items():
    try:
        case = load_case(path)
    except CaseError as exc:
        problems.append(f"case {case_id}: {exc}")
        continue
    if case.case_id != case_id:
        problems.append(f"case file {path.name} declares case_id {case.case_id}")
    problems += [
        f"case {case_id}: {i}"
        for i in check_consistency(case, ROOT / "config/regulations/profiles", registry)
    ]
for src in registry["sources"]:
    if src.get("case_id") is not None and src["case_id"] not in cases:
        problems.append(f"source {src['source_id']} points to unknown case {src['case_id']}")

# Cleanliness: no placeholders, no empty folders, no versioned docs, no data artifacts
for path in walk_files():
    rel = path.relative_to(ROOT).as_posix()
    if path.name == ".gitkeep":
        problems.append(f"placeholder file: {rel}")
    if rel.startswith("docs/") and path.suffix == ".md" and VERSIONED_DOC.search(path.stem):
        problems.append(f"versioned/historical document name: {rel}")
for pattern in FORBIDDEN_DATA:
    for path in ROOT.rglob(pattern):
        if not set(path.relative_to(ROOT).parts) & SKIP:
            problems.append(
                f"data artifact must live outside Git: {path.relative_to(ROOT).as_posix()}"
            )
for folder in ROOT.rglob("*"):
    if (
        folder.is_dir()
        and not set(folder.relative_to(ROOT).parts) & SKIP
        and not any(folder.iterdir())
    ):
        problems.append(f"empty folder: {folder.relative_to(ROOT).as_posix()}")

if problems:
    print("FAIL:\n  " + "\n  ".join(problems), file=sys.stderr)
    sys.exit(1)
print(
    f"PASS: {len(REQUIRED)} required files, {len(spec_dirs)} specs synchronized with "
    f"FEATURE-MAP, {len(cases)} application case(s) consistent, no placeholders, "
    "no versioned docs, no data artifacts"
)
