from designbuilder_schema.extension_visualise.zone import *
from designbuilder_schema.utils import load_model


model = load_model(r"samples\models\Tutorial Model.xml")
building = model.Site.Buildings.Building[0]

zones = building_zones(building)
zones_geometry = [zone_geometry(zone) for zone in zones]

display_zones(zones_geometry)
colours = ["red", "blue", "green", "yellow", "orange", "purple", 
           "cyan", "magenta", "yellowgreen", "lightcoral"]

display_zones_with_defined_colours(zones_geometry, colours=colours)