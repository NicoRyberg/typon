from typing import Set, get_type_hints, Callable


def varnames_with_return(func: Callable) -> Set[str]:
    """Returns all variable names that are used
    in the function signature. Adds 'return' to the
    set and excludes 'args' and 'kwargs'"""
    return (
        set(list(func.__code__.co_varnames) + ['return'])
        - set(['args', 'kwargs'])
    )


def get_missing_typehints(func: Callable) -> Set[str]:
    return (
        varnames_with_return(func) - set(get_type_hints(func).keys())
    )
