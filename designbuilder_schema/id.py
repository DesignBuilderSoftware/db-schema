import threading
from designbuilder_schema.base import BaseModel
from pydantic import Field, ConfigDict
from pydantic_xml import attr

_site_counter = 0
_site_counter_lock = threading.Lock()
# _assembly_counter = 0


def current_site_handle() -> int:
    return _site_counter


def generate_site_handle() -> int:
    global _site_counter
    with _site_counter_lock:
        _site_counter += 1
        return _site_counter - 1


def set_site_counter(value: int) -> None:
    global _site_counter
    with _site_counter_lock:
        _site_counter = value


class ObjectIDs(BaseModel):
    """Unique identifiers for DesignBuilder model objects.

    Maintains a hierarchical system of handles to track object relationships
    throughout the model. Rules:
    1. All defined handles must be unique integers
    2. Undefined handle is -1
    3. Site handle is always the max current handle
    4. Each ObjectID is given new handle on creation

    Attributes:
        handle: Globally unique object handle (auto-generated)
        buildingHandle: Reference to parent building (-1 if undefined)
        buildingBlockHandle: Reference to parent building block (-1 if undefined)
        zoneHandle: Reference to parent zone (-1 if undefined)
        surfaceIndex: Index of surface within parent zone (-1 if undefined)
        openingIndex: Index of opening within parent surface (-1 if undefined)
    """

    handle: int = Field(default_factory=generate_site_handle)
    buildingHandle: int = attr(default=-1)
    buildingBlockHandle: int = attr(default=-1)
    zoneHandle: int = attr(default=-1)
    surfaceIndex: int = attr(default=-1)
    openingIndex: int = attr(default=-1)

    model_config = ConfigDict(
        populate_by_name=True,
    )
