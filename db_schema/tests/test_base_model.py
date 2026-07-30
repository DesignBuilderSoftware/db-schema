"""Tests for db_schema.base.BaseModel configuration behaviour.

BaseModel promises: unordered element search, whitespace stripping,
assignment validation and population by field name. These are exercised
through small concrete models from the package.
"""

import pytest
from pydantic import ValidationError

base = pytest.importorskip("db_schema.base", reason="db_schema.base failed to import")
attributes = pytest.importorskip(
    "db_schema.attributes", reason="db_schema.attributes failed to import"
)
tables_mod = pytest.importorskip(
    "db_schema.tables", reason="db_schema.tables failed to import"
)

BaseModel = base.BaseModel
NameAttribute = attributes.NameAttribute
Table = tables_mod.Table


def test_str_strip_whitespace_on_text_content():
    a = NameAttribute.from_xml(
        b'<NameAttribute name="  padded  ">  0.7  </NameAttribute>'
    )
    assert a.name == "padded"
    assert a.value == "0.7"


def test_unordered_search_mode_configured():
    from pydantic_xml.model import SearchMode

    assert BaseModel.__xml_search_mode__ == SearchMode.UNORDERED


def test_validate_assignment_rejects_bad_type():
    t = Table(name="T", numberOfFields=1)
    with pytest.raises(ValidationError):
        t.numberOfFields = "not-an-int"


def test_validate_assignment_accepts_coercible_value():
    t = Table(name="T", numberOfFields=1)
    t.numberOfFields = "3"
    assert t.numberOfFields == 3


def test_populate_by_name():
    t = Table(name="T", numberOfFields=2)
    assert t.name == "T"
    assert t.numberOfFields == 2


def test_subclasses_share_config():
    # All package models derive from BaseModel, so they inherit the config.
    assert issubclass(NameAttribute, BaseModel)
    assert issubclass(Table, BaseModel)
    assert NameAttribute.model_config.get("validate_assignment") is True
    assert NameAttribute.model_config.get("str_strip_whitespace") is True
