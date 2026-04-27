from __future__ import annotations

from pydantic_xml import attr, element

from db_schema.base import BaseModel


class Table(BaseModel):
    name: str = attr()
    numberOfFields: int = attr()
    category: list[str] = element(tag="Category", default_factory=list)
    field_name: list[str] = element(tag="FieldName")
    row: list[str] = element(tag="Row", default_factory=list)


class Tables(BaseModel):
    table: list[Table] = element(tag="Table", default_factory=list)

    def get_table_by_name(self, name: str) -> Table:
        table_dict = {t.name: t for t in self.table}
        if name not in table_dict:
            raise KeyError(f"Table '{name}' not found")
        return table_dict[name]
