from designbuilder_schema.utils import load_model
from designbuilder_schema.core import Body
from designbuilder_schema.geometry import Point3D
from typing import List

filepath = r"samples\models\model from Tiago.xml"
dsb = load_model(filepath)

site = dsb.Site
first_building = site.Buildings.Building[0]


def floor_faces(body: Body) -> List[List[float]]:
    """List of floor faces where, where each face is a list of x,y,z coordiantes."""

    vertices = [Point3D(Point3D=v).coords for v in body.Vertices]
    faces = []
    for surface in body.Surfaces.Surface:
        if surface.type == "Floor":
            vertex_indices = surface.VertexIndices
            if vertex_indices[-1] == ";":  # remove semicolon if last
                vertex_indices = surface.VertexIndices[0:-1]

            indices = [int(x) for x in vertex_indices.split(";")]
            face = [vertices[i] for i in indices]
            faces.append(face)

    return faces


def body_title(body: Body) -> str:
    for attribute in body.Attributes.Attribute:
        if attribute.key == "Title":
            return attribute.text


for block in first_building.BuildingBlocks.BuildingBlock:
    for zone in block.Zones.Zone:
        # label_position = first_zone.LabelPosition.coords
        body = zone.Body
        print(body_title(body), floor_faces(body))

# if zone floor is not flat, for example has 2 surfaces or sloped
