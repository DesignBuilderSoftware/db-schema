"""
geometry.py
====================================
The geometry module of the designbuilder_schema
"""

from designbuilder_schema.base import BaseModel
from designbuilder_schema.id import ObjectIDs
from typing import List, Union, Annotated
from pydantic import Field


class Point3D(BaseModel):
    Point3D: str

    _coords_cache: Union[tuple, None] = None

    @property
    def _cached_coords(self) -> tuple:
        if self._coords_cache is None:
            parsed = tuple(float(c) for c in self.Point3D.split(";"))
            object.__setattr__(self, "_coords_cache", parsed)
        return self._coords_cache

    @property
    def x(self) -> float:
        return self._cached_coords[0]

    @property
    def y(self) -> float:
        return self._cached_coords[1]

    @property
    def z(self) -> float:
        return self._cached_coords[2]

    @property
    def coords(self) -> List[float]:
        return list(self._cached_coords)

    def __setattr__(self, name: str, value: Union[float, List[float]]) -> None:
        if name == "coords":
            if isinstance(value, list) and len(value) == 3:
                self.Point3D = ";".join(map(str, value))
            else:
                raise ValueError("Coordinates must be a list of 3 numbers")
        elif name in ["x", "y", "z"]:
            index = {"x": 0, "y": 1, "z": 2}[name]
            coords = self.Point3D.split(";")
            coords[index] = str(value)
            self.Point3D = ";".join(coords)
        else:
            # Invalidate cache when Point3D string changes
            if name == "Point3D":
                object.__setattr__(self, "_coords_cache", None)
            super().__setattr__(name, value)


class Vertices(BaseModel):
    Point3D: List["str"]

    def __getitem__(self, index: int) -> "Point3D":
        return Point3D(Point3D=self.Point3D[index])

    def __setitem__(self, index: int, value: Union[str, "Point3D"]) -> None:
        try:
            if isinstance(value, Point3D):
                self.Point3D[index] = value.Point3D
            elif isinstance(value, str):
                self.Point3D[index] = value
        except IndexError as e:
            raise ValueError(f"Invalid index {index} for Vertices.Point3D") from e

    def __iter__(self):
        return iter(self.Point3D)


class Range(BaseModel):
    """Used only in ImageRectangle to represent rectangle relative position.
    Org - top left corner.
    End -  bottom right corner."""

    Org: "Point3D"
    End: "Point3D"


class Line(BaseModel):
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    Begin: "Point3D"
    End: "Point3D"


class ImageRectangle(BaseModel):
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    ImageTextureIndex: int
    MaskTextureIndex: int
    SelectedImageTextureIndex: int
    InactiveImageTextureIndex: int
    Textured: str
    Masked: str
    SelectedImage: str
    InactiveImage: str
    Color: str
    Active: str
    Vertices: "Vertices"
    Range: "Range"


class SegmentList(BaseModel):
    LineArray: "LineArray"


class LineArray(BaseModel):
    Line: Union["Line", list["Line"]]
