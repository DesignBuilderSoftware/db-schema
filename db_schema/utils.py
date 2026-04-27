from functools import lru_cache
from pathlib import Path

from db_schema.id import set_site_counter


def _get_dsbXML():
    """Import dsbXML through the package to trigger lazy loading and model rebuilds"""
    import db_schema

    return db_schema.dsbXML


@lru_cache(maxsize=32)
def _cached_load_model_internal(filepath: str):
    path = Path(filepath)
    dsbXML = _get_dsbXML()
    with open(path, "rb") as f:
        return dsbXML.from_xml(f.read())


def load_model(filepath: str | Path, use_cache: bool = True):
    path = Path(filepath) if isinstance(filepath, str) else filepath

    if path.suffix != ".xml":
        raise ValueError(
            f"Unsupported file format: {path.suffix}. Only .xml files are supported."
        )

    try:
        dsbXML = _get_dsbXML()
        if use_cache:
            dsb = _cached_load_model_internal(str(path.resolve()))
        else:
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


def clear_model_cache():
    _cached_load_model_internal.cache_clear()


def save_model(model, filepath: str | Path) -> None:
    path = Path(filepath) if isinstance(filepath, str) else filepath

    if path.suffix != ".xml":
        raise ValueError(
            f"Unsupported file format: {path.suffix}. Only .xml files are supported."
        )

    xml_output = model.to_xml()
    with open(path, "wb") as f:
        if isinstance(xml_output, bytes):
            f.write(xml_output)
        else:
            f.write(xml_output.encode("utf-8"))
