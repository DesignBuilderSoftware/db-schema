from dsbxml.utils import load_model

filepath = r".\samples\2026.1.0.013\Shoebox261.xml"
model = load_model(filepath)
print(model.version)
