from __future__ import annotations

import datetime
from typing import Annotated

from pydantic import ConfigDict, Field, field_serializer, field_validator
from pydantic_xml import attr, element

from dsbxml.attributes import KeyAttributes, NameAttributes
from dsbxml.base import BaseModel
from dsbxml.geometry import HandlePoint, Line, Vertices, WrappedPoint3D
from dsbxml.hvac.network import HVACNetwork
from dsbxml.id import ObjectIDs, current_site_handle
from dsbxml.tables import Tables


class dsbXML(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = attr()
    date: datetime.date = attr()
    version: str = attr()
    objects: str = attr()
    site: Site | None = element(tag="Site", default=None)

    @classmethod
    def from_xml(cls, source: str | bytes) -> dsbXML:  # pylint: disable=arguments-differ
        from lxml import etree

        if isinstance(source, (str, bytes)):
            # huge_tree: large models can contain a single text node over
            # libxml2's default 10 MB limit, which it otherwise refuses with
            # "xmlSAX2Characters: huge text node". DesignBuilder's own files
            # are trusted input, so lifting the limit is acceptable here.
            root = etree.fromstring(source, parser=etree.XMLParser(huge_tree=True))
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
        root = etree.fromstring(xml_output.encode())
        root.tag = "dsbXML"
        return str(etree.tostring(root, xml_declaration=True, encoding="UTF-8").decode("UTF-8"))


class Site(BaseModel):
    count: int = attr()
    handle: int = attr()
    attributes: NameAttributes = element(
        tag="Attributes", default_factory=lambda: NameAttributes()
    )
    tables: Tables | None = element(tag="Tables", default=None)
    assembly_library: AssemblyLibrary | None = element(tag="AssemblyLibrary", default=None)
    buildings: Buildings | None = element(tag="Buildings", default=None)

    @field_serializer("handle")
    def serialize_handle(self, _) -> int:
        return current_site_handle()


class AssemblyLibrary(BaseModel):
    assemblyHandle: int = attr()
    # DesignBuilder writes <AssemblyLibrary assemblyHandle="0"/> with no
    # <Assembly> children when a model has no assemblies.
    assembly: list[Assembly] = element(tag="Assembly", default_factory=list)


class Assembly(BaseModel):
    assemblyHandle: int = attr()
    componentBlockHandle: int = attr()
    reference: str = attr()
    handle_point: HandlePoint = element(tag="HandlePoint")
    component_blocks: ComponentBlocks = element(tag="ComponentBlocks")
    attributes: KeyAttributes | None = element(tag="Attributes", default=None)


class ComponentBlocks(BaseModel):
    component_block: list[ComponentBlock] = element(tag="ComponentBlock", default_factory=list)


class ComponentBlock(BaseModel):
    type: str = attr()
    body: Body = element(tag="Body")


class Body(BaseModel):
    volume: float = attr()
    extrusionHeight: float = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(
        tag="ObjectIDs"
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
    defaultopenings: str | None = attr(default=None)
    adjacentPartitionHandle: int = attr()
    thickness: float = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(
        tag="ObjectIDs"
    )
    vertex_indices: str | None = element(tag="VertexIndices", default=None)
    hole_indices: str | None = element(tag="HoleIndices", default=None)
    openings: Openings | None = element(tag="Openings", default=None)
    adjacencies: Adjacencies | None = element(tag="Adjacencies", default=None)
    attributes: KeyAttributes | None = element(tag="Attributes", default=None)


class Openings(BaseModel):
    opening: list[Opening] = element(tag="Opening", default_factory=list)


class Opening(BaseModel):
    type: str = attr()
    polygon: Polygon = element(tag="Polygon")
    attributes: KeyAttributes | None = element(tag="Attributes", default=None)
    cfd_segment_list: CFDSegmentList | None = element(tag="CFDSegmentList", default=None)


class Adjacencies(BaseModel):
    adjacency: list[Adjacency] = element(tag="Adjacency", default_factory=list)


class Adjacency(BaseModel):
    type: str = attr()
    adjacencyDistance: float = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(
        tag="ObjectIDs"
    )
    adjacency_polygon_list: AdjacencyPolygonList = element(tag="AdjacencyPolygonList")


class AdjacencyPolygonList(BaseModel):
    polygon: list[Polygon] = element(tag="Polygon")


class Buildings(BaseModel):
    numberOfBuildings: int | None = attr(default=None)
    building: list[Building] = element(tag="Building", default_factory=list)

    @field_validator("numberOfBuildings", mode="before")
    @classmethod
    def _coerce_empty_int(cls, v):
        return None if v == "" else v


class Building(BaseModel):
    currentComponentBlockHandle: int = attr()
    currentAssemblyInstanceHandle: int = attr()
    currentPlaneHandle: int = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(
        tag="ObjectIDs"
    )
    building_blocks: BuildingBlocks | None = element(tag="BuildingBlocks", default=None)
    component_blocks: ComponentBlocks | None = element(tag="ComponentBlocks", default=None)
    assembly_instances: AssemblyInstances | None = element(
        tag="AssemblyInstances", default=None
    )
    profile_outlines: ProfileOutlines | None = element(tag="ProfileOutlines", default=None)
    construction_lines: ConstructionLines | None = element(
        tag="ConstructionLines", default=None
    )
    planes: Planes | None = element(tag="Planes", default=None)
    hvac_network: HVACNetwork | None = element(tag="HVACNetwork", default=None)
    bookmark_buildings: BookmarkBuildings | None = element(
        tag="BookmarkBuildings", default=None
    )
    attributes: KeyAttributes | None = element(tag="Attributes", default=None)


class BuildingBlocks(BaseModel):
    building_block: list[BuildingBlock] = element(tag="BuildingBlock")


class BuildingBlock(BaseModel):
    type: str = attr()
    height: float = attr()
    roofSlope: float = attr()
    roofOverlap: float = attr()
    roofType: str = attr()
    wallSlope: float = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(
        tag="ObjectIDs"
    )
    component_blocks: ComponentBlocks | None = element(tag="ComponentBlocks", default=None)
    cfd_fans: CFDFans | None = element(tag="CFDFans", default=None)
    assembly_instances: AssemblyInstances | None = element(
        tag="AssemblyInstances", default=None
    )
    profile_outlines: ProfileOutlines | None = element(tag="ProfileOutlines", default=None)
    internal_partitions: InternalPartitions | None = element(
        tag="InternalPartitions", default=None
    )
    void_bodies: VoidBodies | None = element(tag="VoidBodies", default=None)
    zones: Zones | None = element(tag="Zones", default=None)
    profile_body: ProfileBody | None = element(tag="ProfileBody", default=None)
    perimeter: Perimeter | None = element(tag="Perimeter", default=None)
    base_profile_body: BaseProfileBody | None = element(tag="BaseProfileBody", default=None)
    attributes: KeyAttributes | None = element(tag="Attributes", default=None)


class InternalPartitions(BaseModel):
    internal_partition: list[InternalPartition] = element(
        tag="InternalPartition", default_factory=list
    )


class InternalPartition(BaseModel):
    type: str = attr()
    height: float = attr()
    area: float = attr()
    floatingPartition: bool = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(
        tag="ObjectIDs"
    )
    start_point: WrappedPoint3D | None = element(tag="StartPoint", default=None)
    end_point: WrappedPoint3D | None = element(tag="EndPoint", default=None)


class Zones(BaseModel):
    zone: list[Zone] = element(tag="Zone")


class Zone(BaseModel):
    parentZoneHandle: str = attr()
    inheritedZoneHandle: str = attr()
    planExtrusion: str = attr()
    innerSurfaceMode: str = attr()
    body: Body = element(tag="Body")
    light_sensor_one: LightSensorOne = element(tag="LightSensorOne")
    light_sensor_two: LightSensorTwo = element(tag="LightSensorTwo")
    label_position: WrappedPoint3D | None = element(tag="LabelPosition", default=None)
    polygon: Polygon | None = element(tag="Polygon", default=None)
    inner_surface_body: InnerSurfaceBody | None = element(tag="InnerSurfaceBody", default=None)


class ProfileBody(BaseModel):
    elementSlope: float = attr()
    roofOverlap: float = attr()
    body: Body = element(tag="Body")


class Perimeter(BaseModel):
    polygon: Polygon = element(tag="Polygon")


class BaseProfileBody(BaseModel):
    profile_body: ProfileBody = element(tag="ProfileBody")


class Polygon(BaseModel):
    auxiliaryType: str = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(
        tag="ObjectIDs"
    )
    vertices: Vertices | None = element(tag="Vertices", default=None)
    polygon_holes: PolygonHoles | None = element(tag="PolygonHoles", default=None)


class PolygonHoles(BaseModel):
    polygon_hole: list[PolygonHole] = element(tag="PolygonHole", default_factory=list)


class PolygonHole(BaseModel):
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(
        tag="ObjectIDs"
    )
    vertices: Vertices = element(tag="Vertices")


class LightSensorOne(BaseModel):
    index: int = attr()
    Point3d: str = element(tag="Point3D")


class LightSensorTwo(BaseModel):
    index: int = attr()
    Point3d: str = element(tag="Point3D")


class InnerSurfaceBody(BaseModel):
    body: Body = element(tag="Body")


class BookmarkBuildings(BaseModel):
    numberOfBuildings: int = attr()


class ConstructionLines(BaseModel):
    construction_line: list[ConstructionLine] = element(
        tag="ConstructionLine", default_factory=list
    )


class ConstructionLine(BaseModel):
    line: Line = element(tag="Line")
    planes: CPlanes = element(tag="Planes")


class CPlanes(BaseModel):
    polygon: list[Polygon] = element(tag="Polygon")


class Planes(BaseModel):
    plane: list[Plane] = element(tag="Plane", default_factory=list)


class Plane(BaseModel):
    type: int = attr()
    polygon: Polygon = element(tag="Polygon")


class AssemblyInstances(BaseModel):
    assembly_instance: list[AssemblyInstance] = element(
        tag="AssemblyInstance", default_factory=list
    )


class AssemblyInstance(BaseModel):
    assemblyHandle: int = attr()
    reflected: int = attr()
    active: int = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(
        tag="ObjectIDs"
    )
    assembly_instance_transformation_matrix: AssemblyInstanceTransformationMatrix = element(
        tag="AssemblyInstanceTransformationMatrix"
    )
    attributes: KeyAttributes | None = element(tag="Attributes", default=None)


class AssemblyInstanceTransformationMatrix(BaseModel):
    matrix: Matrix = element(tag="Matrix")


class Matrix(BaseModel):
    matrix_row: list[str] = element(tag="MatrixRow")


class ProfileOutlines(BaseModel):
    profile_outline: list[ProfileOutline] = element(tag="ProfileOutline", default_factory=list)


class ProfileOutline(BaseModel):
    body: Body = element(tag="Body")


class VoidBodies(BaseModel):
    void_body: list[VoidBody] = element(tag="VoidBody", default_factory=list)


class VoidBody(BaseModel):
    profile_body: ProfileBody = element(tag="ProfileBody")


class VoidPerimeterList(BaseModel):
    polygon: list[Polygon] = element(tag="Polygon", default_factory=list)


class CFDFans(BaseModel):
    cfd_fan: list[CFDFan] = element(tag="CFDFan", default_factory=list)


class CFDFan(BaseModel):
    component_block: ComponentBlock = element(tag="ComponentBlock")


class CFDBoundary(BaseModel):
    type: str = attr()
    polygon: Polygon = element(tag="Polygon")
    cfd_boundary_settings: CFDBoundarySettings = element(tag="CFDBoundarySettings")
    minimum_refinement_region_point: WrappedPoint3D = element(
        tag="MinimumRefinementRegionPoint"
    )
    maximum_refinement_region_point: WrappedPoint3D = element(
        tag="MaximumRefinementRegionPoint"
    )
    cfd_boundary_component_list: None = element(tag="CFDBoundaryComponentList", default=None)


class CFDSegmentList(BaseModel):
    cfd_boundary: CFDBoundary = element(tag="CFDBoundary")


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
    diffuser_element_dimension: float = attr()
    refinement_region_distance: float = attr()
    refinement_region_level: int = attr()
