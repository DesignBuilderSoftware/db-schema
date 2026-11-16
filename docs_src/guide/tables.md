# Tables

```python
tables = model.site.tables
print([table.name for table in tables.table])

table = tables.get_table_by_name("TableOfTables")  # KeyError if missing
print(table.field_name, len(table.row))
```
