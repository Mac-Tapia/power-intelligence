"""Security/regression tests without requiring the MCP SDK or network."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/mcp"))
sys.path.insert(0, str(ROOT / "scripts/agents"))
from bootstrap_mcp import generate
from project_reader import (
    allowed_document,
    list_connector_profiles,
    list_features,
    list_skills,
    read_document,
)
from validate_agent_setup import validate


class AgentScaffoldTests(unittest.TestCase):
    def test_generator_selects_project_interpreter(self):
        import os

        local = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        expected = str(local.absolute()) if local.is_file() else sys.executable
        self.assertEqual(generate()["mcpServers"]["unitesis-project"]["command"], expected)

    def test_generator_preserves_venv_path_when_python_resolves_to_base(self):
        import os
        from unittest.mock import patch

        import bootstrap_mcp

        # Windows cannot create symlinks without privileges. Emulate only the OS
        # resolution of that one executable, as occurs for POSIX virtualenvs.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            local = root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
            local.parent.mkdir(parents=True)
            local.touch()
            original_resolve = Path.resolve

            def resolve(path, *args, **kwargs):
                return (Path(sys.executable) if path == local
                        else original_resolve(path, *args, **kwargs))

            with patch.object(bootstrap_mcp, "ROOT", root), patch.object(Path, "resolve", resolve):
                self.assertEqual(generate()["mcpServers"]["unitesis-project"]["command"],
                                 str(local.absolute()))

    def test_registry_valid(self):
        self.assertEqual(validate(), [])
        self.assertGreaterEqual(len(list_skills()), 18)
        self.assertGreaterEqual(len(list_features()), 8)

    def test_read_spec(self):
        self.assertIn("REQ-015-01", read_document("specs/015-agent-skills-mcp/spec.md"))

    def test_traversal_and_sensitive_blocked(self):
        for path in (
            "../../.env",
            ".env",
            ".git/config",
            "/etc/passwd",
            "specs/../../.env",
            "tools/mcp/unitesis_server.py",
            "datasets/authorized/data.md",
            "AGENTS.md/../.env",
        ):
            with self.subTest(path=path), self.assertRaises((ValueError, PermissionError)):
                allowed_document(path)

    def test_symlink_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            target = ROOT / "specs" / "v6-test-danger-link.md"
            try:
                target.symlink_to(Path(temp) / "outside.md")
            except OSError:
                self.skipTest("No symlink rights")
            try:
                with self.assertRaises(PermissionError):
                    allowed_document("specs/v6-test-danger-link.md")
            finally:
                target.unlink(missing_ok=True)

    def test_config_is_read_only(self):
        self.assertEqual(
            set(json.loads((ROOT / ".cursor/mcp.json").read_text())["mcpServers"]),
            {"unitesis-project"},
        )
        self.assertEqual(set(generate()["mcpServers"]), {"unitesis-project"})
        manifest = list_connector_profiles()
        self.assertEqual(manifest["policy"]["default_mode"], "deny")
        self.assertEqual(
            next(c for c in manifest["connectors"] if c["id"] == "unitesis-project")["status"],
            "implemented",
        )


if __name__ == "__main__":
    unittest.main()
