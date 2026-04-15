from designbuilder_schema.utils import load_model, save_model, clear_model_cache

# Import essential dependencies first
from designbuilder_schema.tables import Tables  # noqa: F401
from designbuilder_schema.geometry import Point3D, Vertices, Line, Range  # noqa: F401
from designbuilder_schema.attributes import NameAttributes, KeyAttributes  # noqa: F401

# Cache for lazy-loaded core classes
_core_classes_cache = {}
_core_module_loaded = False


def _load_core_module():
    """Load and cache core module classes after all dependencies are available"""
    global _core_module_loaded
    if _core_module_loaded:
        return

    import inspect
    from pydantic_xml import BaseXmlModel
    from designbuilder_schema import core, geometry, attributes, tables

    # Cache all public classes from core
    for name, obj in inspect.getmembers(core):
        if (
            inspect.isclass(obj)
            and obj.__module__ == "designbuilder_schema.core"
        ):
            _core_classes_cache[name] = obj

    # Rebuild all models to resolve forward references
    for module in [core, geometry, attributes, tables]:
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, BaseXmlModel)
                and obj is not BaseXmlModel
                and obj.__module__.startswith("designbuilder_schema")
            ):
                try:
                    obj.model_rebuild()
                except Exception:
                    pass

    _core_module_loaded = True


# Lazy loading: defer importing core until first access
def __getattr__(name: str):
    # First try core module (lazy load)
    if name in ("dsbXML", "Site", "Building", "BuildingBlock", "Zone", "Body", "Surface",
                "Assembly", "AssemblyLibrary", "ComponentBlocks", "ComponentBlock",
                "Surfaces", "Openings", "Opening", "Adjacencies", "Adjacency"):
        _load_core_module()
        if name in _core_classes_cache:
            return _core_classes_cache[name]

    # Backwards compatibility alias
    if name == "DSB":
        _load_core_module()
        return _core_classes_cache.get("dsbXML")

    # HVAC modules (original lazy loading)
    if name == "HVACComponents":
        from designbuilder_schema.hvac.components import HVACComponents  # noqa: F401
        return HVACComponents
    elif name == "HVACNetwork":
        from designbuilder_schema.hvac.network import HVACNetwork  # noqa: F401
        return HVACNetwork

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
