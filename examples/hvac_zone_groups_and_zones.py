from dsbxml.utils import load_model

filepath = r".\samples\2025.1.0.095\HVAC_Zones_Coloured.xml"
model = load_model(filepath)

building = model.site.buildings.building[0]


def title(attributes) -> str:
    if attributes is None:
        return "Unknown"
    return next((a.value for a in attributes.attribute if a.name == "Title"), "Unknown")


# Get all HVAC zone groups
zone_groups = building.hvac_network.hvac_zone_groups.hvac_zone_group

print(f"Found {len(zone_groups)} HVAC Zone Groups\n")
print("=" * 80)

for idx, zone_group in enumerate(zone_groups, 1):
    print(f"\n{idx}. HVAC Zone Group: {title(zone_group.zone_group_attributes)}")
    print("-" * 80)

    # Get zone components in this group
    if zone_group.zone_element_list:
        zone_components = zone_group.zone_element_list.hvac_zone_component

        if zone_components:
            print(f"   Zone Components ({len(zone_components)}):")
            for component in zone_components:
                print(f"      - {title(component.attributes)}")
                print(f"        Type: {component.type or 'Unknown type'}")
        else:
            print("   No zone components in this group")
    else:
        print("   No ZoneElementList")

    # Also show building zone handles if available
    if zone_group.building_zone_handle_list:
        zone_handles = zone_group.building_zone_handle_list.building_zone_handle
        if zone_handles:
            print(f"   Building Zone Handles: {', '.join(zone_handles)}")

print("\n" + "=" * 80)
print(f"\nTotal Zone Groups: {len(zone_groups)}")
