from strawberry.experimental.pydantic import type as strawberry_type
from designbuilder_schema.attributes import *


@strawberry_type(model=NameAttribute)
class NameAttributeType:
    name: str
    text: Optional[str] = None


@strawberry_type(model=NameAttributes)
class NameAttributesType:
    Attribute: list[NameAttributeType]


@strawberry_type(model=KeyAttribute, all_fields=True)
class KeyAttributeType:
    pass


@strawberry_type(model=KeyAttributes, all_fields=True)
class KeyAttributesType:
    pass


@strawberry_type(model=HVACAttributeList, all_fields=True)
class HVACAttributeListType:
    pass


@strawberry_type(model=ZoneComponentAttributeList, all_fields=True)
class ZoneComponentAttributeListType:
    pass
