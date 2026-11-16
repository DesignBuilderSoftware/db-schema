# db-schema

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![PyPI](https://img.shields.io/pypi/v/dsbxml)](https://pypi.org/project/dsbxml/)
[![Tests](https://github.com/DesignBuilderSoftware/db-schema/actions/workflows/run-tests.yml/badge.svg)](https://github.com/DesignBuilderSoftware/db-schema/actions/workflows/run-tests.yml)

Python package for reading, editing, and writing DesignBuilder XML (dsbXML) files using Pydantic and pydantic-xml. It also ships `DesignBuilder.xsd`, the schema that defines the format.

Documentation: <https://designbuildersoftware.github.io/db-schema/> (user guide, schema element reference, API reference).

## Install

```bash
pip install dsbxml
```

## Quick Start

```python
from dsbxml import load_model, save_model

dsb = load_model("building.xml")
dsb.name = "Updated Building"
save_model(dsb, "building_updated.xml")
```

## Features

- Type-safe XML handling via Pydantic v2
- Models for the whole dsbXML tree, including detailed HVAC
- Load and save XML; validate against the bundled `DesignBuilder.xsd` (`dsbxml.utils.validate_against_xsd`)
- Semantic diff of two models (`dsbxml.diff_models`)

See the [user guide](https://designbuildersoftware.github.io/db-schema/guide/) for worked examples
(source in [`docs_src/guide/`](docs_src/guide)).

## Data Model

```
dsbXML
└── Site
    ├── Attributes / Tables / AssemblyLibrary
    └── Buildings
        └── Building
            ├── BuildingBlocks
            │   └── BuildingBlock
            │       └── Zones
            │           └── Zone
            │               └── Body
            │                   └── Surfaces
            │                       └── Surface
            │                           └── Openings / Adjacencies
            └── HVACNetwork
                └── HVACLoops / HVACZoneGroups
```

## Development

```bash
git clone https://github.com/DesignBuilderSoftware/db-schema
cd db-schema
uv sync --extra dev
uv run pytest                    # tests (about 8 minutes: they round-trip every sample model)
uv run ruff check dsbxml         # lint, as in CI
uv run pylint dsbxml
uv run mkdocs build --strict -d site   # docs, into an untracked folder
```

The docs sources are in `docs_src/`; the schema element reference page is generated from `dsbxml/DesignBuilder.xsd` at build time by `scripts/docs_xsd_reference.py`.

## License

MIT — [DesignBuilder](https://github.com/DesignBuilderSoftware), [Bartłomiej Tokarzewski](https://github.com/tokarzewski)
