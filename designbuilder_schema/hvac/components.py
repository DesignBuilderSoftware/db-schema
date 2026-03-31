
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
    HVACSubLoopNodeConnection: Annotated[List["HVACSubLoopNodeConnection"], element(tag="HVACSubLoopNodeConnection")]


class ExhaustUnitComponentList(BaseModel):
    AirHandlingUnitHVACComponent: Annotated[List["AirHandlingUnitHVACComponent"], element(tag="AirHandlingUnitHVACComponent")]


class IntakeUnitComponentList(BaseModel):
    AirHandlingUnitHVACComponent: Annotated[List["AirHandlingUnitHVACComponent"], element(tag="AirHandlingUnitHVACComponent")]


class HVACConnectorNode(BaseModel):
    ObjectIDs: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)]
    Name: str
    Active: int


class BranchConnectionList(BaseModel):
    HVACConnectorNode: list["HVACConnectorNode"]


class HVACSubLoopNodeConnection(BaseModel):
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
