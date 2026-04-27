"""
honeybee_to_designbuilder.py
====================================
Convert Honeybee model to DesignBuilder model
"""

import datetime

from small_honeybee import (
    Aperture,
    Door,
    Face,
    Model,
    Room,
    load_and_validate,
)
from small_honeybee import (
    Point3D as HBPoint3D,
)

from db_schema.attributes import (
    KeyAttribute,
    KeyAttributes,
    NameAttribute,
    NameAttributes,
)
from db_schema.core import *
from db_schema.geometry import Point3D as DBPoint3D
from db_schema.geometry import Vertices
from db_schema.utils import save_model

db_point0 = DBPoint3D(Point3D="0.0; 0.0; 0.0")


def convert_point3d(point: HBPoint3D) -> DBPoint3D:
    """Convert a Ladybug Point3D to a DesignBuilder Point3D."""
    return DBPoint3D(Point3D=f"{point.x}; {point.y}; {point.z}")


def convert_aperture_to_opening(aperture: Aperture) -> Opening:
    """Convert a Honeybee Aperture to a DesignBuilder Opening."""
    vertices = [convert_point3d(v).Point3D for v in aperture.geometry.boundary]

    polygon = Polygon(
        auxiliaryType="",
        Vertices=Vertices(Point3D=vertices),
        PolygonHoles=None,
    )

    return Opening(
        type="Window", Polygon=polygon, Attributes=None, SegmentList=None
    )


def convert_door_to_opening(door: Door) -> Opening:
    """Convert a Honeybee Door to a DesignBuilder Opening."""
    vertices = [convert_point3d(v) for v in door.geometry.boundary]

    return Opening(
        type="Door",
        area=door.geometry.area if hasattr(door.geometry, "area") else 0,
        Polygon={"Vertices": {"Point3D": vertices}},
        Attributes=KeyAttributes(
            Attribute=[KeyAttribute(key="Name", text=door.identifier)]
        ),
    )


def convert_face_to_surface(face: Face, vertices: list[str]) -> Surface:
    """Convert a Honeybee Face to a DesignBuilder Surface."""

    # Map Honeybee face types to DesignBuilder surface types
    surface_type_map = {
        "Wall": "Wall",
        "RoofCeiling": "Flat roof",
        "Floor": "Floor",
        "AirBoundary": "Air",
    }

    boundary_indices = [
        vertices.index(convert_point3d(p).Point3D)
        for p in face.geometry.boundary
    ]
    vertex_indices = "; ".join(str(i) for i in boundary_indices)

    surface = Surface(
        type=surface_type_map.get(face.face_type, "Wall"),
        area=0,
        alpha=0,
        phi=0,
        defaultOpenings="",
        adjacentPartitionHandle=0,
        thickness=0.3,
        VertexIndices=vertex_indices,
        HoleIndices=None,
        Openings=None,
        Adjacencies=None,
        Attributes=None,
    )

    # Add openings if any exist
    openings = []
    if hasattr(face, "apertures") and face.apertures:
        openings.extend(
            convert_aperture_to_opening(ap) for ap in face.apertures
        )

    """if hasattr(face, 'doors') and face.doors:
        openings.extend(convert_door_to_opening(door) for door in face.doors)
    """
    if openings:
        surface.Openings = {"Opening": openings}

    return surface


def convert_room_to_building_block(room: Room) -> BuildingBlock:
    """Convert a Honeybee Room to a DesignBuilder BuildingBlock."""
    all_points = {}
    for face in room.faces:
        for point in face.geometry.boundary:
            point_str = str(point)
            if point_str not in all_points:
                all_points[point_str] = convert_point3d(point).Point3D

    vertices = list(all_points.values())

    surfaces = []
    for face in room.faces:
        surface = convert_face_to_surface(face, vertices)
        surfaces.append(surface)

    body = Body(
        volume=0,
        extrusionHeight=3.0,
        Vertices=Vertices(Point3D=vertices),
        Surfaces={"Surface": surfaces},
        VoidPerimeterList=None,
        Attributes=KeyAttributes(
            Attribute=[KeyAttribute(key="Title", text="Zone 1")]
        ),
    )

    profile_body = ProfileBody(elementSlope=30.0, roofOverlap=0.0, Body=body)

    zone = Zone(
        parentZoneHandle="",
        inheritedZoneHandle="",
        planExtrusion="",
        innerSurfaceMode="",
        Body=body,
        LightSensorOne=LightSensorOne(index=0, Point3D=db_point0.Point3D),
        LightSensorTwo=LightSensorTwo(index=1, Point3D=db_point0.Point3D),
        LabelPosition=db_point0,
        Polygon=None,
        InnerSurfaceBody=None,
    )

    return BuildingBlock(
        type="Plan extruusion",
        height=3.0,
        roofSlope=0,
        roofOverlap=0,
        roofType="Flat",
        wallSlope=0,
        ComponentBlocks=None,
        CFDFans=None,
        AssemblyInstances=None,
        ProfileOutlines=None,
        InternalPartitions=None,
        VoidBodies=None,
        Zones=Zones(Zone=zone),
        ProfileBody=profile_body,
        Perimeter=None,
        BaseProfileBody=BaseProfileBody(ProfileBody=profile_body),
        Attributes=KeyAttributes(
            Attribute=[KeyAttribute(key="Title", text="Block 1")]
        ),
    )


def hb_to_dsb(hb_model: Model) -> DSB:
    """Convert a Honeybee Model to a DesignBuilder Schema."""
    # Convert to metric units if necessary
    """if hb_model.units != 'Meters':
        hb_model = hb_model.duplicate()
        hb_model.convert_to_units('Meters')"""

    # Create building blocks from rooms
    building_blocks = [
        convert_room_to_building_block(room) for room in hb_model.rooms
    ]

    # Create building
    building = Building(
        currentComponentBlockHandle=1,
        currentAssemblyInstanceHandle=1,
        currentPlaneHandle=1,
        BuildingBlocks={"BuildingBlock": building_blocks},
        ComponentBlocks=None,
        AssemblyInstances=None,
        ProfileOutlines=None,
        ConstructionLines=None,
        Planes=None,
        HVACNetwork=None,
        BookmarkBuildings=None,
        Attributes=KeyAttributes(
            Attribute=[
                KeyAttribute(key="Title", text=hb_model.display_name),
                KeyAttribute(key="GeometryDataLevel", text="3"),
            ]
        ),
    )
    version = "8.0.0.058"
    version_site_attribute = NameAttribute(name="Version", text=version)
    site_attributes = NameAttributes(Attribute=[version_site_attribute])

    # Create site with building
    site = Site(
        handle=1,
        count=1,
        Attributes=site_attributes,
        Tables=None,
        AssemblyLibrary=None,
        Buildings=Buildings(numberOfBuildings=1, Building=building),
    )

    # Create DesignBuilder model
    model = DSB(
        name=hb_model.display_name,
        date=datetime.date.today().isoformat(),
        version=version,
        objects="all",
        Site=site,
    )

    return model


if __name__ == "__main__":
    hb_filepath = r"apps\honeybee_to_designbuilder\HB Shoebox.json"
    hb_model = load_and_validate(hb_filepath)

    db_model = hb_to_dsb(hb_model)

    db_filepath = r"apps\honeybee_to_designbuilder\HB Shoebox.xml"
    save_model(db_model, db_filepath)
