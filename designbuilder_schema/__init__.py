"""
DesignBuilder XML Schema - pydantic-xml based models for DesignBuilder simulation files

This module provides Pydantic models that can serialize to/from DesignBuilder XML format.
HVAC modules are loaded lazily on first access to reduce import overhead.
"""

from designbuilder_schema.core import (
    dsbXML,
    Site,
    Building,
    BuildingBlock,
    Zone,
    Body,
    Surface,
)

# Backwards compatibility alias
DSB = dsbXML
from designbuilder_schema.utils import load_model, save_model

# Import essential dependencies first
from designbuilder_schema.tables import Tables  # noqa: F401
from designbuilder_schema.geometry import Point3D, Vertices, Line, Range  # noqa: F401
from designbuilder_schema.attributes import NameAttributes, KeyAttributes  # noqa: F401

# Only import HVAC modules here for essential model rebuilding
# They'll be re-imported lazily below for actual use
from pydantic_xml import BaseXmlModel
import inspect

# Rebuild core models to resolve forward references for pydantic-xml
_core_module = inspect.getmodule(dsbXML)
_all_models = [
    obj for name, obj in inspect.getmembers(_core_module)
    if inspect.isclass(obj) and issubclass(obj, BaseXmlModel) and obj is not BaseXmlModel
]

# Rebuild each model, catching individual failures
for _model in _all_models:
    try:
        _model.model_rebuild()
    except Exception:
        # Some models may fail to rebuild due to unsupported field types
        # but they may still be usable if accessed through their parents
        pass

# Clean up namespace
del _core_module, _all_models, _model, inspect, BaseXmlModel

# Lazy loading for HVAC modules
# Import on first access to reduce startup time
def __getattr__(name: str):
    """Lazy load HVAC modules on first access"""
    if name == "HVACComponents":
        from designbuilder_schema.hvac.components import HVACComponents  # noqa: F401
        return HVACComponents
    elif name == "HVACNetwork":
        from designbuilder_schema.hvac.network import HVACNetwork  # noqa: F401
        return HVACNetwork
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
