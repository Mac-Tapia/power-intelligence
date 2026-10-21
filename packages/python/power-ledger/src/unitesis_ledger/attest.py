"""Cryptographic digest of canonical evidence (not blockchain consensus or notarization)."""

import hashlib
import json
from collections.abc import Mapping


def canonical_json(obj: Mapping) -> bytes:
    """Local deterministic JSON serialization; formal external interoperability needs RFC 8785."""
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")


def digest_evidence(evidence: Mapping) -> str:
    return hashlib.sha256(canonical_json(evidence)).hexdigest()


def matches_digest(evidence: Mapping, expected: str) -> bool:
    import hmac

    return hmac.compare_digest(digest_evidence(evidence), expected)
