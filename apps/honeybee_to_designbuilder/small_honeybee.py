from pydantic import BaseModel, field_validator
from typing import List, Union, Optional, Dict, Any


class Point3D(BaseModel):
    coordinates: List[float]

    @field_validator("coordinates")
    def validate_coords(cls, v: List[float]) -> List[float]:
        if len(v) != 3:
            raise ValueError("Point3D must have exactly 3 coordinates")
        return [float(x) for x in v]

    @property
    def x(self) -> float:
        return self.coordinates[0]

    @property
    def y(self) -> float:
        return self.coordinates[1]

    @property
    def z(self) -> float:
        return self.coordinates[2]


class Face3D(BaseModel):
    type: str
    boundary: List[Point3D]
    holes: Optional[List[List[Point3D]]] = None

    @field_validator("boundary", mode="before")
    def validate_boundary(cls, v):
        if isinstance(v, list) and all(isinstance(x, list) for x in v):
            return [Point3D(coordinates=coords) for coords in v]
        return v

    @field_validator("holes", mode="before")
    def validate_holes(cls, v):
        if isinstance(v, list):
            return [[Point3D(coordinates=coords) for coords in hole] for hole in v]
        return v


class BoundaryCondition(BaseModel):
    type: str
    boundary_condition_objects: Optional[List[str]] = None
    sun_exposure: Optional[bool] = None
    wind_exposure: Optional[bool] = None
    view_factor: Optional[Dict[str, Any]] = None


class EnergyMaterial(BaseModel):
    roughness: str
    type: str
    thickness: float
    conductivity: float
    density: float
    specific_heat: float
    thermal_absorptance: float
    solar_absorptance: float
    visible_absorptance: float
    identifier: str


class EnergyWindowMaterialGas(BaseModel):
    gas_type: str
    type: str
    thickness: float
    identifier: str


class EnergyWindowMaterialGlazing(BaseModel):
    type: str
    thickness: float
    solar_transmittance: float
    solar_reflectance: float
    solar_reflectance_back: float
    visible_transmittance: float
    visible_reflectance: float
    visible_reflectance_back: float
    infrared_transmittance: float
    emissivity: float
    emissivity_back: float
    conductivity: float
    dirt_correction: float
    solar_diffusing: bool
    identifier: str


class Construction(BaseModel):
    type: str
    materials: List[str]
    identifier: str


class ShadeConstruction(BaseModel):
    type: str
    solar_reflectance: float
    visible_reflectance: float
    is_specular: bool
    identifier: str


class AirBoundaryConstructionAbridged(BaseModel):
    type: str
    air_mixing_per_area: float
    air_mixing_schedule: str
    identifier: str


class ConstructionSetAbridged(BaseModel):
    type: str
    wall_set: Dict[str, Any]
    floor_set: Dict[str, Any]
    roof_ceiling_set: Dict[str, Any]
    aperture_set: Dict[str, Any]
    door_set: Dict[str, Any]
    shade_construction: str
    air_boundary_construction: str
    identifier: str


class Properties(BaseModel):
    type: str
    energy: Optional[Dict[str, Any]] = None
    radiance: Optional[Dict[str, Any]] = None


class Aperture(BaseModel):
    type: str
    geometry: "Face3D"
    boundary_condition: "BoundaryCondition"
    properties: "Properties"
    identifier: str
    user_data: Optional[Dict[str, Any]] = None


class Door(BaseModel):
    type: str
    geometry: "Face3D"
    boundary_condition: "BoundaryCondition"
    properties: "Properties"
    identifier: str


class Face(BaseModel):
    type: str
    face_type: str
    geometry: "Face3D"
    boundary_condition: "BoundaryCondition"
    apertures: Optional[List["Aperture"]] = None
    doors: Optional[List["Door"]] = None
    identifier: str


class Room(BaseModel):
    type: str
    faces: List["Face"]
    properties: "Properties"
    identifier: str
    display_name: str
    user_data: Optional[Dict[str, Any]] = None


class Shade(BaseModel):
    type: str
    geometry: "Face3D"
    properties: "Properties"
    is_detached: bool
    identifier: str


class ModelProperties(BaseModel):
    type: str
    energy: Dict[str, Any]
    radiance: Dict[str, Any]


class Model(BaseModel):
    units: str
    type: str
    version: str
    properties: "ModelProperties"
    rooms: List["Room"]
    # orphaned_faces: List[Union["Face", str]]
    # orphaned_shades: List[Union["Shade", str]]
    # orphaned_apertures: List[Union["Aperture", str]]
    # orphaned_doors: List[Union["Door", str]]
    tolerance: float
    angle_tolerance: float
    identifier: str
    display_name: str


def load_and_validate(file_path: str) -> Model:
    """Load and validate JSON file against ModelData schema."""
    import json

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return Model(**data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    except Exception as e:
        raise ValueError(f"Validation error: {e}")


if __name__ == "__main__":
    try:
        filepath = r"honeybee_to_designbuilder\HB Shoebox.json"
        model = load_and_validate(filepath)
        print("Model validated successfully")
    except Exception as e:
        print(f"Error: {e}")
