"""Energized network for general solvers (spec 004-B): meshes allowed, ideal switches fused.

Closed switches merge their buses into one electrical node (zero impedance); open switches
and out-of-service lines stay in the inventory as excluded. The energized part is the
component that contains the slack. Rejected (AC-004-01, never simplified silently):
more than one slack, lines or switches joining different nominal voltages (transformers
arrive with 004-B2) and loads on de-energized islands.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from unitesis_domain import ElectricalSnapshot, Line

from .radial import TopologyError, _active_branches


@dataclass(frozen=True, slots=True)
class EnergizedNetwork:
    slack_bus: str
    energized_buses: tuple[str, ...]          # sorted, includes buses fused by switches
    node_of: dict[str, str]                   # energized bus -> representative node bus
    nodes: tuple[str, ...]                    # representative buses, slack node first
    lines: tuple[Line, ...]                   # in-service lines inside the energized part
    excluded: tuple[str, ...]                 # open switches / out-of-service lines
    deenergized_buses: tuple[str, ...]
    meshed: bool


def build_energized_network(snapshot: ElectricalSnapshot) -> EnergizedNetwork:
    if len(snapshot.slacks) != 1:
        raise TopologyError("exactly one slack is supported until multi-source studies (004-B)")
    slack = snapshot.slacks[0].bus
    active, excluded = _active_branches(snapshot)
    for br in active:
        kv_a = snapshot.bus(br.from_bus).nominal_kv
        kv_b = snapshot.bus(br.to_bus).nominal_kv
        if kv_a != kv_b:
            bid = br.line_id if isinstance(br, Line) else br.switch_id
            raise TopologyError(f"{bid}: joins {kv_a} kV and {kv_b} kV; transformers are "
                                "required (004-B2)")

    adj: dict[str, set[str]] = {b.bus_id: set() for b in snapshot.buses}
    for br in active:
        adj[br.from_bus].add(br.to_bus)
        adj[br.to_bus].add(br.from_bus)
    energized = {slack}
    queue = deque([slack])
    while queue:
        for nxt in adj[queue.popleft()]:
            if nxt not in energized:
                energized.add(nxt)
                queue.append(nxt)
    deenergized = sorted(set(adj) - energized)
    for load in snapshot.loads:
        if load.in_service and load.bus in deenergized and (load.p_mw or load.q_mvar):
            raise TopologyError(f"load {load.load_id} is connected to a de-energized island")

    parent = {b: b for b in energized}

    def find(b: str) -> str:
        while parent[b] != b:
            parent[b] = parent[parent[b]]
            b = parent[b]
        return b

    for sw in snapshot.switches:
        if sw.closed and sw.from_bus in energized:
            parent[find(sw.from_bus)] = find(sw.to_bus)
    groups: dict[str, list[str]] = {}
    for b in sorted(energized):
        groups.setdefault(find(b), []).append(b)
    node_of: dict[str, str] = {}
    for members in groups.values():
        rep = slack if slack in members else members[0]  # deterministic representative
        node_of.update(dict.fromkeys(members, rep))
    nodes = (slack, *sorted(set(node_of.values()) - {slack}))
    lines = tuple(sorted(
        (ln for ln in snapshot.lines if ln.in_service and ln.from_bus in energized),
        key=lambda ln: ln.line_id))
    edges = {frozenset((node_of[ln.from_bus], node_of[ln.to_bus])) for ln in lines
             if node_of[ln.from_bus] != node_of[ln.to_bus]}
    meshed = len(lines) > len(edges) or len(edges) > len(nodes) - 1
    return EnergizedNetwork(slack, tuple(sorted(energized)), node_of, nodes, lines,
                            tuple(excluded), tuple(deenergized), meshed)
