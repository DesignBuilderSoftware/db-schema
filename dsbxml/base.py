from decimal import Decimal
from typing import Annotated

from pydantic import ConfigDict, PlainSerializer
from pydantic_xml import BaseXmlModel
from pydantic_xml.model import SearchMode


def _format_decimal(value: float) -> str:
    """Render a float without scientific notation.

    DesignBuilder.xsd declares numeric fields as xs:decimal, which has no
    exponent form, but Python writes very small or large floats as e.g.
    "4.44e-15". Reformatting from repr()'s own digits keeps ordinary values
    (3.14) free of float representation noise.
    """
    text = repr(value)
    if "e" not in text and "E" not in text:
        return text
    return format(Decimal(text), "f")


# A float whose XML (and JSON) form is always a plain decimal; model_dump()
# in python mode still returns the raw float.
XSDFloat = Annotated[float, PlainSerializer(_format_decimal, return_type=str, when_used="json")]


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

    def to_xml_tree(self, **kwargs):
        """Serialise without unset optional values.

        pydantic-xml writes an unset optional attribute as ``name=""`` and an
        unset optional primitive element as an empty tag, both invalid
        against the schema. Empty strings and empty containers are not None
        and are still written.
        """
        kwargs.setdefault("exclude_none", True)
        return super().to_xml_tree(**kwargs)

    def to_xml(self, **kwargs):
        """Serialise to XML text; see to_xml_tree for the unset-value handling."""
        kwargs.setdefault("exclude_none", True)
        return super().to_xml(**kwargs)
