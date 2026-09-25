from dsbxml.utils import load_model

filepath = r"C:\GitHub\db_schema\samples\models\Shoebox10x10.xml"
model = load_model(filepath)
print(model.version)
