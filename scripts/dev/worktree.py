"""Create/attach/list/remove sibling Git worktrees safely on Windows/Linux.

Examples:
 python scripts/dev/worktree.py new 004-physics-engine
 python scripts/dev/worktree.py attach 001-vnrgis-ingestion
 python scripts/dev/worktree.py list
 python scripts/dev/worktree.py remove 001-vnrgis-ingestion

No force deletions, no shell execution, no branch deletion. Git is required.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE_DIR = ROOT.parent / "unitesis-worktrees"
ALLOWED = re.compile(r"^[0-9]{3}-[a-z0-9]+(?:-[a-z0-9]+)*$")


def git(*args: str) -> None:
    subprocess.run(["git", "-C", str(ROOT), *args], check=True)


def path_for(branch: str) -> Path:
    if not ALLOWED.fullmatch(branch):
        raise ValueError("Use NNN-kebab-case branch ID, e.g. 001-vnrgis-ingestion")
    return BASE_DIR / branch


def main() -> int:
    p = argparse.ArgumentParser(description="Manage sibling worktrees for UNITESIS")
    p.add_argument("operation", choices=["list", "new", "attach", "remove"])
    p.add_argument("branch", nargs="?")
    p.add_argument("--base", default="main", help="Base branch for new worktree")
    a = p.parse_args()
    try:
        git("rev-parse", "--show-toplevel")
        if a.operation == "list":
            git("worktree", "list")
            return 0
        if not a.branch:
            p.error("branch is required except for list")
        path = path_for(a.branch)
        if a.operation == "new":
            BASE_DIR.mkdir(parents=True, exist_ok=True)
            git("worktree", "add", "-b", a.branch, str(path), a.base)
        elif a.operation == "attach":
            BASE_DIR.mkdir(parents=True, exist_ok=True)
            git("worktree", "add", str(path), a.branch)
        else:
            if not path.is_dir():
                raise ValueError(f"This sibling worktree is absent: {path}")
            # Git refuses removal of dirty or locked trees; never use --force.
            git("worktree", "remove", str(path))
        print(f"OK: {a.operation}: {path}")
        return 0
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
