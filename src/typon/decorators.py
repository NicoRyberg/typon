import functools
from typing import Any, Callable, Optional
import warnings
from typon.exceptions import TypehintWarning, TypehintError

import utils


class InheritableTypehints:

    _TYPEHINTS_INHERIT_BY_DEFAULT = False

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        for _, method in cls.__dict__.items():
            if not (
                hasattr(method, '__call__')
                and
                getattr(method, "inherit_typehints",
                        cls._TYPEHINTS_INHERIT_BY_DEFAULT)
            ):
                continue

            utils.inherit_typehints_for_mro(method, cls.mro())


def inherit_typehints():

    def decorator(method):
        method.inherit_typehints = True
        return method

    return decorator


def disable_typehint_inheritance():

    def decorator(method):
        method.inherit_typehints = False
        return method

    return decorator


def raises(
    exception_cls_list: tuple[Exception] = (Exception, ),
    unexpected_behaviour: Optional[Callable[[Exception, tuple, dict], Any]] = None
):
    """Decorator to expect explicit exception(s) to be raised."""

    if unexpected_behaviour is None:
        def unexpected_behaviour(exc: Exception, args: tuple, kwargs: dict):
            raise exc

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except exception_cls_list as e:  # type: ignore
                return e
            except Exception as e:
                return unexpected_behaviour(e, args, kwargs)

        wrapper.__doc__ += (
            "\n\nRaises: \n - {}".format("\n - ".join(exception_cls_list))
        )

        return wrapper

    return decorator


def warn_instead_of_raise(
    exception_cls_list: tuple[Exception] = (Exception, ),
    *, disabled=False
):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_cls_list as e:  # type: ignore
                warnings.warn(str(e), TypehintWarning)
                if disabled:
                    raise e

        return wrapper

    return decorator


def enforce_typing(*, raise_error: bool = True):

    @warn_instead_of_raise((TypehintError, ), disabled=raise_error)
    def decorator(func):

        missing_typehints = (
            utils.varnames_with_return(func) - set(func.__annotations__.keys())
        )
        if missing_typehints:
            raise ValueError(
                "Missing typehints for arguments: {}".format(missing_typehints)
            )

        return func

    return decorator


def typechecked(*, raise_error: bool = True):

    def decorator(func):

        @warn_instead_of_raise((TypehintError, ), disabled=raise_error)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            named_args_to_check = dict(
                **dict(zip(func.__code__.co_varnames, args)),
                **kwargs
            )

            for arg_name, arg_value in named_args_to_check.items():
                if arg_name in func.__annotations__:
                    utils.raise_if_typehint_is_not_compatible(
                        arg_value, func.__annotations__[arg_name]
                    )

            ret_value = func(*args, **kwargs)

            if 'return' in func.__annotations__:
                utils.raise_if_typehint_is_not_compatible(
                    'return', ret_value, func.__annotations__['return']
                )

            return ret_value

        return wrapper

    return decorator
