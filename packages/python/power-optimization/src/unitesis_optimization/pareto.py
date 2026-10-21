"""Pareto front for multi-objective alternatives (spec 018, AC-018-E03).

Only alternatives already confirmed technically feasible are candidates. Objectives are
declared with their direction; an alternative is dominated when another one is at least as
good in every objective and strictly better in one. Ties keep both alternatives. Missing or
non-finite objective values exclude the alternative from the front with a reason.
"""

from __future__ import annotations

import math
from typing import Any, Literal

Direction = Literal["min", "max"]


def _value(item: dict[str, Any], key: str) -> float | None:
    v = item.get(key)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        return None
    return float(v)


def pareto_front(items: list[dict[str, Any]], objectives: dict[str, Direction],
                 id_key: str = "id") -> dict[str, Any]:
    if not objectives or any(d not in ("min", "max") for d in objectives.values()):
        raise ValueError("objectives must map names to 'min' or 'max'")
    valid: list[tuple[str, tuple[float, ...]]] = []
    excluded: dict[str, str] = {}
    for item in items:
        vals = [_value(item, k) for k in objectives]
        if any(v is None for v in vals):
            missing = [k for k, v in zip(objectives, vals, strict=True) if v is None]
            excluded[str(item[id_key])] = f"missing or non-finite objectives {missing}"
            continue
        signed = tuple(v if d == "min" else -v
                       for v, d in zip(vals, objectives.values(), strict=True))  # type: ignore[operator]
        valid.append((str(item[id_key]), signed))
    front, dominated = [], {}
    for aid, a in valid:
        dominator = next((bid for bid, b in valid if bid != aid
                          and all(x <= y for x, y in zip(b, a, strict=True))
                          and any(x < y for x, y in zip(b, a, strict=True))), None)
        if dominator is None:
            front.append(aid)
        else:
            dominated[aid] = dominator
    return {"objectives": dict(objectives), "front": sorted(front),
            "dominated_by": dict(sorted(dominated.items())), "excluded": excluded}
