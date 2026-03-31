from designbuilder_schema.utils import load_model


def report_set(hc):
    return f"{hc.__class__.__name__} | {hc.type} | {hc.ComponentType}"


filepath = r".\samples\models\DetailedHVAC.xml"
model = load_model(filepath)

building = model.Site.Buildings.Building[0]
zone_groups = building.HVACNetwork.HVACZoneGroups.HVACZoneGroup

hzc_set = set()
for zone_group in zone_groups:
    zone_components = zone_group.ZoneElementList.HVACZoneComponent

    for hc in zone_components:
        # hzc_set.add(report_set(hc))

        if hasattr(hc, "UnitElementList"):
            if hasattr(hc.UnitElementList, "HVACComponent"):
                sub_hcs = hc.UnitElementList.HVACComponent

                for sub_hc in sub_hcs:
                    hzc_set.add(report_set(sub_hc))

for item in hzc_set:
    print(item)
