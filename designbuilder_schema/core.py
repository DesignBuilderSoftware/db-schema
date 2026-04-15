from typing import Optional, List, Annotated
from pydantic import field_serializer, Field, ConfigDict
from pydantic_xml import attr, element
from designbuilder_schema.hvac.network import HVACNetwork
from designbuilder_schema.base import BaseModel
from designbuilder_schema.id import ObjectIDs, current_site_handle
from designbuilder_schema.geometry import Point3D, Vertices, Line
from designbuilder_schema.tables import Tables
from designbuilder_schema.attributes import NameAttributes, KeyAttributes
import datetime


class dsbXML(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = attr()
    date: datetime.date = attr()
    version: str = attr()
    objects: str = attr()
    site: Optional["Site"] = element(default=None)

    @classmethod
    def from_xml(cls, source: str | bytes) -> "dsbXML":
        from lxml import etree

        if isinstance(source, (str, bytes)):
            root = etree.fromstring(source)
        else:
            root = source

        instance = super().from_xml_tree(root)
        return instance

    def to_xml(self, **kwargs) -> str | bytes:
        from lxml import etree

        xml_output = super().to_xml(**kwargs)
        if isinstance(xml_output, bytes):
            root = etree.fromstring(xml_output)
            root.tag = "dsbXML"
            return bytes(etree.tostring(root, xml_declaration=True, encoding="UTF-8"))
        else:
            root = etree.fromstring(xml_output.encode())
            root.tag = "dsbXML"
            return str(
                etree.tostring(root, xml_declaration=True, encoding="UTF-8").decode(
                    "UTF-8"
                )
            )


class Site(BaseModel):
    count: int = attr()
    handle: int = attr()
    attributes: "NameAttributes" = element(default_factory=lambda: NameAttributes())
    tables: Optional["Tables"] = element(default=None)
    assembly_library: Optional["AssemblyLibrary"] = element(default=None)
    buildings: Optional["Buildings"] = element(default=None)

    @field_serializer("handle")
    def serialize_handle(self, _) -> int:
        return current_site_handle()


class AssemblyLibrary(BaseModel):
    assemblyHandle: int = attr()
    Assembly: List["Assembly"] = element(tag="Assembly")


class Assembly(BaseModel):
    assemblyHandle: int = attr()
    componentBlockHandle: int = attr()
    reference: str = attr()
    HandlePoint: "Point3D" = element()
    ComponentBlocks: "ComponentBlocks" = element()
    attributes: "KeyAttributes" = element()


class ComponentBlocks(BaseModel):
    ComponentBlock: List["ComponentBlock"] = element(tag="ComponentBlock")


class ComponentBlock(BaseModel):
    type: str = attr()
    body: "Body" = element()


class Body(BaseModel):
    volume: float = attr()
    extrusionHeight: float = attr()
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    Vertices: "Vertices" = element()
    Surfaces: "Surfaces" = element()
    VoidPerimeterList: Optional["VoidPerimeterList"] = element()
    attributes: Optional["KeyAttributes"] = element()


class Surfaces(BaseModel):
    Surface: List["Surface"] = element(tag="Surface")


class Surface(BaseModel):
    type: str = attr()
    area: float = attr()
    alpha: float = attr()
    phi: float = attr()
    defaultOpenings: str = attr()
    adjacentPartitionHandle: int = attr()
    thickness: float = attr()
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    VertexIndices: str = element()
    HoleIndices: Optional[str] = element(default=None)
    Openings: Optional["Openings"] = element()
    Adjacencies: Optional["Adjacencies"] = element()
    attributes: Optional["KeyAttributes"] = element()


class Openings(BaseModel):
    Opening: List["Opening"] = element(tag="Opening")


class Opening(BaseModel):
    type: str = attr()
    Polygon: "Polygon" = element()
    attributes: Optional["KeyAttributes"] = element()
    CFDSegmentList: Optional["CFDSegmentList"] = element()


class Adjacencies(BaseModel):
    Adjacency: List["Adjacency"] = element(tag="Adjacency")


class Adjacency(BaseModel):
    type: str = attr()
    adjacencyDistance: float = attr()
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    AdjacencyPolygonList: "AdjacencyPolygonList" = element()


class AdjacencyPolygonList(BaseModel):
    Polygon: List["Polygon"] = element(tag="Polygon")


class Buildings(BaseModel):
    numberOfBuildings: int = attr()
    Building: List["Building"] = element(tag="Building")


class Building(BaseModel):
    currentComponentBlockHandle: int = attr()
    currentAssemblyInstanceHandle: int = attr()
    currentPlaneHandle: int = attr()
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    BuildingBlocks: Optional["BuildingBlocks"] = element()
    ComponentBlocks: Optional["ComponentBlocks"] = element()
    AssemblyInstances: Optional["AssemblyInstances"] = element()
    ProfileOutlines: Optional["ProfileOutlines"] = element()
    ConstructionLines: Optional["ConstructionLines"] = element()
    Planes: Optional["Planes"] = element()
    HVACNetwork: Optional["HVACNetwork"] = element()
    BookmarkBuildings: Optional["BookmarkBuildings"] = element()
    attributes: "KeyAttributes" = element()


class BuildingBlocks(BaseModel):
    BuildingBlock: List["BuildingBlock"] = element(tag="BuildingBlock")


class BuildingBlock(BaseModel):
    type: str = attr()
    height: float = attr()
    roofSlope: float = attr()
    roofOverlap: float = attr()
    roofType: str = attr()
    wallSlope: float = attr()
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    ComponentBlocks: Optional["ComponentBlocks"] = element()
    CFDFans: Optional["CFDFans"] = element()
    AssemblyInstances: Optional["AssemblyInstances"] = element()
    ProfileOutlines: Optional["ProfileOutlines"] = element()
    InternalPartitions: Optional["InternalPartitions"] = element()
    VoidBodies: Optional["VoidBodies"] = element()
    Zones: Optional["Zones"] = element()
    ProfileBody: Optional["ProfileBody"] = element()
    Perimeter: Optional["Perimeter"] = element()
    BaseProfileBody: Optional["BaseProfileBody"] = element()
    attributes: "KeyAttributes" = element()


class InternalPartitions(BaseModel):
    InternalPartition: List["InternalPartition"] = element(tag="InternalPartition")


class InternalPartition(BaseModel):
    type: str = attr()
    height: float = attr()
    area: float = attr()
    floatingPartition: bool = attr()
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    StartPoint: "Point3D" = element()
    EndPoint: "Point3D" = element()


class Zones(BaseModel):
    Zone: List["Zone"] = element(tag="Zone")


class Zone(BaseModel):
    parentZoneHandle: str = attr()
    inheritedZoneHandle: str = attr()
    planExtrusion: str = attr()
    innerSurfaceMode: str = attr()
    Body: "Body" = element()
    LightSensorOne: "LightSensorOne" = element()
    LightSensorTwo: "LightSensorTwo" = element()
    LabelPosition: "Point3D" = element()
    Polygon: Optional["Polygon"] = element(default=None)
    InnerSurfaceBody: Optional["InnerSurfaceBody"] = element()


class ProfileBody(BaseModel):
    elementSlope: float = attr()
    roofOverlap: float = attr()
    Body: "Body" = element()


class Perimeter(BaseModel):
    Polygon: "Polygon" = element()


class BaseProfileBody(BaseModel):
    ProfileBody: "ProfileBody" = element()


class Polygon(BaseModel):
    auxiliaryType: str = attr()
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    Vertices: Optional["Vertices"] = element(default=None)
    PolygonHoles: Optional["PolygonHoles"] = element()


class PolygonHoles(BaseModel):
    PolygonHole: List["PolygonHole"] = element(tag="PolygonHole")


class PolygonHole(BaseModel):
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    Vertices: "Vertices" = element()


class LightSensorOne(BaseModel):
    index: int = attr()
    point_3d: str = element()


class LightSensorTwo(BaseModel):
    index: int = attr()
    point_3d: str = element()


class InnerSurfaceBody(BaseModel):
    body: "Body" = element()


class BookmarkBuildings(BaseModel):
    numberOfBuildings: int = attr()


class ConstructionLines(BaseModel):
    construction_line: List["ConstructionLine"] = element(tag="ConstructionLine")


class ConstructionLine(BaseModel):
    line: "Line" = element()
    planes: "CPlanes" = element()


class CPlanes(BaseModel):
    polygon: List["Polygon"] = element(tag="Polygon")


class Planes(BaseModel):
    plane: List["Plane"] = element(tag="Plane")


class Plane(BaseModel):
    type: int = attr()
    polygon: "Polygon" = element()


class AssemblyInstances(BaseModel):
    assembly_instance: List["AssemblyInstance"] = element(tag="AssemblyInstance")


class AssemblyInstance(BaseModel):
    assemblyHandle: int = attr()
    reflected: int = attr()
    active: int = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    assembly_instance_transformation_matrix: "AssemblyInstanceTransformationMatrix" = (
        element()
    )
    attributes: Optional["KeyAttributes"] = element()


class AssemblyInstanceTransformationMatrix(BaseModel):
    matrix: "Matrix" = element()


class Matrix(BaseModel):
    matrix_row: List[str] = element(tag="MatrixRow")


class ProfileOutlines(BaseModel):
    profile_outline: List["ProfileOutline"] = element(tag="ProfileOutline")


class ProfileOutline(BaseModel):
    body: "Body" = element()


class VoidBodies(BaseModel):
    void_body: List["VoidBody"] = element(tag="VoidBody")


class VoidBody(BaseModel):
    profile_body: "ProfileBody" = element()


class VoidPerimeterList(BaseModel):
    polygon: List["Polygon"] = element(tag="Polygon")


class CFDFans(BaseModel):
    cfd_fan: List["CFDFan"] = element(tag="CFDFan")


class CFDFan(BaseModel):
    component_block: "ComponentBlock" = element()


class CFDBoundary(BaseModel):
    type: str = attr()
    polygon: "Polygon" = element()
    cfd_boundary_settings: "CFDBoundarySettings" = element()
    minimum_refinement_region_point: "Point3D" = element()
    maximum_refinement_region_point: "Point3D" = element()
    cfd_boundary_component_list: Optional[None] = element(default=None)


class CFDSegmentList(BaseModel):
    cfd_boundary: "CFDBoundary" = element()


class CFDBoundarySettings(BaseModel):
    temperature: float = attr()
    flow_rate: float = attr()
    x_direction_discharge_angle: float = attr()
    y_direction_discharge_angle: float = attr()
    multi_way_diffuser_discharge_angle: float = attr()
    two_way_diffuser_discharge_direction: int = attr()
    minimum_discharge_velocity: float = attr()
    actual_discharge_velocity: float = attr()
    heat_flux: float = attr()
    pressure: float = attr()
    pressure_type: int = attr()
    moisture_source: float = attr()
    contaminant_source: float = attr()
    relative_humidity: float = attr()
    non_ortho_element_width: float = attr()
    non_ortho_element_height: float = attr()
    non_ortho_face_offset: float = attr()
    non_ortho_element_x_spacing: float = attr()
    non_ortho_element_y_spacing: float = attr()
    non_ortho_element_x_edge_offset: float = attr()
    non_ortho_element_y_edge_offset: float = attr()
    DiffuserElementDimension: float
    RefinementRegionDistance: float
    RefinementRegionLevel: int
