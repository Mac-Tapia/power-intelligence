"""Reference-only structural graph checks; NOT a power flow or CIM validator.

Inputs are derived read projections. Does not repair missing topology, infer phases,
perform impedance inference, or substitute for equipment-terminal-phase modeling.
"""

from collections.abc import Mapping

ALLOWED_PHASES = set("ABCN")


class GraphProjectionError(ValueError):
    pass


def validate_projection(snapshot: Mapping) -> None:
    """Require snapshot and phase-labelled endpoints; fail closed on inconsistencies."""
    if not snapshot.get("network_snapshot_id") or not snapshot.get("topology_hash"):
        raise GraphProjectionError("missing immutable snapshot identity")
    nodes = snapshot.get("nodes")
    edges = snapshot.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise GraphProjectionError("nodes/edges must be lists")
    by_id = {}
    for node in nodes:
        ident = node.get("id")
        phases = node.get("phases")
        if not isinstance(ident, str) or not ident or ident in by_id:
            raise GraphProjectionError("node id missing or duplicated")
        if (
            not isinstance(phases, list)
            or len(set(phases)) != len(phases)
            or not phases
            or not set(phases) <= ALLOWED_PHASES
        ):
            raise GraphProjectionError("missing, duplicated or invalid node phases")
        by_id[ident] = set(phases)
    seen = set()
    for edge in edges:
        ident = edge.get("id")
        if not isinstance(ident, str) or not ident or ident in seen:
            raise GraphProjectionError("edge id missing or duplicated")
        seen.add(ident)
        a, b, phase = edge.get("from_node"), edge.get("to_node"), edge.get("phase")
        if a not in by_id or b not in by_id or a == b:
            raise GraphProjectionError("edge has missing endpoint or self-loop")
        if phase not in ALLOWED_PHASES or phase not in by_id[a] or phase not in by_id[b]:
            raise GraphProjectionError("edge phase incompatible with endpoints")
