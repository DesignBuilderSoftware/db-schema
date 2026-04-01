
from pydantic import field_validator, Field
from pydantic_xml import attr, element
from typing import Optional, Literal, List, Annotated
from designbuilder_schema.base import BaseModel
from designbuilder_schema.id import ObjectIDs
from designbuilder_schema.attributes import NameAttributes, ZoneComponentAttributeList
from designbuilder_schema.geometry import (
    Point3D,
    ImageRectangle,
    LineArray,
    SegmentList,
)


class HVACComponents(BaseModel):
    """Container for HVAC component list with automatic type casting.

    Holds all HVAC components (boilers, chillers, pumps, etc.) with type-aware parsing.

    Attributes:
        hvac_component: List of HVAC components
    """
    hvac_component: List["HVACComponent"] = element(tag="HVACComponent")

    @field_validator("hvac_component", mode="before")
    def recast_components(cls, components):
        if not isinstance(components, list):
            components = [components]
        return [
            HVAC_COMPONENT_MAPPING.get(component["type"], HVACComponent)(**component)
            for component in components
        ]


class NoTypeHVACComponent(BaseModel):
    """Base class for HVAC components without an explicit type attribute.

    Provides common properties for all HVAC equipment and connection information.

    Attributes:
        image_rectangle: Visualization rectangle for the component
        connecting_plant_loop_handle: References to connected loops
        connecting_air_loop_handle: Reference to air loop
        loop_type: Type of loop (heating/cooling/air)
        sub_loop_type: Sub-loop classification
        plant_loop_type: Plant equipment type
        air_loop_duct_type: Duct type if air system
        component_type: Component equipment type
        location: Position in loop
        connection_offset: Offset for connection point
        editable: Whether component properties are editable
        zone_branch_flag: Zone branch indicator
        orientation: Component orientation/rotation
        water_in/out_connection_orientation: Inlet/outlet orientations
        air_in/out_connection_orientation: Air side orientations
        water_in/out_connection: Water connection indices
        air_in/out_connection: Air connection indices
        water_in/out_connected: Water connection flags
        air_in/out_connected: Air connection flags
        fan_placement: Placement location for fans
        *_connection_coordinate: 3D connection points
        zone_component_attribute_list: Zone-specific attributes
        attributes: Named attributes for the component
    """
    image_rectangle: Optional["ImageRectangle"] = element(default=None)
    connecting_plant_loop_handle: List[int] = element(tag="ConnectingPlantLoopHandle", default_factory=list)
    connecting_air_loop_handle: int = attr()
    loop_type: int = attr()
    sub_loop_type: int = attr()
    plant_loop_type: int = attr()
    air_loop_duct_type: int = attr()
    component_type: int = attr()
    location: int = attr()
    connection_offset: float = attr()
    editable: int = attr()
    zone_branch_flag: int = attr()
    orientation: int = attr()
    water_in_connection_orientation: int = attr()
    water_out_connection_orientation: int = attr()
    air_in_connection_orientation: int = attr()
    air_out_connection_orientation: int = attr()
    water_in_connection: int = attr()
    water_out_connection: int = attr()
    air_in_connection: int = attr()
    air_out_connection: int = attr()
    water_in_connected: int = attr()
    water_out_connected: int = attr()
    air_in_connected: int = attr()
    air_out_connected: int = attr()
    fan_placement: int = attr()
    water_in_connection_coordinate: Optional["Point3D"] = element(default=None)
    water_out_connection_coordinate: Optional["Point3D"] = element(default=None)
    air_in_connection_coordinate: Optional["Point3D"] = element(default=None)
    air_out_connection_coordinate: Optional["Point3D"] = element(default=None)
    zone_component_attribute_list: Optional["ZoneComponentAttributeList"] = element(default=None)
    attributes: Optional["NameAttributes"] = element(default=None)


class HVACComponent(NoTypeHVACComponent):
    """Base class for HVAC components with explicit type attribute.

    Represents generic HVAC equipment with a type classifier.

    Attributes:
        type: Equipment type identifier
    """
    type: str


class SubLoopNode(NoTypeHVACComponent):
    type: Literal["Sub-loop node"]
    NumberOfFlowConnections: int
    FlowConnections: "FlowConnections"
    HVACSubLoopNodeConnection: "HVACSubLoopNodeConnection"
    Origin: "Point3D"


class ZoneMixer(NoTypeHVACComponent):
    type: Literal["Zone mixer"]
    LoopFlowDirection: int
    Origin: "Point3D"
    HVACConnectorNode: "HVACConnectorNode"
    BranchConnectionList: "BranchConnectionList"


class ZoneSplitter(NoTypeHVACComponent):
    type: Literal["Zone splitter"]
    LoopFlowDirection: int
    Origin: "Point3D"
    HVACConnectorNode: "HVACConnectorNode"
    BranchConnectionList: "BranchConnectionList"


class Splitter(NoTypeHVACComponent):
    type: Literal["Splitter"]
    LoopFlowDirection: int
    Origin: "Point3D"
    HVACConnectorNode: "HVACConnectorNode"
    BranchConnectionList: "BranchConnectionList"


class Mixer(NoTypeHVACComponent):
    type: Literal["Mixer"]
    LoopFlowDirection: int
    Origin: "Point3D"
    HVACConnectorNode: "HVACConnectorNode"
    BranchConnectionList: "BranchConnectionList"


class SetpointManager(NoTypeHVACComponent):
    type: Literal["Setpoint manager"]
    Origin: "Point3D"
    ControlPoint: "Point3D"
    UpStreamNode: "Point3D"
    DownStreamNode: "Point3D"
    SegmentList: "SegmentList"


class AirHandlingUnit(NoTypeHVACComponent):
    type: Literal["Air handling unit"]
    Width: float
    Height: float
    FanType: int
    DOASAirInConnected: int
    DOASAirOutConnected: int
    Origin: "Point3D"
    OutdoorAirSystem: "OutdoorAirSystem"
    IntakeDamper: "IntakeDamper"
    ExhaustDamper: "ExhaustDamper"
    DOASIntakeDamper: "DOASIntakeDamper"
    DOASExhaustDamper: "DOASExhaustDamper"
    MixingDamper: "MixingDamper"
    ExhaustUnitComponentList: Optional["ExhaustUnitComponentList"]
    IntakeUnitComponentList: "IntakeUnitComponentList"
    LineArray: "LineArray"


class Pump(NoTypeHVACComponent):
    type: Literal["Pump"]
    ...


class Boiler(NoTypeHVACComponent):
    type: Literal["Boiler"]
    ...


class CoolingTower(NoTypeHVACComponent):
    type: Literal["Cooling tower"]
    ...


class Chiller(NoTypeHVACComponent):
    type: Literal["Chiller"]
    WaterCooledCondenser: "WaterCooledCondenser"
    ChillerHRHeatExchanger: "ChillerHRHeatExchanger"
    AbsorptionChillerUnit: "AbsorptionChillerUnit"


class WaterCooledCondenser(NoTypeHVACComponent):
    pass


class ChillerHRHeatExchanger(NoTypeHVACComponent):
    pass


class AbsorptionChillerUnit(NoTypeHVACComponent):
    AbsorptionChillerGeneratorHeatExchanger: "AbsorptionChillerGeneratorHeatExchanger"


class AbsorptionChillerGeneratorHeatExchanger(NoTypeHVACComponent):
    pass


class FlowConnections(BaseModel):
    """Container for sub-loop node flow connections.

    Attributes:
        HVACSubLoopNodeConnection: List of node connections
    """
    HVACSubLoopNodeConnection: Annotated[List["HVACSubLoopNodeConnection"], element(tag="HVACSubLoopNodeConnection")]


class ExhaustUnitComponentList(BaseModel):
    """Container for air handling unit exhaust components.

    Attributes:
        AirHandlingUnitHVACComponent: List of exhaust components
    """
    AirHandlingUnitHVACComponent: Annotated[List["AirHandlingUnitHVACComponent"], element(tag="AirHandlingUnitHVACComponent")]


class IntakeUnitComponentList(BaseModel):
    """Container for air handling unit intake components.

    Attributes:
        AirHandlingUnitHVACComponent: List of intake components
    """
    AirHandlingUnitHVACComponent: Annotated[List["AirHandlingUnitHVACComponent"], element(tag="AirHandlingUnitHVACComponent")]


class HVACConnectorNode(BaseModel):
    """Connection node in the HVAC network.

    Represents a junction or connection point between components.

    Attributes:
        ObjectIDs: Unique object identifiers
        Name: Name of the connection node
        Active: Whether the node is active
    """
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    Name: str
    Active: int


class BranchConnectionList(BaseModel):
    """Container for branch connection node list.

    Attributes:
        HVACConnectorNode: List of connector nodes
    """
    HVACConnectorNode: list["HVACConnectorNode"]


class HVACSubLoopNodeConnection(BaseModel):
    """Connection detail for a sub-loop node.

    Specifies how a component connects to a sub-loop.

    Attributes:
        ObjectIDs: Unique object identifiers
        Connected: Connection status flag
        Coordinate: 3D location of the connection
        Attributes: Named attributes for the connection
    """
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    Connected: int
    Coordinate: "Point3D"
    Attributes: "NameAttributes"


class OutdoorAirSystem(NoTypeHVACComponent):
    HeatRecovery: int
    Recirculation: int
    HeatRecoveryDevice: "HeatRecoveryDevice"
    # OutdoorAirSystemComponentList:


class IntakeDamper(NoTypeHVACComponent):
    pass


class ExhaustDamper(NoTypeHVACComponent):
    pass


class DOASIntakeDamper(NoTypeHVACComponent):
    pass


class DOASExhaustDamper(NoTypeHVACComponent):
    pass


class MixingDamper(NoTypeHVACComponent):
    pass


class HeatRecoveryDevice(NoTypeHVACComponent):
    pass


class AirHandlingUnitHVACComponent(HVACComponent):
    pass


class Generator(NoTypeHVACComponent):
    type: Literal["Generator"]


class HeatPumpHeating(NoTypeHVACComponent):
    type: Literal["Heat pump heating"]


class HeatPumpCooling(NoTypeHVACComponent):
    type: Literal["Heat pump cooling"]


class FluidCooler(NoTypeHVACComponent):
    type: Literal["Fluid cooler"]


class ChilledWaterStorage(NoTypeHVACComponent):
    type: Literal["Chilled water storage"]


class IceThermalStorage(NoTypeHVACComponent):
    type: Literal["Ice thermal storage"]


class WaterHeater(NoTypeHVACComponent):
    type: Literal["Water heater"]


class DomesticWaterConnections(NoTypeHVACComponent):
    type: Literal["Domestic water connections"]


class FluidToFluidHeatExchanger(NoTypeHVACComponent):
    type: Literal["Fluid-to-fluid heat exchanger"]


class GroundHeatExchanger(NoTypeHVACComponent):
    type: Literal["Ground heat exchanger"]


class UnitarySystem(NoTypeHVACComponent):
    type: Literal["Unitary system"]
    Width: float
    Height: float
    FanType: int
    DOASAirInConnected: int
    DOASAirOutConnected: int
    Origin: "Point3D"
    OutdoorAirSystem: "OutdoorAirSystem"
    IntakeDamper: "IntakeDamper"
    ExhaustDamper: "ExhaustDamper"
    DOASIntakeDamper: "DOASIntakeDamper"
    DOASExhaustDamper: "DOASExhaustDamper"
    MixingDamper: "MixingDamper"
    ExhaustUnitComponentList: Optional["ExhaustUnitComponentList"]
    IntakeUnitComponentList: "IntakeUnitComponentList"
    LineArray: "LineArray"


class UnitaryHeatPumpAirToAir(NoTypeHVACComponent):
    type: Literal["Unitary heat pump air-to-air"]
    Width: float
    Height: float
    FanType: int
    DOASAirInConnected: int
    DOASAirOutConnected: int
    Origin: "Point3D"
    OutdoorAirSystem: "OutdoorAirSystem"
    IntakeDamper: "IntakeDamper"
    ExhaustDamper: "ExhaustDamper"
    DOASIntakeDamper: "DOASIntakeDamper"
    DOASExhaustDamper: "DOASExhaustDamper"
    MixingDamper: "MixingDamper"
    ExhaustUnitComponentList: Optional["ExhaustUnitComponentList"]
    IntakeUnitComponentList: "IntakeUnitComponentList"
    LineArray: "LineArray"


class TemperingValve(NoTypeHVACComponent):
    type: Literal["Tempering valve"]


class SolarCollector(NoTypeHVACComponent):
    type: Literal["Solar collector"]


class WaterHeaterHeatPump(NoTypeHVACComponent):
    type: Literal["Water heater heat pump"]


class UnitaryHeatPumpWaterToAir(NoTypeHVACComponent):
    type: Literal["Unitary heat pump water-to-air"]
    Width: float
    Height: float
    FanType: int
    DOASAirInConnected: int
    DOASAirOutConnected: int
    Origin: "Point3D"
    OutdoorAirSystem: "OutdoorAirSystem"
    IntakeDamper: "IntakeDamper"
    ExhaustDamper: "ExhaustDamper"
    DOASIntakeDamper: "DOASIntakeDamper"
    DOASExhaustDamper: "DOASExhaustDamper"
    MixingDamper: "MixingDamper"
    ExhaustUnitComponentList: Optional["ExhaustUnitComponentList"]
    IntakeUnitComponentList: "IntakeUnitComponentList"
    LineArray: "LineArray"


class WaterCoolingCoil(NoTypeHVACComponent):
    type: Literal["Water cooling coil"]


class GenericHeatingCoil(NoTypeHVACComponent):
    type: Literal["Generic heating coil"]


HVAC_COMPONENT_MAPPING = {
    "Sub-loop node": SubLoopNode,
    "Zone mixer": ZoneMixer,
    "Zone splitter": ZoneSplitter,
    "Splitter": Splitter,
    "Mixer": Mixer,
    "Setpoint manager": SetpointManager,
    "Pump": Pump,
    "Boiler": Boiler,
    "Generator": Generator,
    "Heat pump heating": HeatPumpHeating,
    "Water heater heat pump": WaterHeaterHeatPump,
    "Chiller": Chiller,
    "Heat pump cooling": HeatPumpCooling,
    "Cooling tower": CoolingTower,
    "Fluid cooler": FluidCooler,
    "Chilled water storage": ChilledWaterStorage,
    "Ice thermal storage": IceThermalStorage,
    "Water heater": WaterHeater,
    "Domestic water connections": DomesticWaterConnections,
    "Fluid-to-fluid heat exchanger": FluidToFluidHeatExchanger,
    "Ground heat exchanger": GroundHeatExchanger,
    "Air handling unit": AirHandlingUnit,
    "Unitary system": UnitarySystem,
    "Unitary heat pump air-to-air": UnitaryHeatPumpAirToAir,
    "Unitary heat pump water-to-air": UnitaryHeatPumpWaterToAir,
    "Tempering valve": TemperingValve,
    "Solar collector": SolarCollector,
    "Generic heating coil": GenericHeatingCoil,
    "Water cooling coil": WaterCoolingCoil,
}
