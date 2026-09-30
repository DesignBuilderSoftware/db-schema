"""A loaded model must be written back as XML that the schema accepts.

Covers the round-trip fixes in base.py, core.py and hvac/components.py:
ObjectIDs handles are attributes, Surface.defaultOpenings has its real casing,
floats never use an exponent (xs:decimal has none), required-but-empty elements
are kept, unset optionals are not written, and HVAC component children follow
the schema's order.
"""

import functools
import re
from pathlib import Path

import pytest
from lxml import etree

from dsbxml.utils import load_model

test_dir = Path(__file__).parent
repo_root = test_dir.parent.parent
xsd_path = test_dir.parent / "DesignBuilder.xsd"
sample_files = sorted((repo_root / "samples" / "models_dhvac").glob("*.xml"))


@pytest.fixture(scope="module")
def xsd_schema():
    return etree.XMLSchema(etree.parse(str(xsd_path)))


def _to_bytes(model) -> bytes:
    xml = model.to_xml()
    return xml if isinstance(xml, bytes) else xml.encode("utf-8")


@functools.lru_cache(maxsize=None)
def _round_trip(filepath: Path) -> bytes:
    return _to_bytes(load_model(str(filepath)))


@pytest.mark.parametrize("filepath", sample_files, ids=lambda p: p.name)
def test_round_trip_output_validates_against_xsd(filepath, xsd_schema):
    if not xsd_schema.validate(etree.parse(str(filepath))):
        pytest.skip("the source file itself does not validate")
    document = etree.fromstring(_round_trip(filepath)).getroottree()
    if not xsd_schema.validate(document):
        errors = "\n".join(e.message for e in list(xsd_schema.error_log)[:5])
        pytest.fail(f"round-trip output is invalid:\n{errors}")


# --- The individual fixes ---------------------------------------------------


def test_object_ids_handle_is_a_real_attribute():
    from dsbxml.id import ObjectIDs

    ids = ObjectIDs.from_xml(
        b'<ObjectIDs handle="42" buildingHandle="1" buildingBlockHandle="2" '
        b'zoneHandle="3" surfaceIndex="4" openingIndex="5"/>'
    )
    assert ids.handle == 42
    written = etree.fromstring(ids.to_xml())
    assert written.get("handle") == "42"
    assert not (written.text or "").strip()


def test_loaded_handles_come_from_the_file(xsd_schema):
    """Handles used to be regenerated on load, so they never matched the file.

    Checked on the building geometry, where handles identify real objects.
    """
    geometry = {"Building", "BuildingBlock", "Zone", "Surface", "Opening", "Adjacency"}

    def handles(root):
        return [el.get("handle") for el in root.iter("ObjectIDs")
                if el.getparent().tag in geometry]

    sample = sample_files[0]
    source = etree.parse(str(sample)).getroot()
    written = etree.fromstring(_round_trip(sample))
    assert handles(source)
    assert handles(source) == handles(written)


def test_surface_default_openings_keeps_its_casing():
    sample = sample_files[0]
    source = etree.parse(str(sample)).getroot()
    written = etree.fromstring(_round_trip(sample))
    wanted = [s.get("defaultOpenings") for s in source.iter("Surface")]
    assert wanted and all(v is not None for v in wanted)
    assert [s.get("defaultOpenings") for s in written.iter("Surface")] == wanted
    assert not any(s.get("defaultopenings") for s in written.iter("Surface"))


def test_floats_are_written_without_an_exponent():
    sample = sample_files[0]
    written = etree.fromstring(_round_trip(sample))
    exponent = re.compile(r"^-?\d+(\.\d+)?[eE][+-]?\d+$")
    for el in written.iter("Surface"):
        for name in ("area", "alpha", "phi", "thickness"):
            assert not exponent.match(el.get(name, "")), (name, el.get(name))


def test_small_floats_format_as_plain_decimals():
    from dsbxml.base import _format_decimal

    assert _format_decimal(4.956e-17) == "0.00000000000000004956"
    assert _format_decimal(3.14) == "3.14"
    assert _format_decimal(-2.2222222084825e-07) == "-0.00000022222222084825"
    assert _format_decimal(12345678901234567890.0) == "12345678901234567000"


def test_required_empty_elements_are_kept():
    """<HoleIndices></HoleIndices> is required by the schema even when empty."""
    sample = sample_files[0]
    written = etree.fromstring(_round_trip(sample))
    surfaces = list(written.iter("Surface"))
    assert surfaces
    assert all(s.find("HoleIndices") is not None for s in surfaces)
    assert all(s.find("Openings") is not None for s in surfaces)


def test_unset_optional_values_are_not_written():
    sample = sample_files[0]
    written = etree.fromstring(_round_trip(sample))
    # No empty numeric tags and no empty "type" attributes.
    for tag in ("Width", "Height", "MixingBoxWidth"):
        assert all((el.text or "").strip() for el in written.iter(tag)), tag
    assert not [el for el in written.iter() if el.get("type") == ""]


def test_hvac_components_keep_the_schema_child_order():
    sample = sample_files[0]
    written = etree.fromstring(_round_trip(sample))
    for component in written.iter("HVACComponent"):
        tags = [c.tag for c in component]
        if "ImageRectangle" in tags and "Attributes" in tags and "ZoneComponentAttributeList" in tags:
            assert tags.index("Attributes") < tags.index("ZoneComponentAttributeList")
        if "Origin" in tags and "Width" in tags:
            assert tags.index("Width") < tags.index("Origin")


def test_validate_against_xsd_accepts_a_round_tripped_model():
    from dsbxml.utils import validate_against_xsd

    sample = next(f for f in sample_files if not validate_against_xsd(f))
    assert validate_against_xsd(load_model(str(sample))) == []


def test_validate_against_xsd_reports_problems():
    from dsbxml.utils import validate_against_xsd

    errors = validate_against_xsd(b"<dsbXML><Nonsense/></dsbXML>")
    assert errors and all(isinstance(message, str) for message in errors)
