from . import utils


def require_annotations(func):

    missing_typehints = utils.get_missing_typehints(func)
    if missing_typehints:
        raise RuntimeError(
            "Missing typehints for arguments: {}".format(missing_typehints)
        )

    return func
