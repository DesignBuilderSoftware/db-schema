from designbuilder_schema.utils import load_model

filepath = r"samples\models\Shoebox10x10.xml"
model = load_model(filepath)

site = model.Site
first_building = site.Buildings.Building[0]
first_building_blocks = first_building.BuildingBlocks.BuildingBlock[0]
first_zone = first_building_blocks.Zones.Zone[0]
vertices = first_zone.Body.Vertices

first_point = vertices[0]
print(first_point)

first_point.coords = [10, 0, 0]
print(first_point)

first_point.z = 20
print(first_point)
