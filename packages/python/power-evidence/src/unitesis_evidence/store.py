"""Atomic local evidence publication and effective read-back with integrity check."""

import json
import os
import tempfile
from hashlib import sha256
from pathlib import Path


class EvidenceError(ValueError):
    pass


def canonical(payload: dict) -> bytes:
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def read_evidence(path: str | Path) -> dict:
    try:
        envelope = json.loads(Path(path).read_text(encoding="utf-8"))
        if envelope["schema"] != "power-intelligence.evidence/1":
            raise EvidenceError("Unsupported evidence schema")
        payload = envelope["payload"]
        if (
            not isinstance(payload, dict)
            or sha256(canonical(payload)).hexdigest() != envelope["payload_sha256"]
        ):
            raise EvidenceError("Evidence digest mismatch")
        return payload
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise EvidenceError(f"Evidence read-back failed: {error}") from error


def publish_evidence(path: str | Path, payload: dict) -> dict:
    target = Path(path)
    envelope = {
        "schema": "power-intelligence.evidence/1",
        "payload_sha256": sha256(canonical(payload)).hexdigest(),
        "payload": payload,
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=target.parent, prefix=target.name + ".", suffix=".tmp", delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(canonical(envelope))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
        result = read_evidence(target)
        if canonical(result) != canonical(payload):
            raise EvidenceError("Effective read-back differs from requested evidence")
        return result
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
