from __future__ import annotations

from typing import Annotated

from pydantic import Field
from pydantic_xml import attr, element

from db_schema.attributes import NameAttributes
from db_schema.base import BaseModel
from db_schema.geometry import Line, SegmentList, WrappedPoint3D
from db_schema.hvac.components import (
    HVACComponents,
    NoTypeHVACComponent,
)
from db_schema.hvac.zone_components import ZoneElementList
from db_schema.id import ObjectIDs


class HVACNetwork(BaseModel):
    ObjectHandle: int | None = element(tag="ObjectHandle", default=None)
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element(tag="ObjectIDs")
    )
    hvac_loops: HVACLoops | None = element(tag="HVACLoops", default=None)
    hvac_zone_groups: HVACZoneGroups | None = element(tag="HVACZoneGroups", default=None)


class HVACLoops(BaseModel):
    hvac_loop: list[HVACLoop] = element(tag="HVACLoop", default_factory=list)


class HVACZoneGroups(BaseModel):
    hvac_zone_group: list[HVACZoneGroup] = element(tag="HVACZoneGroup", default_factory=list)


class HVACLoop(BaseModel):
    currentSubLoopIndex: int = attr()
    loopType: int = attr()
    plantLoopType: int = attr()
    numberOfFlowNodes: int = attr()
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element(tag="ObjectIDs")
    )
    origin: WrappedPoint3D = element(tag="Origin")
    plant_operation_schemes: PlantOperationSchemes | None = element(
        tag="PlantOperationSchemes", default=None
    )
    demand_sub_loop: DemandSubLoop = element(tag="DemandSubLoop")
    supply_sub_loop: SupplySubLoop = element(tag="SupplySubLoop")
    attributes: NameAttributes = element(tag="Attributes")


class PlantOperationSchemes(BaseModel):
    plant_operation_scheme: list[PlantOperationScheme] = element(
        tag="PlantOperationScheme", default_factory=list
    )


class PlantOperationScheme(BaseModel):
    plant_operation_ranges: list[PlantOperationRanges] = element(
        tag="PlantOperationRanges"
    )
    attributes: NameAttributes = element(tag="Attributes")


class PlantOperationRanges(BaseModel):
    plant_operation_range: PlantOperationRange = element(tag="PlantOperationRange")


class PlantOperationRange(BaseModel):
    attributes: NameAttributes = element(tag="Attributes")


class DemandSubLoop(BaseModel):
    loopType: int = element(tag="LoopType")
    plantLoopType: int = element(tag="PlantLoopType")
    subLoopType: int = element(tag="SubLoopType")
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element(tag="ObjectIDs")
    )
    hvac_components: HVACComponents = element(tag="HVACComponents")
    hvac_connections: HVACConnections = element(tag="HVACConnections")
    attributes: NameAttributes = element(tag="Attributes")


class SupplySubLoop(BaseModel):
    loopType: int = element(tag="LoopType")
    plantLoopType: int = element(tag="PlantLoopType")
    subLoopType: int = element(tag="SubLoopType")
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element(tag="ObjectIDs")
    )
    hvac_components: HVACComponents = element(tag="HVACComponents")
    hvac_connections: HVACConnections = element(tag="HVACConnections")
    attributes: NameAttributes = element(tag="Attributes")


class HVACZoneGroup(NoTypeHVACComponent):
    # width, height, origin, valid_zone_group, zone_group_attributes are
    # inherited from NoTypeHVACComponent (fixes pydantic-xml nested serializer bug).
    # zone_element_list and building_zone_handle_list are injected at model_rebuild().
    pass


class BuildingZoneHandle(BaseModel):
    building_zone_handle: list[str] = element(tag="BuildingZoneHandle", default_factory=list)


class HVACConnections(BaseModel):
    hvac_connection: list[HVACConnection] = element(tag="HVACConnection")


class HVACConnection(BaseModel):
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = (
        element(tag="ObjectIDs")
    )
    loopHandle: int = element(tag="LoopHandle")
    subLoopType: int = element(tag="SubLoopType")
    loopType: int = element(tag="LoopType")
    plantLoopType: int = element(tag="PlantLoopType")
    loopFlowDirection: int = element(tag="LoopFlowDirection")
    element_list: ElementList = element(tag="ElementList")


class ElementList(BaseModel):
    hvac_connection_element: list[HVACConnectionElement] = element(
        tag="HVACConnectionElement"
    )


class HVACConnectionElement(BaseModel):
    line: Line = element(tag="Line")
    segment_list: SegmentList = element(tag="SegmentList")
