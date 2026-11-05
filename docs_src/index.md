# DesignBuilder Schema

`dsbxml` is a Python package for reading, editing and writing DesignBuilder
XML (dsbXML) files, built on Pydantic v2 and pydantic-xml. It also ships the
`DesignBuilder.xsd` schema that defines the file format.

## Installation

```bash
pip install dsbxml
```

Requires Python 3.10 or later.

## Quick start

```python
from dsbxml import load_model, save_model
from dsbxml.utils import validate_against_xsd

model = load_model("path/to/model.xml")

for building in model.site.buildings.building:
    for block in building.building_blocks.building_block:
        for zone in block.zones.zone if block.zones else []:
            print(zone.body.vertices[0].coords)

model.name = "Updated model"
print(validate_against_xsd(model))  # [] if the saved file would be schema-valid
save_model(model, "output.xml")
```

## Where to go next

- [User guide](guide.md): loading and saving, the model tree, attributes,
  geometry, HVAC, validation, diffs and errors.
- [Schema element reference](schema/elements.md): every element and
  attribute in `DesignBuilder.xsd`, generated from the schema.
- API reference: the [package functions and supporting models](api/overview.md),
  the [core building models](api/models.md) and the
  [HVAC models](api/hvac.md), generated from the code.

## Features

- Typed models for the whole dsbXML tree, including detailed HVAC
- Load, modify and save while keeping the file valid against the schema
- Validation against the bundled `DesignBuilder.xsd`
- Semantic diff of two models that ignores handle renumbering
- Validation errors that name the building, zone or surface at fault
