import numpy as np
import typing_extensions as tp

import pytest

from static_frame.core.validate import InterfaceClinic
from static_frame.test.test_case import skip_nple119

@skip_nple119
def test_ndarray_a() -> None:
    v = np.array([False, True, False])
    # NOTE: must type this as a dytpe, not just a a generic
    h1 = np.ndarray[tp.Any, np.dtype[np.bool_]]

    # check_type(v, h1)

def test_interface_clinic_a() -> None:

    @InterfaceClinic.check(fail_fast=False)
    def proc1(a: int, b: bool) -> int:
        return a if b else -1

    assert proc1(2, False) == -1
    assert proc1(2, True) == 2
