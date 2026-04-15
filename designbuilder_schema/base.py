from pydantic_xml import BaseXmlModel
from pydantic import ConfigDict


class BaseModel(BaseXmlModel):
    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        slots=True,
    )
