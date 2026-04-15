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
    assembly: List["Assembly"] = element(tag="Assembly")


class Assembly(BaseModel):
    assemblyHandle: int = attr()
    componentBlockHandle: int = attr()
    reference: str = attr()
    handle_point: "Point3D" = element()
    component_blocks: "ComponentBlocks" = element()
    attributes: "KeyAttributes" = element()


class ComponentBlocks(BaseModel):
    component_block: List["ComponentBlock"] = element(tag="ComponentBlock")


class ComponentBlock(BaseModel):
    type: str = attr()
    body: "Body" = element()


class Body(BaseModel):
    volume: float = attr()
    extrusionHeight: float = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    vertices: "Vertices" = element()
    surfaces: "Surfaces" = element()
    void_perimeter_list: Optional["VoidPerimeterList"] = element(tag="VoidPerimeterList")
    attributes: Optional["KeyAttributes"] = element()


class Surfaces(BaseModel):
    surface: List["Surface"] = element(tag="Surface")


class Surface(BaseModel):
    type: str = attr()
    area: float = attr()
    alpha: float = attr()
    phi: float = attr()
    defaultopenings: str = attr()
    adjacentPartitionHandle: int = attr()
    thickness: float = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    vertex_indices: str = element()
    hole_indices: Optional[str] = element(default=None)
    openings: Optional["Openings"] = element()
    adjacencies: Optional["Adjacencies"] = element()
    attributes: Optional["KeyAttributes"] = element()


class Openings(BaseModel):
    opening: List["Opening"] = element(tag="Opening")


class Opening(BaseModel):
    type: str = attr()
    polygon: "Polygon" = element(tag="Polygon")
    attributes: Optional["KeyAttributes"] = element()
    cfd_segment_list: Optional["CFDSegmentList"] = element(tag="CFDSegmentList")


class Adjacencies(BaseModel):
    adjacency: List["Adjacency"] = element(tag="Adjacency")


class Adjacency(BaseModel):
    type: str = attr()
    adjacencyDistance: float = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    adjacency_polygon_list: "AdjacencyPolygonList" = element(tag="AdjacencyPolygonList")


class AdjacencyPolygonList(BaseModel):
    polygon: List["Polygon"] = element(tag="Polygon")


class Buildings(BaseModel):
    numberOfBuildings: int = attr()
    building: List["Building"] = element(tag="Building")


class Building(BaseModel):
    currentComponentBlockHandle: int = attr()
    currentAssemblyInstanceHandle: int = attr()
    currentPlaneHandle: int = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    building_blocks: Optional["BuildingBlocks"] = element()
    component_blocks: Optional["ComponentBlocks"] = element()
    assembly_instances: Optional["AssemblyInstances"] = element()
    profile_outlines: Optional["ProfileOutlines"] = element()
    construction_lines: Optional["ConstructionLines"] = element()
    planes: Optional["Planes"] = element()
    hvac_network: Optional["HVACNetwork"] = element()
    bookmark_buildings: Optional["BookmarkBuildings"] = element()
    attributes: "KeyAttributes" = element()


class BuildingBlocks(BaseModel):
    building_block: List["BuildingBlock"] = element(tag="BuildingBlock")


class BuildingBlock(BaseModel):
    type: str = attr()
    height: float = attr()
    roofSlope: float = attr()
    roofOverlap: float = attr()
    roofType: str = attr()
    wallSlope: float = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    component_blocks: Optional["ComponentBlocks"] = element()
    cfd_fans: Optional["CFDFans"] = element()
    assembly_instances: Optional["AssemblyInstances"] = element()
    profile_outlines: Optional["ProfileOutlines"] = element()
    internal_partitions: Optional["InternalPartitions"] = element()
    void_bodies: Optional["VoidBodies"] = element()
    zones: Optional["Zones"] = element()
    profile_body: Optional["ProfileBody"] = element()
    perimeter: Optional["Perimeter"] = element()
    Baseprofile_body: Optional["BaseProfileBody"] = element()
    attributes: "KeyAttributes" = element()


class InternalPartitions(BaseModel):
    internal_partition: List["InternalPartition"] = element(tag="InternalPartition")


class InternalPartition(BaseModel):
    type: str = attr()
    height: float = attr()
    area: float = attr()
    floatingPartition: bool = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    start_point: "Point3D" = element()
    end_point: "Point3D" = element()


class Zones(BaseModel):
    zone: List["Zone"] = element(tag="Zone")


class Zone(BaseModel):
    parentZoneHandle: str = attr()
    inheritedZoneHandle: str = attr()
    planExtrusion: str = attr()
    innerSurfaceMode: str = attr()
    body: "Body" = element()
    light_sensor_one: "LightSensorOne" = element()
    light_sensor_two: "LightSensorTwo" = element()
    label_position: "Point3D" = element()
    polygon: Optional["Polygon"] = element(default=None)
    inner_surface_body: Optional["InnerSurfaceBody"] = element()


class ProfileBody(BaseModel):
    elementSlope: float = attr()
    roofOverlap: float = attr()
    body: "Body" = element()


class Perimeter(BaseModel):
    polygon: "Polygon" = element(tag="Polygon")


class BaseProfileBody(BaseModel):
    profile_body: "ProfileBody" = element()


class Polygon(BaseModel):
    auxiliaryType: str = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    vertices: Optional["Vertices"] = element(default=None)
    polygon_holes: Optional["PolygonHoles"] = element()


class PolygonHoles(BaseModel):
    polygon_hole: List["PolygonHole"] = element(tag="PolygonHole")


class PolygonHole(BaseModel):
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    vertices: "Vertices" = element()


class LightSensorOne(BaseModel):
    index: int = attr()
    Point3d: str = element()


class LightSensorTwo(BaseModel):
    index: int = attr()
    Point3d: str = element()


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
    polygon: "Polygon" = element(tag="Polygon")


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
    polygon: "Polygon" = element(tag="Polygon")
    cfd_boundary_settings: "CFDBoundarySettings" = element()
    minimum_refinement_region_point: "Point3D" = element()
    maximum_refinement_region_point: "Point3D" = element()
    cfd_boundary_component_list: Optional[None] = element(default=None)


class CFDSegmentList(BaseModel):
    cfd_boundary: "CFDBoundary" = element()


class CFDBoundarySettings(BaseModel):
    temperature: float = attr()
    flowRate: float = attr()
    xDirectionDischargeAngle: float = attr()
    yDirectionDischargeAngle: float = attr()
    multiWayDiffuserDischargeAngle: float = attr()
    twoWayDiffuserDischargeDirection: int = attr()
    minimumDischargeVelocity: float = attr()
    actualDischargeVelocity: float = attr()
    heatFlux: float = attr()
    pressure: float = attr()
    pressureType: int = attr()
    moistureSource: float = attr()
    contaminantSource: float = attr()
    relativeHumidity: float = attr()
    nonOrthoElementWidth: float = attr()
    nonOrthoElementHeight: float = attr()
    nonOrthoFaceOffset: float = attr()
    nonOrthoElementXSpacing: float = attr()
    nonOrthoElementYSpacing: float = attr()
    nonOrthoElementXEdgeOffset: float = attr()
    nonOrthoElementYEdgeOffset: float = attr()
    diffuser_element_dimension: float
    refinement_region_distance: float
    refinement_region_level: int
