from pydantic import ConfigDict
from pydantic_xml import BaseXmlModel
from pydantic_xml.model import SearchMode


class BaseModel(BaseXmlModel, search_mode=SearchMode.UNORDERED):
    """Base XML model with unordered element search.

    UNORDERED: pydantic-xml's default ORDERED mode consumes elements
    sequentially, so any field that scans past a later-appearing tag makes
    it invisible to subsequent fields. UNORDERED finds every element by tag
    name regardless of position — required because DesignBuilder XML places
    the same tags in different orders across component types.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        slots=True,
    )
