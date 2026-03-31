from pydantic_xml import BaseXmlModel
from pydantic import ConfigDict, BeforeValidator
from typing import Annotated, TypeVar, List


class BaseModel(BaseXmlModel):
    """Base class for all DesignBuilder XML models"""

    # slots=True could be enabled on leaf models for memory/speed gains
    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        str_strip_whitespace=True,
    )


T = TypeVar("T")


def ensure_list(v):
    if isinstance(v, list):
        return v
    return [v]


AlwaysList = Annotated[List[T], BeforeValidator(ensure_list)]
