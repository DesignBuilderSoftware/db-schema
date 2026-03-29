"""
core.py
====================================
The core module of the designbuilder_schema
"""

from typing import Optional, List, Annotated
from pydantic import field_serializer, Field
from designbuilder_schema.hvac.network import HVACNetwork
from designbuilder_schema.base import BaseModel, AlwaysList
from designbuilder_schema.id import ObjectIDs, current_site_handle
from designbuilder_schema.geometry import Point3D, Vertices, Line
from designbuilder_schema.tables import Tables
from designbuilder_schema.attributes import NameAttributes, KeyAttributes
import datetime


class DSB(BaseModel):
    name: str
    date: datetime.date
    version: str
    objects: str
    Site: Optional["Site"]


class Site(BaseModel):
    count: int
    handle: int
    Attributes: "NameAttributes"
    Tables: Optional["Tables"]
    AssemblyLibrary: Optional["AssemblyLibrary"]
    Buildings: Optional["Buildings"]

    @field_serializer("handle")
    def serialize_handle(self, _) -> int:
        return current_site_handle()


class AssemblyLibrary(BaseModel):
    assemblyHandle: int
    Assembly: AlwaysList["Assembly"]


class Assembly(BaseModel):
    assemblyHandle: int
    componentBlockHandle: int
    reference: str
    HandlePoint: "Point3D"
    ComponentBlocks: "ComponentBlocks"
    Attributes: "KeyAttributes"


class ComponentBlocks(BaseModel):
    ComponentBlock: AlwaysList["ComponentBlock"]


class ComponentBlock(BaseModel):
    type: str
    Body: "Body"


class Body(BaseModel):
    volume: float
    extrusionHeight: float
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    Vertices: "Vertices"
    Surfaces: "Surfaces"
    VoidPerimeterList: Optional["VoidPerimeterList"]
    Attributes: Optional["KeyAttributes"]


class Surfaces(BaseModel):
    Surface: List["Surface"]


class Surface(BaseModel):
    type: str
    area: float
    alpha: float
    phi: float
    defaultOpenings: str
    adjacentPartitionHandle: int
    thickness: float
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    VertexIndices: str  # vertex indexes of parent body
    HoleIndices: Optional[str]
    Openings: Optional["Openings"]
    Adjacencies: Optional["Adjacencies"]
    Attributes: Optional["KeyAttributes"]


class Openings(BaseModel):
    Opening: AlwaysList["Opening"]


class Opening(BaseModel):
    type: str
    Polygon: "Polygon"
    Attributes: Optional["KeyAttributes"]
    SegmentList: Optional["CFDSegmentList"]


class Adjacencies(BaseModel):
    Adjacency: AlwaysList["Adjacency"]


class Adjacency(BaseModel):
    type: str
    adjacencyDistance: float
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    AdjacencyPolygonList: "AdjacencyPolygonList"


class AdjacencyPolygonList(BaseModel):
    Polygon: AlwaysList["Polygon"]


class Buildings(BaseModel):
    numberOfBuildings: int
    Building: AlwaysList["Building"]


class Building(BaseModel):
    currentComponentBlockHandle: int
    currentAssemblyInstanceHandle: int
    currentPlaneHandle: int
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    BuildingBlocks: Optional["BuildingBlocks"]
    ComponentBlocks: Optional["ComponentBlocks"]
    AssemblyInstances: Optional["AssemblyInstances"]
    ProfileOutlines: Optional["ProfileOutlines"]  # OutlineBlocks
    ConstructionLines: Optional["ConstructionLines"]
    Planes: Optional["Planes"]
    HVACNetwork: Optional["HVACNetwork"]
    BookmarkBuildings: Optional["BookmarkBuildings"]
    Attributes: "KeyAttributes"


class BuildingBlocks(BaseModel):
    BuildingBlock: AlwaysList["BuildingBlock"]


class BuildingBlock(BaseModel):
    type: str
    height: float
    roofSlope: float
    roofOverlap: float
    roofType: str
    wallSlope: float
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    ComponentBlocks: Optional["ComponentBlocks"]
    CFDFans: Optional["CFDFans"]
    AssemblyInstances: Optional["AssemblyInstances"]
    ProfileOutlines: Optional["ProfileOutlines"]
    InternalPartitions: Optional["InternalPartitions"]
    VoidBodies: Optional["VoidBodies"]
    Zones: Optional["Zones"]
    ProfileBody: Optional["ProfileBody"]
    Perimeter: Optional["Perimeter"]
    BaseProfileBody: Optional["BaseProfileBody"]
    Attributes: "KeyAttributes"


class InternalPartitions(BaseModel):
    InternalPartition: AlwaysList["InternalPartition"]


class InternalPartition(BaseModel):
    type: str
    height: float
    area: float
    floatingPartition: bool
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    StartPoint: "Point3D"
    EndPoint: "Point3D"


class Zones(BaseModel):
    Zone: AlwaysList["Zone"]


class Zone(BaseModel):
    parentZoneHandle: str
    inheritedZoneHandle: str
    planExtrusion: str
    innerSurfaceMode: str
    Body: "Body"
    LightSensorOne: "LightSensorOne"
    LightSensorTwo: "LightSensorTwo"
    LabelPosition: "Point3D"
    Polygon: Optional["Polygon"]
    InnerSurfaceBody: Optional["InnerSurfaceBody"]


class ProfileBody(BaseModel):
    elementSlope: float
    roofOverlap: float
    Body: "Body"


class Perimeter(BaseModel):
    Polygon: "Polygon"


class BaseProfileBody(BaseModel):
    ProfileBody: "ProfileBody"


class Polygon(BaseModel):
    auxiliaryType: str
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    Vertices: Optional["Vertices"]
    PolygonHoles: Optional["PolygonHoles"]


class PolygonHoles(BaseModel):
    PolygonHole: AlwaysList["PolygonHole"]


class PolygonHole(BaseModel):
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    Vertices: "Vertices"


class LightSensorOne(BaseModel):
    index: int
    Point3D: str


class LightSensorTwo(BaseModel):
    index: int
    Point3D: str


class InnerSurfaceBody(BaseModel):
    Body: "Body"


class BookmarkBuildings(BaseModel):
    numberOfBuildings: int


class ConstructionLines(BaseModel):
    ConstructionLine: AlwaysList["ConstructionLine"]


class ConstructionLine(BaseModel):
    Line: "Line"
    Planes: "CPlanes"


class CPlanes(BaseModel):
    Polygon: AlwaysList["Polygon"]


class Planes(BaseModel):
    Plane: AlwaysList["Plane"]


class Plane(BaseModel):
    type: int
    Polygon: "Polygon"


class AssemblyInstances(BaseModel):
    AssemblyInstance: AlwaysList["AssemblyInstance"]


class AssemblyInstance(BaseModel):
    assemblyHandle: int
    reflected: int
    active: int
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    AssemblyInstanceTransformationMatrix: "AssemblyInstanceTransformationMatrix"
    Attributes: Optional["KeyAttributes"]


class AssemblyInstanceTransformationMatrix(BaseModel):
    Matrix: "Matrix"


class Matrix(BaseModel):
    MatrixRow: List[str]


class ProfileOutlines(BaseModel):
    ProfileOutline: AlwaysList["ProfileOutline"]


class ProfileOutline(BaseModel):
    Body: "Body"


class VoidBodies(BaseModel):
    VoidBody: AlwaysList["VoidBody"]


class VoidBody(BaseModel):
    ProfileBody: "ProfileBody"


class VoidPerimeterList(BaseModel):
    Polygon: AlwaysList["Polygon"]


class CFDFans(BaseModel):
    CFDFan: AlwaysList["CFDFan"]


class CFDFan(BaseModel):
    ComponentBlock: "ComponentBlock"


class CFDBoundary(BaseModel):
    type: str
    Polygon: "Polygon"
    CFDBoundarySettings: "CFDBoundarySettings"
    MinimumRefinementRegionPoint: "Point3D"
    MaximumRefinementRegionPoint: "Point3D"
    CFDBoundaryComponentList: None


class CFDSegmentList(BaseModel):
    CFDBoundary: "CFDBoundary"


class CFDBoundarySettings(BaseModel):
    Temperature: float
    FlowRate: float
    XDirectionDischargeAngle: float
    YDirectionDischargeAngle: float
    MultiWayDiffuserDischargeAngle: float
    TwoWayDiffuserDischargeDirection: int
    MinimumDischargeVelocity: float
    ActualDischargeVelocity: float
    HeatFlux: float
    Pressure: float
    PressureType: int
    MoistureSource: float
    ContaminantSource: float
    RelativeHumidity: float
    NonOrthoElementWidth: float
    NonOrthoElementHeight: float
    NonOrthoFaceOffset: float
    NonOrthoElementXSpacing: float
    NonOrthoElementYSpacing: float
    NonOrthoElementXEdgeOffset: float
    NonOrthoElementYEdgeOffset: float
    DiffuserElementDimension: float
    RefinementRegionDistance: float
    RefinementRegionLevel: int
