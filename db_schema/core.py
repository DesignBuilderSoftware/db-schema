from __future__ import annotations

import datetime
from typing import Annotated, Optional

from pydantic import ConfigDict, Field, field_serializer
from pydantic_xml import attr, element

from db_schema.attributes import KeyAttributes, NameAttributes
from db_schema.base import BaseModel
from db_schema.geometry import HandlePoint, Line, Point3D, Vertices
from db_schema.hvac.network import HVACNetwork
from db_schema.id import ObjectIDs, current_site_handle
from db_schema.tables import Tables


class dsbXML(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = attr()
    date: datetime.date = attr()
    version: str = attr()
    objects: str = attr()
    site: Site | None = element(tag="Site", default=None)

    @classmethod
    def from_xml(cls, source: str | bytes) -> dsbXML:
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
            return bytes(
                etree.tostring(root, xml_declaration=True, encoding="UTF-8")
            )
        else:
            root = etree.fromstring(xml_output.encode())
            root.tag = "dsbXML"
            return str(
                etree.tostring(
                    root, xml_declaration=True, encoding="UTF-8"
                ).decode("UTF-8")
            )


class Site(BaseModel):
    count: int = attr()
    handle: int = attr()
    attributes: NameAttributes = element(
        tag="Attributes", default_factory=lambda: NameAttributes()
    )
    tables: Tables | None = element(tag="Tables", default=None)
    assembly_library: AssemblyLibrary | None = element(
        tag="AssemblyLibrary", default=None
    )
    buildings: Buildings | None = element(tag="Buildings", default=None)

    @field_serializer("handle")
    def serialize_handle(self, _) -> int:
        return current_site_handle()


class AssemblyLibrary(BaseModel):
    assemblyHandle: int = attr()
    assembly: list[Assembly] = element(tag="Assembly")


class Assembly(BaseModel):
    assemblyHandle: int = attr()
    componentBlockHandle: int = attr()
    reference: str = attr()
    handle_point: HandlePoint = element(tag="HandlePoint")
    component_blocks: ComponentBlocks = element(tag="ComponentBlocks")
    attributes: KeyAttributes | None = element(tag="Attributes", default=None)


class ComponentBlocks(BaseModel):
    component_block: list[ComponentBlock] = element(tag="ComponentBlock")


class ComponentBlock(BaseModel):
    type: str = attr()
    body: Body = element(tag="Body")


class Body(BaseModel):
    volume: float = attr()
    extrusionHeight: float = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element(tag="ObjectIDs")
    )
    vertices: Vertices = element(tag="Vertices")
    surfaces: Surfaces = element(tag="Surfaces")
    void_perimeter_list: VoidPerimeterList | None = element(
        tag="VoidPerimeterList", default=None
    )
    attributes: KeyAttributes | None = element(tag="Attributes", default=None)


class Surfaces(BaseModel):
    surface: list[Surface] = element(tag="Surface")


class Surface(BaseModel):
    type: str = attr()
    area: float = attr()
    alpha: float = attr()
    phi: float = attr()
    defaultopenings: str = attr()
    adjacentPartitionHandle: int = attr()
    thickness: float = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    vertex_indices: str = element()
    hole_indices: str | None = element(default=None)
    openings: Openings | None = element()
    adjacencies: Adjacencies | None = element()
    attributes: KeyAttributes | None = element()


class Openings(BaseModel):
    opening: list[Opening] = element(tag="Opening")


class Opening(BaseModel):
    type: str = attr()
    polygon: Polygon = element(tag="Polygon")
    attributes: KeyAttributes | None = element()
    cfd_segment_list: CFDSegmentList | None = element(tag="CFDSegmentList")


class Adjacencies(BaseModel):
    adjacency: list[Adjacency] = element(tag="Adjacency")


class Adjacency(BaseModel):
    type: str = attr()
    adjacencyDistance: float = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    adjacency_polygon_list: AdjacencyPolygonList = element(
        tag="AdjacencyPolygonList"
    )


class AdjacencyPolygonList(BaseModel):
    polygon: list[Polygon] = element(tag="Polygon")


class Buildings(BaseModel):
    numberOfBuildings: int = attr()
    building: list[Building] = element(tag="Building")


class Building(BaseModel):
    currentComponentBlockHandle: int = attr()
    currentAssemblyInstanceHandle: int = attr()
    currentPlaneHandle: int = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    building_blocks: BuildingBlocks | None = element()
    component_blocks: ComponentBlocks | None = element()
    assembly_instances: AssemblyInstances | None = element()
    profile_outlines: ProfileOutlines | None = element()
    construction_lines: ConstructionLines | None = element()
    planes: Planes | None = element()
    hvac_network: HVACNetwork | None = element()
    bookmark_buildings: BookmarkBuildings | None = element()
    attributes: KeyAttributes = element()


class BuildingBlocks(BaseModel):
    building_block: list[BuildingBlock] = element(tag="BuildingBlock")


class BuildingBlock(BaseModel):
    type: str = attr()
    height: float = attr()
    roofSlope: float = attr()
    roofOverlap: float = attr()
    roofType: str = attr()
    wallSlope: float = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    component_blocks: ComponentBlocks | None = element()
    cfd_fans: CFDFans | None = element()
    assembly_instances: AssemblyInstances | None = element()
    profile_outlines: ProfileOutlines | None = element()
    internal_partitions: InternalPartitions | None = element()
    void_bodies: VoidBodies | None = element()
    zones: Zones | None = element()
    profile_body: ProfileBody | None = element()
    perimeter: Perimeter | None = element()
    Baseprofile_body: BaseProfileBody | None = element()
    attributes: KeyAttributes = element()


class InternalPartitions(BaseModel):
    internal_partition: list[InternalPartition] = element(
        tag="InternalPartition"
    )


class InternalPartition(BaseModel):
    type: str = attr()
    height: float = attr()
    area: float = attr()
    floatingPartition: bool = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    start_point: Point3D = element()
    end_point: Point3D = element()


class Zones(BaseModel):
    zone: list[Zone] = element(tag="Zone")


class Zone(BaseModel):
    parentZoneHandle: str = attr()
    inheritedZoneHandle: str = attr()
    planExtrusion: str = attr()
    innerSurfaceMode: str = attr()
    body: Body = element()
    light_sensor_one: LightSensorOne = element()
    light_sensor_two: LightSensorTwo = element()
    label_position: Point3D = element()
    polygon: Polygon | None = element(default=None)
    inner_surface_body: InnerSurfaceBody | None = element()


class ProfileBody(BaseModel):
    elementSlope: float = attr()
    roofOverlap: float = attr()
    body: Body = element()


class Perimeter(BaseModel):
    polygon: Polygon = element(tag="Polygon")


class BaseProfileBody(BaseModel):
    profile_body: ProfileBody = element()


class Polygon(BaseModel):
    auxiliaryType: str = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    vertices: Vertices | None = element(default=None)
    polygon_holes: PolygonHoles | None = element()


class PolygonHoles(BaseModel):
    polygon_hole: list[PolygonHole] = element(tag="PolygonHole")


class PolygonHole(BaseModel):
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    vertices: Vertices = element()


class LightSensorOne(BaseModel):
    index: int = attr()
    Point3d: str = element()


class LightSensorTwo(BaseModel):
    index: int = attr()
    Point3d: str = element()


class InnerSurfaceBody(BaseModel):
    body: Body = element()


class BookmarkBuildings(BaseModel):
    numberOfBuildings: int = attr()


class ConstructionLines(BaseModel):
    construction_line: list[ConstructionLine] = element(tag="ConstructionLine")


class ConstructionLine(BaseModel):
    line: Line = element()
    planes: CPlanes = element()


class CPlanes(BaseModel):
    polygon: list[Polygon] = element(tag="Polygon")


class Planes(BaseModel):
    plane: list[Plane] = element(tag="Plane")


class Plane(BaseModel):
    type: int = attr()
    polygon: Polygon = element(tag="Polygon")


class AssemblyInstances(BaseModel):
    assembly_instance: list[AssemblyInstance] = element(tag="AssemblyInstance")


class AssemblyInstance(BaseModel):
    assemblyHandle: int = attr()
    reflected: int = attr()
    active: int = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    assembly_instance_transformation_matrix: AssemblyInstanceTransformationMatrix = element()
    attributes: KeyAttributes | None = element()


class AssemblyInstanceTransformationMatrix(BaseModel):
    matrix: Matrix = element()


class Matrix(BaseModel):
    matrix_row: list[str] = element(tag="MatrixRow")


class ProfileOutlines(BaseModel):
    profile_outline: list[ProfileOutline] = element(tag="ProfileOutline")


class ProfileOutline(BaseModel):
    body: Body = element()


class VoidBodies(BaseModel):
    void_body: list[VoidBody] = element(tag="VoidBody")


class VoidBody(BaseModel):
    profile_body: ProfileBody = element()


class VoidPerimeterList(BaseModel):
    polygon: list[Polygon] = element(tag="Polygon")


class CFDFans(BaseModel):
    cfd_fan: list[CFDFan] = element(tag="CFDFan")


class CFDFan(BaseModel):
    component_block: ComponentBlock = element()


class CFDBoundary(BaseModel):
    type: str = attr()
    polygon: Polygon = element(tag="Polygon")
    cfd_boundary_settings: CFDBoundarySettings = element()
    minimum_refinement_region_point: Point3D = element()
    maximum_refinement_region_point: Point3D = element()
    cfd_boundary_component_list: Optional[None] = element(default=None)


class CFDSegmentList(BaseModel):
    cfd_boundary: CFDBoundary = element()


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
