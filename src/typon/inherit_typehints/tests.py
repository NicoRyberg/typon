import unittest
from typon.inherit_typehints import utils


class TestUtils(unittest.TestCase):

    def test_varnames_with_return__no_args(self):
        """Asserts that 'return' is added to the set"""
        def foo():
            pass

        self.assertEqual(
            utils.varnames_with_return(foo), {'return'}
        )

    def test_varnames_with_return__all_features(self):
        """Asserts that 'args' and 'kwargs' are not in
        the set and that 'return' is added to it"""
        def foo(a, b, c, *args, d=10, **kwargs):
            pass

        self.assertEqual(
            utils.varnames_with_return(foo),
            {'a', 'b', 'c', 'd' 'return'}
        )

    def test_inherit_typehints_from_parent_method__forbid_inheritance(self):
        """Asserts that ValueError is raised from the function if the method
        is not configured to be inherited"""

        def foo():
            pass

        def bar():
            pass

        with self.assertRaises(ValueError):
            utils._inherit_typehints_from_parent_method(foo, bar)

    def setUp(self) -> None:
        super().setUp()

        class A:

            def inherit_ommitted_typehints(self, a: int, b: int):
                pass

            def overwrite_typehints(self, a: str, b: str):
                pass

            def removed_args(self, a: int, b: int):
                pass

        class B(A):

            def inherit_ommitted_typehints(self, a, b):
                pass
            inherit_ommitted_typehints.inherit_typehints = True

            def overwrite_typehints(self, a: bool, b: bool):
                pass
            overwrite_typehints.inherit_typehints = True

            def removed_args(self, a: int):
                pass
            removed_args.inherit_typehints = True

        class C(B):

            def overwrite_typehints(self, a: int, b: int):
                pass

        self.A = A
        self.B = B
        self.C = C

    def test_inherit_typehints_from_parent_method__ommitted_typehints(self):
        method = self.B.inherit_ommitted_typehints
        parent_method = self.A.inherit_ommitted_typehints
        utils._inherit_typehints_from_parent_method(
            method, parent_method
        )
        self.assertEqual(
            method.__annotations__, parent_method.__annotations__
        )
