from dsbxml.utils import load_model

filepath = r".\samples\2026.1.0.013\Shoebox261.xml"

model = load_model(filepath)

tables = model.site.tables
glazing_table = tables.get_table_by_name("Glazing")  # KeyError if missing

# Each row is one string of "#"-prefixed values, in field_name order.
# This split assumes no value contains "#".
print(glazing_table.field_name[:5])


def read_row(row: str) -> list[str]:
    return [value.strip() for value in row.split("#")[1:]]


def write_row(values: list[str]) -> str:
    return "#" + " #".join(values)


id_column = glazing_table.field_name.index("Id")
print([read_row(row)[id_column] for row in glazing_table.row])  # every Id

values = read_row(glazing_table.row[0])
print(values[id_column])  # Id of the first row

values[id_column] = "123"  # set the Id of the first row
glazing_table.row[0] = write_row(values)
print(read_row(glazing_table.row[0])[id_column])
