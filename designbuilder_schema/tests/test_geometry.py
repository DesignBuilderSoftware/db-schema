import pytest
from designbuilder_schema.geometry import Point3D, Vertices, Line, Range
from designbuilder_schema.id import ObjectIDs


class TestPoint3D:

    def test_point3d_creation(self):
        point = Point3D(value="1.0;2.0;3.0")
        assert point.value == "1.0;2.0;3.0"

    def test_point3d_x_property(self):
        point = Point3D(value="1.5;2.0;3.0")
        assert point.x == 1.5

    def test_point3d_y_property(self):
        point = Point3D(value="1.0;2.5;3.0")
        assert point.y == 2.5

    def test_point3d_z_property(self):
        point = Point3D(value="1.0;2.0;3.5")
        assert point.z == 3.5

    def test_point3d_coords_property(self):
        point = Point3D(value="1.0;2.0;3.0")
        assert point.coords == [1.0, 2.0, 3.0]

    def test_point3d_x_coordinate_in_value(self):
        point = Point3D(value="5.0;2.0;3.0")
        assert point.x == 5.0
        assert point.y == 2.0
        assert point.z == 3.0

    def test_point3d_coords_from_value_string(self):
        point = Point3D(value="4.0;5.0;6.0")
        assert point.coords == [4.0, 5.0, 6.0]

    def test_point3d_value_format(self):
        point = Point3D(value="1.0;2.0;3.0")
        # Verify the format is correct
        assert ";" in point.value
        parts = point.value.split(";")
        assert len(parts) == 3


class TestVertices:

    def test_vertices_creation(self):
        vertices = Vertices(
            point_3d=[Point3D(value="1.0;2.0;3.0"), Point3D(value="4.0;5.0;6.0")]
        )
        assert len(vertices.point_3d) == 2

    def test_vertices_getitem(self):
        vertices = Vertices(
            point_3d=[Point3D(value="1.0;2.0;3.0"), Point3D(value="4.0;5.0;6.0")]
        )
        point = vertices[0]
        assert isinstance(point, Point3D)
        assert point.x == 1.0
        assert point.y == 2.0
        assert point.z == 3.0

    def test_vertices_setitem_with_point3d(self):
        vertices = Vertices(
            point_3d=[Point3D(value="1.0;2.0;3.0"), Point3D(value="4.0;5.0;6.0")]
        )
        new_point = Point3D(value="7.0;8.0;9.0")
        vertices[0] = new_point
        assert vertices.point_3d[0].value == "7.0;8.0;9.0"

    def test_vertices_setitem_with_string(self):
        vertices = Vertices(
            point_3d=[Point3D(value="1.0;2.0;3.0"), Point3D(value="4.0;5.0;6.0")]
        )
        vertices[1] = "7.0;8.0;9.0"
        assert vertices.point_3d[1].value == "7.0;8.0;9.0"

    def test_vertices_iter(self):
        vertices = Vertices(
            point_3d=[Point3D(value="1.0;2.0;3.0"), Point3D(value="4.0;5.0;6.0")]
        )
        coords_list: list[Point3D] = list(vertices)
        assert len(coords_list) == 2
        assert coords_list[0].value == "1.0;2.0;3.0"
        assert coords_list[1].value == "4.0;5.0;6.0"


class TestLine:

    def test_line_creation(self):
        begin = Point3D(value="0.0;0.0;0.0")
        end = Point3D(value="10.0;10.0;10.0")
        line = Line(object_ids=ObjectIDs(), begin=begin, end=end)
        assert line.begin.value == "0.0;0.0;0.0"
        assert line.end.value == "10.0;10.0;10.0"

    def test_line_has_object_ids(self):
        begin = Point3D(value="0.0;0.0;0.0")
        end = Point3D(value="10.0;10.0;10.0")
        line = Line(object_ids=ObjectIDs(), begin=begin, end=end)
        assert isinstance(line.object_ids, ObjectIDs)
        assert line.object_ids.handle >= 0  # Auto-generated handle


class TestRange:

    def test_range_creation(self):
        org = Point3D(value="0.0;0.0;0.0")
        end = Point3D(value="100.0;100.0;0.0")
        range_obj = Range(org=org, end=end)
        assert range_obj.org.value == "0.0;0.0;0.0"
        assert range_obj.end.value == "100.0;100.0;0.0"
