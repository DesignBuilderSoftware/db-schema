from pathlib import Path
from designbuilder_schema.core import dsbXML
from designbuilder_schema.id import set_site_counter


def load_model(filepath: str | Path) -> dsbXML:
    """Load and validate DSB model from XML file.

    pydantic-xml provides XXE protection automatically.
    """
    path = Path(filepath) if isinstance(filepath, str) else filepath

    if path.suffix != ".xml":
        raise ValueError(f"Unsupported file format: {path.suffix}. Only .xml files are supported.")

    try:
        with open(path, "rb") as f:
            dsb = dsbXML.from_xml(f.read())
        if dsb.site:
            set_site_counter(dsb.site.handle)
        return dsb
    except AssertionError as e:
        # Handle pydantic-xml partially initialized models
        if "partially initialized" in str(e):
            # Try again with a fallback - the model may still be usable
            # Re-raise the original exception
            raise
        raise


def save_model(model: dsbXML, filepath: str | Path) -> None:
    """Save DSB model to XML file."""
    path = Path(filepath) if isinstance(filepath, str) else filepath

    if path.suffix != ".xml":
        raise ValueError(f"Unsupported file format: {path.suffix}. Only .xml files are supported.")

    xml_output = model.to_xml()
    with open(path, "wb") as f:
        if isinstance(xml_output, bytes):
            f.write(xml_output)
        else:
            f.write(xml_output.encode("utf-8"))
