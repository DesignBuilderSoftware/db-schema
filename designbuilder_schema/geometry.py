
"""
geometry.py
====================================
The geometry module of the designbuilder_schema
"""

from designbuilder_schema.base import BaseModel
from designbuilder_schema.id import ObjectIDs
from pydantic_xml import attr, element
from typing import List, Union, Annotated
from pydantic import Field


class Point3D(BaseModel):
    """A 3D point in space.

    Represents coordinates with cached property accessors for x, y, z values.
    Internally stores coordinates as a semicolon-separated string.

    Attributes:
        value: Semicolon-separated coordinates as string (e.g., "10.5;20.3;5.0")
    """
    value: str

    _coords_cache: Union[tuple[float, float, float], None] = None

    @property
    def _cached_coords(self) -> tuple[float, float, float]:
        if self._coords_cache is None:
            parsed = tuple(float(c) for c in self.value.split(";"))
            assert len(parsed) == 3, "Expected 3 coordinates"
            object.__setattr__(self, "_coords_cache", tuple(parsed))
        assert self._coords_cache is not None
        return self._coords_cache

    @property
    def x(self) -> float:
        return float(self._cached_coords[0])

    @property
    def y(self) -> float:
        return float(self._cached_coords[1])

    @property
    def z(self) -> float:
        return float(self._cached_coords[2])

    @property
    def coords(self) -> List[float]:
        return list(self._cached_coords)

    def __setattr__(self, name: str, value: Union[float, List[float]]) -> None:
        if name == "coords":
            if isinstance(value, list) and len(value) == 3:
                self.value = ";".join(map(str, value))
            else:
                raise ValueError("Coordinates must be a list of 3 numbers")
        elif name in ["x", "y", "z"]:
            index = {"x": 0, "y": 1, "z": 2}[name]
            coords = self.value.split(";")
            coords[index] = str(value)
            self.value = ";".join(coords)
        else:
            # Invalidate cache when value string changes
            if name == "value":
                object.__setattr__(self, "_coords_cache", None)
            super().__setattr__(name, value)


class Vertices(BaseModel):
    """Container for a list of 3D vertices.

    Represents a collection of 3D points with array-like access.

    Attributes:
        point_3d: List of 3D point coordinates
    """
    point_3d: List[Point3D] = element(tag="Point3D")

    def __getitem__(self, index: int) -> Point3D:
        return self.point_3d[index]

    def __setitem__(self, index: int, value: Union[str, Point3D]) -> None:
        try:
            if isinstance(value, Point3D):
                self.point_3d[index] = value
            elif isinstance(value, str):
                self.point_3d[index] = Point3D(value=value)
        except IndexError as e:
            raise ValueError(f"Invalid index {index} for Vertices.point_3d") from e

    def __iter__(self) -> iter:
        return iter(self.point_3d)


class Range(BaseModel):
    """Used only in ImageRectangle to represent rectangle relative position.
    Org - top left corner.
    End -  bottom right corner."""

    org: "Point3D" = element()
    end: "Point3D" = element()


class Line(BaseModel):
    """A line segment defined by start and end points.

    Represents a straight line in 3D space.

    Attributes:
        object_ids: Unique object identifiers
        begin: Starting point of the line
        end: Ending point of the line
    """
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    begin: "Point3D" = element()
    end: "Point3D" = element()


class ImageRectangle(BaseModel):
    """A rectangle with texture mapping for visualization.

    Represents a textured rectangle used for background images or materials.

    Attributes:
        object_ids: Unique object identifiers
        image_texture_index: Index of the primary image texture
        mask_texture_index: Index of the mask texture
        selected_image_texture_index: Index of selected state image
        inactive_image_texture_index: Index of inactive state image
        textured: Whether texturing is enabled
        masked: Whether masking is enabled
        selected_image: Selected image reference
        inactive_image: Inactive image reference
        color: Color value
        active: Whether rectangle is active
        vertices: Corner vertices of the rectangle
        range: Position range relative to top-left
    """
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    image_texture_index: int = attr()
    mask_texture_index: int = attr()
    selected_image_texture_index: int = attr()
    inactive_image_texture_index: int = attr()
    textured: str = attr()
    masked: str = attr()
    selected_image: str = attr()
    inactive_image: str = attr()
    color: str = attr()
    active: str = attr()
    vertices: "Vertices" = element()
    range: "Range" = element()


class SegmentList(BaseModel):
    """Container for a list of line segments.

    Attributes:
        line_array: Array of line segments
    """
    line_array: "LineArray" = element()


class LineArray(BaseModel):
    """Container for multiple line segment definitions.

    Attributes:
        line: List of line segments
    """
    line: List["Line"] = element(tag="Line")
