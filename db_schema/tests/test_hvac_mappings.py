"""Consistency tests for the HVAC component type mappings.

ZONE_COMPONENT_MAPPING and UNIT_COMPONENT_MAPPING drive runtime recasting
of parsed components; each key must match the class's `type` Literal.
"""

import typing

import pytest

components = pytest.importorskip(
    "db_schema.hvac.components",
    reason="db_schema.hvac.components failed to import",
)
zone_components = pytest.importorskip(
    "db_schema.hvac.zone_components",
    reason="db_schema.hvac.zone_components failed to import",
)
unit_components = pytest.importorskip(
    "db_schema.hvac.unit_components",
    reason="db_schema.hvac.unit_components failed to import",
)

HVACComponent = components.HVACComponent
NoTypeHVACComponent = components.NoTypeHVACComponent
ZONE_COMPONENT_MAPPING = zone_components.ZONE_COMPONENT_MAPPING
UNIT_COMPONENT_MAPPING = unit_components.UNIT_COMPONENT_MAPPING
ZoneElementList = zone_components.ZoneElementList


@pytest.fixture(scope="module", autouse=True)
def _resolve_forward_refs():
    """Touch the lazy package API so model_rebuild() has run for HVAC models."""
    db_schema = pytest.importorskip("db_schema")
    getattr(db_schema, "dsbXML", None)


def _type_literal(cls):
    field = cls.model_fields.get("type")
    if field is None:
        return None
    args = typing.get_args(field.annotation)
    return args[0] if args else field.annotation


@pytest.mark.parametrize(
    "key,cls",
    ZONE_COMPONENT_MAPPING.items(),
    ids=list(ZONE_COMPONENT_MAPPING),
)
def test_zone_mapping_key_matches_type_literal(key, cls):
    assert _type_literal(cls) == key


@pytest.mark.parametrize(
    "key,cls",
    UNIT_COMPONENT_MAPPING.items(),
    ids=list(UNIT_COMPONENT_MAPPING),
)
def test_unit_mapping_key_matches_type_literal(key, cls):
    assert _type_literal(cls) == key


def test_zone_mapping_classes_are_no_type_components():
    for cls in ZONE_COMPONENT_MAPPING.values():
        assert issubclass(cls, NoTypeHVACComponent), cls.__name__


def test_unit_mapping_classes_are_no_type_components():
    for cls in UNIT_COMPONENT_MAPPING.values():
        assert issubclass(cls, NoTypeHVACComponent), cls.__name__


def test_mapping_keys_are_unique_across_mappings():
    # A type string must not map to two different classes.
    overlap = set(ZONE_COMPONENT_MAPPING) & set(UNIT_COMPONENT_MAPPING)
    for key in overlap:
        assert ZONE_COMPONENT_MAPPING[key] is UNIT_COMPONENT_MAPPING[key]


class TestZoneElementListRecast:
    def test_recast_known_type_dict(self):
        result = ZoneElementList.recast_components([{"type": "Zone extract"}])
        assert type(result[0]) is zone_components.ZoneExtract

    def test_recast_unknown_type_falls_back_to_hvac_component(self):
        result = ZoneElementList.recast_components([{"type": "No such thing"}])
        assert type(result[0]) is HVACComponent

    def test_recast_wraps_single_item(self):
        result = ZoneElementList.recast_components({"type": "Zone extract"})
        assert isinstance(result, list)
        assert len(result) == 1

    def test_recast_passes_through_instances(self):
        comp = HVACComponent(type="Extract grille")
        result = ZoneElementList.recast_components([comp])
        assert result[0] is comp

    def test_parse_from_xml_produces_components(self):
        z = ZoneElementList.from_xml(
            b"<ZoneElementList>"
            b'<HVACZoneComponent type="Zone extract"></HVACZoneComponent>'
            b"</ZoneElementList>"
        )
        assert len(z.hvac_zone_component) == 1
        assert z.hvac_zone_component[0].type == "Zone extract"
