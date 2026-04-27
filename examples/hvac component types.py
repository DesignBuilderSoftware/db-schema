from db_schema.hvac.components import HVACComponent
from db_schema.utils import load_model


def report_set(hc: HVACComponent):
    return f"{hc.__class__.__name__} | {hc.type} | {hc.ComponentType} | {hc.ImageRectangle.ImageTextureIndex}"


filepath = r".\samples\models\DetailedHVAC.xml"
model = load_model(filepath)

building = model.Site.Buildings.Building[0]
hvac_network = building.HVACNetwork
hvac_loops = hvac_network.HVACLoops.HVACLoop

hc_set = set()
for loop in hvac_loops:
    for subloop in [loop.SupplySubLoop, loop.DemandSubLoop]:
        for hc in subloop.HVACComponents.HVACComponent:
            hc_set.add(report_set(hc))

for item in hc_set:
    print(item)
