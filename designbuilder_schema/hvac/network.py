"""
hvac_network.py
====================================
The hvac network module of the designbuilder_schema
"""

from typing import Optional, Annotated
from pydantic import Field
from designbuilder_schema.base import BaseModel, AlwaysList
from designbuilder_schema.geometry import Line, SegmentList, Point3D
from designbuilder_schema.id import ObjectIDs
from designbuilder_schema.hvac.components import HVACComponents, NoTypeHVACComponent
from designbuilder_schema.hvac.zone_components import ZoneElementList
from designbuilder_schema.attributes import NameAttributes


class HVACNetwork(BaseModel):
    ObjectHandle: int
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    HVACLoops: Optional["HVACLoops"]
    HVACZoneGroups: Optional["HVACZoneGroups"]


class HVACLoops(BaseModel):
    HVACLoop: AlwaysList["HVACLoop"]


class HVACZoneGroups(BaseModel):
    HVACZoneGroup: AlwaysList["HVACZoneGroup"]


class HVACLoop(BaseModel):
    currentSubLoopIndex: int
    loopType: int
    plantLoopType: int
    numberOfFlowNodes: int
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    Origin: "Point3D"
    PlantOperationSchemes: Optional["PlantOperationSchemes"]
    DemandSubLoop: "DemandSubLoop"
    SupplySubLoop: "SupplySubLoop"
    Attributes: "NameAttributes"


class PlantOperationSchemes(BaseModel):
    PlantOperationScheme: AlwaysList["PlantOperationScheme"]


class PlantOperationScheme(BaseModel):
    PlantOperationRanges: AlwaysList["PlantOperationRanges"]
    Attributes: "NameAttributes"


class PlantOperationRanges(BaseModel):
    PlantOperationRange: "PlantOperationRange"


class PlantOperationRange(BaseModel):
    Attributes: "NameAttributes"


class DemandSubLoop(BaseModel):
    LoopType: int
    PlantLoopType: int
    SubLoopType: int
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    HVACComponents: "HVACComponents"
    HVACConnections: "HVACConnections"
    Attributes: "NameAttributes"


class SupplySubLoop(BaseModel):
    LoopType: int
    PlantLoopType: int
    SubLoopType: int
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    HVACComponents: "HVACComponents"
    HVACConnections: "HVACConnections"
    Attributes: "NameAttributes"


class HVACZoneGroup(NoTypeHVACComponent):
    ValidZoneGroup: str
    Width: float
    Height: float
    Origin: "Point3D"
    BuildingZoneHandleList: Optional["BuildingZoneHandle"]
    ZoneElementList: "ZoneElementList"
    ZoneGroupAttributes: "NameAttributes"


class BuildingZoneHandle(BaseModel):
    BuildingZoneHandle: AlwaysList[str]


class HVACConnections(BaseModel):
    HVACConnection: AlwaysList["HVACConnection"]


class HVACConnection(BaseModel):
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    LoopHandle: int
    SubLoopType: int
    LoopType: int
    PlantLoopType: int
    LoopFlowDirection: int
    ElementList: "ElementList"


class ElementList(BaseModel):
    HVACConnectionElement: AlwaysList["HVACConnectionElement"]


class HVACConnectionElement(BaseModel):
    Line: "Line"
    SegmentList: "SegmentList"
