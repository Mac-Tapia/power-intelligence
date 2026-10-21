"""Immutable input inventory: recursive discovery, SHA-256 and terminal states.

Adapted from Prodma ``custody/inventory.py`` (states, signature checks, duplicate
detection, fail-closed acceptance) and generalized: supported formats are a parameter,
and the published inventory is re-read and checked (PITELD ``audit.py`` pattern).
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from pathlib import Path

SUPPORTED = "SUPPORTED"
QUARANTINED = "QUARANTINED"
DUPLICATE = "DUPLICATE"
FAILED = "FAILED"
DOCUMENTATION = "DOCUMENTATION"
MISSING_EXPECTED = "MISSING_EXPECTED"
BLOCKING_STATES = frozenset({QUARANTINED, FAILED, MISSING_EXPECTED})

DEFAULT_DATA_SUFFIXES = frozenset({".csv", ".json", ".xlsx", ".xls", ".dgs", ".mdb", ".sxst"})
_SIGNATURES = {
    ".xlsx": (b"PK\x03\x04",),
    ".xls": (b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1",),
    ".mdb": (b"\x00\x01\x00\x00Standard Jet DB", b"\x00\x01\x00\x00Standard ACE DB"),
}
_TEXT_SUFFIXES = frozenset({".csv", ".json", ".dgs"})


class CustodyBlockedError(RuntimeError):
    """The inventory has blocking states; ingestion must not start."""


@dataclass(frozen=True, slots=True)
class InventoryEntry:
    path: str
    size: int
    sha256: str
    state: str
    reason: str


@dataclass
class Inventory:
    entries: list[InventoryEntry]
    expected_missing: list[str] = field(default_factory=list)

    def by_state(self) -> dict[str, int]:
        counts = Counter(e.state for e in self.entries)
        counts.update(MISSING_EXPECTED for _ in self.expected_missing)
        return dict(counts)

    @property
    def accepted(self) -> bool:
        return (not any(e.state in BLOCKING_STATES for e in self.entries)
                and not self.expected_missing)

    def require_accepted(self) -> None:
        if not self.accepted:
            raise CustodyBlockedError(f"custody blocked: {self.by_state()}")


def file_sha256(path: Path) -> tuple[str, int]:
    digest, size = hashlib.sha256(), 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
            size += len(block)
    return digest.hexdigest(), size


def _classify(path: Path, suffixes: frozenset[str]) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix == ".md":
        return DOCUMENTATION, "informative documentation; not a pipeline input"
    if suffix not in suffixes:
        return QUARANTINED, f"unsupported extension {suffix or '(none)'}"
    with path.open("rb") as stream:
        head = stream.read(4096)
    if suffix in _SIGNATURES and not head.startswith(_SIGNATURES[suffix]):
        return QUARANTINED, f"content signature does not match {suffix}"
    if suffix in _TEXT_SUFFIXES and b"\x00" in head:
        return QUARANTINED, f"binary content in {suffix}"
    return SUPPORTED, "recognized format"


def discover_inputs(roots: Iterable[Path | str], expected: Iterable[Path | str] = (),
                    suffixes: frozenset[str] = DEFAULT_DATA_SUFFIXES) -> Inventory:
    entries: list[InventoryEntry] = []
    seen: dict[str, str] = {}
    files = sorted({p for r in map(Path, roots) if r.is_dir()
                    for p in r.rglob("*") if p.is_file() and p.name != ".gitkeep"})
    for path in files:
        try:
            digest, size = file_sha256(path)
            state, reason = _classify(path, suffixes)
        except OSError as exc:
            entries.append(InventoryEntry(str(path), 0, "", FAILED, f"{type(exc).__name__}: {exc}"))
            continue
        if state == SUPPORTED and digest in seen:
            state, reason = DUPLICATE, f"identical content to {seen[digest]}"
        elif state == SUPPORTED:
            seen[digest] = path.name
        entries.append(InventoryEntry(str(path), size, digest, state, reason))
    missing = [str(p) for p in map(Path, expected) if not p.is_file()]
    for root in map(Path, roots):
        if not root.is_dir():
            missing.append(str(root))
    return Inventory(entries, missing)


def write_inventory(inventory: Inventory, out_dir: Path | str) -> dict[str, object]:
    """Publish JSONL + summary, then re-read both and verify counts and digest."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    jsonl, summary_path = out / "inventory.jsonl", out / "inventory_summary.json"
    lines = [json.dumps(asdict(e), ensure_ascii=False) for e in inventory.entries]
    lines += [json.dumps({"path": m, "state": MISSING_EXPECTED})
              for m in inventory.expected_missing]
    jsonl.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    digest = hashlib.sha256(jsonl.read_bytes()).hexdigest()
    summary = {"total": len(inventory.entries), "by_state": inventory.by_state(),
               "accepted": inventory.accepted, "inventory_sha256": digest}
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    reread = json.loads(summary_path.read_text(encoding="utf-8"))
    if (reread != summary or len(jsonl.read_text(encoding="utf-8").splitlines()) != len(lines)
            or hashlib.sha256(jsonl.read_bytes()).hexdigest() != digest):
        raise CustodyBlockedError("inventory read-back mismatch")
    return {"inventory": str(jsonl), "summary": reread}
