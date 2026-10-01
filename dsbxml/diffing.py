"""Semantic diff between two loaded models.

Reports added/removed buildings, zones, surfaces, and openings, changed
attributes (old -> new), and HVAC topology changes. Handle/index fields on
ObjectIDs (handle, buildingHandle, buildingBlockHandle, zoneHandle,
surfaceIndex, openingIndex) are ignored throughout — DesignBuilder
renumbers these on every save, so they're noise, not a semantic change.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Fields whose list items represent structural entities: matched by
# position, with any length difference reported as added/removed rather
# than a plain value change.
_CONTAINER_LIST_FIELDS = {
    "building": "buildings",
    "building_block": "building_blocks",
    "zone": "zones",
    "surface": "surfaces",
    "opening": "openings",
    "hvac_component": "hvac_components",
    "hvac_zone_component": "hvac_zone_components",
}

# Fields whose list items are {"name"|"key": ..., "value": ...} pairs:
# matched by that key, not position, since attribute order isn't semantic.
_ATTRIBUTE_LIST_FIELDS = {"attribute"}


def _summarize(entity) -> dict:
    if not isinstance(entity, dict):
        return {"value": entity}
    summary = {}
    if "type" in entity:
        summary["type"] = entity["type"]
    attrs = entity.get("attributes")
    if isinstance(attrs, dict):
        for a in attrs.get("attribute", []):
            if a.get("key") in ("Title", "Name") or a.get("name") in (
                "Title",
                "Name",
            ):
                summary["name"] = a.get("value")
                break
    return summary


def _path_str(path: list) -> str:
    return ".".join(str(p) for p in path)


@dataclass
class ModelDiff:
    added: dict[str, list] = field(default_factory=dict)
    removed: dict[str, list] = field(default_factory=dict)
    attribute_changes: list[dict] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return bool(self.added or self.removed or self.attribute_changes)

    def summary(self) -> str:
        lines = []
        for label, items in self.added.items():
            lines.append(f"+ {len(items)} {label} added")
        for label, items in self.removed.items():
            lines.append(f"- {len(items)} {label} removed")
        for change in self.attribute_changes:
            lines.append(f"~ {change['path']}: {change['old']!r} -> {change['new']!r}")
        return "\n".join(lines) if lines else "No semantic changes"


def _diff_attribute_list(a: list, b: list, path: list, diff: ModelDiff) -> None:
    def key_of(item):
        return item.get("key", item.get("name"))

    a_by_key = {key_of(item): item.get("value") for item in a}
    b_by_key = {key_of(item): item.get("value") for item in b}
    for key in sorted(set(a_by_key) | set(b_by_key), key=str):
        old, new = a_by_key.get(key), b_by_key.get(key)
        if old != new:
            diff.attribute_changes.append(
                {"path": _path_str(path + [key]), "old": old, "new": new}
            )


def _record_change(a, b, path: list, diff: ModelDiff) -> None:
    if a != b:
        diff.attribute_changes.append({"path": _path_str(path), "old": a, "new": b})


def _diff_dict(a: dict, b: dict, path: list, diff: ModelDiff) -> None:
    for key in sorted(set(a) | set(b), key=str):
        if key == "object_ids":
            continue
        _diff_value(a.get(key), b.get(key), path + [key], diff)


def _diff_model_list(a: list, b: list, path: list, diff: ModelDiff) -> None:
    """Match a list of model dicts by position and recurse into each pair.

    Any such list is recursed into, not just the named entities
    (building/zone/surface/...) — otherwise unmapped nested lists (HVAC
    loops, schemes, ...) would show up as one opaque whole-subtree change.
    """
    field_name = path[-1] if path else None
    label = _CONTAINER_LIST_FIELDS.get(field_name, field_name)
    common = min(len(a), len(b))
    for i in range(common):
        _diff_value(a[i], b[i], path + [i], diff)
    for item in a[common:]:
        diff.removed.setdefault(label, []).append(_summarize(item))
    for item in b[common:]:
        diff.added.setdefault(label, []).append(_summarize(item))


def _diff_list(a: list, b: list, path: list, diff: ModelDiff) -> None:
    if path and path[-1] in _ATTRIBUTE_LIST_FIELDS:
        _diff_attribute_list(a, b, path[:-1], diff)
    elif (a or b) and all(isinstance(x, dict) for x in a + b):
        _diff_model_list(a, b, path, diff)
    else:
        _record_change(a, b, path, diff)


def _diff_value(a, b, path: list, diff: ModelDiff) -> None:
    if isinstance(a, dict) and isinstance(b, dict):
        _diff_dict(a, b, path, diff)
    elif isinstance(a, list) and isinstance(b, list):
        _diff_list(a, b, path, diff)
    else:
        _record_change(a, b, path, diff)


def diff_models(model_a, model_b) -> ModelDiff:
    """Compare two dsbXML models, ignoring handle/index renumbering."""
    diff = ModelDiff()
    _diff_value(model_a.model_dump(), model_b.model_dump(), [], diff)
    return diff
