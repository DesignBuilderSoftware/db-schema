import pandas as pd
from designbuilder_schema.tables import Table


def to_dataframe(self: Table) -> pd.DataFrame:
    return pd.DataFrame(self.Row, columns=self.FieldName)


def from_dataframe(self: Table, dataframe: pd.DataFrame) -> None:
    def compose_row(row) -> str:
        return "#" + str(row[0]) + " #" + " #".join(str(item) for item in row[1:])

    self.Row = [compose_row(row[1:]) for row in dataframe.itertuples()]


def add_extension():
    Table.to_dataframe = to_dataframe
    Table.from_dataframe = from_dataframe
