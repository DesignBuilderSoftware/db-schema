"""Tests for dsbxml.tables (Table / Tables XML models)."""

import pytest

tables_mod = pytest.importorskip(
    "dsbxml.tables",
    reason="dsbxml.tables failed to import",
)

Table = tables_mod.Table
Tables = tables_mod.Tables

SAMPLE_XML = b"""<Tables>
  <Table name="T1" numberOfFields="2">
    <Category>c1</Category>
    <FieldName>f1</FieldName>
    <FieldName>f2</FieldName>
    <Row>r1</Row>
    <Row>r2</Row>
  </Table>
  <Table name="T2" numberOfFields="1">
    <FieldName>only</FieldName>
  </Table>
</Tables>"""


class TestTableParsing:
    def test_parse_attributes_and_elements(self):
        t = Tables.from_xml(SAMPLE_XML)
        tab = t.table[0]
        assert tab.name == "T1"
        assert tab.numberOfFields == 2
        assert tab.category == ["c1"]
        assert tab.field_name == ["f1", "f2"]
        assert tab.row == ["r1", "r2"]

    def test_missing_child_elements_default_to_empty_lists(self):
        t = Tables.from_xml(SAMPLE_XML)
        tab = t.table[1]
        assert tab.category == []
        assert tab.row == []
        assert tab.field_name == ["only"]

    def test_number_of_fields_coerced_to_int(self):
        t = Tables.from_xml(SAMPLE_XML)
        assert isinstance(t.table[0].numberOfFields, int)

    def test_elements_parsed_regardless_of_document_order(self):
        # BaseModel uses SearchMode.UNORDERED: tags may appear in any order.
        t = Tables.from_xml(
            b'<Tables><Table name="T" numberOfFields="1">'
            b"<Row>r</Row><FieldName>f</FieldName><Category>c</Category>"
            b"</Table></Tables>"
        )
        tab = t.table[0]
        assert tab.category == ["c"]
        assert tab.field_name == ["f"]
        assert tab.row == ["r"]

    def test_round_trip(self):
        t = Tables.from_xml(SAMPLE_XML)
        again = Tables.from_xml(t.to_xml())
        assert again == t


class TestGetTableByName:
    def test_returns_named_table(self):
        t = Tables.from_xml(SAMPLE_XML)
        assert t.get_table_by_name("T2").name == "T2"

    def test_unknown_name_raises_key_error(self):
        t = Tables.from_xml(SAMPLE_XML)
        with pytest.raises(KeyError, match="Nope"):
            t.get_table_by_name("Nope")

    def test_empty_tables_raises_key_error(self):
        with pytest.raises(KeyError):
            Tables().get_table_by_name("anything")
