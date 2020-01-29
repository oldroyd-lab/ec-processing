import pytest
import numpy as np
import pandas as pd

@pytest.fixture()
def test_data_1var():
    """
    Return test data with 1 array of size 2**3
    """

    a1 = np.array([1., 3., 2., 5., 1., 2., 1., 3.])
    a2 = np.array([1., 3., 2., 5., 1., 2., 1., 3.])

    return a1, a2

@pytest.fixture()
def test_data_2var():
    """
    Return test data with two different arrays of size 2**3
    """
    a = np.array([1., 3., 2., 5., 1., 2., 1., 3.])
    b = np.array([2., 5., 1., 2., 1., 4., 1., 2.])

    return a, b

def test_1var_mrd_given_m(test_data_1var):
    """
    Test example of 1 var MRD from Vickers and Mahrt, 2003 given an M value
    """

    a1, a2 = test_data_1var

    truth_t = np.array([2., 4., 8.])
    truth_d = np.array([.25, .3125, 1.125])
    M = 3

    t, d = mrd(a1, a2, M)

    return

def test_1var_mrd_infer_m(test_data_1var):
    """
    Test example of 1 var MRD from Vickers and Mahrt, 2003 when not given an M value
    """

    return

def test_2var_mrd(test_data_2var):
    """

    """

    return