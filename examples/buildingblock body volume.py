from dsbxml.utils import load_model

filepath = r".\samples\2026.1.0.013\Shoebox261.xml"
model = load_model(filepath)

site = model.site
first_building = site.buildings.building[0]
first_building_block = first_building.building_blocks.building_block[0]
first_zone = first_building_block.zones.zone[0]
body = first_zone.body

print(body.volume)
