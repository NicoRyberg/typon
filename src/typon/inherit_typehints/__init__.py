from . import utils


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
