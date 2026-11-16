from dsbxml.hvac.components import HVACComponent
from dsbxml.utils import load_model


def report_set(hc: HVACComponent):
    texture = hc.image_rectangle.imageTextureIndex if hc.image_rectangle else None
    return f"{hc.__class__.__name__} | {hc.type} | {hc.componentType} | {texture}"


filepath = r".\samples\8.0.0.058\DetailedHVAC.xml"
model = load_model(filepath)

building = model.site.buildings.building[0]
hvac_network = building.hvac_network
hvac_loops = hvac_network.hvac_loops.hvac_loop

hc_set = set()
for loop in hvac_loops:
    for subloop in [loop.supply_sub_loop, loop.demand_sub_loop]:
        for hc in subloop.hvac_components.hvac_component:
            hc_set.add(report_set(hc))

for item in sorted(hc_set):
    print(item)
