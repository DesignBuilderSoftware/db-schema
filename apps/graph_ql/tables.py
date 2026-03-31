from strawberry.experimental.pydantic import type as strawberry_type
from designbuilder_schema.tables import *
from strawberry import auto


@strawberry_type(model=Table)
class TableType:
    name: auto
    numberOfFields: auto
    Category: auto
    FieldName: auto
    Row: auto = None


@strawberry_type(model=Tables)
class TablesType:
    Table: list[TableType]
