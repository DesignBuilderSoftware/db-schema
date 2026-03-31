## TODO Query:
# list all surfaces
# constructions assigned to surfaces
# name and U-values for constructions
# name and U-values of all assigned constructions
# surface area, (object ID handle), construction name

from designbuilder_schema.utils import load_model

filepath = r".\samples\models\Shoebox10x10.xml"
model = load_model(filepath)

building = model.Site.Buildings.Building[0]

zones = [
    zone for block in building.BuildingBlocks.BuildingBlock for zone in block.Zones.Zone
]

surfaces = [zone.Body.Surfaces.Surface for zone in zones]

print(surfaces[zone_index := 0][surface_index := 0])

# surfaces generally do not store constructions...
# surface only stores construction if defined at surface level
# even if defined it is ID that has to be found in Construction Table
# constructions may be defined at Building, buildingBlock, Zone, Surface levels
# depends on surfac type, zone type, adjacency...
