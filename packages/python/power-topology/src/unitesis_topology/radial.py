"""Energized topology from terminal connections and switch states (never GIS proximity).

Open switches and out-of-service lines stay in the snapshot inventory and are reported
as excluded; they are not deleted. Meshes, multiple slacks and voltage mismatches across
a line are rejected because the solver scope 008-A is radial and balanced.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from unitesis_domain import ElectricalSnapshot, Line, Switch


class TopologyError(ValueError):
    """The network is outside the supported radial scope."""


Branch = Line | Switch


@dataclass(frozen=True, slots=True)
class RadialTree:
    slack_bus: str
    order: tuple[str, ...]                    # BFS order from the slack
    parent_branch: dict[str, Branch]          # child bus -> branch to its parent
    parent_bus: dict[str, str]
    excluded: tuple[str, ...]                 # open / out-of-service element ids
    deenergized_buses: tuple[str, ...]

    def children(self, bus: str) -> list[str]:
        return [b for b, p in self.parent_bus.items() if p == bus]


def _active_branches(snapshot: ElectricalSnapshot) -> tuple[list[Branch], list[str]]:
    active: list[Branch] = []
    excluded: list[str] = []
    for line in snapshot.lines:
        (active if line.in_service else excluded).append(line if line.in_service else line.line_id)
    for sw in snapshot.switches:
        (active if sw.closed else excluded).append(sw if sw.closed else sw.switch_id)
    return active, sorted(excluded)


def _branch_id(br: Branch) -> str:
    return br.line_id if isinstance(br, Line) else br.switch_id


def energized_components(snapshot: ElectricalSnapshot) -> list[set[str]]:
    active, _ = _active_branches(snapshot)
    adj: dict[str, set[str]] = {b.bus_id: set() for b in snapshot.buses}
    for br in active:
        adj[br.from_bus].add(br.to_bus)
        adj[br.to_bus].add(br.from_bus)
    seen: set[str] = set()
    comps: list[set[str]] = []
    for start in sorted(adj):
        if start in seen:
            continue
        comp, queue = {start}, deque([start])
        while queue:
            for nxt in adj[queue.popleft()]:
                if nxt not in comp:
                    comp.add(nxt)
                    queue.append(nxt)
        seen |= comp
        comps.append(comp)
    return comps


def require_balanced(snapshot: ElectricalSnapshot) -> None:
    """Balanced engines cannot represent phase-frame data; never simplified silently."""
    ids = snapshot.phase_frame_elements()
    if ids:
        shown = ", ".join(ids[:10]) + (f" (+{len(ids) - 10})" if len(ids) > 10 else "")
        raise TopologyError(f"phase-frame elements need the three-phase engine (008-C): {shown}")


def build_radial_tree(snapshot: ElectricalSnapshot) -> RadialTree:
    require_balanced(snapshot)
    if len(snapshot.slacks) != 1:
        raise TopologyError("exactly one slack is supported in the radial scope")
    if any(t.in_service for t in snapshot.transformers):
        raise TopologyError("transformers are outside the radial sweep scope; use the "
                            "Newton-Raphson engine (008-B2)")
    slack = snapshot.slacks[0].bus
    active, excluded = _active_branches(snapshot)
    adj: dict[str, list[tuple[str, Branch]]] = {b.bus_id: [] for b in snapshot.buses}
    for br in active:
        adj[br.from_bus].append((br.to_bus, br))
        adj[br.to_bus].append((br.from_bus, br))

    order: list[str] = [slack]
    parent_bus: dict[str, str] = {}
    parent_branch: dict[str, Branch] = {}
    visited = {slack}
    queue = deque([slack])
    used: set[str] = set()
    while queue:
        bus = queue.popleft()
        for nxt, br in sorted(adj[bus], key=lambda item: _branch_id(item[1])):
            bid = _branch_id(br)
            if bid in used:
                continue
            used.add(bid)
            if nxt in visited:
                raise TopologyError(f"mesh detected through branch {bid}; radial scope only")
            visited.add(nxt)
            parent_bus[nxt] = bus
            parent_branch[nxt] = br
            order.append(nxt)
            queue.append(nxt)

    for child, br in parent_branch.items():
        if isinstance(br, Line):
            kv_a = snapshot.bus(br.from_bus).nominal_kv
            kv_b = snapshot.bus(br.to_bus).nominal_kv
            if kv_a != kv_b:
                raise TopologyError(
                    f"{br.line_id}: nominal voltage mismatch {kv_a} vs {kv_b} kV "
                    "(transformers are outside the initial scope)")
        elif snapshot.bus(br.from_bus).nominal_kv != snapshot.bus(br.to_bus).nominal_kv:
            raise TopologyError(f"{br.switch_id}: switch joins different voltage levels")
        del child

    deenergized = sorted(set(adj) - visited)
    for load in snapshot.loads:
        if load.in_service and load.bus in deenergized and (load.p_mw or load.q_mvar):
            raise TopologyError(f"load {load.load_id} is connected to a de-energized island")
    return RadialTree(slack, tuple(order), parent_branch, parent_bus,
                      tuple(excluded), tuple(deenergized))
