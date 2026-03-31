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
    """
    RULES:
    1. All defined handles must be unique integers
    2. undefined handle is -1
    3. Site handle is always the max current handle
    4. each ObjectID is given new handle on creation
    """

    handle: int = attr(default=Field(default_factory=generate_site_handle))
    buildingHandle: int = attr(default=-1)
    buildingBlockHandle: int = attr(default=-1)
    zoneHandle: int = attr(default=-1)
    surfaceIndex: int = attr(default=-1)
    openingIndex: int = attr(default=-1)

    model_config = ConfigDict(
        populate_by_name=True,
    )
