from __future__ import annotations

from collections.abc import Iterator
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_xml import element

from dsbxml.base import BaseModel
from dsbxml.id import ObjectIDs


class Point3D(BaseModel):
    value: str = "0;0;0"

    @field_validator("value", mode="before")
    @classmethod
    def _coerce_empty(cls, v):
        """Treat empty or whitespace-only text as the origin sentinel."""
        if not v or not str(v).strip():
            return "0;0;0"
        return v

    def _parse_coords(self) -> tuple[float, float, float]:
        parsed = tuple(float(c) for c in self.value.split(";"))
        if len(parsed) != 3:
            raise ValueError(f"Expected 3 coordinates, got {len(parsed)}: {self.value!r}")
        return parsed

    @property
    def x(self) -> float:
        return self._parse_coords()[0]

    @property
    def y(self) -> float:
        return self._parse_coords()[1]

    @property
    def z(self) -> float:
        return self._parse_coords()[2]

    @property
    def coords(self) -> list[float]:
        return list(self._parse_coords())

    @property
    def is_zero(self) -> bool:
        """True when all coordinates are zero — the sentinel for 'no position'."""
        return self.value == "0;0;0" or all(c == 0.0 for c in self._parse_coords())

    def __setattr__(self, name: str, value: float | list[float]) -> None:
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
            super().__setattr__(name, value)


class Vertices(BaseModel):
    point_3d: list[Point3D] = element(tag="Point3D", default_factory=list)

    def __iter__(self) -> Iterator[Point3D]:
        return iter(self.point_3d)

    def __getitem__(self, index: int) -> Point3D:
        return self.point_3d[index]

    def __setitem__(self, index: int, value: str | Point3D) -> None:
        try:
            if isinstance(value, Point3D):
                self.point_3d[index] = value
            elif isinstance(value, str):
                self.point_3d[index] = Point3D(value=value)
        except IndexError as e:
            raise ValueError(f"Invalid index {index} for Vertices.point_3d") from e


class HandlePoint(BaseModel):
    point_3d: Point3D = element(tag="Point3D")

    def __iter__(self) -> Iterator[Point3D]:
        return iter([self.point_3d])


class WrappedPoint3D(BaseModel):
    """A Point3D nested one level deeper under its own <Point3D> child tag.

    Most single-coordinate fields in the DesignBuilder XML (Origin,
    Coordinate, Begin, End, ControlPoint, ...) are not the coordinate text
    themselves but a wrapper element containing a single <Point3D> child,
    e.g. <Origin><Point3D>1;2;3</Point3D></Origin>. Typing these fields as
    plain Point3D silently parses to the "0;0;0" default, since pydantic-xml
    looks for the coordinate text directly on the wrapper element rather
    than recursing into the nested tag. Exposes the same x/y/z/coords/
    is_zero interface as Point3D so existing call sites are unaffected.
    """

    point_3d: Point3D = element(tag="Point3D", default_factory=Point3D)

    @property
    def x(self) -> float:
        return self.point_3d.x

    @property
    def y(self) -> float:
        return self.point_3d.y

    @property
    def z(self) -> float:
        return self.point_3d.z

    @property
    def coords(self) -> list[float]:
        return self.point_3d.coords

    @property
    def is_zero(self) -> bool:
        return self.point_3d.is_zero


class Range(BaseModel):
    org: WrappedPoint3D = element(tag="Org")
    end: WrappedPoint3D = element(tag="End")


class Line(BaseModel):
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(
        tag="ObjectIDs"
    )
    begin: WrappedPoint3D = element(tag="Begin")
    end: WrappedPoint3D = element(tag="End")


class ImageRectangle(BaseModel):
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(
        tag="ObjectIDs"
    )
    imageTextureIndex: int = element(tag="ImageTextureIndex")
    maskTextureIndex: int = element(tag="MaskTextureIndex")
    selectedImageTextureIndex: int = element(tag="SelectedImageTextureIndex")
    inactiveImageTextureIndex: int = element(tag="InactiveImageTextureIndex")
    textured: str = element(tag="Textured")
    masked: str = element(tag="Masked")
    selectedImage: str = element(tag="SelectedImage")
    inactiveImage: str = element(tag="InactiveImage")
    color: str = element(tag="Color")
    active: str = element(tag="Active")
    vertices: Vertices = element(tag="Vertices")
    range: Range | None = element(tag="Range", default=None)


class SegmentList(BaseModel):
    line_array: LineArray = element(tag="LineArray")


class LineArray(BaseModel):
    line: list[Line] = element(tag="Line")
