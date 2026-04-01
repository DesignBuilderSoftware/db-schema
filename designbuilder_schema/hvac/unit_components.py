from pydantic import field_validator
from pydantic_xml import element
from typing import List, Literal
from designbuilder_schema.base import BaseModel
from designbuilder_schema.hvac.components import (
    NoTypeHVACComponent,
    HVACComponent,
    GenericHeatingCoil,
    WaterCoolingCoil,
)


class UnitElementList(BaseModel):
    """Container for unitary HVAC system components.

    Attributes:
        hvac_component: List of components in the unitary system
    """
    hvac_component: List[HVACComponent] = element(tag="HVACComponent")


class SupplyFan(NoTypeHVACComponent):
    """Supply fan for air circulation.

    Attributes:
        type: Component type identifier
    """
    type: Literal["Supply fan"]


class ZoneADULouvre(NoTypeHVACComponent):
    """Louvre for zone air distribution unit.

    Attributes:
        type: Component type identifier
    """
    type: Literal["Zone ADU louvre"]


class ZoneADUPIUIntakeLouvre(NoTypeHVACComponent):
    """Intake louvre for zone air distribution unit.

    Attributes:
        type: Component type identifier
    """
    type: Literal["Zone ADU PIU intake louvre"]


class VariableRefrigerantFlowCoolingDXCoil(NoTypeHVACComponent):
    """VRF direct expansion cooling coil.

    Attributes:
        type: Component type identifier
    """
    type: Literal["Variable refrigerant flow cooling DX coil"]


class VariableRefrigerantFlowHeatingDXCoil(NoTypeHVACComponent):
    """VRF direct expansion heating coil.

    Attributes:
        type: Component type identifier
    """
    type: Literal["Variable refrigerant flow heating DX coil"]


class DXCoolingCoil(NoTypeHVACComponent):
    """Direct expansion cooling coil.

    Attributes:
        type: Component type identifier
    """
    type: Literal["DX cooling coil"]


class DXHeatingCoil(NoTypeHVACComponent):
    """Direct expansion heating coil.

    Attributes:
        type: Component type identifier
    """
    type: Literal["DX heating coil"]


class WaterToAirHeatPumpCoolingCoil(NoTypeHVACComponent):
    """Water-to-air heat pump cooling coil.

    Attributes:
        type: Component type identifier
    """
    type: Literal["Water-to-air heat pump cooling coil"]


class WaterToAirHeatPumpHeatingCoil(NoTypeHVACComponent):
    """Water-to-air heat pump heating coil.

    Attributes:
        type: Component type identifier
    """
    type: Literal["Water-to-air heat pump heating coil"]


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
