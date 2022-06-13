import functools
from typing import Optional, Callable, Any


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
