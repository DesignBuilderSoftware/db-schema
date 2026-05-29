# DesignBuilder Schema

Python package for reading, editing, and writing DesignBuilder XML simulation files using Pydantic v2 and pydantic-xml.

## Installation

```bash
pip install designbuilder-schema
```

## Quick start

```python
from db_schema.utils import load_model, save_model

# Load a DesignBuilder XML file
model = load_model("path/to/model.xml")

# Inspect geometry
for building in model.site.buildings.building:
    for block in building.building_blocks.building_block:
        for zone in block.zones.zone:
            print(zone.body.vertices.point_3d)

# Save back to XML
save_model(model, "output.xml")
```

## Features

- Type-safe XML parsing via Pydantic v2 and pydantic-xml
- Full DesignBuilder schema support: geometry, surfaces, openings, HVAC
- Round-trip load → modify → save fidelity
- Thread-safe handle generation
- LRU caching for repeated loads
