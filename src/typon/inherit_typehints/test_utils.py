# type: ignore

import pytest
import unittest
from . import utils


@pytest.mark.skip("Old implementation")
def test_inherit_typehints_from_parent_method__forbid_inheritance():
    """Asserts that ValueError is raised from the function if the method
    is not configured to be inherited"""

    def foo():
        pass

    def bar():
        pass

    with pytest.raises(ValueError):
        utils.inherit_typehints_from_parent_method(foo, bar)


@unittest.skip("Old implementation")
class TestUtils(unittest.TestCase):

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
