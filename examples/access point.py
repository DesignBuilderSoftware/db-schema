from dsbxml.utils import load_model

filepath = r"samples\models\Shoebox261.xml"
model = load_model(filepath)

site = model.site
first_building = site.buildings.building[0]
first_building_blocks = first_building.building_blocks.building_block[0]
first_zone = first_building_blocks.zones.zone[0]
vertices = first_zone.body.vertices

first_point = vertices[0]
print(first_point)

first_point.coords = [10, 0, 0]
print(first_point)

first_point.z = 20
print(first_point)
