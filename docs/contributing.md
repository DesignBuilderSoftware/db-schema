# Contributing

Contributions are welcome! Here's how to help:

## Documentation

Documentation is auto-generated from docstrings. Make sure your models have clear Google-style docstrings:

```python
class MyModel(BaseModel):
    """A detailed description of the model.

    This model does something important.

    Attributes:
        field_name: Description of the field
    """
    field_name: str
```

## Building Docs Locally

```bash
pip install mkdocs mkdocs-material mkdocstrings[python]
mkdocs serve
```

Then visit `http://localhost:8000` to preview.
