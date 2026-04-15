from designbuilder_schema.utils import load_model

filepath = r"C:\GitHub\designbuilder_schema\samples\models\Shoebox10x10.xml"
model = load_model(filepath)

site = model.Site
first_building = site.Buildings.Building[0]
first_building_blocks = first_building.BuildingBlocks.BuildingBlock[0]
first_zone = first_building_blocks.Zones.Zone[0]
body = first_zone.Body

print(body.volume)
