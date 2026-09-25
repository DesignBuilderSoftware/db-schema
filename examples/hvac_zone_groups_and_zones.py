from dsbxml.utils import load_model

filepath = r".\samples\models_dhvac\HVAC_Zones_Coloured.xml"
model = load_model(filepath)

building = model.Site.Buildings.Building[0]

# Get all HVAC zone groups
zone_groups = building.HVACNetwork.HVACZoneGroups.HVACZoneGroup

print(f"Found {len(zone_groups)} HVAC Zone Groups\n")
print("=" * 80)

for idx, zone_group in enumerate(zone_groups, 1):
    # Get zone group title
    group_title = next(
        (
            attr.text
            for attr in zone_group.Attributes.Attribute
            if attr.name == "Title"
        ),
        "Unknown",
    )

    print(f"\n{idx}. HVAC Zone Group: {group_title}")
    print("-" * 80)

    # Get zone components in this group
    if zone_group.ZoneElementList:
        zone_components = zone_group.ZoneElementList.HVACZoneComponent

        if zone_components:
            print(f"   Zone Components ({len(zone_components)}):")
            for component in zone_components:
                component_title = next(
                    (
                        attr.text
                        for attr in component.Attributes.Attribute
                        if attr.name == "Title"
                    ),
                    "Unknown",
                )
                component_type = (
                    component.type
                    if hasattr(component, "type")
                    else "Unknown type"
                )
                print(f"      - {component_title}")
                print(f"        Type: {component_type}")
        else:
            print("   No zone components in this group")
    else:
        print("   No ZoneElementList")

    # Also show building zone handles if available
    if zone_group.BuildingZoneHandleList:
        zone_handles = zone_group.BuildingZoneHandleList.BuildingZoneHandle
        if zone_handles:
            print(f"   Building Zone Handles: {', '.join(zone_handles)}")

print("\n" + "=" * 80)
print(f"\nTotal Zone Groups: {len(zone_groups)}")
