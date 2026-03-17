from pydantic import Field, field_validator
from typing import Annotated, List, Literal, Optional
from designbuilder_schema.base import BaseModel
from designbuilder_schema.geometry import Point3D
from designbuilder_schema.hvac.unit_components import UnitElementList
from designbuilder_schema.hvac.components import NoTypeHVACComponent, HVACComponent


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


class ZoneElementList(BaseModel):
    HVACZoneComponent: List

    @field_validator("HVACZoneComponent", mode="before")
    def recast_components(cls, components) -> List:
        mapping = {
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
        if not isinstance(components, list):
            components = [components]
        return [
            mapping.get(component["type"], HVACComponent)(**component)
            for component in components
        ]


class ZoneExtract(NoTypeHVACComponent):
    type: Literal["Zone extract"]
    Width: float
    Height: float
    Origin: "Point3D"
    ExtractGrille: "ExtractGrille"


class ADU(NoTypeHVACComponent):
    Width: float
    Height: float
    MixingBoxWidth: float
    Origin: "Point3D"
    SupplyDiffuser: "SupplyDiffuser"
    UnitElementList: Optional["UnitElementList"]
    IntakeLouvre: Annotated[Optional["IntakeLouvre"], Field(default=None)]
    MixingBox: Annotated[Optional["MixingBox"], Field(default=None)]


class ZoneADUSingleDuctCAVNoReheat(ADU):
    type: Literal["Zone ADU single duct CAV no reheat"]


class ZoneADUSingleDuctVAVReheat(ADU):
    type: Literal["Zone ADU single duct VAV reheat"]


class ZoneADUSingleDuctVAVNoReheat(ADU):
    type: Literal["Zone ADU single duct VAV no reheat"]


class ZoneADUParallelPIU(ADU):
    type: Literal["Zone ADU parallel PIU"]
    ExtractGrille: "ExtractGrille"


class ZoneADUCooledBeam(ADU):
    type: Literal["Zone ADU cooled beam"]
    CooledBeam: "CooledBeam"


class ZoneADUFourPipeInduction(ADU):
    type: Literal["Zone ADU four-pipe induction"]


class ZoneADUSeriesPIU(ADU):
    type: Literal["Zone ADU series PIU"]


class ZoneADUDualDuctVAV(ADU):
    type: Literal["Zone ADU dual duct VAV"]


class ZoneExtract(NoTypeHVACComponent):
    type: Literal["Zone extract"]


class ZoneUnit(NoTypeHVACComponent):
    Width: float
    Height: float
    MixingBoxWidth: float
    Origin: "Point3D"
    SupplyDiffuser: "SupplyDiffuser"
    UnitElementList: Optional["UnitElementList"]
    IntakeLouvre: Annotated[Optional["IntakeLouvre"], Field(default=None)]
    MixingBox: Annotated[Optional["MixingBox"], Field(default=None)]


class ZoneFanCoilUnit(ZoneUnit):
    type: Literal["Zone fan-coil unit"]


class ZoneTerminalPackagedHeatPump(ZoneUnit):
    type: Literal["Zone terminal packaged heat pump"]


class ZoneWaterToAirHeatPump(ZoneUnit):
    type: Literal["Zone water-to-air heat pump"]


class ZoneVariableRefrigerantFlowUnit(ZoneUnit):
    type: Literal["Zone variable refrigerant flow unit"]


class ZoneHighTemperatureRadiantHeating(NoTypeHVACComponent):
    type: Literal["Zone high temperature radiant heating"]


class ZoneHeatedFloor(NoTypeHVACComponent):
    type: Literal["Zone heated floor"]


class ZoneChilledCeiling(NoTypeHVACComponent):
    type: Literal["Zone chilled ceiling"]


class ZoneRadiantSurface(NoTypeHVACComponent):
    type: Literal["Zone radiant surface"]


class ZoneConvectiveElectricBaseboard(NoTypeHVACComponent):
    type: Literal["Zone convective electric baseboard"]


class ZoneConvectiveElectricBaseboard(NoTypeHVACComponent):
    type: Literal["Zone convective electric baseboard"]


class ZoneConvectiveWaterBaseboard(NoTypeHVACComponent):
    type: Literal["Zone convective water baseboard"]


class ZoneRadiativeConvectiveElectricBaseboard(NoTypeHVACComponent):
    type: Literal["Zone radiative convective electric baseboard"]


class ZoneRadiativeConvectiveWaterBaseboard(NoTypeHVACComponent):
    type: Literal["Zone radiative convective water baseboard"]


