from dsbxml.core import Body
from dsbxml.utils import load_model

filepath = r"samples\7.3.1.003\model from Tiago.xml"
dsb = load_model(filepath)

site = dsb.site
first_building = site.buildings.building[0]


def floor_faces(body: Body) -> list[list[list[float]]]:
    """List of floor faces, where each face is a list of x,y,z coordinates."""

    vertices = [vertex.coords for vertex in body.vertices]
    faces = []
    for surface in body.surfaces.surface:
        if surface.type == "Floor" and surface.vertex_indices:
            vertex_indices = surface.vertex_indices.rstrip(";")  # drop a trailing semicolon
            indices = [int(x) for x in vertex_indices.split(";")]
            faces.append([vertices[i] for i in indices])

    return faces


def body_title(body: Body) -> str | None:
    if body.attributes is None:
        return None
    for attribute in body.attributes.attribute:
        if attribute.key == "Title":
            return attribute.value
    return None


for block in first_building.building_blocks.building_block:
    if block.zones is None:
        continue
    for zone in block.zones.zone:
        body = zone.body
        print(body_title(body), floor_faces(body))

# if zone floor is not flat, for example has 2 surfaces or sloped
