from pydantic import BaseModel
from typing import Optional, List, Any
import datetime


class dbXML(BaseModel):
    name: str
    date: datetime.date
    version: str
    objects: str
    Site: "Site"


class Site(BaseModel):
    handle: int
    count: int
    Attributes: "Attributes"
    Tables: "Tables"
    AssemblyLibrary: "AssemblyLibrary"
    Buildings: "Buildings"


class Attributes(BaseModel):
    Attribute: Any


class Tables(BaseModel):
    Table: "Table"


class AssemblyLibrary(BaseModel):
    assemblyHandle: int
    Assembly: "Assembly"


class Buildings(BaseModel):
    numberOfBuildings: int
    Building: "Building"


class Attribute(BaseModel):
    name: str


class Table(BaseModel):
    name: str
    numberOfFields: int
    Category: str
    FieldName: str
    Row: str


class Assembly(BaseModel):
    assemblyHandle: int
    componentBlockHandle: int
    reference: str
    HandlePoint: "HandlePoint"
    ComponentBlocks: "ComponentBlocks"
    Attributes: "Attributes"


class Building(BaseModel):
    currentComponentBlockHandle: int
    currentAssemblyInstanceHandle: int
    currentPlaneHandle: int
    ObjectIDs: "ObjectIDs"
    BuildingBlocks: "BuildingBlocks"
    ComponentBlocks: "ComponentBlocks"
    AssemblyInstances: "AssemblyInstances"
    ProfileOutlines: "ProfileOutlines"
    ConstructionLines: "ConstructionLines"
    HVACNetwork: "HVACNetwork"
    BookmarkBuildings: "BookmarkBuildings"
    Attributes: "Attributes"


class Category(BaseModel):
    pass


class FieldName(BaseModel):
    pass


class Row(BaseModel):
    pass


class HandlePoint(BaseModel):
    Point3D: str


class ComponentBlocks(BaseModel):
    ComponentBlock: "ComponentBlock"


class ObjectIDs(BaseModel):
    handle: int
    buildingHandle: int
    buildingBlockHandle: int
    zoneHandle: int
    surfaceIndex: int
    openingIndex: int


class BuildingBlocks(BaseModel):
    BuildingBlock: "BuildingBlock"


class AssemblyInstances(BaseModel):
    AssemblyInstance: "AssemblyInstance"


class ProfileOutlines(BaseModel):
    ProfileOutline: "ProfileOutline"


class ConstructionLines(BaseModel):
    ConstructionLine: "ConstructionLine"


class HVACNetwork(BaseModel):
    ObjectHandle: int
    ObjectIDs: "ObjectIDs"
    HVACLoops: "HVACLoops"
    HVACZoneGroups: "HVACZoneGroups"


class BookmarkBuildings(BaseModel):
    numberOfBuildings: int


class Point3D(BaseModel):
    pass


class ComponentBlock(BaseModel):
    type: str
    Body: "Body"


class BuildingBlock(BaseModel):
    type: str
    height: float
    roofSlope: float
    roofOverlap: float
    roofType: str
    wallSlope: float
    ObjectIDs: "ObjectIDs"
    ComponentBlocks: "ComponentBlocks"
    AssemblyInstances: "AssemblyInstances"
    ProfileOutlines: "ProfileOutlines"
    InternalPartitions: "InternalPartitions"
    VoidBodies: "VoidBodies"
    Zones: "Zones"
    ProfileBody: "ProfileBody"
    Perimeter: "Perimeter"
    BaseProfileBody: "BaseProfileBody"
    Attributes: "Attributes"


class AssemblyInstance(BaseModel):
    assemblyHandle: int
    reflected: int
    active: int
    ObjectIDs: "ObjectIDs"
    AssemblyInstanceTransformationMatrix: "AssemblyInstanceTransformationMatrix"
    Attributes: "Attributes"


class ProfileOutline(BaseModel):
    Body: "Body"


class ConstructionLine(BaseModel):
    Line: "Line"
    Planes: "Planes"


class ObjectHandle(BaseModel):
    pass


class HVACLoops(BaseModel):
    HVACLoop: "HVACLoop"
    HVACVRFLoop: "HVACVRFLoop"


class HVACZoneGroups(BaseModel):
    HVACZoneGroup: "HVACZoneGroup"


class Body(BaseModel):
    volume: float
    extrusionHeight: float
    ObjectIDs: "ObjectIDs"
    Vertices: "Vertices"
    Surfaces: "Surfaces"
    VoidPerimeterList: "VoidPerimeterList"
    Attributes: "Attributes"


class InternalPartitions(BaseModel):
    InternalPartition: "InternalPartition"


class VoidBodies(BaseModel):
    VoidBody: "VoidBody"


class Zones(BaseModel):
    Zone: "Zone"


class ProfileBody(BaseModel):
    elementSlope: float
    roofOverlap: float
    Body: "Body"


class Perimeter(BaseModel):
    Polygon: "Polygon"


class BaseProfileBody(BaseModel):
    ProfileBody: "ProfileBody"


class AssemblyInstanceTransformationMatrix(BaseModel):
    Matrix: "Matrix"


class Line(BaseModel):
    ObjectIDs: "ObjectIDs"
    Begin: "Begin"
    End: "End"


class Planes(BaseModel):
    Polygon: "Polygon"


class HVACLoop(BaseModel):
    currentSubLoopIndex: int
    loopType: int
    plantLoopType: int
    numberOfFlowNodes: int
    ObjectIDs: "ObjectIDs"
    Origin: "Origin"
    PlantOperationSchemes: "PlantOperationSchemes"
    DemandSubLoop: "DemandSubLoop"
    SupplySubLoop: "SupplySubLoop"
    Attributes: "Attributes"


class HVACVRFLoop(BaseModel):
    ObjectIDs: "ObjectIDs"
    Origin: "Origin"
    VRFAirConditionerUnit: "VRFAirConditionerUnit"
    HVACConnections: "HVACConnections"
    Attributes: "Attributes"


class HVACZoneGroup(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: "ZoneComponentAttributeList"
    ValidZoneGroup: int
    Width: float
    Height: float
    Origin: "Origin"
    BuildingZoneHandleList: "BuildingZoneHandleList"
    ZoneElementList: "ZoneElementList"
    ZoneGroupAttributes: "ZoneGroupAttributes"


class Vertices(BaseModel):
    Point3D: str


class Surfaces(BaseModel):
    Surface: "Surface"


class VoidPerimeterList(BaseModel):
    Polygon: "Polygon"


class InternalPartition(BaseModel):
    type: str
    height: float
    area: float
    floatingPartition: str
    ObjectIDs: "ObjectIDs"
    StartPoint: "StartPoint"
    EndPoint: "EndPoint"


class VoidBody(BaseModel):
    ProfileBody: "ProfileBody"


class Zone(BaseModel):
    parentZoneHandle: int
    inheritedZoneHandle: int
    planExtrusion: str
    innerSurfaceMode: str
    Body: "Body"
    LightSensorOne: "LightSensorOne"
    LightSensorTwo: "LightSensorTwo"
    LabelPosition: "LabelPosition"
    Polygon: "Polygon"
    InnerSurfaceBody: "InnerSurfaceBody"


class Polygon(BaseModel):
    auxiliaryType: int
    ObjectIDs: "ObjectIDs"
    Vertices: "Vertices"
    PolygonHoles: "PolygonHoles"


class Matrix(BaseModel):
    MatrixRow: str


class Begin(BaseModel):
    Point3D: str


class End(BaseModel):
    Point3D: str


class Origin(BaseModel):
    Point3D: str


class PlantOperationSchemes(BaseModel):
    PlantOperationScheme: "PlantOperationScheme"


class DemandSubLoop(BaseModel):
    LoopType: int
    PlantLoopType: int
    SubLoopType: int
    ObjectIDs: "ObjectIDs"
    HVACComponents: "HVACComponents"
    HVACConnections: "HVACConnections"
    Attributes: "Attributes"


class SupplySubLoop(BaseModel):
    LoopType: int
    PlantLoopType: int
    SubLoopType: int
    ObjectIDs: "ObjectIDs"
    HVACComponents: "HVACComponents"
    HVACConnections: "HVACConnections"
    Attributes: "Attributes"


class VRFAirConditionerUnit(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str
    RefrigerantConnected: int
    RefrigerantConnectionCoordinate: "RefrigerantConnectionCoordinate"
    WaterCooledCondenser: "WaterCooledCondenser"


class HVACConnections(BaseModel):
    HVACConnection: "HVACConnection"


class ImageRectangle(BaseModel):
    ObjectIDs: "ObjectIDs"
    ImageTextureIndex: int
    MaskTextureIndex: int
    SelectedImageTextureIndex: int
    InactiveImageTextureIndex: int
    Textured: int
    Masked: int
    SelectedImage: int
    InactiveImage: int
    Color: int
    Active: int
    Vertices: "Vertices"
    Range: "Range"


class ConnectingPlantLoopHandle(BaseModel):
    pass


class ConnectingAirLoopHandle(BaseModel):
    pass


class LoopType(BaseModel):
    pass


class SubLoopType(BaseModel):
    pass


class PlantLoopType(BaseModel):
    pass


class AirLoopDuctType(BaseModel):
    pass


class ComponentType(BaseModel):
    pass


class Location(BaseModel):
    pass


class ConnectionOffset(BaseModel):
    pass


class Editable(BaseModel):
    pass


class ZoneBranchFlag(BaseModel):
    pass


class Orientation(BaseModel):
    pass


class WaterInConnectionOrientation(BaseModel):
    pass


class WaterOutConnectionOrientation(BaseModel):
    pass


class AirInConnectionOrientation(BaseModel):
    pass


class AirOutConnectionOrientation(BaseModel):
    pass


class WaterInConnection(BaseModel):
    pass


class WaterOutConnection(BaseModel):
    pass


class AirInConnection(BaseModel):
    pass


class AirOutConnection(BaseModel):
    pass


class WaterInConnected(BaseModel):
    pass


class WaterOutConnected(BaseModel):
    pass


class AirInConnected(BaseModel):
    pass


class AirOutConnected(BaseModel):
    pass


class FanPlacement(BaseModel):
    pass


class WaterInConnectionCoordinate(BaseModel):
    Point3D: str


class WaterOutConnectionCoordinate(BaseModel):
    Point3D: str


class AirInConnectionCoordinate(BaseModel):
    Point3D: str


class AirOutConnectionCoordinate(BaseModel):
    Point3D: str


class ZoneComponentAttributeList(BaseModel):
    pass


class ValidZoneGroup(BaseModel):
    pass


class Width(BaseModel):
    pass


class Height(BaseModel):
    pass


class BuildingZoneHandleList(BaseModel):
    BuildingZoneHandle: int


class ZoneElementList(BaseModel):
    HVACZoneComponent: "HVACZoneComponent"


class ZoneGroupAttributes(BaseModel):
    Attribute: Any


class Surface(BaseModel):
    type: str
    area: float
    alpha: float
    phi: float
    defaultOpenings: str
    adjacentPartitionHandle: int
    thickness: float
    ObjectIDs: "ObjectIDs"
    VertexIndices: str
    HoleIndices: str
    Openings: "Openings"
    Adjacencies: "Adjacencies"
    Attributes: "Attributes"


class StartPoint(BaseModel):
    Point3D: str


class EndPoint(BaseModel):
    Point3D: str


class LightSensorOne(BaseModel):
    index: int
    Point3D: str


class LightSensorTwo(BaseModel):
    index: int
    Point3D: str


class LabelPosition(BaseModel):
    Point3D: str


class InnerSurfaceBody(BaseModel):
    Body: "Body"


class PolygonHoles(BaseModel):
    PolygonHole: "PolygonHole"


class MatrixRow(BaseModel):
    pass


class PlantOperationScheme(BaseModel):
    PlantOperationRanges: "PlantOperationRanges"
    Attributes: "Attributes"


class HVACComponents(BaseModel):
    HVACComponent: "HVACComponent"


class RefrigerantConnected(BaseModel):
    pass


class RefrigerantConnectionCoordinate(BaseModel):
    Point3D: str


class WaterCooledCondenser(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str


class HVACConnection(BaseModel):
    ObjectIDs: "ObjectIDs"
    LoopHandle: int
    SubLoopType: int
    LoopType: int
    PlantLoopType: int
    LoopFlowDirection: int
    ElementList: "ElementList"


class ImageTextureIndex(BaseModel):
    pass


class MaskTextureIndex(BaseModel):
    pass


class SelectedImageTextureIndex(BaseModel):
    pass


class InactiveImageTextureIndex(BaseModel):
    pass


class Textured(BaseModel):
    pass


class Masked(BaseModel):
    pass


class SelectedImage(BaseModel):
    pass


class InactiveImage(BaseModel):
    pass


class Color(BaseModel):
    pass


class Active(BaseModel):
    pass


class Range(BaseModel):
    Org: "Org"
    End: "End"


class HVACAttributeList(BaseModel):
    buildingZoneHandle: int
    Attributes: "Attributes"


class BuildingZoneHandle(BaseModel):
    pass


class HVACZoneComponent(BaseModel):
    type: str
    Width: float
    Height: float
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: "ZoneComponentAttributeList"
    Origin: "Origin"
    ExtractGrille: "ExtractGrille"
    MixingBoxWidth: float
    SupplyDiffuser: "SupplyDiffuser"
    UnitElementList: "UnitElementList"
    OutdoorAirSupply: int
    IntakeLouvre: "IntakeLouvre"
    MixingBox: "MixingBox"
    RefrigerantConnected: int


class VertexIndices(BaseModel):
    pass


class HoleIndices(BaseModel):
    pass


class Openings(BaseModel):
    pass


class Adjacencies(BaseModel):
    pass


class PlantOperationRanges(BaseModel):
    PlantOperationRange: "PlantOperationRange"


class HVACComponent(BaseModel):
    type: str
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: "ZoneComponentAttributeList"


class LoopHandle(BaseModel):
    pass


class LoopFlowDirection(BaseModel):
    pass


class ElementList(BaseModel):
    HVACConnectionElement: "HVACConnectionElement"


class Org(BaseModel):
    Point3D: str


class ExtractGrille(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: str
    ZoneComponentAttributeList: str


class MixingBoxWidth(BaseModel):
    pass


class SupplyDiffuser(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: str
    ZoneComponentAttributeList: str


class UnitElementList(BaseModel):
    HVACComponent: "HVACComponent"


class OutdoorAirSupply(BaseModel):
    pass


class IntakeLouvre(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: str
    ZoneComponentAttributeList: str


class MixingBox(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: str
    ZoneComponentAttributeList: str


class PlantOperationRange(BaseModel):
    Attributes: "Attributes"


class HotWaterHeatExchanger(BaseModel):
    pass


class FanType(BaseModel):
    pass


class HeaterElement(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str


class ChillerHRHeatExchanger(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str


class AbsorptionChillerUnit(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str
    AbsorptionChillerGeneratorHeatExchanger: "AbsorptionChillerGeneratorHeatExchanger"


class NumberOfFlowConnections(BaseModel):
    pass


class FlowConnections(BaseModel):
    HVACSubLoopNodeConnection: "HVACSubLoopNodeConnection"


class HVACSubLoopNodeConnection(BaseModel):
    ObjectIDs: "ObjectIDs"
    Connected: int
    Coordinate: "Coordinate"
    Attributes: "Attributes"


class HVACConnectorNode(BaseModel):
    ObjectIDs: "ObjectIDs"
    Name: str
    Active: int


class BranchConnectionList(BaseModel):
    HVACConnectorNode: "HVACConnectorNode"


class ControlPoint(BaseModel):
    Point3D: str


class UpStreamNode(BaseModel):
    Point3D: str


class DownStreamNode(BaseModel):
    Point3D: str


class SegmentList(BaseModel):
    pass


class OutdoorAirSystem(BaseModel):
    HeatRecovery: int
    Recirculation: int
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str
    HeatRecoveryDevice: "HeatRecoveryDevice"
    OutdoorAirSystemComponentList: "OutdoorAirSystemComponentList"


class IntakeDamper(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str


class ExhaustDamper(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str


class MixingDamper(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str


class ExhaustUnitComponentList(BaseModel):
    AirHandlingUnitHVACComponent: "AirHandlingUnitHVACComponent"


class IntakeUnitComponentList(BaseModel):
    AirHandlingUnitHVACComponent: "AirHandlingUnitHVACComponent"


class LineArray(BaseModel):
    Line: "Line"


class HVACConnectionElement(BaseModel):
    Line: "Line"
    SegmentList: "SegmentList"


class Adjacency(BaseModel):
    type: str
    adjacencyDistance: float
    ObjectIDs: "ObjectIDs"
    AdjacencyPolygonList: "AdjacencyPolygonList"


class AbsorptionChillerGeneratorHeatExchanger(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str


class Connected(BaseModel):
    pass


class Coordinate(BaseModel):
    Point3D: str


class Name(BaseModel):
    pass


class HeatRecovery(BaseModel):
    pass


class Recirculation(BaseModel):
    pass


class HeatRecoveryDevice(BaseModel):
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str


class OutdoorAirSystemComponentList(BaseModel):
    OutdoorAirSystemHVACComponent: "OutdoorAirSystemHVACComponent"


class AirHandlingUnitHVACComponent(BaseModel):
    type: str
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str


class Opening(BaseModel):
    type: str
    Polygon: "Polygon"
    Attributes: "Attributes"
    SegmentList: "SegmentList"


class AdjacencyPolygonList(BaseModel):
    Polygon: "Polygon"


class OutdoorAirSystemHVACComponent(BaseModel):
    type: str
    ImageRectangle: "ImageRectangle"
    ConnectingPlantLoopHandle: int
    ConnectingAirLoopHandle: int
    LoopType: int
    SubLoopType: int
    PlantLoopType: int
    AirLoopDuctType: int
    ComponentType: int
    Location: int
    ConnectionOffset: float
    Editable: int
    ZoneBranchFlag: int
    Orientation: int
    WaterInConnectionOrientation: int
    WaterOutConnectionOrientation: int
    AirInConnectionOrientation: int
    AirOutConnectionOrientation: int
    WaterInConnection: int
    WaterOutConnection: int
    AirInConnection: int
    AirOutConnection: int
    WaterInConnected: int
    WaterOutConnected: int
    AirInConnected: int
    AirOutConnected: int
    FanPlacement: int
    WaterInConnectionCoordinate: "WaterInConnectionCoordinate"
    WaterOutConnectionCoordinate: "WaterOutConnectionCoordinate"
    AirInConnectionCoordinate: "AirInConnectionCoordinate"
    AirOutConnectionCoordinate: "AirOutConnectionCoordinate"
    Attributes: "Attributes"
    ZoneComponentAttributeList: str


class PolygonHole(BaseModel):
    ObjectIDs: "ObjectIDs"
    Vertices: "Vertices"
