from designbuilder_schema.base import BaseModel, AlwaysList
from typing import Optional


class NameAttribute(BaseModel):
    """Site and HVAC Attribute"""

    name: str
    text: Optional[str] = None


class KeyAttribute(BaseModel):
    """Non-Site and Non-HVAC Attribute"""

    key: str
    text: str = None


class NameAttributes(BaseModel):
    """Site and HVAC Attributes"""

    Attribute: AlwaysList["NameAttribute"]


class KeyAttributes(BaseModel):
    """Non-Site and Non-HVAC Attribute"""

    Attribute: AlwaysList["KeyAttribute"]


class HVACAttributeList(BaseModel):
    buildingZoneHandle: str
    Attributes: "NameAttributes"


class ZoneComponentAttributeList(BaseModel):
    HVACAttributeList: AlwaysList["HVACAttributeList"]
