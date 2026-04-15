from designbuilder_schema.base import BaseModel
from designbuilder_schema.id import ObjectIDs
from pydantic_xml import attr, element
from typing import List, Union, Annotated, Iterator
from pydantic import Field


class Point3D(BaseModel):
    value: str

    def _parse_coords(self) -> tuple[float, float, float]:
        parsed = tuple(float(c) for c in self.value.split(";"))
        assert len(parsed) == 3, "Expected 3 coordinates"
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
    def coords(self) -> List[float]:
        return list(self._parse_coords())

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
            super().__setattr__(name, value)


class Vertices(BaseModel):
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

    def __iter__(self) -> Iterator[Point3D]:
        return iter(self.point_3d)


class Range(BaseModel):
    org: "Point3D" = element()
    end: "Point3D" = element()


class Line(BaseModel):
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    begin: "Point3D" = element()
    end: "Point3D" = element()


class ImageRectangle(BaseModel):
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    imageTextureIndex: int = attr()
    maskTextureIndex: int = attr()
    selectedImageTextureIndex: int = attr()
    inactiveImageTextureIndex: int = attr()
    textured: str = attr()
    masked: str = attr()
    selectedImage: str = attr()
    inactiveImage: str = attr()
    color: str = attr()
    active: str = attr()
    vertices: "Vertices" = element()
    range: "Range" = element()


class SegmentList(BaseModel):
    line_array: "LineArray" = element()


class LineArray(BaseModel):
    line: List["Line"] = element(tag="Line")
