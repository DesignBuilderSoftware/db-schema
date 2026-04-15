from designbuilder_schema.base import BaseModel
from pydantic_xml import attr, element
from typing import Optional, List


class NameAttribute(BaseModel):
    name: str = attr()
    value: Optional[str] = None


class KeyAttribute(BaseModel):
    key: str = attr()
    value: Optional[str] = None


class NameAttributes(BaseModel):
    attribute: List["NameAttribute"] = element(tag="Attribute", default_factory=list)


class KeyAttributes(BaseModel):
    attribute: List["KeyAttribute"] = element(tag="Attribute", default_factory=list)


class HVACAttributeList(BaseModel):
    buildingZoneHandle: str = attr()
    attributes: "NameAttributes" = element(default_factory=lambda: NameAttributes())


class ZoneComponentAttributeList(BaseModel):
    hvac_attribute_list: List["HVACAttributeList"] = element(
        tag="HVACAttributeList", default_factory=list
    )
