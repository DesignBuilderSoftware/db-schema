---
name: dsbxml-model-change
description: Use when adding or changing a dsbxml model class or field (core, geometry, attributes, tables or HVAC components) in db-schema, when a dsbXML element or attribute is dropped or changed on load/save, or when a saved model fails validate_against_xsd.
---

# Changing the dsbxml models

`dsbxml` (repo `db-schema`, package on PyPI as `dsbxml`) maps DesignBuilder's dsbXML onto pydantic-xml models. The schema is `dsbxml/DesignBuilder.xsd`, bundled with the package.

## The rule that bites

**pydantic-xml ignores what the models don't declare.** An element or attribute missing from a model loads without error and is gone when the model is saved, so a saved file loses data DesignBuilder wrote. Every model change needs a round-trip check, not just a load.

## Where things live

| Module | Holds |
| --- | --- |
| `dsbxml/core.py` | `dsbXML`, `Site`, `Building`, `BuildingBlock`, `Zone`, ... |
| `dsbxml/geometry.py`, `attributes.py`, `tables.py`, `id.py` | Geometry, attribute lists, tables, `ObjectIDs` and the site-wide handle counter |
| `dsbxml/hvac/components.py` | `NoTypeHVACComponent` and one subclass per `type`, each with `type: Literal["<DesignBuilder type>"] = attr(default=...)` |
| `dsbxml/hvac/zone_components.py`, `unit_components.py` | Zone and unit components and `ZONE_COMPONENT_MAPPING` / `UNIT_COMPONENT_MAPPING` (type string to class), used to recast parsed components |
| `dsbxml/hvac/network.py` | `HVACNetwork`, loops, zone groups |
| `dsbxml/__init__.py` | Lazy loading: `_load_core_module` injects every HVAC class into each HVAC module's and `dsbxml.core`'s namespace, then calls `model_rebuild()` in dependency order |

## Adding an HVAC component or field

1. Find the element in a sample: `samples/8.0.0.058/DetailedHVAC.xml` and the 66 detailed HVAC samples (the 65 in `samples/2026.1.0.004/` plus `samples/2025.1.0.095/HVAC_Zones_Coloured.xml`) carry the detailed HVAC parts. `scripts/report_hvac_component_coverage.py` reports which component types are mapped.
2. Add the subclass with its `type` Literal, or the field with the XML name DesignBuilder uses (`attr(...)`, `element(...)`).
3. Add zone and unit components to their `*_MAPPING`; `dsbxml/tests/test_hvac_mappings.py` checks each key equals its class's `type` Literal.
4. Forward references to classes in other HVAC modules resolve through the namespace injection in `__init__.py`; don't add direct imports between the HVAC modules (that is what the cycle avoidance is for). ruff's F821 is ignored for `dsbxml/hvac/components.py` for this reason.
5. Touch the package API (`import dsbxml; dsbxml.dsbXML`) before using HVAC classes in a test, or `model_rebuild()` hasn't run (see the autouse fixture in `test_hvac_mappings.py`).

## Tests

The full suite takes about 8 minutes: it round-trips every sample model. While iterating, run the files you touch:

```bash
uv sync --extra dev
uv run pytest dsbxml/tests/test_hvac_mappings.py dsbxml/tests/test_hvac_components.py -q
uv run pytest dsbxml/tests/test_hvac_roundtrip_completeness.py -q -k "DetailedHVAC"
uv run pytest -q          # once, before pushing
```

- `test_full_model_round_trip.py`: load, `to_xml()`, reload, compare, for every XML in `samples/*/` (one folder per DesignBuilder version).
- `test_hvac_roundtrip_completeness.py`: counts every element path under the HVAC network before and after a round trip.
- `test_roundtrip_xsd_validity.py` / `test_xsd_validation.py`: saved XML against the bundled XSD (`dsbxml.utils.validate_against_xsd`). A building without detailed HVAC writes `<ObjectIDs>` into an empty `<HVACNetwork>`, which the XSD rejects; that is a known issue in `USAGE_GUIDE.md`.
- `test_usage_guide.py` runs every Python block in `USAGE_GUIDE.md`, so a change to public behaviour must keep the guide's examples working.

Lint as CI does: `uv run ruff check dsbxml`, `uv run ruff format --check dsbxml`, `uv run pylint dsbxml`. `apps/`, `examples/` and `scripts/` are excluded from ruff.

## Handles and diffing

New `ObjectIDs` take handles from a module-level counter that `load_model` resets to the loaded site's `handle`; it is shared by every model in the process. `diff_models` ignores handles and indices because DesignBuilder renumbers them on every save. Tests that create objects must not depend on handle values from another test.

`scripts/check_xml_vs_xsd.py` validates the 66 detailed HVAC samples against the XSD with lxml only; run it from the repo root (it uses relative paths).
