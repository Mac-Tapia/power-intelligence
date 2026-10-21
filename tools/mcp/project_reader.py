"""Small read-only repository data service used by the optional MCP server.

No shell, no globbing unrestricted repository, no write, and no secrets.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_ROOTS = ('.specify/memory', 'specs', 'docs/architecture', 'docs/development',
                 'docs/agents', 'docs/traceability', 'contracts', 'connectors')
ALLOWED_FILES = ('AGENTS.md', 'README.md')
ALLOWED_SUFFIXES = ('.md', '.json', '.yaml', '.yml')
MAX_BYTES = 96 * 1024


def allowed_document(path: str) -> Path:
    if not isinstance(path, str) or not path or '\\' in path or '\x00' in path:
        raise ValueError('Invalid path')
    relative = Path(path)
    if relative.is_absolute() or any(part in ('..', '.') for part in relative.parts):
        raise ValueError('Path traversal blocked')
    name = relative.as_posix()
    if name not in ALLOWED_FILES and not any(
            name.startswith(prefix + '/') for prefix in ALLOWED_ROOTS):
        raise PermissionError('Document outside allowlist')
    candidate = ROOT / relative
    # Even in allowlisted subtree, reject symlink files/dirs (including nested).
    part = ROOT
    for item in relative.parts:
        part = part / item
        if part.is_symlink():
            raise PermissionError('Symlinks are denied')
    if candidate.suffix not in ALLOWED_SUFFIXES or not candidate.is_file():
        raise ValueError('Unsupported or missing document')
    if not candidate.resolve().is_relative_to(ROOT.resolve()):
        raise PermissionError('Outside repository')
    if candidate.stat().st_size > MAX_BYTES:
        raise ValueError('Document exceeds size limit')
    return candidate


def read_document(path: str) -> str:
    return allowed_document(path).read_text(encoding='utf-8')


def list_features() -> list[dict[str, str]]:
    features = ROOT / 'specs'
    out = []
    for item in sorted(features.iterdir()):
        if item.is_dir() and not item.is_symlink() and (item / 'spec.md').is_file():
            out.append({'feature': item.name, 'spec': f'specs/{item.name}/spec.md'})
    return out


def list_skills() -> list[dict[str, str]]:
    base = ROOT / '.agents' / 'skills'
    out = []
    for item in sorted(base.iterdir()):
        if item.is_dir() and not item.is_symlink() and (item / 'SKILL.md').is_file():
            out.append({'name': item.name, 'path': f'.agents/skills/{item.name}/SKILL.md'})
    return out


def list_connector_profiles() -> dict:
    # Only public metadata; no credentials or runtime capabilities are returned.
    return json.loads((ROOT / 'connectors' / 'registry.json').read_text(encoding='utf-8'))
