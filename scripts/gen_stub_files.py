import subprocess

from dsbxml.tables import Table
from dsbxml.utils import load_model

# Run stubgen first
subprocess.run(["stubgen", "./dsbxml/tables.py"], check=True)

# Load and process the model
filepath = (
    r"C:\GitHub\dsbxml\samples\models\Shoebox10x10-All.xml"
)

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


with open("dsbxml/tables.pyi", "w") as f1:
    with open("out/dsbxml/tables.pyi") as f2:
        f1.write(f2.read())
        f1.write("\n")

    for table in tables.Table:
        f1.write(generate_stub(table))


# TODO remove out folder with all contents
