import subprocess
from designbuilder_schema.tables import Table
from designbuilder_schema.utils import load_model

# Run stubgen first
subprocess.run(["stubgen", "./designbuilder_schema/tables.py"], check=True)

# Load and process the model
filepath = r"C:\GitHub\designbuilder_schema\samples\models\Shoebox10x10-All.xml"

db_xml = load_model(filepath)
tables = db_xml.Site.Tables


def unique_fields(fields):
    seen = set()
    seen_add = seen.add
    return [x for x in fields if not (x in seen or seen_add(x))]


def generate_stub(table: Table) -> str:
    stub = f"class {table.name}(Table):\n"

    for field in unique_fields(table.FieldName):
        stub += f"    {field}: ...\n"
    stub += "\n"

    return stub


with open("designbuilder_schema/tables.pyi", "w") as f1:
    with open("out/designbuilder_schema/tables.pyi") as f2:
        f1.write(f2.read())
        f1.write("\n")

    for table in tables.Table:
        f1.write(generate_stub(table))


# TODO remove out folder with all contents
