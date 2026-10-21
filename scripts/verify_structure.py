"""Portable structural contract test; no external dependencies."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "AGENTS.md", ".specify/memory/constitution.md",
    ".github/workflows/scaffold-ci.yml", ".github/PULL_REQUEST_TEMPLATE.md",
    "docs/architecture/MODULE-BOUNDARIES.md", "docs/development/SDD-WORKTREE-GUIDE.md",
    "specs/000-repository-foundation/spec.md", "specs/001-vnrgis-ingestion/spec.md",
    "packages/python/power-domain/src/unitesis_domain/models.py",
    "scripts/dev/worktree.py", "tests/bootstrap/test_domain.py", "pnpm-workspace.yaml",
]
problems = [item for item in REQUIRED if not (ROOT / item).is_file()]
if problems:
    print("FAIL: missing files:\n" + "\n".join(problems), file=sys.stderr)
    sys.exit(1)
# No large/source data leaked into repo scaffold
for extension in ("*.mdb", "*.dgs", "*.parquet", "*.pt", "*.ckpt"):
    leaked = list(ROOT.rglob(extension))
    if leaked:
        print(f"FAIL: forbidden artifact {extension}: {leaked[0]}", file=sys.stderr)
        sys.exit(1)
print(f"PASS: structural invariants ({len(REQUIRED)} required files)")

# V5 extension invariants: require every new feature's 3 SDD artifacts and 4 schemas
V5_FEATURES = ("010-electrical-graph","011-p2p-federation","012-ledger-evidence",
               "013-p2p-energy-market","014-graphrag-knowledge")
V5_SCHEMAS = ("graph-projection.v1.schema.json", "p2p-envelope.v1.schema.json",
              "p2p-energy-trade.v1.schema.json", "ledger-anchor.v1.schema.json")
missing_v5 = [f"specs/{f}/{n}" for f in V5_FEATURES for n in ("spec.md","plan.md","tasks.md")
             if not (ROOT / "specs" / f / n).is_file()]
missing_v5 += [f"contracts/schemas/json/{n}" for n in V5_SCHEMAS
               if not (ROOT / "contracts/schemas/json" / n).is_file()]
if missing_v5:
    print("FAIL: V5 required files missing: " + ", ".join(missing_v5), file=sys.stderr)
    sys.exit(1)
print("PASS: V5 SDD feature artifacts and schemas")

# V6 AI-SDD addendum
V6_REQUIRED = ["specs/015-agent-skills-mcp/spec.md", "specs/015-agent-skills-mcp/plan.md", "specs/015-agent-skills-mcp/tasks.md", ".cursor/mcp.json", ".cursor/worktrees.json", "connectors/registry.json", "tools/mcp/unitesis_server.py", "docs/architecture/BACKEND-FRONTEND-BLUEPRINT_V6.md", "docs/agents/AGENT-ROLES.md", "scripts/agents/validate_agent_setup.py"]
missing_v6 = [v for v in V6_REQUIRED if not (ROOT / v).is_file()]
if missing_v6:
    print("FAIL: V6 artifacts missing: " + ", ".join(missing_v6), file=sys.stderr)
    sys.exit(1)
print(f"PASS: V6 AI agents / MCP artifacts ({len(V6_REQUIRED)} required files)")
