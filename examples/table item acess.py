from designbuilder_schema.utils import load_model
from designbuilder_schema.tables import *

filepath = r"samples\models\Shoebox10x10.xml"

model = load_model(filepath)

site = model.Site
tables = site.Tables
glazing_table = Tables.get_table_by_name(tables, "Glazing")  # type: Glazing
# print(glazing_table.Id) # returns vector

glazing_item = glazing_table[0]  # type: Glazing
print(glazing_item.Id)  # returns 1 value

glazing_item.Id = 123  # sets 1 value
print(glazing_item.Id)  # returns 1 value
