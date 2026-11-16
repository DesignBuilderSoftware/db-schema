from dsbxml.utils import load_model


def report_set(hc):
    return f"{hc.__class__.__name__} | {hc.type} | {hc.componentType}"


filepath = r".\samples\8.0.0.058\DetailedHVAC.xml"
model = load_model(filepath)

building = model.site.buildings.building[0]
zone_groups = building.hvac_network.hvac_zone_groups.hvac_zone_group

hzc_set = set()
for zone_group in zone_groups:
    if zone_group.zone_element_list is None:
        continue

    for hc in zone_group.zone_element_list.hvac_zone_component:
        unit_element_list = getattr(hc, "unit_element_list", None)
        if unit_element_list is not None:
            for sub_hc in unit_element_list.hvac_component:
                hzc_set.add(report_set(sub_hc))

for item in sorted(hzc_set):
    print(item)
