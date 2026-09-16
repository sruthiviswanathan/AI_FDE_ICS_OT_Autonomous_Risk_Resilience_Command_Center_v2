"""Hop-capped evidence graph slice (FR-006). No whole-estate dump. No tag-to-unit imputation."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

from ..repository import rows

UNITS_PATH = "data/raw/process_units.csv"
DEPS_PATH = "data/raw/process_dependencies.csv"
TAGS_PATH = "data/reference/tags.csv"
BARRIERS_PATH = "data/raw/safety_barriers.csv"
HOP_CAP = 8
TRANSFORM = "enh-10-graph.1"

_CACHE: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    units = {r["unit_id"]: r for r in rows(UNITS_PATH)}
    deps = rows(DEPS_PATH)
    adj: dict[str, list[dict]] = defaultdict(list)
    for dep in deps:
        adj[dep["upstream_unit"]].append(dep)
        adj[dep["downstream_unit"]].append(dep)
    tags_by_asset: dict[str, list[dict]] = defaultdict(list)
    for tag in rows(TAGS_PATH):
        tags_by_asset[tag["asset_id"]].append(tag)
    barriers_by_unit: dict[str, list[dict]] = defaultdict(list)
    for bar in rows(BARRIERS_PATH):
        barriers_by_unit[bar["unit_id"]].append(bar)
    _CACHE = {"units": units, "deps": deps, "adj": adj, "tags_by_asset": tags_by_asset, "barriers_by_unit": barriers_by_unit}
    return _CACHE


def graph_slice(
    plant_id: str | None = None,
    unit_id: str | None = None,
    asset_id: str | None = None,
    hops: int = 4,
) -> dict[str, Any]:
    """Return a bounded slice. Missing plant/unit/asset ⇒ empty slice, not 18-plant dump."""
    data = _load()
    hops = min(max(int(hops or 1), 1), HOP_CAP)
    seed_units: list[str] = []
    imputed = False
    if unit_id and unit_id in data["units"]:
        seed_units = [unit_id]
        plant_id = plant_id or data["units"][unit_id]["plant_id"]
    elif asset_id:
        tagged = [t.get("unit_id") for t in data["tags_by_asset"].get(asset_id, []) if t.get("unit_id")]
        seed_units = list(dict.fromkeys(tagged))
        if not seed_units:
            return {
                "plant_id": plant_id,
                "asset_id": asset_id,
                "hops": hops,
                "hop_cap": HOP_CAP,
                "whole_graph_dump": False,
                "imputed_tag_to_unit": False,
                "nodes": [],
                "edges": [],
                "note": "asset has no tag-to-unit join; not imputed (1834 untagged remain UNKNOWN)",
                "transform_version": TRANSFORM,
            }
        plant_id = plant_id or data["units"].get(seed_units[0], {}).get("plant_id")
    elif plant_id:
        seed_units = [uid for uid, row in data["units"].items() if row.get("plant_id") == plant_id]
    else:
        return {
            "plant_id": None,
            "hops": hops,
            "hop_cap": HOP_CAP,
            "whole_graph_dump": False,
            "imputed_tag_to_unit": False,
            "nodes": [],
            "edges": [],
            "note": "plant_id, unit_id, or asset_id required — no estate dump",
            "transform_version": TRANSFORM,
        }

    seen: dict[str, int] = {}
    q: deque[tuple[str, int]] = deque((u, 0) for u in seed_units)
    for u, d in q:
        seen[u] = d
    while q:
        cur, dist = q.popleft()
        if dist >= hops:
            continue
        for dep in data["adj"].get(cur, []):
            if plant_id and dep.get("plant_id") != plant_id:
                continue
            nxt = dep["downstream_unit"] if dep["upstream_unit"] == cur else dep["upstream_unit"]
            if nxt not in seen and nxt in data["units"]:
                if plant_id and data["units"][nxt].get("plant_id") != plant_id:
                    continue
                seen[nxt] = dist + 1
                q.append((nxt, dist + 1))

    nodes = []
    for uid, dist in seen.items():
        row = data["units"][uid]
        nodes.append(
            {
                "id": uid,
                "type": "process_unit",
                "plant_id": row["plant_id"],
                "safe_state": row.get("safe_state"),
                "hop": dist,
            }
        )
        for bar in data["barriers_by_unit"].get(uid, []):
            nodes.append(
                {
                    "id": bar["barrier_id"],
                    "type": "safety_barrier",
                    "unit_id": uid,
                    "state": bar.get("state"),
                    "hop": dist,
                }
            )
    edges = []
    for dep in data["deps"]:
        if dep["upstream_unit"] in seen and dep["downstream_unit"] in seen:
            edges.append(
                {
                    "from": dep["upstream_unit"],
                    "to": dep["downstream_unit"],
                    "type": dep.get("dependency_type"),
                    "documented": dep.get("documented"),
                    "critical": dep.get("critical"),
                }
            )
    return {
        "plant_id": plant_id,
        "asset_id": asset_id,
        "hops": hops,
        "hop_cap": HOP_CAP,
        "whole_graph_dump": False,
        "imputed_tag_to_unit": imputed,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
        "live_ot": False,
        "transform_version": TRANSFORM,
    }
