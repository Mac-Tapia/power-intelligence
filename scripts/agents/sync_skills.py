"""Idempotent opt-in copy of canonical Agent Skills to client-specific locations."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / ".agents/skills"
DESTS = {"claude": ROOT / ".claude/skills", "copilot": ROOT / ".github/skills"}


def sync(target: str) -> int:
    dest = DESTS[target]
    dest.mkdir(parents=True, exist_ok=True)
    count = 0
    for directory in sorted(SRC.iterdir()):
        if not directory.is_dir() or directory.is_symlink():
            continue
        dst = dest / directory.name
        if dst.exists():
            if dst.is_symlink() or not dst.is_dir():
                raise ValueError(f"Unsafe destination: {dst}")
            # Protect manually edited files rather than silently overwrite.
            src_bytes = (directory / "SKILL.md").read_bytes()
            dst_file = dst / "SKILL.md"
            if dst_file.exists() and dst_file.read_bytes() != src_bytes:
                raise ValueError(f"Existing customized skill differs: {dst_file}")
            continue
        shutil.copytree(directory, dst)
        count += 1
    return count


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--target", choices=DESTS, required=True)
    args = p.parse_args()
    print(f"{sync(args.target)} skills copied; canonical source remains .agents/skills")
