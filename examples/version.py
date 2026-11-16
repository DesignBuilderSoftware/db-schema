from dsbxml.utils import load_model

filepath = r".\samples\models\Shoebox261.xml"
model = load_model(filepath)
print(model.version)
