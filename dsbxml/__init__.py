from dsbxml.utils import load_model as load_model
from dsbxml.utils import save_model as save_model

# Cache for lazy-loaded core classes
_core_classes_cache = {}
_core_module_loaded = False
_core_module_loading = False  # re-entrancy guard


def _load_core_module():  # noqa: C901  # pylint: disable=too-many-locals,too-many-branches
    """Load and cache core module classes after all dependencies are available"""
    global _core_module_loaded, _core_module_loading
    if _core_module_loaded or _core_module_loading:
        return

    _core_module_loading = True
    try:
        import importlib
        import inspect

        from pydantic_xml import BaseXmlModel

        core = importlib.import_module("dsbxml.core")
        geometry = importlib.import_module("dsbxml.geometry")
        attributes = importlib.import_module("dsbxml.attributes")
        tables = importlib.import_module("dsbxml.tables")
        hvac_components = importlib.import_module("dsbxml.hvac.components")
        hvac_network = importlib.import_module("dsbxml.hvac.network")
        hvac_unit = importlib.import_module("dsbxml.hvac.unit_components")
        hvac_zone = importlib.import_module("dsbxml.hvac.zone_components")

        # Cache all public classes from core
        for name, obj in inspect.getmembers(core):
            if inspect.isclass(obj) and obj.__module__ == "dsbxml.core":
                _core_classes_cache[name] = obj

        import sys

        # Pydantic uses the SUBCLASS's module namespace when resolving forward
        # refs during model_rebuild(), even for inherited fields. Every module
        # that defines a NoTypeHVACComponent subclass must have all types that
        # NoTypeHVACComponent references (OutdoorAirSystem, ZoneElementList, …).
        all_hvac_types: dict = {}
        for _mod in [hvac_components, hvac_unit, hvac_zone, hvac_network]:
            for _name in dir(_mod):
                _obj = getattr(_mod, _name)
                if isinstance(_obj, type):
                    all_hvac_types[_name] = _obj

        for _mod_name in [
            "dsbxml.hvac.components",
            "dsbxml.hvac.unit_components",
            "dsbxml.hvac.zone_components",
            "dsbxml.hvac.network",
            "dsbxml.core",
        ]:
            _ns = sys.modules[_mod_name].__dict__
            for _name, _obj in all_hvac_types.items():
                _ns.setdefault(_name, _obj)

        # Rebuild every model once, each after the models its fields hold (a depth-first
        # walk over the field types). The HVAC component classes that only a `type`
        # mapping selects are left for their first use: each carries the ~105 fields all
        # components share, so building the 97 of them took 5.5 of the 5.7 s this step
        # took, while a file uses a few. pydantic builds one when it is first created
        # (HVAC_COMPONENT_MAPPING[...](**fields)); BaseModel._built covers a direct
        # from_xml or to_xml.
        import typing

        from dsbxml.hvac.components import NoTypeHVACComponent

        models: dict[str, type] = {}
        for module in [
            geometry,
            attributes,
            tables,
            hvac_components,
            hvac_unit,
            hvac_zone,
            hvac_network,
            core,
        ]:
            for _name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, BaseXmlModel)
                    and obj is not BaseXmlModel
                    and obj.__module__.startswith("dsbxml")
                ):
                    models.setdefault(f"{obj.__module__}.{obj.__qualname__}", obj)

        # Every module's names and every model, to resolve any class's annotations.
        everything: dict = {}
        for _mod in list(sys.modules.values()):
            if getattr(_mod, "__name__", "").startswith("dsbxml"):
                everything.update(vars(_mod))
        everything.update({c.__name__: c for c in models.values()})

        def held(annotation, out: list) -> None:
            if isinstance(annotation, str):
                return
            if inspect.isclass(annotation) and issubclass(annotation, BaseXmlModel):
                out.append(annotation)
            for arg in typing.get_args(annotation):
                held(arg, out)

        done: set[type] = set()

        def rebuild(cls: type) -> None:
            if cls in done:
                return
            done.add(cls)
            try:
                hints = typing.get_type_hints(cls, globalns=everything)
            except Exception:  # pylint: disable=broad-exception-caught
                hints = {}
            deps: list = []
            for annotation in hints.values():
                held(annotation, deps)
            for dep in deps:
                rebuild(dep)
            try:
                cls.model_rebuild()
            except Exception as e:  # pylint: disable=broad-exception-caught
                import warnings

                warnings.warn(f"model_rebuild failed for {cls.__name__}: {e}", stacklevel=2)

        for cls in models.values():
            if not issubclass(cls, NoTypeHVACComponent):
                rebuild(cls)

        _core_module_loaded = True
    finally:
        _core_module_loading = False


# Lazy loading: defer importing core until first access
def __getattr__(name: str):
    # Try core module (lazy load) — check cache after loading rather than
    # maintaining a manual whitelist of class names.
    if not name.startswith("_"):
        _load_core_module()
        if name in _core_classes_cache:
            return _core_classes_cache[name]

    # Backwards compatibility alias
    if name == "DSB":
        _load_core_module()
        return _core_classes_cache.get("dsbXML")

    # HVAC modules (original lazy loading)
    if name == "HVACComponents":
        from dsbxml.hvac.components import HVACComponents  # noqa: F401

        return HVACComponents
    if name == "HVACNetwork":
        from dsbxml.hvac.network import HVACNetwork  # noqa: F401

        return HVACNetwork

    if name in ("diff_models", "ModelDiff"):
        from dsbxml import diffing

        return getattr(diffing, name)
    if name == "ModelValidationError":
        from dsbxml.errors import ModelValidationError  # noqa: F401

        return ModelValidationError

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
