from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, field_validator
from pydantic_xml import attr, element

from db_schema.attributes import NameAttributes, ZoneComponentAttributeList
from db_schema.base import BaseModel
from db_schema.geometry import ImageRectangle, LineArray, Point3D, SegmentList
from db_schema.id import ObjectIDs


# ---------------------------------------------------------------------------
# Helper / sub-component classes (defined before NoTypeHVACComponent so they
# can be referenced directly; forward refs to zone/unit types are injected at
# model_rebuild() time via _load_core_module in __init__.py)
# ---------------------------------------------------------------------------

class HVACConnectorNode(BaseModel):
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(tag="ObjectIDs")
    name: str = element(tag="Name", default="")
    active: int = element(tag="Active", default=0)


class BranchConnectionList(BaseModel):
    hvac_connector_node: list[HVACConnectorNode] = element(tag="HVACConnectorNode", default_factory=list)


class HVACSubLoopNodeConnection(BaseModel):
    object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = element(tag="ObjectIDs")
    connected: int = element(tag="Connected", default=0)
    coordinate: Point3D | None = element(tag="Coordinate", default=None)
    attributes: NameAttributes = element(tag="Attributes")


class FlowConnections(BaseModel):
    hvac_sub_loop_node_connection: list[HVACSubLoopNodeConnection] = element(
        tag="HVACSubLoopNodeConnection", default_factory=list
    )


class ExhaustUnitComponentList(BaseModel):
    air_handling_unit_hvac_component: list[AirHandlingUnitHVACComponent] = element(
        tag="AirHandlingUnitHVACComponent", default_factory=list
    )


class IntakeUnitComponentList(BaseModel):
    air_handling_unit_hvac_component: list[AirHandlingUnitHVACComponent] = element(
        tag="AirHandlingUnitHVACComponent", default_factory=list
    )


# ---------------------------------------------------------------------------
# Base class — ALL possible HVAC element fields live here so pydantic-xml's
# serializer (built once, always correct) picks them up regardless of which
# subclass is actually being instantiated.
# ---------------------------------------------------------------------------

class NoTypeHVACComponent(BaseModel):
    # Shared image / positioning
    image_rectangle: ImageRectangle | None = element(tag="ImageRectangle", default=None)
    connecting_plant_loop_handle: list[int] = element(
        tag="ConnectingPlantLoopHandle", default_factory=list
    )

    # Loop / connection metadata (formerly attr(), now element())
    connectingAirLoopHandle: int = element(tag="ConnectingAirLoopHandle", default=-1)
    loopType: int = element(tag="LoopType", default=0)
    subLoopType: int = element(tag="SubLoopType", default=0)
    plantLoopType: int = element(tag="PlantLoopType", default=0)
    airLoopDuctType: int = element(tag="AirLoopDuctType", default=0)
    componentType: int = element(tag="ComponentType", default=0)
    location: int = element(tag="Location", default=0)
    connectionOffset: float = element(tag="ConnectionOffset", default=0.0)
    editable: int = element(tag="Editable", default=0)
    zoneBranchFlag: int = element(tag="ZoneBranchFlag", default=0)
    orientation: int = element(tag="Orientation", default=0)
    waterInConnectionOrientation: int = element(tag="WaterInConnectionOrientation", default=0)
    waterOutConnectionOrientation: int = element(tag="WaterOutConnectionOrientation", default=0)
    airInConnectionOrientation: int = element(tag="AirInConnectionOrientation", default=0)
    airOutConnectionOrientation: int = element(tag="AirOutConnectionOrientation", default=0)
    waterInConnection: int = element(tag="WaterInConnection", default=0)
    waterOutConnection: int = element(tag="WaterOutConnection", default=0)
    airInConnection: int = element(tag="AirInConnection", default=0)
    airOutConnection: int = element(tag="AirOutConnection", default=0)
    waterInConnected: int = element(tag="WaterInConnected", default=0)
    waterOutConnected: int = element(tag="WaterOutConnected", default=0)
    airInConnected: int = element(tag="AirInConnected", default=0)
    airOutConnected: int = element(tag="AirOutConnected", default=0)
    fanPlacement: int = element(tag="FanPlacement", default=0)

    # Connection coordinates
    water_in_connection_coordinate: Point3D | None = element(tag="WaterInConnectionCoordinate", default=None)
    water_out_connection_coordinate: Point3D | None = element(tag="WaterOutConnectionCoordinate", default=None)
    air_in_connection_coordinate: Point3D | None = element(tag="AirInConnectionCoordinate", default=None)
    air_out_connection_coordinate: Point3D | None = element(tag="AirOutConnectionCoordinate", default=None)

    # Attributes
    zone_component_attribute_list: ZoneComponentAttributeList | None = element(
        tag="ZoneComponentAttributeList", default=None
    )
    attributes: NameAttributes | None = element(tag="Attributes", default=None)

    # Type discriminator — present as XML attribute on every HVAC component
    type: str = attr(default="")

    # -----------------------------------------------------------------------
    # Fields previously bare (no XML mapping) on subclasses — now properly
    # mapped here so every component type parses them correctly.
    # -----------------------------------------------------------------------

    # Geometry / positioning (AHU, Splitter/Mixer, zone units, zone groups)
    origin: Point3D | None = element(tag="Origin", default=None)
    width: float | None = element(tag="Width", default=None)
    height: float | None = element(tag="Height", default=None)
    mixing_box_width: float | None = element(tag="MixingBoxWidth", default=None)

    # Splitter / Mixer / Zone splitter / Zone mixer
    loop_flow_direction: int | None = element(tag="LoopFlowDirection", default=None)
    hvac_connector_node: HVACConnectorNode | None = element(tag="HVACConnectorNode", default=None)
    branch_connection_list: BranchConnectionList | None = element(tag="BranchConnectionList", default=None)

    # Sub-loop node
    number_of_flow_connections: int | None = element(tag="NumberOfFlowConnections", default=None)
    flow_connections: FlowConnections | None = element(tag="FlowConnections", default=None)
    hvac_sub_loop_node_connection: HVACSubLoopNodeConnection | None = element(
        tag="HVACSubLoopNodeConnection", default=None
    )

    # Setpoint manager
    control_point: Point3D | None = element(tag="ControlPoint", default=None)
    upstream_node: Point3D | None = element(tag="UpStreamNode", default=None)
    downstream_node: Point3D | None = element(tag="DownStreamNode", default=None)
    segment_list: SegmentList | None = element(tag="SegmentList", default=None)

    # AHU / Unitary system
    fan_type: int | None = element(tag="FanType", default=None)
    doas_air_in_connected: int | None = element(tag="DOASAirInConnected", default=None)
    doas_air_out_connected: int | None = element(tag="DOASAirOutConnected", default=None)
    outdoor_air_system: OutdoorAirSystem | None = element(tag="OutdoorAirSystem", default=None)
    intake_damper: IntakeDamper | None = element(tag="IntakeDamper", default=None)
    exhaust_damper: ExhaustDamper | None = element(tag="ExhaustDamper", default=None)
    doas_intake_damper: DOASIntakeDamper | None = element(tag="DOASIntakeDamper", default=None)
    doas_exhaust_damper: DOASExhaustDamper | None = element(tag="DOASExhaustDamper", default=None)
    mixing_damper: MixingDamper | None = element(tag="MixingDamper", default=None)
    exhaust_unit_component_list: ExhaustUnitComponentList | None = element(
        tag="ExhaustUnitComponentList", default=None
    )
    intake_unit_component_list: IntakeUnitComponentList | None = element(
        tag="IntakeUnitComponentList", default=None
    )
    line_array: LineArray | None = element(tag="LineArray", default=None)

    # Chiller
    water_cooled_condenser: WaterCooledCondenser | None = element(tag="WaterCooledCondenser", default=None)
    chiller_hr_heat_exchanger: ChillerHRHeatExchanger | None = element(
        tag="ChillerHRHeatExchanger", default=None
    )
    absorption_chiller_unit: AbsorptionChillerUnit | None = element(
        tag="AbsorptionChillerUnit", default=None
    )
    absorption_chiller_generator_heat_exchanger: AbsorptionChillerGeneratorHeatExchanger | None = element(
        tag="AbsorptionChillerGeneratorHeatExchanger", default=None
    )

    # HVACZoneGroup (injected via __init__.py before model_rebuild)
    valid_zone_group: str | None = element(tag="ValidZoneGroup", default=None)
    zone_group_attributes: NameAttributes | None = element(tag="ZoneGroupAttributes", default=None)
    # Zone group (types injected at model_rebuild time — see __init__.py)
    zone_element_list: ZoneElementList | None = element(tag="ZoneElementList", default=None)
    building_zone_handle_list: BuildingZoneHandle | None = element(
        tag="BuildingZoneHandleList", default=None
    )

    # Zone components (types injected at model_rebuild time — see __init__.py)
    supply_diffuser: SupplyDiffuser | None = element(tag="SupplyDiffuser", default=None)
    extract_grille: ExtractGrille | None = element(tag="ExtractGrille", default=None)
    intake_louvre: IntakeLouvre | None = element(tag="IntakeLouvre", default=None)
    mixing_box: MixingBox | None = element(tag="MixingBox", default=None)
    cooled_beam: CooledBeam | None = element(tag="CooledBeam", default=None)
    unit_element_list: UnitElementList | None = element(tag="UnitElementList", default=None)


# ---------------------------------------------------------------------------
# HVACComponent and type-specific subclasses
# ---------------------------------------------------------------------------

class HVACComponent(NoTypeHVACComponent):
    pass


class SubLoopNode(NoTypeHVACComponent):
    type: Literal["Sub-loop node"] = attr(default="Sub-loop node")


class ZoneMixer(NoTypeHVACComponent):
    type: Literal["Zone mixer"] = attr(default="Zone mixer")


class ZoneSplitter(NoTypeHVACComponent):
    type: Literal["Zone splitter"] = attr(default="Zone splitter")


class Splitter(NoTypeHVACComponent):
    type: Literal["Splitter"] = attr(default="Splitter")


class Mixer(NoTypeHVACComponent):
    type: Literal["Mixer"] = attr(default="Mixer")


class SetpointManager(NoTypeHVACComponent):
    type: Literal["Setpoint manager"] = attr(default="Setpoint manager")


class AirHandlingUnit(NoTypeHVACComponent):
    type: Literal["Air handling unit"] = attr(default="Air handling unit")


class Pump(NoTypeHVACComponent):
    type: Literal["Pump"] = attr(default="Pump")


class Boiler(NoTypeHVACComponent):
    type: Literal["Boiler"] = attr(default="Boiler")


class CoolingTower(NoTypeHVACComponent):
    type: Literal["Cooling tower"] = attr(default="Cooling tower")


class Chiller(NoTypeHVACComponent):
    type: Literal["Chiller"] = attr(default="Chiller")


class WaterCooledCondenser(NoTypeHVACComponent):
    pass


class ChillerHRHeatExchanger(NoTypeHVACComponent):
    pass


class AbsorptionChillerUnit(NoTypeHVACComponent):
    pass


class AbsorptionChillerGeneratorHeatExchanger(NoTypeHVACComponent):
    pass


class OutdoorAirSystem(NoTypeHVACComponent):
    heat_recovery: int = element(tag="HeatRecovery", default=0)
    recirculation: int = element(tag="Recirculation", default=0)
    heat_recovery_device: HeatRecoveryDevice | None = element(tag="HeatRecoveryDevice", default=None)


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
    type: Literal["Generator"] = attr(default="Generator")


class HeatPumpHeating(NoTypeHVACComponent):
    type: Literal["Heat pump heating"] = attr(default="Heat pump heating")


class HeatPumpCooling(NoTypeHVACComponent):
    type: Literal["Heat pump cooling"] = attr(default="Heat pump cooling")


class FluidCooler(NoTypeHVACComponent):
    type: Literal["Fluid cooler"] = attr(default="Fluid cooler")


class ChilledWaterStorage(NoTypeHVACComponent):
    type: Literal["Chilled water storage"] = attr(default="Chilled water storage")


class IceThermalStorage(NoTypeHVACComponent):
    type: Literal["Ice thermal storage"] = attr(default="Ice thermal storage")


class WaterHeater(NoTypeHVACComponent):
    type: Literal["Water heater"] = attr(default="Water heater")


class DomesticWaterConnections(NoTypeHVACComponent):
    type: Literal["Domestic water connections"] = attr(default="Domestic water connections")


class FluidToFluidHeatExchanger(NoTypeHVACComponent):
    type: Literal["Fluid-to-fluid heat exchanger"] = attr(default="Fluid-to-fluid heat exchanger")


class GroundHeatExchanger(NoTypeHVACComponent):
    type: Literal["Ground heat exchanger"] = attr(default="Ground heat exchanger")


class UnitarySystem(NoTypeHVACComponent):
    type: Literal["Unitary system"] = attr(default="Unitary system")


class UnitaryHeatPumpAirToAir(NoTypeHVACComponent):
    type: Literal["Unitary heat pump air-to-air"] = attr(default="Unitary heat pump air-to-air")


class TemperingValve(NoTypeHVACComponent):
    type: Literal["Tempering valve"] = attr(default="Tempering valve")


class SolarCollector(NoTypeHVACComponent):
    type: Literal["Solar collector"] = attr(default="Solar collector")


class WaterHeaterHeatPump(NoTypeHVACComponent):
    type: Literal["Water heater heat pump"] = attr(default="Water heater heat pump")


class UnitaryHeatPumpWaterToAir(NoTypeHVACComponent):
    type: Literal["Unitary heat pump water-to-air"] = attr(default="Unitary heat pump water-to-air")


class WaterCoolingCoil(NoTypeHVACComponent):
    type: Literal["Water cooling coil"] = attr(default="Water cooling coil")


class GenericHeatingCoil(NoTypeHVACComponent):
    type: Literal["Generic heating coil"] = attr(default="Generic heating coil")


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


class HVACComponents(BaseModel):
    hvac_component: list[HVACComponent] = element(tag="HVACComponent", default_factory=list)

    @field_validator("hvac_component", mode="before")
    @classmethod
    def recast_components(cls, components):
        if not isinstance(components, list):
            components = [components]
        result = []
        for component in components:
            if isinstance(component, dict):
                comp_type = component.get("type", "")
                result.append(HVAC_COMPONENT_MAPPING.get(comp_type, HVACComponent)(**component))
            else:
                result.append(component)
        return result
