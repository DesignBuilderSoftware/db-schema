"""Compare the dsbxml classes with DesignBuilder.xsd, element by element from the root.

Each class is matched to the XSD element it reads (dsbXML first, then down every element
field), and every difference is reported:

- dropped:     the XSD declares an attribute or child element the class has no field for, so
               db-schema loses it when a file has it;
- extra:       the class reads an attribute or element the XSD does not declare there;
- location:    the class reads as an attribute what the XSD declares as a child element, or
               the other way round;
- single:      the XSD allows the element itself more than once, the class keeps one;
- any-order:   the element sits in an unbounded <xs:choice> (the XSD's way of saying "in any
               order"), which also allows it more than once; the class keeps one. Repeats in
               the samples are counted beside each;
- required:    the class requires what the XSD makes optional, so a valid file fails to load;
- untyped:     the XSD leaves the element's content open, so it checks nothing.

Run from the repo root: uv run python scripts/audit_classes_vs_xsd.py [--only KIND,...]
"""

from __future__ import annotations

import argparse
import inspect
import typing
import types
from collections import defaultdict

import xmlschema
from pydantic_core import PydanticUndefined
from pydantic_xml import BaseXmlModel

import dsbxml
from dsbxml.hvac.components import NoTypeHVACComponent

KINDS = ("dropped", "extra", "location", "single", "any-order", "required", "untyped")


def namespace() -> dict:
    import importlib
    import pkgutil

    ns: dict = {}
    for m in pkgutil.walk_packages(dsbxml.__path__, "dsbxml."):
        if ".tests" not in m.name:
            ns.update(vars(importlib.import_module(m.name)))
    return ns


NS = namespace()


def location(field) -> tuple[str, str | None]:
    info = [x for x in field.metadata if type(x).__name__ == "XmlEntityInfo"]
    if not info or info[0].location is None:
        return "text", None
    return {1: "element", 2: "attr"}[int(info[0].location.value)], info[0].path


def unwrap(t):
    """(the model class or None, whether a list, whether optional)."""
    many = optional = False
    origin, args = typing.get_origin(t), typing.get_args(t)
    if origin in (typing.Union, types.UnionType):
        rest = [a for a in args if a is not type(None)]
        optional = len(rest) < len(args)
        t = rest[0] if len(rest) == 1 else None
        origin, args = typing.get_origin(t), typing.get_args(t)
    if origin is list:
        many, t = True, args[0]
    if inspect.isclass(t) and issubclass(t, BaseXmlModel):
        return t, many, optional
    return None, many, optional


def class_fields(cls) -> list[tuple[str, str, str, type | None, bool, bool]]:
    """(field, location, tag, model class, many, required) for each field of `cls`."""
    hints = typing.get_type_hints(cls, globalns=NS)
    out = []
    for name, f in cls.model_fields.items():
        loc, path = location(f)
        model, many, optional = unwrap(hints[name])
        required = f.is_required() and not optional and f.default is PydanticUndefined
        out.append((name, loc, path or f.alias or name, model, many, required))
    return out


def xsd_children(el) -> dict[str, list]:
    t = el.type
    if not t.is_complex() or t.content is None or not hasattr(t.content, "iter_elements"):
        return {}
    out = defaultdict(list)
    for c in t.content.iter_elements():
        if getattr(c, "name", None):
            out[c.local_name].append(c)
    return out


def max_occurs(c) -> float:
    m = c.max_occurs
    parent = c.parent
    while parent is not None and hasattr(parent, "max_occurs"):  # a repeated group repeats it
        pm = parent.max_occurs
        m = None if m is None or pm is None else m * pm
        parent = getattr(parent, "parent", None)
    return float("inf") if m is None else m


def audit() -> list[tuple[str, str, str]]:
    schema = xmlschema.XMLSchema(str(__import__("pathlib").Path(dsbxml.__file__).parent / "DesignBuilder.xsd"))
    findings: list[tuple[str, str, str]] = []
    seen: set[tuple[str, int]] = set()

    def visit(cls, el, path):
        key = (cls.__name__, id(el.type))
        if key in seen:
            return
        seen.add(key)
        # Every HVAC class carries the shared fields of all of them, by design: not "extra".
        hvac = issubclass(cls, NoTypeHVACComponent)
        t = el.type
        attrs = {a for a in t.attributes if a} if t.is_complex() else set()
        kids = xsd_children(el)
        if not t.is_complex() or (t.content is not None and hasattr(t.content, "iter_elements") and any(type(c).__name__ == "XsdAnyElement" for c in t.content.iter_elements())):
            if cls.model_fields:
                findings.append(("untyped", path, f"{cls.__name__}: the XSD leaves this element open"))
        fields = class_fields(cls)
        have_attrs = {tag for _, loc, tag, *_ in fields if loc == "attr"}
        have_kids = {tag for _, loc, tag, *_ in fields if loc == "element"}
        for name, loc, tag, model, many, required in fields:
            if loc == "attr":
                if tag in attrs:
                    if required and not t.attributes[tag].is_required():
                        findings.append(("required", path, f"{cls.__name__}.{name} (@{tag})"))
                elif tag in kids or tag[:1].upper() + tag[1:] in kids:
                    findings.append(("location", path, f"{cls.__name__}.{name}: attribute here, child element <{tag}> in the XSD"))
                elif (attrs or kids) and not hvac:
                    findings.append(("extra", path, f"{cls.__name__}.{name} (@{tag})"))
            elif loc == "element":
                if tag in kids:
                    c = kids[tag][0]
                    if not many and (c.max_occurs is None or c.max_occurs > 1):
                        findings.append(("single", f"{path}/{tag}", f"{cls.__name__}.{name}"))
                    elif not many and max_occurs(c) > 1:
                        findings.append(("any-order", f"{path}/{tag}", f"{cls.__name__}.{name}"))
                    if required and c.min_occurs == 0:
                        findings.append(("required", path, f"{cls.__name__}.{name} (<{tag}>)"))
                    if model is not None:
                        visit(model, c, f"{path}/{tag}")
                elif tag in attrs:
                    findings.append(("location", path, f"{cls.__name__}.{name}: child element here, attribute @{tag} in the XSD"))
                elif (attrs or kids) and not hvac:
                    findings.append(("extra", path, f"{cls.__name__}.{name} (<{tag}>)"))
        for a in sorted(attrs - have_attrs):
            findings.append(("dropped", path, f"{cls.__name__}: @{a}"))
        for k in sorted(set(kids) - have_kids):
            findings.append(("dropped", path, f"{cls.__name__}: <{k}>"))

    visit(dsbxml.dsbXML, schema.elements["dsbXML"], "/dsbXML")
    return findings


def repeats() -> dict[str, int]:
    """Per element path: the most times it occurs under one parent in any sample."""
    from pathlib import Path

    from lxml import etree

    most: dict[str, int] = defaultdict(int)
    root = Path(dsbxml.__file__).resolve().parent.parent / "samples"
    for f in sorted(root.glob("*/*.xml")):
        for el in etree.parse(str(f)).iter():
            if not isinstance(el.tag, str):
                continue
            counts: dict[str, int] = defaultdict(int)
            for c in el:
                if isinstance(c.tag, str):
                    counts[c.tag] += 1
            here = "/" + "/".join(a.tag for a in reversed(list(el.iterancestors()))) + ("/" if el.getparent() is not None else "") + el.tag
            for tag, n in counts.items():
                key = f"{here}/{tag}"
                most[key] = max(most[key], n)
    return most


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", default=",".join(KINDS))
    only = set(ap.parse_args().only.split(","))
    found = [f for f in audit() if f[0] in only]
    if only & {"single", "any-order"}:
        most = repeats()
        found = [(k, p, w + (f" (at most {most.get(p, 0)} in one parent in the samples)" if k in ("single", "any-order") else "")) for k, p, w in found]
    for kind in KINDS:
        rows = [f for f in found if f[0] == kind]
        if rows:
            print(f"## {kind} ({len(rows)})")
            for _, path, what in rows:
                print(f"  {path}: {what}")
    print(f"{len(found)} findings")


if __name__ == "__main__":
    main()
