import pandas as pd
from typing import TYPE_CHECKING
from designbuilder_schema.tables import Table

if TYPE_CHECKING:
    from typing import Any


def to_dataframe(self: Table) -> pd.DataFrame:
    if self.rows is None:
        return pd.DataFrame(columns=self.field_name)
    return pd.DataFrame([row.cells for row in self.rows], columns=self.field_name)


def from_dataframe(self: Table, dataframe: pd.DataFrame) -> None:
    from designbuilder_schema.tables import TableRow

    def compose_row(row: Any) -> str:
        return ";".join(str(item) for item in row)

    self.rows = [
        TableRow(cells=compose_row(row).split(";")) for _, row in dataframe.iterrows()
    ]


def add_extension() -> None:
    setattr(Table, "to_dataframe", to_dataframe)
    setattr(Table, "from_dataframe", from_dataframe)
