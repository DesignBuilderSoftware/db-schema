from pydantic import ConfigDict
from pydantic_xml import BaseXmlModel
from pydantic_xml.model import SearchMode


class BaseModel(BaseXmlModel, search_mode=SearchMode.UNORDERED):
    """Base XML model with unordered element search.

    pydantic-xml's default ORDERED mode consumes elements sequentially,
    causing fields to return None when the XML element order doesn't match
    the model field order. UNORDERED mode finds elements by tag name
    regardless of their position in the XML, which is required for
    DesignBuilder XML where element ordering varies by component type.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        str_strip_whitespace=True,
        slots=True,
    )
