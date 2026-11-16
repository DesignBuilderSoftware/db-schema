# User guide

`dsbxml` loads DesignBuilder XML (dsbXML) files into typed Pydantic models,
lets you read and change them in Python, and writes them back as XML.

Every Python example in this guide is run by the test suite
(`dsbxml/tests/test_usage_guide.py`) against a real DesignBuilder model
saved as `building.xml`, so the examples stay in step with the package.
The examples build on each other: the pages run in the order listed
below, and later pages use `model`, `building` and `zone` from earlier
ones.

## Installation

```bash
pip install dsbxml
```

## Contents

- [Loading and saving](loading-and-saving.md)
- [Model structure](model-structure.md)
- [Attributes](attributes.md)
- [Geometry](geometry.md)
- [Tables](tables.md)
- [HVAC](hvac.md)
- [Validating against the schema](validation.md)
- [Comparing two models](comparing-models.md)
- [Errors](errors.md)
- [Handles](handles.md)
- [Package imports](package-imports.md)
