from pydantic_xml import BaseXmlModel
from pydantic import ConfigDict
from typing import List


class BaseModel(BaseXmlModel):
    """Base class for all DesignBuilder XML models.

    Provides consistent configuration for XML serialization:
    - populate_by_name: Accept both snake_case and XML names
    - validate_assignment: Validate on field assignment
    - str_strip_whitespace: Trim whitespace from strings
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        str_strip_whitespace=True,
    )
