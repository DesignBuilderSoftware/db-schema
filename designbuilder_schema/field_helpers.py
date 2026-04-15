from __future__ import annotations

from typing import Optional, Type, TypeVar, Any
from pydantic import Field
from pydantic_xml import attr, element

T = TypeVar("T")


# Attribute helpers
def required_attr(alias: str | None = None, **kwargs) -> Any:
    return attr(alias=alias, **kwargs)


def optional_attr(alias: str | None = None, **kwargs) -> Any:
    return attr(alias=alias, default=None, **kwargs)


def int_attr(alias: str | None = None, default: int = 0, **kwargs) -> Any:
    return attr(alias=alias, default=default, **kwargs)


def float_attr(alias: str | None = None, default: float = 0.0, **kwargs) -> Any:
    return attr(alias=alias, default=default, **kwargs)


# Element helpers
def required_element(tag: str | None = None, **kwargs) -> Any:
    return element(tag=tag, **kwargs)


def optional_element(tag: str | None = None, **kwargs) -> Any:
    return element(tag=tag, default=None, **kwargs)


def list_element(tag: str | None = None, **kwargs) -> Any:
    return element(tag=tag, **kwargs)


def annotated_element(
    type_hint: Type[T], tag: str | None = None, default: Any = None, **kwargs
) -> Any:
    if default is not None:
        return element(tag=tag, default=default, **kwargs)
    return element(tag=tag, **kwargs)


# Composite helpers
def nested_model(tag: str | None = None, required: bool = True) -> Any:
    if required:
        return element(tag=tag)
    return element(tag=tag, default=None)


def object_ids_field() -> Any:
    from designbuilder_schema.id import ObjectIDs

    return element(tag="ObjectIDs", default=Field(default_factory=ObjectIDs))
