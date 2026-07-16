from __future__ import annotations

from typing import Literal

from pydantic import field_validator
from pydantic_xml import attr, element

from db_schema.base import BaseModel
from db_schema.hvac.components import HVACComponent, NoTypeHVACComponent


class ZoneElementList(BaseModel):
    hvac_zone_component: list[HVACComponent] = element(tag="HVACZoneComponent", default_factory=list)

    @field_validator("hvac_zone_component", mode="before")
    @classmethod
    def recast_components(cls, components) -> list:
        if not isinstance(components, list):
            components = [components]
        result = []
        for component in components:
            if isinstance(component, dict):
                comp_type = component.get("type", "")
                result.append(ZONE_COMPONENT_MAPPING.get(comp_type, HVACComponent)(**component))
            else:
                result.append(component)
        return result


# Sub-components — all fields inherited from NoTypeHVACComponent
class ExtractGrille(NoTypeHVACComponent):
    pass


class SupplyDiffuser(NoTypeHVACComponent):
    pass


class IntakeLouvre(NoTypeHVACComponent):
    pass


class MixingBox(NoTypeHVACComponent):
    pass


class CooledBeam(NoTypeHVACComponent):
    pass


# Zone component types — Width/Height/MixingBoxWidth/Origin/SupplyDiffuser/
# UnitElementList/ExtractGrille/CooledBeam are all in NoTypeHVACComponent.
class ZoneExtract(NoTypeHVACComponent):
    type: Literal["Zone extract"] = attr(default="Zone extract")


class ADU(NoTypeHVACComponent):
    pass


class ZoneADUSingleDuctCAVNoReheat(ADU):
    type: Literal["Zone ADU single duct CAV no reheat"] = attr(
        default="Zone ADU single duct CAV no reheat"
    )


class ZoneADUSingleDuctVAVReheat(ADU):
    type: Literal["Zone ADU single duct VAV reheat"] = attr(
        default="Zone ADU single duct VAV reheat"
    )


class ZoneADUSingleDuctVAVNoReheat(ADU):
    type: Literal["Zone ADU single duct VAV no reheat"] = attr(
        default="Zone ADU single duct VAV no reheat"
    )


class ZoneADUParallelPIU(ADU):
    type: Literal["Zone ADU parallel PIU"] = attr(default="Zone ADU parallel PIU")


class ZoneADUCooledBeam(ADU):
    type: Literal["Zone ADU cooled beam"] = attr(default="Zone ADU cooled beam")


class ZoneADUFourPipeInduction(ADU):
    type: Literal["Zone ADU four-pipe induction"] = attr(default="Zone ADU four-pipe induction")


class ZoneADUSeriesPIU(ADU):
    type: Literal["Zone ADU series PIU"] = attr(default="Zone ADU series PIU")


class ZoneADUDualDuctVAV(ADU):
    type: Literal["Zone ADU dual duct VAV"] = attr(default="Zone ADU dual duct VAV")


class ZoneUnit(NoTypeHVACComponent):
    pass


class ZoneFanCoilUnit(ZoneUnit):
    type: Literal["Zone fan-coil unit"] = attr(default="Zone fan-coil unit")


class ZoneTerminalPackagedHeatPump(ZoneUnit):
    type: Literal["Zone terminal packaged heat pump"] = attr(
        default="Zone terminal packaged heat pump"
    )


class ZoneWaterToAirHeatPump(ZoneUnit):
    type: Literal["Zone water-to-air heat pump"] = attr(default="Zone water-to-air heat pump")


class ZoneVariableRefrigerantFlowUnit(ZoneUnit):
    type: Literal["Zone variable refrigerant flow unit"] = attr(
        default="Zone variable refrigerant flow unit"
    )


class ZoneHighTemperatureRadiantHeating(NoTypeHVACComponent):
    type: Literal["Zone high temperature radiant heating"] = attr(
        default="Zone high temperature radiant heating"
    )


class ZoneHeatedFloor(NoTypeHVACComponent):
    type: Literal["Zone heated floor"] = attr(default="Zone heated floor")


class ZoneChilledCeiling(NoTypeHVACComponent):
    type: Literal["Zone chilled ceiling"] = attr(default="Zone chilled ceiling")


class ZoneRadiantSurface(NoTypeHVACComponent):
    type: Literal["Zone radiant surface"] = attr(default="Zone radiant surface")


class ZoneConvectiveElectricBaseboard(NoTypeHVACComponent):
    type: Literal["Zone convective electric baseboard"] = attr(
        default="Zone convective electric baseboard"
    )


class ZoneConvectiveWaterBaseboard(NoTypeHVACComponent):
    type: Literal["Zone convective water baseboard"] = attr(
        default="Zone convective water baseboard"
    )


class ZoneRadiativeConvectiveElectricBaseboard(NoTypeHVACComponent):
    type: Literal["Zone radiative convective electric baseboard"] = attr(
        default="Zone radiative convective electric baseboard"
    )


class ZoneRadiativeConvectiveWaterBaseboard(NoTypeHVACComponent):
    type: Literal["Zone radiative convective water baseboard"] = attr(
        default="Zone radiative convective water baseboard"
    )


ZONE_COMPONENT_MAPPING = {
    "Zone ADU single duct CAV no reheat": ZoneADUSingleDuctCAVNoReheat,
    "Zone ADU single duct VAV reheat": ZoneADUSingleDuctVAVReheat,
    "Zone ADU single duct VAV no reheat": ZoneADUSingleDuctVAVNoReheat,
    "Zone ADU parallel PIU": ZoneADUParallelPIU,
    "Zone ADU cooled beam": ZoneADUCooledBeam,
    "Zone ADU four-pipe induction": ZoneADUFourPipeInduction,
    "Zone ADU dual duct VAV": ZoneADUDualDuctVAV,
    "Zone ADU series PIU": ZoneADUSeriesPIU,
    "Zone extract": ZoneExtract,
    "Zone fan-coil unit": ZoneFanCoilUnit,
    "Zone terminal packaged heat pump": ZoneTerminalPackagedHeatPump,
    "Zone water-to-air heat pump": ZoneWaterToAirHeatPump,
    "Zone variable refrigerant flow unit": ZoneVariableRefrigerantFlowUnit,
    "Zone high temperature radiant heating": ZoneHighTemperatureRadiantHeating,
    "Zone heated floor": ZoneHeatedFloor,
    "Zone chilled ceiling": ZoneChilledCeiling,
    "Zone radiant surface": ZoneRadiantSurface,
    "Zone convective electric baseboard": ZoneConvectiveElectricBaseboard,
    "Zone convective water baseboard": ZoneConvectiveWaterBaseboard,
    "Zone radiative convective electric baseboard": ZoneRadiativeConvectiveElectricBaseboard,
    "Zone radiative convective water baseboard": ZoneRadiativeConvectiveWaterBaseboard,
}
