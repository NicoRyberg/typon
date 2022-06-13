from typing import Any, Callable, Set, get_type_hints
import warnings

from exceptions import TypeHintTypeError


def varnames_with_return(func) -> Set[str]:
    """Returns all variable names that are used
    in the function signature. Adds 'return' to the
    set and excludes 'args' and 'kwargs'"""
    return (
        set(list(func.__code__.co_varnames) + ['return'])
        - set(['args', 'kwargs'])
    )


def inherit_typehints_for_mro(method: Callable, mro: list):
    if not getattr(method, 'inherit_typehints', False):
        raise ValueError("Method cannot inherit typehints")

    new_annotations = {}

    for parent_cls in reversed(mro):
        parent_method = getattr(parent_cls, method.__name__, None)
        if parent_method is None:
            continue

        annotations_to_inherit = {
            k: v for k, v
            in get_type_hints(parent_method).items()
            if k in varnames_with_return(method)
        }
        new_annotations.update(annotations_to_inherit)

    method.__annotations__ = new_annotations


def raise_if_is_not_method(method: Callable):
    if not hasattr(method, '__call__'):
        raise ValueError("Method must be callable")

    if not method.__code__.co_argcount:
        raise ValueError("Method must have at least one argument")

    if method.__code__.co_varnames[0] != 'self':
        raise ValueError("Method must have 'self' as first argument")


def check_against_typehint(
    value: Any, typehint: Any
):
    try:
        return typehint.is_compatible_typehint(value)
    except AttributeError:
        if not typehint.__class__.__module__ == '__builtin__':
            # typehint is not builtin type
            # cannot assert that isinstance is a valid compatibility check in
            # this case
            warnings.warn(
                "Checking of typehint compatibility was done using isinstance"
                + " instead of is_compatible method",
                DeprecationWarning
            )
        return isinstance(value, typehint)


def raise_if_typehint_is_not_compatible(
    arg_name: str, arg_value: Any, typehint: Any
):
    if not check_against_typehint(
        arg_value, typehint
    ):
        raise TypeHintTypeError(
            "Argument '{}' has type '{}' but typehint '{}'".format(
                arg_name,
                type(arg_value).__name__,
                typehint,
            )
        )
