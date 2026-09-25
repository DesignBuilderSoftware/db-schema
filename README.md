# db-schema

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-241%20passing-brightgreen)

Python package for reading, editing, and writing DesignBuilder XML files using Pydantic and pydantic-xml.

## Install

```bash
pip install dsbxml
```

The PyPI package is named `dsbxml`; the import name is `db_schema`.

## Quick Start

```python
from db_schema import load_model, save_model

dsb = load_model("building.xml")
dsb.name = "Updated Building"
save_model(dsb, "building_updated.xml")
```

## Features

- Type-safe XML handling via Pydantic v2
- XXE attack protection built-in
- Full DesignBuilder XML schema support including HVAC
- Load/save XML and JSON formats

## Data Model

```
dsbXML
└── Site
    ├── Attributes / Tables / AssemblyLibrary
    └── Buildings
        └── Building
            ├── BuildingBlocks / Zones / Surfaces
            └── HVACNetwork
                └── HVACLoops / HVACZoneGroups
```

## Development

```bash
git clone https://github.com/DesignBuilderSoftware/db-schema
cd db-schema
pip install -e ".[dev]"
pytest
```

## License

MIT — [Bartłomiej Tokarzewski](https://github.com/tokarzewski)
