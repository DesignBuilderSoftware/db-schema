from designbuilder_schema.utils import load_model
from designbuilder_schema.extension_visualise.zone import (
    zone_geometry,
    display_zones_with_defined_colours,
)
import matplotlib.colors as mcolors

filepath = r".\samples\models_dhvac\HVAC_Zones_Coloured.xml"
model = load_model(filepath)

building = model.Site.Buildings.Building[0]

# Get all zones from building blocks and create handle mapping
zone_handle_to_zone = {}
for block in building.BuildingBlocks.BuildingBlock:
    for zone in block.Zones.Zone:
        zone_handle_to_zone[zone.inheritedZoneHandle] = zone

# Get all HVAC zone groups
zone_groups = building.HVACNetwork.HVACZoneGroups.HVACZoneGroup

# Create a color palette for zone groups
colors = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())

# Map zone groups to colors and collect zones
zones_with_colours = []

for idx, zone_group in enumerate(zone_groups):
    # Get zone group title
    group_title = next(
        (attr.text for attr in zone_group.Attributes.Attribute if attr.name == "Title"),
        "Unknown",
    )

    # Assign color to this zone group
    color = colors[idx % len(colors)]

    # Get building zone handles for this group
    if zone_group.BuildingZoneHandleList:
        zone_handles = zone_group.BuildingZoneHandleList.BuildingZoneHandle

        if zone_handles:
            for handle in zone_handles:
                # Find zone with matching inheritedZoneHandle
                if handle in zone_handle_to_zone:
                    zone = zone_handle_to_zone[handle]
                    geometry = zone_geometry(zone)
                    zones_with_colours.append(
                        {"geometry": geometry, "colour": color, "group": group_title}
                    )

print(f"Found {len(zone_groups)} HVAC Zone Groups")
print(f"Displaying {len(zones_with_colours)} zones with HVAC group colors")

zones_geometry = [item["geometry"] for item in zones_with_colours]
colours = [item["colour"] for item in zones_with_colours]

display_zones_with_defined_colours(zones_geometry, colours)
