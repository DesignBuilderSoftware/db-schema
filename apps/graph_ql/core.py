from attributes import NameAttributesType
from strawberry import auto
from strawberry.experimental.pydantic import type as strawberry_type
from tables import TablesType

from db_schema.attributes import *
from db_schema.core import DSB, Site

"""@strawberry_type(model=Buildings, all_fields=True)
class BuildingsType:
    pass"""


@strawberry_type(model=Site)
class SiteType:
    count: auto
    handle: auto
    Attributes: NameAttributesType
    Tables: TablesType | None
    # AssemblyLibrary: Optional["AssemblyLibrary"]
    # Buildings: Optional["Buildings"]


@strawberry_type(model=DSB)
class DSBType:
    name: auto
    date: auto
    version: auto
    objects: auto
    Site: SiteType | None


"""

from pydantic import Field
from db_schema.hvac.network import HVACNetwork
from db_schema.base import BaseModel
from db_schema.id import ObjectIDs
from db_schema.geometry import Point3D, Vertices, Line
from db_schema.attributes import KeyAttributes


class AssemblyLibrary(BaseModel):
    assemblyHandle: int
    Assembly: Union["Assembly", List["Assembly"]]


class Assembly(BaseModel):
    assemblyHandle: int
    componentBlockHandle: int
    reference: str
    HandlePoint: "Point3D"
    ComponentBlocks: "ComponentBlocks"
    Attributes: "KeyAttributes"


class ComponentBlocks(BaseModel):
    ComponentBlock: Union["ComponentBlock", List["ComponentBlock"]]


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
    Opening: Union[List["Opening"], "Opening"]


class Opening(BaseModel):
    type: str
    Polygon: "Polygon"
    Attributes: Optional["KeyAttributes"]
    SegmentList: Optional["SegmentList"]


class Adjacencies(BaseModel):
    Adjacency: Union["Adjacency", List["Adjacency"]]


class Adjacency(BaseModel):
    type: str
    adjacencyDistance: float
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    AdjacencyPolygonList: "AdjacencyPolygonList"


class AdjacencyPolygonList(BaseModel):
    Polygon: Union["Polygon", List["Polygon"]]


class Buildings(BaseModel):
    numberOfBuildings: int
    Building: Union["Building", List["Building"]]


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
    BuildingBlock: Union["BuildingBlock", List["BuildingBlock"]]


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
    InternalPartition: Union["InternalPartition", List["InternalPartition"]]


class InternalPartition(BaseModel):
    type: str
    height: float
    area: float
    floatingPartition: bool
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    StartPoint: "Point3D"
    EndPoint: "Point3D"


class Zones(BaseModel):
    Zone: Union["Zone", List["Zone"]]


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
    PolygonHole: Union["PolygonHole", List["PolygonHole"]]


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
    ConstructionLine: Union["ConstructionLine", List["ConstructionLine"], None]


class ConstructionLine(BaseModel):
    Line: "Line"
    Planes: "CPlanes"


class CPlanes(BaseModel):
    Polygon: Union["Polygon", List["Polygon"]]


class Planes(BaseModel):
    Plane: Union["Plane", List["Plane"]]


class Plane(BaseModel):
    type: int
    Polygon: "Polygon"


class AssemblyInstances(BaseModel):
    AssemblyInstance: Union["AssemblyInstance", List["AssemblyInstance"], None]


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
    ProfileOutline: Union["ProfileOutline", List["ProfileOutline"], None]


class ProfileOutline(BaseModel):
    Body: "Body"


class VoidBodies(BaseModel):
    VoidBody: Union["VoidBody", List["VoidBody"]]


class VoidBody(BaseModel):
    ProfileBody: "ProfileBody"


class VoidPerimeterList(BaseModel):
    Polygon: Union["Polygon", List["Polygon"]]


class CFDFans(BaseModel):
    CFDFan: Union["CFDFan", List["CFDFan"]]


class CFDFan(BaseModel):
    ComponentBlock: "ComponentBlock"


class CFDBoundary(BaseModel):
    type: str
    Polygon: "Polygon"
    CFDBoundarySettings: "CFDBoundarySettings"
    MinimumRefinementRegionPoint: "Point3D"
    MaximumRefinementRegionPoint: "Point3D"
    CFDBoundaryComponentList: None


class SegmentList(BaseModel):
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

"""
