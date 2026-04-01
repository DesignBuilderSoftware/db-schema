from pydantic import Field, field_validator
from pydantic_xml import attr, element
from typing import Annotated, List, Literal, Optional
from designbuilder_schema.base import BaseModel
from designbuilder_schema.geometry import Point3D
from designbuilder_schema.hvac.unit_components import UnitElementList
from designbuilder_schema.hvac.components import NoTypeHVACComponent, HVACComponent


class ZoneElementList(BaseModel):
    """Container for zone HVAC component list with automatic type casting.

    Attributes:
        hvac_zone_component: List of zone HVAC components
    """
    hvac_zone_component: List["HVACComponent"] = element(tag="HVACZoneComponent")

    @field_validator("hvac_zone_component", mode="before")
    def recast_components(cls, components) -> List:
        if not isinstance(components, list):
            components = [components]
        return [
            ZONE_COMPONENT_MAPPING.get(component["type"], HVACComponent)(**component)
            for component in components
        ]


class ExtractGrille(NoTypeHVACComponent):
    """Air extraction grille in a zone."""
    pass


class SupplyDiffuser(NoTypeHVACComponent):
    """Air supply diffuser in a zone."""
    pass


class IntakeLouvre(NoTypeHVACComponent):
    """Air intake louvre in a zone."""
    pass


class MixingBox(NoTypeHVACComponent):
    """Mixing box for zone air conditioning."""
    pass


class CooledBeam(NoTypeHVACComponent):
    """Cooled ceiling beam for zone conditioning."""
    pass


class ZoneExtract(NoTypeHVACComponent):
    """Zone extract air component.

    Represents exhaust air from a zone.

    Attributes:
        type: Component type identifier
        Width: Width of the extraction unit
        Height: Height of the extraction unit
        Origin: Location of the unit
        ExtractGrille: The extraction grille component
    """
    type: Literal["Zone extract"]
    Width: float
    Height: float
    Origin: "Point3D"
    ExtractGrille: "ExtractGrille"


class ADU(NoTypeHVACComponent):
    """Base class for air distribution units in zones.

    Represents zone-level air conditioning equipment with supply and intake.

    Attributes:
        Width: Unit width
        Height: Unit height
        MixingBoxWidth: Width of mixing section
        Origin: Unit location
        SupplyDiffuser: Supply air diffuser
        UnitElementList: Internal components
        IntakeLouvre: Air intake section
        MixingBox: Mixing section
    """
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


class ZoneConvectiveWaterBaseboard(NoTypeHVACComponent):
    type: Literal["Zone convective water baseboard"]


class ZoneRadiativeConvectiveElectricBaseboard(NoTypeHVACComponent):
    type: Literal["Zone radiative convective electric baseboard"]


class ZoneRadiativeConvectiveWaterBaseboard(NoTypeHVACComponent):
    type: Literal["Zone radiative convective water baseboard"]


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


