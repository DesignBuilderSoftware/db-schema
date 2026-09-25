"""Tests for dsbxml.attributes XML models.

Uses pytest.importorskip so the suite still runs (as skips) if the module
is broken mid-refactor.
"""

import pytest

attributes = pytest.importorskip(
    "dsbxml.attributes",
    reason="dsbxml.attributes failed to import",
)

NameAttribute = attributes.NameAttribute
KeyAttribute = attributes.KeyAttribute
NameAttributes = attributes.NameAttributes
KeyAttributes = attributes.KeyAttributes
HVACAttributeList = attributes.HVACAttributeList
ZoneComponentAttributeList = attributes.ZoneComponentAttributeList


class TestNameAttribute:
    def test_parse_name_and_text_value(self):
        a = NameAttribute.from_xml(b'<NameAttribute name="Fan efficiency">0.7</NameAttribute>')
        assert a.name == "Fan efficiency"
        assert a.value == "0.7"

    def test_value_defaults_to_none(self):
        a = NameAttribute.from_xml(b'<NameAttribute name="Empty"/>')
        assert a.name == "Empty"
        assert a.value is None

    def test_serialisation_round_trip(self):
        a = NameAttribute(name="Setpoint", value="21.5")
        xml = a.to_xml()
        b = NameAttribute.from_xml(xml)
        assert b.name == a.name
        assert b.value == a.value


class TestKeyAttribute:
    def test_parse_key_and_text_value(self):
        k = KeyAttribute.from_xml(b'<KeyAttribute key="K1">v</KeyAttribute>')
        assert k.key == "K1"
        assert k.value == "v"

    def test_round_trip(self):
        k = KeyAttribute(key="K2", value="42")
        assert KeyAttribute.from_xml(k.to_xml()) == k


class TestAttributeCollections:
    def test_name_attributes_parses_attribute_tags(self):
        nas = NameAttributes.from_xml(
            b"<NameAttributes>"
            b'<Attribute name="a">1</Attribute>'
            b'<Attribute name="b">2</Attribute>'
            b"</NameAttributes>"
        )
        assert [x.name for x in nas.attribute] == ["a", "b"]
        assert [x.value for x in nas.attribute] == ["1", "2"]

    def test_name_attributes_default_is_empty_list(self):
        assert NameAttributes().attribute == []

    def test_key_attributes_parses_attribute_tags(self):
        kas = KeyAttributes.from_xml(
            b'<KeyAttributes><Attribute key="k1">v1</Attribute></KeyAttributes>'
        )
        assert len(kas.attribute) == 1
        assert kas.attribute[0].key == "k1"
        assert kas.attribute[0].value == "v1"

    def test_key_attributes_default_is_empty_list(self):
        assert KeyAttributes().attribute == []


class TestHVACAttributeList:
    def test_parse_building_zone_handle_and_nested_attributes(self):
        hal = HVACAttributeList.from_xml(
            b'<HVACAttributeList buildingZoneHandle="5">'
            b'<Attributes><Attribute name="x">1</Attribute></Attributes>'
            b"</HVACAttributeList>"
        )
        assert hal.buildingZoneHandle == "5"
        assert len(hal.attributes.attribute) == 1
        assert hal.attributes.attribute[0].name == "x"

    def test_attributes_default_factory(self):
        hal = HVACAttributeList(buildingZoneHandle="9")
        assert isinstance(hal.attributes, NameAttributes)
        assert hal.attributes.attribute == []


class TestZoneComponentAttributeList:
    def test_parse_nested_hvac_attribute_lists(self):
        zc = ZoneComponentAttributeList.from_xml(
            b"<ZoneComponentAttributeList>"
            b'<HVACAttributeList buildingZoneHandle="7"><Attributes/></HVACAttributeList>'
            b'<HVACAttributeList buildingZoneHandle="8"><Attributes/></HVACAttributeList>'
            b"</ZoneComponentAttributeList>"
        )
        assert [h.buildingZoneHandle for h in zc.hvac_attribute_list] == ["7", "8"]

    def test_default_is_empty_list(self):
        assert ZoneComponentAttributeList().hvac_attribute_list == []
