import importhook

import decorators


@importhook.on_import(importhook.ANY_MODULE)
def on_module_import(module):
    for attr, value in module.__dict__:
        if isinstance(value, type):
            module.__dict__[attr] = type(
                value.__name__, (value, decorators.InheritableTypehints), {}
            )

        if hasattr(value, '__call__') and not isinstance(value, type):
            module.__dict__[attr] = decorators.detect_missing_typehints(
                value
            )

            module.__dict__[attr] = (
                decorators.detect_unmatching_typehints_on_execution(value)
            )


def back_to_the_present():
    del(importhook.registry[None])
