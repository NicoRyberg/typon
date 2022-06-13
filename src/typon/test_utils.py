from . import utils


def test_varnames_with_return__no_args():
    """Asserts that 'return' is added to the set"""
    def foo():
        pass

    assert utils.varnames_with_return(foo) == {'return'}


def test_varnames_with_return__all_features():
    """Asserts that 'args' and 'kwargs' are not in
    the set and that 'return' is added to it"""
    def foo(a, b, c, *args, d=10, **kwargs):
        pass

    assert utils.varnames_with_return(foo) == {'a', 'b', 'c', 'd', 'return'}
