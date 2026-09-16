"""Test helpers only. No ranking, isolation, or recovery predicates."""

from __future__ import annotations

from typing import Any


def field(obj: Any, name: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def as_id_set(bundle: Any) -> set[str]:
    ids = field(bundle, "asset_ids")
    if ids is None:
        identities = field(bundle, "identities") or field(bundle, "aliases") or []
        ids = [
            field(item, "asset_id") or field(item, "asset_uid")
            for item in identities
        ]
    return {str(i) for i in ids if i}


def rec_id(item: Any) -> str | None:
    return (
        field(item, "id")
        or field(item, "finding_id")
        or field(item, "asset_id")
        or field(item, "asset_uid")
    )
