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
from designbuilder_schema.utils import load_model, save_model, clear_model_cache

# Import essential dependencies first
from designbuilder_schema.tables import Tables  # noqa: F401
from designbuilder_schema.geometry import Point3D, Vertices, Line, Range  # noqa: F401
from designbuilder_schema.attributes import NameAttributes, KeyAttributes  # noqa: F401

# Rebuild core and essential models to resolve forward references for pydantic-xml
def _rebuild_models():
    """Rebuild all models with forward references.

    This is necessary for pydantic-xml to properly resolve string type hints
    like "Site", "Building", etc. that reference classes defined later.
    Uses inspect to automatically find all BaseModel subclasses in each module.
    """
    import inspect
    from pydantic_xml import BaseXmlModel

    # Rebuild all core models
    from designbuilder_schema import core, geometry, attributes, tables
    for module in [core, geometry, attributes, tables]:
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and
                issubclass(obj, BaseXmlModel) and
                obj is not BaseXmlModel and
                obj.__module__.startswith('designbuilder_schema')):
                try:
                    obj.model_rebuild()
                except Exception:
                    # Some models may fail due to unsupported field types
                    # but they're still usable through parent classes
                    pass

_rebuild_models()
del _rebuild_models

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
