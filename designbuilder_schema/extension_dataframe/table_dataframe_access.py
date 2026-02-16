from designbuilder_schema.utils import load_model
from designbuilder_schema.tables import *
from dataframe_extension import add_extension


filepath = r"samples\models\Shoebox10x10.xml"
model = load_model(filepath)

site = model.Site
tables = site.Tables
glazing_table = Tables.get_table_by_name(tables, "Glazing")  # type: Glazing

print(glazing_table.Id[0])

add_extension()

dataframe = glazing_table.to_dataframe()
dataframe.loc[0, "Id"] = "9"
glazing_table.from_dataframe(dataframe)

print(glazing_table[0].Id)
