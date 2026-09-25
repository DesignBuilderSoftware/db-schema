from functools import lru_cache
from pathlib import Path

from dsbxml.id import set_site_counter


def _get_dsbXML():
    """Import dsbXML through the package to trigger lazy loading and model rebuilds"""
    import dsbxml

    return dsbxml.dsbXML


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

    dsbXML = _get_dsbXML()
    if use_cache:
        dsb = _cached_load_model_internal(str(path.resolve()))
    else:
        with open(path, "rb") as f:
            dsb = dsbXML.from_xml(f.read())

    if dsb.site:
        set_site_counter(dsb.site.handle)
    return dsb


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
