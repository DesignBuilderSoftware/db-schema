# Errors

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
