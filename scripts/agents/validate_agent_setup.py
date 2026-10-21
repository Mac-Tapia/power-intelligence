"""Portable validation for skills, agents, connector registry and configs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate() -> list[str]:
    errors: list[str] = []
    skills_dir = ROOT / ".agents/skills"
    names: set[str] = set()
    for directory in sorted(skills_dir.iterdir()):
        if not directory.is_dir():
            continue
        file = directory / "SKILL.md"
        if not file.is_file():
            errors.append(f"Missing SKILL.md: {directory.name}")
            continue
        data = file.read_text(encoding="utf-8")
        m = re.match(r"\A---\n(.*?)\n---\n", data, re.S)
        if not m:
            errors.append(f"Missing YAML frontmatter: {directory.name}")
            continue
        metadata = {}
        for line in m.group(1).splitlines():
            if ": " in line:
                k, v = line.split(": ", 1)
                metadata[k] = v.strip().strip('"')
        name = metadata.get("name", "")
        if not name or name != directory.name or len(name) > 64 or not NAME_RE.fullmatch(name):
            errors.append(f"Invalid name: {directory.name}")
        desc = metadata.get("description", "")
        if not desc or len(desc) > 1024:
            errors.append(f"Invalid description: {directory.name}")
        if name in names:
            errors.append(f"Duplicate skill name: {name}")
        names.add(name)
    reg = json.loads((ROOT / "connectors/registry.json").read_text(encoding="utf-8"))
    ids = [x["id"] for x in reg["connectors"]]
    if len(ids) != len(set(ids)):
        errors.append("Duplicated connector IDs")
    for x in reg["connectors"]:
        if x["status"] not in {"implemented", "optional", "planned"}:
            errors.append(f"Invalid status: {x['id']}")
    for profile in reg["profiles"]:
        for name in profile["skills"]:
            if name not in names:
                errors.append(f"Unknown skill: {profile['id']}:{name}")
        for conn in profile["connectors"]:
            if conn not in ids:
                errors.append(f"Unknown connector: {profile['id']}:{conn}")
    cursor = json.loads((ROOT / ".cursor/mcp.json").read_text(encoding="utf-8"))
    if set(cursor["mcpServers"]) != {"unitesis-project"}:
        errors.append("Cursor must start with only local MCP")
    for file in [ROOT / ".cursor/mcp.json", ROOT / "connectors/registry.json"]:
        data = file.read_text(encoding="utf-8")
        if re.search(r"ghp_[A-Za-z0-9]{12}|sk-[A-Za-z0-9]{20}", data):
            errors.append(f"Looks like credential in {file}")
    return errors


if __name__ == "__main__":
    issues = validate()
    if issues:
        print("FAIL:\n" + "\n".join(issues), file=sys.stderr)
        sys.exit(1)
    print(
        f"PASS: {len(list((ROOT / '.agents/skills').iterdir()))} Agent Skills "
        "and MCP registry validated"
    )
