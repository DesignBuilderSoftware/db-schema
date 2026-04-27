"""
geometry.py
====================================
The geometry module of the db_schema
"""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from db_schema.base import BaseModel
from db_schema.id import ObjectIDs


class Point3D(BaseModel):
    Point3D: str

    @property
    def x(self) -> float:
        return float(self.Point3D.split(";")[0])

    @property
    def y(self) -> float:
        return float(self.Point3D.split(";")[1])

    @property
    def z(self) -> float:
        return float(self.Point3D.split(";")[2])

    @property
    def coords(self) -> list[float]:
        return [float(coord) for coord in self.Point3D.split(";")]

    def __setattr__(self, name: str, value: float | list[float]) -> None:
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
            super().__setattr__(name, value)


class Vertices(BaseModel):
    Point3D: list[str]

    def __getitem__(self, index: int) -> Point3D:
        return Point3D(Point3D=self.Point3D[index])

    def __setitem__(self, index: int, value: str | Point3D) -> None:
        try:
            if isinstance(value, Point3D):
                self.Point3D[index] = value.Point3D
            elif isinstance(value, str):
                self.Point3D[index] = value
        except IndexError as e:
            raise ValueError(
                f"Invalid index {index} for Vertices.Point3D"
            ) from e

    def __iter__(self):
        return iter(self.Point3D)


class Range(BaseModel):
    """Used only in ImageRectangle to represent rectangle relative position.
    Org - top left corner.
    End -  bottom right corner."""

    Org: Point3D
    End: Point3D


class Line(BaseModel):
    ObjectIDs: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)]
    Begin: Point3D
    End: Point3D


class ImageRectangle(BaseModel):
    ObjectIDs: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)]
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
    Vertices: Vertices
    Range: Range


class SegmentList(BaseModel):
    LineArray: LineArray


class LineArray(BaseModel):
    Line: Line | list[Line]
