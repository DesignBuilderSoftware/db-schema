from __future__ import annotations

from typing import Literal

from pydantic_xml import attr, element

from db_schema.base import BaseModel
from db_schema.hvac.components import (
    GenericHeatingCoil,
    HVACComponent,
    NoTypeHVACComponent,
    WaterCoolingCoil,
)


class UnitElementList(BaseModel):
    hvac_component: list[HVACComponent] = element(tag="HVACComponent", default_factory=list)


class SupplyFan(NoTypeHVACComponent):
    type: Literal["Supply fan"] = attr()
class ZoneADULouvre(NoTypeHVACComponent):
    type: Literal["Zone ADU louvre"] = attr()
class ZoneADUPIUIntakeLouvre(NoTypeHVACComponent):
    type: Literal["Zone ADU PIU intake louvre"] = attr()
class VariableRefrigerantFlowCoolingDXCoil(NoTypeHVACComponent):
    type: Literal["Variable refrigerant flow cooling DX coil"] = attr()
class VariableRefrigerantFlowHeatingDXCoil(NoTypeHVACComponent):
    type: Literal["Variable refrigerant flow heating DX coil"] = attr()
class DXCoolingCoil(NoTypeHVACComponent):
    type: Literal["DX cooling coil"] = attr()
class DXHeatingCoil(NoTypeHVACComponent):
    type: Literal["DX heating coil"] = attr()
class WaterToAirHeatPumpCoolingCoil(NoTypeHVACComponent):
    type: Literal["Water-to-air heat pump cooling coil"] = attr()
class WaterToAirHeatPumpHeatingCoil(NoTypeHVACComponent):
    type: Literal["Water-to-air heat pump heating coil"] = attr()
UNIT_COMPONENT_MAPPING = {
    "Supply fan": SupplyFan,
    "Zone ADU louvre": ZoneADULouvre,
    "Zone ADU PIU intake louvre": ZoneADUPIUIntakeLouvre,
    "Water cooling coil": WaterCoolingCoil,
    "Generic heating coil": GenericHeatingCoil,
    "DX cooling coil": DXCoolingCoil,
    "DX heating coil": DXHeatingCoil,
    "Variable refrigerant flow cooling DX coil": VariableRefrigerantFlowCoolingDXCoil,
    "Variable refrigerant flow heating DX coil": VariableRefrigerantFlowHeatingDXCoil,
    "Water-to-air heat pump cooling coil": WaterToAirHeatPumpCoolingCoil,
    "Water-to-air heat pump heating coil": WaterToAirHeatPumpHeatingCoil,
}
