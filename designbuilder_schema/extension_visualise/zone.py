"""
visualise.py
====================================
Extension module that adds visualization capabilities
"""

from designbuilder_schema.core import Building, BuildingBlock, Zone, Body
from designbuilder_schema.geometry import Point3D
from typing import List
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def faces(body: Body) -> List[List[float]]:
    """List of faces where, where each face is a list of x,y,z coordiantes."""

    vertices = [v.coords for v in body.vertices.point_3d]
    faces = []
    for surface in body.surfaces.surface:
        vertex_indices = surface.vertex_indices
        if vertex_indices[-1] == ";":  # remove semicolon if last
            vertex_indices = surface.vertex_indices[0:-1]

        indices = [int(x) for x in vertex_indices.split(";")]
        face = [vertices[i] for i in indices]
        faces.append(face)

    return faces


def openings(body: Body) -> List[List[float]]:
    """List of openings where, where each opening is a list of x,y,z coordiantes."""
    opening_list = []
    for surface in body.surfaces.surface:
        if surface.openings:
            openings_list = surface.openings.opening
            if isinstance(openings_list, List):
                opening_list.extend(openings_list)
            else:
                opening_list.append(openings_list)

    return [
        [v.coords for v in o.polygon.vertices.point_3d] if o.polygon.vertices else []
        for o in opening_list
    ]


def zone_geometry(zone: Zone):
    # attributes = {a.key: a.value for a in zone.attributes.attribute}
    # attributes["Title"]
    body = zone.body
    return {"faces": faces(body), "openings": openings(body)}


def building_block_geometry(building_block: BuildingBlock):
    # attributes = {a.key: a.value for a in self.attributes.attribute}
    # attributes["Title"]
    body = building_block.base_profile_body.profile_body.body
    return {"faces": faces(body), "openings": openings(body)}


def display_zones(zones_geometry: list):
    """Display all zone faces and openings with random colours."""
    # Create 3D figure
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection="3d")

    # Generate distinct colors for each zone
    base_colors = ["lightgray", "lightgreen", "lightpink", "lightyellow", "lightblue"]
    colors = base_colors * (len(zones_geometry) // len(base_colors) + 1)

    # Track bounds for axis scaling
    x_coords: list[float] = []
    y_coords: list[float] = []
    z_coords: list[float] = []

    # Plot each zone
    for zone_idx, zone in enumerate(zones_geometry):

        faces = zone["faces"]
        if faces:
            face_collection = Poly3DCollection(faces, alpha=1.0)
            face_collection.set_facecolor(colors[zone_idx])
            face_collection.set_edgecolor("black")
            ax.add_collection3d(face_collection)

            # Collect coordinates for bounds
            for face in faces:
                x, y, z = zip(*face)
                x_coords.extend(x)
                y_coords.extend(y)
                z_coords.extend(z)

        openings = zone["openings"]
        if openings:
            opening_collection = Poly3DCollection(openings, alpha=0.5)
            opening_collection.set_facecolor("lightblue")
            opening_collection.set_edgecolor("blue")
            ax.add_collection3d(opening_collection)

    # Set axis labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    max_range = max([max(x_coords), max(y_coords), max(z_coords)])
    min_range = min([min(x_coords), min(y_coords), min(z_coords)])

    # Set the limits with equal scaling
    ax.set_xlim(min_range, max_range)
    ax.set_ylim(min_range, max_range)
    ax.set_zlim(min_range, max_range)

    # Add title
    plt.title(f"Visualization of {len(zones_geometry)} Zones")

    plt.show()


def display_zones_with_defined_colours(zones_geometry: list, colours: list):
    """Display zone faces and openings with user-defined colours.

    Args:
        zones_geometry: List of zone geometries, each with 'faces' and 'openings' keys.
        colours: List of matplotlib color strings corresponding to each zone.

    Example:
        zones_geometry = [{'faces': [...], 'openings': [...]}, ...]
        colours = ['red', 'blue', 'green', 'yellow']
    """
    # Create 3D figure
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection="3d")

    # Track bounds for axis scaling
    x_coords: list[float] = []
    y_coords: list[float] = []
    z_coords: list[float] = []

    # Plot each zone with its defined colour
    for zone_idx, zone in enumerate(zones_geometry):
        colour = colours[zone_idx] if zone_idx < len(colours) else "lightgray"

        faces = zone["faces"]
        if faces:
            face_collection = Poly3DCollection(faces, alpha=1.0)
            face_collection.set_facecolor(colour)
            face_collection.set_edgecolor("black")
            ax.add_collection3d(face_collection)

            # Collect coordinates for bounds
            for face in faces:
                x, y, z = zip(*face)
                x_coords.extend(x)
                y_coords.extend(y)
                z_coords.extend(z)

        openings = zone["openings"]
        if openings:
            opening_collection = Poly3DCollection(openings, alpha=0.5)
            opening_collection.set_facecolor("lightblue")
            opening_collection.set_edgecolor("blue")
            ax.add_collection3d(opening_collection)

    # Set axis labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    max_range = max([max(x_coords), max(y_coords), max(z_coords)])
    min_range = min([min(x_coords), min(y_coords), min(z_coords)])

    # Set the limits with equal scaling
    ax.set_xlim(min_range, max_range)
    ax.set_ylim(min_range, max_range)
    ax.set_zlim(min_range, max_range)

    # Add title
    plt.title(f"Visualization of {len(zones_geometry)} Zones")

    plt.show()


def building_zones(building: Building):
    """Show matplotlib plot for all zones in building."""
    zones = []
    if building.building_blocks:
        zones = [
            zone
            for block in building.building_blocks.building_block
            if block.zones
            for zone in block.zones.zone
        ]
    return zones


def vis_building(self: Building):
    zones = building_zones(self)
    display_zones([zone_geometry(zone) for zone in zones])
