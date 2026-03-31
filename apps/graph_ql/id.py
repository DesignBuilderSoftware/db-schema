from strawberry.experimental.pydantic import type as strawberry_type
from designbuilder_schema.id import ObjectIDs


@strawberry_type(model=ObjectIDs)
class ObjectIDsType:
    handle: int
    buildingHandle: int
    buildingBlockHandle: int
    zoneHandle: int
    surfaceIndex: int
    openingIndex: int
