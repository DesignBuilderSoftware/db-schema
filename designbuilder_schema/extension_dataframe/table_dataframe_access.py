from designbuilder_schema.utils import load_model
from designbuilder_schema.tables import Tables
from dataframe_extension import add_extension

filepath = r"samples/models/Shoebox10x10.xml"
model = load_model(filepath)

site = model.site
tables = site.tables
if tables is not None:
    glazing_table = tables.get_table_by_name("Glazing")

    print(glazing_table.Id[0])

    add_extension()

    dataframe = glazing_table.to_dataframe()
    dataframe.loc[0, "Id"] = "9"
    glazing_table.from_dataframe(dataframe)

    print(glazing_table[0].Id)
