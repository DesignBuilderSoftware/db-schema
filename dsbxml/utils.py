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


@lru_cache(maxsize=1)
def _xsd_schema():
    from lxml import etree

    return etree.XMLSchema(etree.parse(str(Path(__file__).with_name("DesignBuilder.xsd"))))


def validate_against_xsd(source) -> list[str]:
    """Check a model, an XML file path or XML bytes against DesignBuilder.xsd.

    Returns the schema's error messages; an empty list means the XML is valid.
    A loaded model is serialised first, so this also tells whether saving it
    would produce a file DesignBuilder's schema accepts.
    """
    from lxml import etree

    if isinstance(source, (str, Path)):
        document = etree.parse(str(source))
    else:
        xml = source if isinstance(source, bytes) else source.to_xml()
        xml = xml if isinstance(xml, bytes) else xml.encode("utf-8")
        document = etree.fromstring(xml).getroottree()
    schema = _xsd_schema()
    schema.validate(document)
    # lxml's error_log is a C extension type pylint cannot see is iterable.
    return [error.message for error in schema.error_log]  # pylint: disable=not-an-iterable
