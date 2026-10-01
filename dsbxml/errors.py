"""Validation error formatting with model context (building/zone/surface).

Pydantic's default ValidationError shows the field path as raw indices
(``site.buildings.building.0...zones.zone.3...surfaces.surface.2.area``),
which doesn't say *which* building or zone that is without cross-referencing
the source file by hand. ModelValidationError re-walks the original XML tree
along that same path and adds the building title / zone handle / surface
index actually found there.
"""

from __future__ import annotations

from pydantic import ValidationError

# Model field name (as it appears in a pydantic error "loc") -> XML tag,
# restricted to the site -> building -> zone -> surface path this error
# formatter knows how to label. Fields outside this map (e.g. anything
# HVAC-related, whose tags aren't a simple PascalCase of the field name)
# just stop the walk, falling back to the raw loc path for the remainder.
_FIELD_TAG = {
    "site": "Site",
    "assembly_library": "AssemblyLibrary",
    "assembly": "Assembly",
    "component_blocks": "ComponentBlocks",
    "component_block": "ComponentBlock",
    "buildings": "Buildings",
    "building": "Building",
    "building_blocks": "BuildingBlocks",
    "building_block": "BuildingBlock",
    "zones": "Zones",
    "zone": "Zone",
    "body": "Body",
    "surfaces": "Surfaces",
    "surface": "Surface",
}

# Fields that identify a labeled node worth calling out in the breadcrumb,
# as opposed to plain pass-through containers (e.g. "buildings", "body").
_LABELED = {"building", "building_block", "zone", "surface"}


def _label_for(elem, field: str) -> str:
    kind = field.replace("_", " ").title()

    if field == "surface":
        parent = elem.getparent()
        siblings = parent.findall("Surface") if parent is not None else []
        idx = siblings.index(elem) if elem in siblings else "?"
        return f"{kind}[{idx}]"

    title = None
    attributes = elem.find("Attributes")
    if attributes is not None:
        for attribute in attributes.findall("Attribute"):
            if attribute.get("key") in ("Title", "Name") and attribute.text:
                title = attribute.text
                break
    if title:
        return f"{kind} '{title}'"

    object_ids = elem.find("ObjectIDs") or elem.find("Body/ObjectIDs")
    if object_ids is not None and object_ids.get("handle") is not None:
        return f"{kind} handle={object_ids.get('handle')}"

    parent = elem.getparent()
    index = list(parent).index(elem) if parent is not None else "?"
    return f"{kind}[{index}]"


def _breadcrumb(loc: tuple, root) -> str | None:
    if root is None:
        return None

    parts = []
    node = root
    i = 0
    while i < len(loc) and node is not None:
        field = loc[i]
        tag = _FIELD_TAG.get(field) if isinstance(field, str) else None
        if tag is None:
            break  # left the mapped building/zone/surface path

        children = node.findall(tag)
        if not children:
            break

        if i + 1 < len(loc) and isinstance(loc[i + 1], int):
            idx = loc[i + 1]
            if idx >= len(children):
                break
            node = children[idx]
            i += 2
        else:
            node = children[0]
            i += 1

        if field in _LABELED:
            parts.append(_label_for(node, field))

    return " > ".join(parts) if parts else None


class ModelValidationError(ValueError):
    """Wraps a pydantic ValidationError, adding model context to each error.

    Falls back to pydantic's own field path when the source XML tree isn't
    available, or an error's path leaves the mapped building/zone/surface
    hierarchy (e.g. HVAC fields).
    """

    def __init__(self, original: ValidationError, root=None):
        self.original = original
        self.errors = original.errors()
        super().__init__(self._format(root))

    def _format(self, root) -> str:
        lines = [f"{len(self.errors)} validation error(s) for {self.original.title}:"]
        for error in self.errors:
            loc = error.get("loc", ())
            crumb = _breadcrumb(loc, root)
            field = loc[-1] if loc else "?"
            path = ".".join(str(part) for part in loc)
            if crumb:
                lines.append(f"  {crumb} > {field}: {error['msg']} ({path})")
            else:
                lines.append(f"  {path}: {error['msg']}")
        return "\n".join(lines)
