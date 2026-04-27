from __future__ import annotations

from typing import Annotated

from pydantic import Field
from pydantic_xml import attr, element

from db_schema.attributes import NameAttributes
from db_schema.base import BaseModel
from db_schema.geometry import Line, Point3D, SegmentList
from db_schema.hvac.components import (
    HVACComponents,
    NoTypeHVACComponent,
)
from db_schema.hvac.zone_components import ZoneElementList
from db_schema.id import ObjectIDs


class HVACNetwork(BaseModel):
    ObjectHandle: int = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    hvac_loops: HVACLoops | None = element()
    hvac_zone_groups: HVACZoneGroups | None = element()


class HVACLoops(BaseModel):
    hvac_loop: list[HVACLoop] = element(tag="HVACLoop")


class HVACZoneGroups(BaseModel):
    hvac_zone_group: list[HVACZoneGroup] = element(tag="HVACZoneGroup")


class HVACLoop(BaseModel):
    currentSubLoopIndex: int = attr()
    loopType: int = attr()
    plantLoopType: int = attr()
    numberOfFlowNodes: int = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    origin: Point3D = element()
    plant_operation_schemes: PlantOperationSchemes | None = element()
    demand_sub_loop: DemandSubLoop = element()
    supply_sub_loop: SupplySubLoop = element()
    attributes: NameAttributes = element()


class PlantOperationSchemes(BaseModel):
    plant_operation_scheme: list[PlantOperationScheme] = element(
        tag="PlantOperationScheme"
    )


class PlantOperationScheme(BaseModel):
    plant_operation_ranges: list[PlantOperationRanges] = element(
        tag="PlantOperationRanges"
    )
    attributes: NameAttributes = element()


class PlantOperationRanges(BaseModel):
    plant_operation_range: PlantOperationRange = element()


class PlantOperationRange(BaseModel):
    attributes: NameAttributes = element()


class DemandSubLoop(BaseModel):
    loopType: int = attr()
    plantLoopType: int = attr()
    subLoopType: int = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    hvac_components: HVACComponents = element()
    hvac_connections: HVACConnections = element()
    attributes: NameAttributes = element()


class SupplySubLoop(BaseModel):
    loopType: int = attr()
    plantLoopType: int = attr()
    subLoopType: int = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    hvac_components: HVACComponents = element()
    hvac_connections: HVACConnections = element()
    attributes: NameAttributes = element()


class HVACZoneGroup(NoTypeHVACComponent):
    validZoneGroup: str = attr()
    width: float = attr()
    height: float = attr()
    origin: Point3D = element()
    building_zone_handle_list: BuildingZoneHandle | None = element()
    zone_element_list: ZoneElementList = element()
    zone_group_attributes: NameAttributes = element()


class BuildingZoneHandle(BaseModel):
    building_zone_handle: list[str] = element(tag="BuildingZoneHandle")


class HVACConnections(BaseModel):
    hvac_connection: list[HVACConnection] = element(tag="HVACConnection")


class HVACConnection(BaseModel):
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element()
    )
    loopHandle: int = attr()
    subLoopType: int = attr()
    loopType: int = attr()
    plantLoopType: int = attr()
    loopFlowDirection: int = attr()
    element_list: ElementList = element()


class ElementList(BaseModel):
    hvac_connection_element: list[HVACConnectionElement] = element(
        tag="HVACConnectionElement"
    )


class HVACConnectionElement(BaseModel):
    line: Line = element()
    segment_list: SegmentList = element()
