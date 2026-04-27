from db_schema.utils import load_model, save_model

filepath = r".\samples\models\DetailedHVAC.xml"
model = load_model(filepath)
save_model(model, r".\samples\models\DetailedHVAC_resaved.xml")
