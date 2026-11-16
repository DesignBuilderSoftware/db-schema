from dsbxml.utils import load_model, save_model

filepath = r".\samples\8.0.0.058\DetailedHVAC.xml"
model = load_model(filepath)
save_model(model, r".\samples\8.0.0.058\DetailedHVAC_resaved.xml")
