from __future__ import annotations

from pydantic_xml import attr, element

from db_schema.base import BaseModel


class NameAttribute(BaseModel):
    name: str = attr()
    value: str | None = None


class KeyAttribute(BaseModel):
    key: str = attr()
    value: str | None = None


class NameAttributes(BaseModel):
    attribute: list[NameAttribute] = element(
        tag="Attribute", default_factory=list
    )


class KeyAttributes(BaseModel):
    attribute: list[KeyAttribute] = element(
        tag="Attribute", default_factory=list
    )


class HVACAttributeList(BaseModel):
    buildingZoneHandle: str = attr()
    attributes: NameAttributes = element(
        tag="Attributes", default_factory=lambda: NameAttributes()
    )


class ZoneComponentAttributeList(BaseModel):
    hvac_attribute_list: list[HVACAttributeList] = element(
        tag="HVACAttributeList", default_factory=list
    )
