"""MkDocs hook: generate the dsbXML element reference from DesignBuilder.xsd.

The schema is one deeply nested (Russian-doll) document with no named types,
so the same element name (Polygon, ObjectIDs, Point3D...) is declared many
times. This groups the declarations by element name, merges the ones that
are structurally identical, and writes one section per element listing its
attributes, child elements and the parents it appears under.

The page is generated at build time, so it always matches the bundled
schema. Run this file directly to print the Markdown instead:

    uv run python scripts/docs_xsd_reference.py > elements.md
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from lxml import etree

XSD_PATH = Path(__file__).resolve().parent.parent / "dsbxml" / "DesignBuilder.xsd"
PAGE_URI = "schema/elements.md"
XS = "{http://www.w3.org/2001/XMLSchema}"
# Paths listed per variant before the rest are summarised as a count.
MAX_PATHS = 8


def _parent_element(node):
    """The nearest enclosing xs:element of a schema node, or None at the root."""
    node = node.getparent()
    while node is not None and node.tag != f"{XS}element":
        node = node.getparent()
    return node


def _path(decl) -> str:
    """Slash-separated element names from the root down to decl."""
    names = []
    while decl is not None:
        names.append(decl.get("name"))
        decl = _parent_element(decl)
    return "/".join(reversed(names))


def _occurs(decl) -> str:
    low = decl.get("minOccurs", "1")
    high = decl.get("maxOccurs", "1")
    high = "*" if high == "unbounded" else high
    return low if low == high else f"{low}..{high}"


def _describe(decl) -> dict:
    """Attributes, children and text content of one xs:element declaration."""
    info = {"attributes": [], "children": [], "text": decl.get("type")}
    complex_type = decl.find(f"{XS}complexType")
    if complex_type is None:
        return info
    for node in complex_type.iter(f"{XS}attribute", f"{XS}element", f"{XS}extension"):
        if node.tag == f"{XS}element":
            if _parent_element(node) is decl:
                group = node.getparent().tag.replace(XS, "")
                info["children"].append((node.get("name"), _occurs(node), group))
        elif _parent_element(node) is decl:
            if node.tag == f"{XS}extension":
                info["text"] = node.get("base")
            else:
                info["attributes"].append(
                    (node.get("name"), node.get("type", ""), node.get("use", "optional"))
                )
    return info


def _signature(info: dict) -> tuple:
    return (
        tuple(info["attributes"]),
        tuple(info["children"]),
        info["text"],
    )


def collect(xsd_path: Path = XSD_PATH) -> dict[str, list[dict]]:
    """Map element name -> distinct variants, each with its info and parents."""
    root = etree.parse(str(xsd_path)).getroot()
    variants: dict[str, dict[tuple, dict]] = defaultdict(dict)
    for decl in root.iter(f"{XS}element"):
        info = _describe(decl)
        parent = _parent_element(decl)
        parent_name = parent.get("name") if parent is not None else None
        variant = variants[decl.get("name")].setdefault(
            _signature(info), {"info": info, "parents": set(), "paths": [], "count": 0}
        )
        variant["count"] += 1
        if parent_name:
            variant["parents"].add(parent_name)
            variant["paths"].append(_path(parent))
    return {name: list(found.values()) for name, found in variants.items()}


def _link(name: str) -> str:
    return f"[`{name}`](#{name.lower()})"


def _render_variant(variant: dict, show_paths: bool = False) -> list[str]:
    info = variant["info"]
    lines = []
    if show_paths and variant["paths"]:
        paths = sorted(set(variant["paths"]))
        shown = paths[:MAX_PATHS]
        lines.append("Found under:")
        lines.append("")
        lines += [f"- `{path}`" for path in shown]
        if len(paths) > len(shown):
            lines.append(f"- ...and {len(paths) - len(shown)} more")
        lines.append("")
    elif variant["parents"]:
        parents = ", ".join(_link(p) for p in sorted(variant["parents"], key=str.lower))
        lines.append(f"Appears under: {parents}")
        lines.append("")
    if info["text"]:
        lines.append(f"Text content: `{info['text']}`")
        lines.append("")
    if info["attributes"]:
        lines += ["| Attribute | Type | Use |", "|---|---|---|"]
        lines += [f"| `{n}` | `{t}` | {u} |" for n, t, u in info["attributes"]]
        lines.append("")
    if info["children"]:
        lines += ["| Child element | Occurs | Group |", "|---|---|---|"]
        lines += [f"| {_link(n)} | {o} | {g} |" for n, o, g in info["children"]]
        lines.append("")
    if not (info["text"] or info["attributes"] or info["children"]):
        lines += ["Empty element.", ""]
    return lines


def render(xsd_path: Path = XSD_PATH) -> str:
    elements = collect(xsd_path)
    declarations = sum(v["count"] for vs in elements.values() for v in vs)
    lines = [
        "# Schema element reference",
        "",
        "Generated from the `DesignBuilder.xsd` bundled with the `dsbxml` package "
        f"({len(elements)} element names, {declarations} declarations). "
        "Each section lists an element's attributes, its child elements and the "
        "elements it appears under. Where the schema declares the same element name "
        "with different content in different places, each distinct form is shown "
        "as a numbered variant.",
        "",
        "Occurs is `minOccurs..maxOccurs` (`*` means unbounded). "
        "Group is the content model the child belongs to: `sequence` children must "
        "appear in the order listed, `choice` children are alternatives.",
        "",
        "The schema is the contract for files DesignBuilder accepts; to check a file "
        "or a loaded model against it, use `dsbxml.utils.validate_against_xsd`.",
        "",
    ]
    for name in sorted(elements, key=str.lower):
        found = elements[name]
        lines += [f"## {name} {{#{name.lower()}}}", ""]
        if len(found) == 1:
            lines += _render_variant(found[0])
            continue
        lines += [f"Declared with {len(found)} different forms.", ""]
        for number, variant in enumerate(found, start=1):
            lines += [f"**Variant {number}**", ""]
            lines += _render_variant(variant, show_paths=True)
    return "\n".join(lines)


def on_files(files, config):  # pragma: no cover - exercised by mkdocs build
    from mkdocs.structure.files import File

    files.append(File.generated(config, PAGE_URI, content=render()))
    return files


if __name__ == "__main__":
    print(render())
