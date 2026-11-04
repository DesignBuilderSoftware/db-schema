# Usage guide

`dsbxml` loads DesignBuilder XML (dsbXML) files into typed Pydantic models,
lets you read and change them in Python, and writes them back as XML.

Every Python example on this page is run by the test suite
(`dsbxml/tests/test_usage_guide.py`) against a real DesignBuilder model
saved as `building.xml`, so the examples stay in step with the package.

## Installation

```bash
pip install dsbxml
```

## Loading and saving

```python
from dsbxml import load_model, save_model

model = load_model("building.xml")

print(model.name)     # model title, e.g. "~Shoebox261"
print(model.version)  # DesignBuilder version that wrote the file
print(model.date)     # datetime.date

model.name = "Updated building"
save_model(model, "building_updated.xml")
```

`load_model` and `save_model` accept a `str` or `pathlib.Path` and only
handle `.xml` files; any other suffix raises `ValueError`.

!!! warning "Loaded models are cached"
    `load_model` keeps the last 32 models in an LRU cache keyed by the
    file's resolved path, and returns the **same object** each time. A
    change made to one loaded model is therefore visible to every other
    caller that loaded the same path, and edits to the file on disk are not
    picked up. Pass `use_cache=False` to get a fresh, independent copy, or
    call `dsbxml.utils.clear_model_cache()`.

```python
from dsbxml.utils import clear_model_cache

fresh = load_model("building.xml", use_cache=False)
assert fresh is not load_model("building.xml")
clear_model_cache()
```

## Model structure

Python attribute names are snake_case versions of the XML tags; each XML
container element (`<Buildings>`, `<Zones>`, ...) is a model whose list of
children has the singular name:

```text
dsbXML                      model
└── Site                    model.site
    ├── Attributes          model.site.attributes.attribute[]
    ├── Tables              model.site.tables.table[]
    ├── AssemblyLibrary     model.site.assembly_library.assembly[]
    └── Buildings           model.site.buildings.building[]
        └── Building
            ├── Attributes      building.attributes.attribute[]
            ├── BuildingBlocks  building.building_blocks.building_block[]
            │   └── BuildingBlock
            │       └── Zones   block.zones.zone[]
            │           └── Zone
            │               └── Body          zone.body
            │                   ├── Vertices  zone.body.vertices
            │                   └── Surfaces  zone.body.surfaces.surface[]
            │                       └── Surface
            │                           └── Openings  surface.openings.opening[]
            └── HVACNetwork     building.hvac_network
                ├── HVACLoops       .hvac_loops.hvac_loop[]
                └── HVACZoneGroups  .hvac_zone_groups.hvac_zone_group[]
```

Many elements are optional, so check for `None` before going deeper:

```python
for building in model.site.buildings.building:
    for block in building.building_blocks.building_block:
        if block.zones is None:
            continue
        for zone in block.zones.zone:
            print(zone.body.volume, len(zone.body.surfaces.surface))
```

The [schema element reference](https://designbuildersoftware.github.io/db-schema/schema/elements/) lists every element,
attribute and child the file format allows; the API reference documents
each Python model.

## Attributes

Most DesignBuilder settings are stored as attribute lists rather than as
typed fields. The site and HVAC objects use `name`/value pairs
(`NameAttributes`); buildings, blocks, bodies, surfaces and openings use
`key`/value pairs (`KeyAttributes`). Values are strings, or `None` when the
element is empty.

```python
site_settings = {a.name: a.value for a in model.site.attributes.attribute}

building = model.site.buildings.building[0]
building_settings = {a.key: a.value for a in building.attributes.attribute}

zone = building.building_blocks.building_block[0].zones.zone[0]
zone_settings = {a.key: a.value for a in zone.body.attributes.attribute}
print(zone_settings["Title"])  # e.g. "Zone 1"
```

## Geometry

Coordinates are stored as `"x;y;z"` text in `Point3D.value`; the `x`, `y`,
`z` and `coords` properties parse it, and assigning to them rewrites the
text.

```python
vertices = zone.body.vertices
point = vertices[0]
print(point.coords)  # [x, y, z] as floats

for point in vertices:
    print(point.x, point.y, point.z)

point.z = 3.0
```

## Tables

```python
tables = model.site.tables
print([table.name for table in tables.table])

table = tables.get_table_by_name("TableOfTables")  # KeyError if missing
print(table.field_name, len(table.row))
```

## HVAC

Detailed HVAC lives on each building's `hvac_network`. Buildings without
detailed HVAC have an empty network, where `hvac_loops` is `None`.

```python
for building in model.site.buildings.building:
    network = building.hvac_network
    if network is None or network.hvac_loops is None:
        continue
    for loop in network.hvac_loops.hvac_loop:
        loop_name = {a.name: a.value for a in loop.attributes.attribute}.get("Title")
        print(loop.loopType, loop_name)
```

## Validating against the schema

`validate_against_xsd` checks a loaded model, a file path or XML bytes
against the `DesignBuilder.xsd` bundled with the package and returns the
error messages; an empty list means the XML is valid. For a loaded model
this tells you whether saving it would produce a file the schema accepts.

```python
from dsbxml.utils import validate_against_xsd

errors = validate_against_xsd(model)
assert errors == []
```

Loading is more lenient than the schema: some files that do not validate
still load, so validate explicitly when that matters.

## Comparing two models

`diff_models` reports added and removed buildings, zones, surfaces and
openings, changed values, and HVAC changes. Handles and indices are
ignored because DesignBuilder renumbers them on every save.

```python
from dsbxml import diff_models

before = load_model("building.xml", use_cache=False)
after = load_model("building.xml", use_cache=False)
after.name = "Renamed"

diff = diff_models(before, after)
print(diff.has_changes)  # True
print(diff.summary())    # ~ name: '...' -> 'Renamed'
```

## Errors

- A missing file raises `FileNotFoundError`.
- A suffix other than `.xml` raises `ValueError`.
- XML that does not match the models raises `dsbxml.ModelValidationError`
  (a `ValueError` subclass). Its message names the building, zone or
  surface where each problem is, and `.errors` holds pydantic's error
  list.

```python
from dsbxml import ModelValidationError, dsbXML

try:
    dsbXML.from_xml(b'<dsbXML name="a" date="not a date" version="1" objects="all"/>')
except ModelValidationError as error:
    print(error)
    print(error.errors[0]["loc"])  # ('date',)
```

## Handles

Objects are identified by integer handles held in their `ObjectIDs`. Handles
read from a file are kept as they are. New `ObjectIDs` take the next handle
from a site-wide counter, which `load_model` resets to the loaded site's
`handle`; the site's `handle` is written back as the counter's current
value.

```python
from dsbxml.id import ObjectIDs, current_site_handle

next_handle = current_site_handle()
new_ids = ObjectIDs()
assert new_ids.handle == next_handle
```

The counter is a module-level global (guarded by a lock), so it is shared
by every model in the process.

## Package imports

`dsbxml` loads its model classes lazily. Every class in `dsbxml.core`
(`dsbXML`, `Site`, `Building`, `Zone`, ...) is available from the package
root, as are `HVACNetwork`, `HVACComponents`, `diff_models`, `ModelDiff`
and `ModelValidationError`; `DSB` is a backwards-compatible alias for
`dsbXML`. Classes in the other modules are imported from their module,
e.g. `from dsbxml.geometry import Point3D`.
