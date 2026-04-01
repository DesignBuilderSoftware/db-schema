from designbuilder_schema.utils import load_model
from designbuilder_schema.tables import Tables
from dataframe_extension import add_extension

filepath = r"samples/models/Shoebox10x10.xml"
model = load_model(filepath)

site = model.site
if site is None:
    raise ValueError("Model must have a site defined")

tables = site.tables
if tables is not None:
    glazing_table = tables.get_table_by_name("Glazing")

    # Access the "Id" field using getattr since it's a dynamic attribute
    id_values: list[str] = getattr(glazing_table, "Id")
    print(id_values[0])

    add_extension()

    dataframe = getattr(glazing_table, "to_dataframe")()
    dataframe.loc[0, "Id"] = "9"
    getattr(glazing_table, "from_dataframe")(dataframe)

    print(getattr(glazing_table[0], "Id"))
