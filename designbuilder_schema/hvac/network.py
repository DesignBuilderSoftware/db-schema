"""
hvac_network.py
====================================
The hvac network module of the designbuilder_schema
"""

from typing import Optional, Annotated, List
from pydantic import Field
from pydantic_xml import attr, element
from designbuilder_schema.base import BaseModel
from designbuilder_schema.geometry import Line, SegmentList, Point3D
from designbuilder_schema.id import ObjectIDs
from designbuilder_schema.hvac.components import HVACComponents, NoTypeHVACComponent
from designbuilder_schema.hvac.zone_components import ZoneElementList
from designbuilder_schema.attributes import NameAttributes


class HVACNetwork(BaseModel):
    ObjectHandle: int = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    hvac_loops: Optional["HVACLoops"] = element()
    hvac_zone_groups: Optional["HVACZoneGroups"] = element()


class HVACLoops(BaseModel):
    hvac_loop: List["HVACLoop"] = element(tag="HVACLoop")


class HVACZoneGroups(BaseModel):
    hvac_zone_group: List["HVACZoneGroup"] = element(tag="HVACZoneGroup")


class HVACLoop(BaseModel):
    currentSubLoopIndex: int = attr()
    loopType: int = attr()
    plantLoopType: int = attr()
    numberOfFlowNodes: int = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    origin: "Point3D" = element()
    plant_operation_schemes: Optional["PlantOperationSchemes"] = element()
    demand_sub_loop: "DemandSubLoop" = element()
    supply_sub_loop: "SupplySubLoop" = element()
    attributes: "NameAttributes" = element()


class PlantOperationSchemes(BaseModel):
    plant_operation_scheme: List["PlantOperationScheme"] = element(
        tag="PlantOperationScheme"
    )


class PlantOperationScheme(BaseModel):
    plant_operation_ranges: List["PlantOperationRanges"] = element(
        tag="PlantOperationRanges"
    )
    attributes: "NameAttributes" = element()


class PlantOperationRanges(BaseModel):
    plant_operation_range: "PlantOperationRange" = element()


class PlantOperationRange(BaseModel):
    attributes: "NameAttributes" = element()


class DemandSubLoop(BaseModel):
    loop_type: int = attr()
    plant_loop_type: int = attr()
    sub_loop_type: int = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    hvac_components: "HVACComponents" = element()
    hvac_connections: "HVACConnections" = element()
    attributes: "NameAttributes" = element()


class SupplySubLoop(BaseModel):
    loop_type: int = attr()
    plant_loop_type: int = attr()
    sub_loop_type: int = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    hvac_components: "HVACComponents" = element()
    hvac_connections: "HVACConnections" = element()
    attributes: "NameAttributes" = element()


class HVACZoneGroup(NoTypeHVACComponent):
    valid_zone_group: str = attr()
    width: float = attr()
    height: float = attr()
    origin: "Point3D" = element()
    building_zone_handle_list: Optional["BuildingZoneHandle"] = element()
    zone_element_list: "ZoneElementList" = element()
    zone_group_attributes: "NameAttributes" = element()


class BuildingZoneHandle(BaseModel):
    building_zone_handle: List[str] = element(tag="BuildingZoneHandle")


class HVACConnections(BaseModel):
    hvac_connection: List["HVACConnection"] = element(tag="HVACConnection")


class HVACConnection(BaseModel):
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    loop_handle: int = attr()
    sub_loop_type: int = attr()
    loop_type: int = attr()
    plant_loop_type: int = attr()
    loop_flow_direction: int = attr()
    element_list: "ElementList" = element()


class ElementList(BaseModel):
    hvac_connection_element: List["HVACConnectionElement"] = element(
        tag="HVACConnectionElement"
    )


class HVACConnectionElement(BaseModel):
    line: "Line" = element()
    segment_list: "SegmentList" = element()
