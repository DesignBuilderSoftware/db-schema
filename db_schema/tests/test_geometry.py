from db_schema.geometry import Line, Point3D, Range, Vertices, WrappedPoint3D
from db_schema.id import ObjectIDs


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


class TestWrappedPoint3D:
    """Regression coverage for the nested <Tag><Point3D>...</Point3D></Tag>
    parsing bug: fields like Line.begin/end and Origin previously typed as
    plain Point3D always parsed to the zero default, because pydantic-xml
    looks for coordinate text directly on the wrapper element rather than
    recursing into the nested <Point3D> child.
    """

    def test_wrapped_point3d_exposes_point3d_interface(self):
        wrapped = WrappedPoint3D(point_3d=Point3D(value="1.0;2.0;3.0"))
        assert wrapped.x == 1.0
        assert wrapped.y == 2.0
        assert wrapped.z == 3.0
        assert wrapped.coords == [1.0, 2.0, 3.0]
        assert wrapped.is_zero is False

    def test_wrapped_point3d_is_zero(self):
        wrapped = WrappedPoint3D(point_3d=Point3D(value="0;0;0"))
        assert wrapped.is_zero is True

    def test_line_parses_nested_point3d_from_xml(self):
        xml = (
            b"<Line>"
            b'<ObjectIDs handle="1" buildingHandle="-1" buildingBlockHandle="-1" '
            b'zoneHandle="-1" surfaceIndex="-1" openingIndex="-1"></ObjectIDs>'
            b"<Begin><Point3D>1.0;2.0;3.0</Point3D></Begin>"
            b"<End><Point3D>4.0;5.0;6.0</Point3D></End>"
            b"</Line>"
        )
        line = Line.from_xml(xml)
        assert line.begin.coords == [1.0, 2.0, 3.0]
        assert line.end.coords == [4.0, 5.0, 6.0]

    def test_range_parses_nested_point3d_from_xml(self):
        xml = (
            b"<Range>"
            b"<Org><Point3D>0.0;0.0;0.0</Point3D></Org>"
            b"<End><Point3D>100.0;100.0;0.0</Point3D></End>"
            b"</Range>"
        )
        range_obj = Range.from_xml(xml)
        assert range_obj.org.coords == [0.0, 0.0, 0.0]
        assert range_obj.end.coords == [100.0, 100.0, 0.0]


class TestVertices:
    def test_vertices_creation(self):
        vertices = Vertices(
            point_3d=[
                Point3D(value="1.0;2.0;3.0"),
                Point3D(value="4.0;5.0;6.0"),
            ]
        )
        assert len(vertices.point_3d) == 2

    def test_vertices_getitem(self):
        vertices = Vertices(
            point_3d=[
                Point3D(value="1.0;2.0;3.0"),
                Point3D(value="4.0;5.0;6.0"),
            ]
        )
        point = vertices[0]
        assert isinstance(point, Point3D)
        assert point.x == 1.0
        assert point.y == 2.0
        assert point.z == 3.0

    def test_vertices_setitem_with_point3d(self):
        vertices = Vertices(
            point_3d=[
                Point3D(value="1.0;2.0;3.0"),
                Point3D(value="4.0;5.0;6.0"),
            ]
        )
        new_point = Point3D(value="7.0;8.0;9.0")
        vertices[0] = new_point
        assert vertices.point_3d[0].value == "7.0;8.0;9.0"

    def test_vertices_setitem_with_string(self):
        vertices = Vertices(
            point_3d=[
                Point3D(value="1.0;2.0;3.0"),
                Point3D(value="4.0;5.0;6.0"),
            ]
        )
        vertices[1] = "7.0;8.0;9.0"
        assert vertices.point_3d[1].value == "7.0;8.0;9.0"

    def test_vertices_iter(self):
        vertices = Vertices(
            point_3d=[
                Point3D(value="1.0;2.0;3.0"),
                Point3D(value="4.0;5.0;6.0"),
            ]
        )
        coords_list: list[Point3D] = list(vertices)
        assert len(coords_list) == 2
        assert coords_list[0].value == "1.0;2.0;3.0"
        assert coords_list[1].value == "4.0;5.0;6.0"


class TestLine:
    def test_line_creation(self):
        begin = WrappedPoint3D(point_3d=Point3D(value="0.0;0.0;0.0"))
        end = WrappedPoint3D(point_3d=Point3D(value="10.0;10.0;10.0"))
        line = Line(object_ids=ObjectIDs(), begin=begin, end=end)
        assert line.begin.coords == [0.0, 0.0, 0.0]
        assert line.end.coords == [10.0, 10.0, 10.0]

    def test_line_has_object_ids(self):
        begin = WrappedPoint3D(point_3d=Point3D(value="0.0;0.0;0.0"))
        end = WrappedPoint3D(point_3d=Point3D(value="10.0;10.0;10.0"))
        line = Line(object_ids=ObjectIDs(), begin=begin, end=end)
        assert isinstance(line.object_ids, ObjectIDs)
        assert line.object_ids.handle >= 0  # Auto-generated handle


class TestRange:
    def test_range_creation(self):
        org = WrappedPoint3D(point_3d=Point3D(value="0.0;0.0;0.0"))
        end = WrappedPoint3D(point_3d=Point3D(value="100.0;100.0;0.0"))
        range_obj = Range(org=org, end=end)
        assert range_obj.org.coords == [0.0, 0.0, 0.0]
        assert range_obj.end.coords == [100.0, 100.0, 0.0]
