"""Produce portable .mcp.json using an absolute path, no network or secrets."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def generate() -> dict:
    server = (ROOT / "tools/mcp/unitesis_server.py").resolve()
    local = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    # Keep the venv path: resolving POSIX's python symlink selects the base interpreter.
    command = str(local.absolute()) if local.is_file() else sys.executable
    return {"mcpServers": {"unitesis-project": {"command": command, "args": [str(server)]}}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=["vscode"], required=True)
    parser.add_argument("--write", action="store_true", help="Write .mcp.json ignored local file")
    args = parser.parse_args()
    payload = json.dumps(generate(), ensure_ascii=False, indent=2)
    if args.write:
        (ROOT / ".mcp.json").write_text(payload + "\n", encoding="utf-8")
        print("Generated .mcp.json. Check the path and install MCP SDK before connecting.")
    else:
        print(payload)
