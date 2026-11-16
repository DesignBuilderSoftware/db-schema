# Validating against the schema

`validate_against_xsd` checks a loaded model, a file path or XML bytes
against the `DesignBuilder.xsd` bundled with the package and returns the
error messages; an empty list means the XML is valid. For a loaded model
this tells you whether saving it would produce a file the schema accepts.

```python
from dsbxml.utils import validate_against_xsd

errors = validate_against_xsd(model)
for message in errors:
    print(message)
```

Loading is more lenient than the schema: some files that do not validate
still load, so validate explicitly when that matters.

Known issue: a building without detailed HVAC has an empty
`<HVACNetwork></HVACNetwork>`, which the model writes back with an
`<ObjectIDs>` child. The schema does not allow that, so such models
report an `ObjectIDs` error after loading even though the source file was
valid.
