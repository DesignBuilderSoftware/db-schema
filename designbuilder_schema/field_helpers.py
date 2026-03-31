"""
field_helpers.py
====================================
Helper functions for common field definition patterns in pydantic-xml models.

Reduces boilerplate and improves consistency across the schema.
"""

from __future__ import annotations

from typing import Optional, Type, TypeVar, Any
from pydantic import Field
from pydantic_xml import attr, element

T = TypeVar("T")


# Attribute helpers
def required_attr(alias: str | None = None, **kwargs) -> Any:
    """Helper for required XML attributes.

    Example:
        handle: int = required_attr(alias="ObjectHandle")
    """
    return attr(alias=alias, **kwargs)


def optional_attr(alias: str | None = None, **kwargs) -> Any:
    """Helper for optional XML attributes with default None.

    Example:
        description: str | None = optional_attr(alias="Description")
    """
    return attr(alias=alias, default=None, **kwargs)


def int_attr(alias: str | None = None, default: int = 0, **kwargs) -> Any:
    """Helper for integer attributes with sensible defaults.

    Example:
        count: int = int_attr(alias="Count")
    """
    return attr(alias=alias, default=default, **kwargs)


def float_attr(alias: str | None = None, default: float = 0.0, **kwargs) -> Any:
    """Helper for float attributes with sensible defaults.

    Example:
        temperature: float = float_attr(alias="Temperature")
    """
    return attr(alias=alias, default=default, **kwargs)


# Element helpers
def required_element(tag: str | None = None, **kwargs) -> Any:
    """Helper for required nested XML elements.

    Example:
        site: Site = required_element(tag="Site")
    """
    return element(tag=tag, **kwargs)


def optional_element(tag: str | None = None, **kwargs) -> Any:
    """Helper for optional nested XML elements.

    Example:
        tables: Tables | None = optional_element(tag="Tables")
    """
    return element(tag=tag, default=None, **kwargs)


def list_element(tag: str | None = None, **kwargs) -> Any:
    """Helper for list elements (1-to-many relationships).

    Example:
        buildings: list[Building] = list_element(tag="Building")
    """
    return element(tag=tag, **kwargs)


def annotated_element(
    type_hint: Type[T],
    tag: str | None = None,
    default: Any = None,
    **kwargs
) -> Any:
    """Helper for annotated elements with Field metadata.

    Example:
        object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = annotated_element(
            ObjectIDs, tag="ObjectIDs"
        )
    """
    if default is not None:
        return element(tag=tag, default=default, **kwargs)
    return element(tag=tag, **kwargs)


# Composite helpers
def nested_model(tag: str | None = None, required: bool = True) -> Any:
    """Helper for nested model elements.

    Args:
        tag: XML tag name for this element
        required: If True, field is required; if False, use optional_element

    Example:
        building_block: BuildingBlock = nested_model(tag="BuildingBlock")
    """
    if required:
        return element(tag=tag)
    return element(tag=tag, default=None)


def object_ids_field() -> Any:
    """Helper for ObjectIDs fields that are factory-initialized.

    Example:
        object_ids: Annotated[ObjectIDs, Field(default_factory=ObjectIDs)] = object_ids_field()
    """
    from designbuilder_schema.id import ObjectIDs
    return element(
        tag="ObjectIDs",
        default=Field(default_factory=ObjectIDs)
    )
