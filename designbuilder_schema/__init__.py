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

# Import all dependent models first to ensure they're registered
# before rebuilding parent models
from designbuilder_schema.tables import Tables  # noqa: F401
from designbuilder_schema.geometry import Point3D, Vertices, Line, Range  # noqa: F401
from designbuilder_schema.attributes import NameAttributes, KeyAttributes  # noqa: F401
from designbuilder_schema.hvac.components import HVACComponents  # noqa: F401
from designbuilder_schema.hvac.network import HVACNetwork  # noqa: F401

from pydantic_xml import BaseXmlModel

# Rebuild models to resolve forward references for pydantic-xml
# This rebuilds models in the order they were imported, which generally works
# for most forward references
import inspect
from pydantic_xml import BaseXmlModel

# Get all BaseXmlModel classes from the core module and rebuild them
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
del _core_module, _all_models, _model
