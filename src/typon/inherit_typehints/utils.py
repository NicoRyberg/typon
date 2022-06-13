from typing import Callable, get_type_hints

from .. import utils as typon_utils


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
            if k in typon_utils.varnames_with_return(method)
        }
        new_annotations.update(annotations_to_inherit)

    method.__annotations__ = new_annotations
