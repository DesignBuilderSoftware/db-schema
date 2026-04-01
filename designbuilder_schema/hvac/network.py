
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
    """Complete HVAC heating/cooling system network for a building.

    Defines all heating and cooling loops, zone groups, and connections.

    Attributes:
        ObjectHandle: Unique handle for the network
        object_ids: Object identifiers
        hvac_loops: Supply and demand loops
        hvac_zone_groups: Grouped zones served by the system
    """
    ObjectHandle: int = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    hvac_loops: Optional["HVACLoops"] = element()
    hvac_zone_groups: Optional["HVACZoneGroups"] = element()


class HVACLoops(BaseModel):
    """Container for HVAC loop list.

    Attributes:
        hvac_loop: List of heating/cooling loops
    """
    hvac_loop: List["HVACLoop"] = element(tag="HVACLoop")


class HVACZoneGroups(BaseModel):
    """Container for zone groups served by the HVAC system.

    Attributes:
        hvac_zone_group: List of zone groups
    """
    hvac_zone_group: List["HVACZoneGroup"] = element(tag="HVACZoneGroup")


class HVACLoop(BaseModel):
    """A single heating or cooling loop in the HVAC network.

    Represents a complete circuit for heat transfer with demand and supply sides.

    Attributes:
        currentSubLoopIndex: Current sub-loop index
        loopType: Type of loop (heating, cooling, etc.)
        plantLoopType: Plant equipment type
        numberOfFlowNodes: Number of nodes in the loop
        object_ids: Object identifiers
        origin: Origin point of the loop
        plant_operation_schemes: Operating schemes and setpoints
        demand_sub_loop: Demand side of the loop
        supply_sub_loop: Supply side of the loop
        attributes: Named attributes
    """
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
    """Container for plant operation scheme list.

    Attributes:
        plant_operation_scheme: List of operation schemes
    """
    plant_operation_scheme: List["PlantOperationScheme"] = element(
        tag="PlantOperationScheme"
    )


class PlantOperationScheme(BaseModel):
    """Operating scheme for plant equipment with setpoint ranges.

    Defines how plant equipment operates under different load conditions.

    Attributes:
        plant_operation_ranges: Load ranges and associated equipment
        attributes: Named attributes for the scheme
    """
    plant_operation_ranges: List["PlantOperationRanges"] = element(
        tag="PlantOperationRanges"
    )
    attributes: "NameAttributes" = element()


class PlantOperationRanges(BaseModel):
    """Container for plant operation range.

    Attributes:
        plant_operation_range: The operation range definition
    """
    plant_operation_range: "PlantOperationRange" = element()


class PlantOperationRange(BaseModel):
    """Operating range for plant equipment under specific load conditions.

    Attributes:
        attributes: Named attributes defining the range parameters
    """
    attributes: "NameAttributes" = element()


class DemandSubLoop(BaseModel):
    """Demand side (load) of an HVAC loop - consumes heating/cooling.

    Represents zones and equipment that require heating or cooling.

    Attributes:
        loop_type: Type of loop
        plant_loop_type: Plant equipment type
        sub_loop_type: Sub-loop classification
        object_ids: Object identifiers
        hvac_components: Components on demand side
        hvac_connections: Connections between components
        attributes: Named attributes
    """
    loop_type: int = attr()
    plant_loop_type: int = attr()
    sub_loop_type: int = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    hvac_components: "HVACComponents" = element()
    hvac_connections: "HVACConnections" = element()
    attributes: "NameAttributes" = element()


class SupplySubLoop(BaseModel):
    """Supply side (source) of an HVAC loop - provides heating/cooling.

    Represents plant equipment that generates heating or cooling.

    Attributes:
        loop_type: Type of loop
        plant_loop_type: Plant equipment type
        sub_loop_type: Sub-loop classification
        object_ids: Object identifiers
        hvac_components: Supply components (boiler, chiller, etc.)
        hvac_connections: Connections between components
        attributes: Named attributes
    """
    loop_type: int = attr()
    plant_loop_type: int = attr()
    sub_loop_type: int = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    hvac_components: "HVACComponents" = element()
    hvac_connections: "HVACConnections" = element()
    attributes: "NameAttributes" = element()


class HVACZoneGroup(NoTypeHVACComponent):
    """A group of zones served by the same HVAC equipment.

    Represents a zone thermostat or zone group in the system.

    Attributes:
        valid_zone_group: Validity flag for the zone group
        width: Zone group width
        height: Zone group height
        origin: Origin point for positioning
        building_zone_handle_list: References to zones in this group
        zone_element_list: Zone component elements
        zone_group_attributes: Attributes for the zone group
    """
    valid_zone_group: str = attr()
    width: float = attr()
    height: float = attr()
    origin: "Point3D" = element()
    building_zone_handle_list: Optional["BuildingZoneHandle"] = element()
    zone_element_list: "ZoneElementList" = element()
    zone_group_attributes: "NameAttributes" = element()


class BuildingZoneHandle(BaseModel):
    """Container for zone handle references.

    Attributes:
        building_zone_handle: List of zone identifiers
    """
    building_zone_handle: List[str] = element(tag="BuildingZoneHandle")


class HVACConnections(BaseModel):
    """Container for HVAC connection list.

    Attributes:
        hvac_connection: List of component connections
    """
    hvac_connection: List["HVACConnection"] = element(tag="HVACConnection")


class HVACConnection(BaseModel):
    """Connection between HVAC components in a loop.

    Represents a piping or ductwork connection with geometry.

    Attributes:
        object_ids: Object identifiers
        loop_handle: Reference to the containing loop
        sub_loop_type: Sub-loop type
        loop_type: Loop type
        plant_loop_type: Plant type
        loop_flow_direction: Flow direction in connection
        element_list: Geometric elements of the connection
    """
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    loop_handle: int = attr()
    sub_loop_type: int = attr()
    loop_type: int = attr()
    plant_loop_type: int = attr()
    loop_flow_direction: int = attr()
    element_list: "ElementList" = element()


class ElementList(BaseModel):
    """Container for connection element list.

    Attributes:
        hvac_connection_element: List of connection path elements
    """
    hvac_connection_element: List["HVACConnectionElement"] = element(
        tag="HVACConnectionElement"
    )


class HVACConnectionElement(BaseModel):
    """Single element (segment) of an HVAC connection path.

    Represents a line segment with optional CFD mesh definition.

    Attributes:
        line: The line segment geometry
        segment_list: CFD mesh segments for this connection
    """
    line: "Line" = element()
    segment_list: "SegmentList" = element()
