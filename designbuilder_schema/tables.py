"""
tables.py
====================================
The tables module of the designbuilder_schema
"""

from pydantic import field_validator, field_serializer, BaseModel as PydanticBaseModel
from pydantic_xml import attr, element
from typing import Any, List, Optional
from designbuilder_schema.base import BaseModel


class TableRow(BaseModel):
    """Single row of data in a table - XML compatible"""

    cells: List[str] = element(tag="Cell")

    def __getitem__(self, index: int) -> str:
        return self.cells[index]

    def __setitem__(self, index: int, value: str) -> None:
        self.cells[index] = value

    def __iter__(self):
        return iter(self.cells)

    def __len__(self) -> int:
        return len(self.cells)


class Table(BaseModel):
    """Table data container - now fully XML-compatible"""

    name: str = attr()
    numberOfFields: int = attr()
    category: Optional[List[str]] = element(tag="Category", default=None)
    field_name: List[str] = element(tag="FieldName")
    rows: Optional[List[TableRow]] = element(tag="Row", default=None)

    @field_validator("category", mode="before")
    def parse_category(cls, value: Optional[str | List]) -> Optional[List[str]]:
        if value is None:
            return None
        if isinstance(value, str):
            return [value]
        return value

    def __getitem__(self, index: int) -> "TableRow":
        """Get a specific row by index"""
        if self.rows is None or index >= len(self.rows):
            raise IndexError("Table row index out of range")
        return self.rows[index]

    def __getattr__(self, name: str) -> List[str]:
        """Get all values for a specific field by name"""
        try:
            field_index = self.field_name.index(name)
        except ValueError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

        if self.rows is None:
            return []

        return [row.cells[field_index] for row in self.rows]

    def __setattr__(self, name: str, value: Any) -> None:
        """Set values for a specific field by name"""
        # Let Pydantic handle special attributes
        if name in self.__dict__ or name.startswith("_"):
            super().__setattr__(name, value)
            return

        # Handle field_name and rows specially
        if name in ("field_name", "rows", "name", "numberOfFields", "category"):
            super().__setattr__(name, value)
            return

        # Handle custom field setting
        if self.rows is not None and name in self.field_name:
            field_index = self.field_name.index(name)
            if isinstance(value, list) and len(value) == len(self.rows):
                for i, row in enumerate(self.rows):
                    row.cells[field_index] = value[i]
            else:
                raise ValueError(f"Value must be a list with {len(self.rows)} elements")
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )


class Tables(BaseModel):
    """Tables container - now fully XML-compatible"""

    table: List[Table] = element(tag="Table", default_factory=list)

    def get_table_by_name(self, name: str) -> Table:
        """Get a table by its name"""
        table_dict = {t.name: t for t in self.table}
        if name not in table_dict:
            raise KeyError(f"Table '{name}' not found")
        return table_dict[name]


# Legacy compatibility class - for code that expects TableItem
class TableItem(PydanticBaseModel):
    """Helper class for accessing table row data like a dictionary"""

    field_name: List[str]
    row: List[Any]

    def __getattr__(self, name: str) -> Any:
        if name in self.field_name:
            i = self.field_name.index(name)
            return self.row[i]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__dict__:
            super().__setattr__(name, value)
        elif name in self.field_name:
            index = self.field_name.index(name)
            self.row[index] = value
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
