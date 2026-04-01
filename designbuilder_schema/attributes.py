
from designbuilder_schema.base import BaseModel
from pydantic_xml import attr, element
from typing import Optional, List


class NameAttribute(BaseModel):
    """A single named attribute for sites and HVAC components.

    Represents a key-value pair with a name identifier.

    Attributes:
        name: Name of the attribute
        value: Value of the attribute
    """

    name: str = attr()
    value: Optional[str] = None


class KeyAttribute(BaseModel):
    """A single keyed attribute for buildings and surfaces.

    Represents a key-value pair with a key identifier.

    Attributes:
        key: Key identifier for the attribute
        value: Value of the attribute
    """

    key: str = attr()
    value: Optional[str] = None


class NameAttributes(BaseModel):
    """Collection of named attributes for sites and HVAC components.

    Container for multiple named attributes.

    Attributes:
        attribute: List of named attributes
    """

    attribute: List["NameAttribute"] = element(tag="Attribute", default_factory=list)


class KeyAttributes(BaseModel):
    """Collection of keyed attributes for buildings and surfaces.

    Container for multiple keyed attributes.

    Attributes:
        attribute: List of keyed attributes
    """

    attribute: List["KeyAttribute"] = element(tag="Attribute", default_factory=list)


class HVACAttributeList(BaseModel):
    """Attributes for a single HVAC zone component.

    Links attributes to a specific building zone in an HVAC context.

    Attributes:
        buildingZoneHandle: Reference to the building/zone
        attributes: Named attributes for this zone component
    """
    buildingZoneHandle: str = attr()
    attributes: "NameAttributes" = element(default_factory=lambda: NameAttributes())


class ZoneComponentAttributeList(BaseModel):
    """Collection of HVAC zone component attribute lists.

    Container for multiple zone-specific HVAC attribute lists.

    Attributes:
        hvac_attribute_list: List of zone component attributes
    """
    hvac_attribute_list: List["HVACAttributeList"] = element(tag="HVACAttributeList", default_factory=list)
