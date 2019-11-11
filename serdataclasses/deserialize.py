"""Deserialize a Python List or Dictionary into a dataclass"""

from dataclasses import is_dataclass, InitVar
from typing import get_type_hints
from typing import Type, Any, Union

from .typedefs import JsonType, T


class DeserializeError(Exception):
    """Exception for when deserialization fails"""


def deserialize(obj: JsonType, constructor: Type[T]) -> T:
    """Deserialize the type

    NOTE: we use typing.get_type_hints because it correctly handles
    ForwardRefs, translating string references into their correct type in
    strange and mysterious ways.
    """
    if _is_dataclass(obj, constructor):
        return constructor(
            **{
                name: deserialize(obj.get(name), _type)
                for name, _type in get_type_hints(constructor).items()
            }
        )
    if _is_list(obj, constructor):
        return [
            deserialize(value, getattr(constructor, "__args__", (object,))[0])
            for value in obj
        ]
    if isinstance(constructor, InitVar):
        return deserialize(obj, constructor.type)
    if (
        _is_nonetype(obj, constructor)
        or _is_any(obj, constructor)
        or _is_primitive(obj, constructor)
    ):
        return obj
    if _is_union(obj, constructor):
        _union_errors = []
        for argument in constructor.__args__:
            try:
                return deserialize(obj, argument)
            except DeserializeError as error:
                _union_errors.append(str(error))
        raise DeserializeError(
            f"Failed to deserialize '{obj}' with '{constructor}' "
            f"for all provided types: {' && '.join(_union_errors)}"
        )

    raise DeserializeError(f"Cannot deserialize {obj} with {constructor}")


def _is_dataclass(obj: JsonType, constructor: Type) -> bool:
    """Check if the type is a dataclasses"""
    if is_dataclass(constructor):
        if not isinstance(obj, dict):
            raise DeserializeError(f"Expected Dict, received {type(obj)}")
        return True
    return False


def _is_list(obj: JsonType, constructor: Type) -> bool:
    """Check if the type is a list"""
    if constructor == list or getattr(constructor, "__origin__", None) == list:
        if not isinstance(obj, list):
            raise DeserializeError(f"Expected list, received {type(obj)}")
        return True
    return False


def _is_nonetype(obj: JsonType, constructor: Type) -> bool:
    """Check if type is NoneType, or None"""
    if constructor is None or constructor == type(None):
        if not obj is None:
            raise DeserializeError(f"Expected NoneType, received {type(obj)}")
        return True
    return False


def _is_any(
    obj: JsonType, constructor: Type  # pylint: disable=unused-argument
) -> bool:
    """Check if type is Any"""
    return constructor in (Any, object, InitVar)


def _is_primitive(obj: JsonType, constructor: Type) -> bool:
    """Check if a type is a primitive type"""
    if constructor in (str, int, float, bool):
        if not isinstance(obj, constructor):
            raise DeserializeError(f"Expected {constructor}, got {type(obj)}")
        return True
    return False


def _is_union(
    obj: JsonType, constructor: Type  # pylint: disable=unused-argument
) -> bool:
    """check whether a type is Union

    Note: Optional[str] is an alias for Union[str, NoneType]
    """
    return getattr(constructor, "__origin__", None) == Union
