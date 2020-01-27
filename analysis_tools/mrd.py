import numpy as np
import pandas as pd


def mrd(a, b, M):
    '''
    Calculate the Multiresolution Decomposition for a given timeseries of two variables
    Howell and Mahrt, 1997; Vickers and Mahrt, 2003; Vickers and Mahrt 2006

    Args:
        a (array) : Array for timeseries "a"
        b (array) : Array for timeseries "b"
        M (int) : Number of points in the MRD (2^M points)

    Returns:
        D (array) : Decomposition array
        T (array) : Time array
    '''

    # Pre-allocate time and decomposition arrays
    T = np.zeros(M)
    D = np.zeros(M)

    # Loop through 0 - M values (reversed)
    for m in np.flip(np.arange(M + 1)):

        ms = M - m  # M - m in Vickers and Mahrt 2003
        L = 2 ** ms 
        sum_ab = 0.

        # Split arrays into m equal slices
        arr_list_a = np.split(a, L)
        arr_list_b = np.split(b, L)

        for i, (temp_a, temp_b) in enumerate(zip(arr_list_a, arr_list_b)):

            # Get the mean for each segment, then calculate cumulative sum
            mean_a = temp_a.mean()
            mean_b = temp_b.mean()
            sum_ab += np.sum(mean_a * mean_b)

            # Subtract mean if number of segments < number of values
            if arr_list_a[0].shape[0] > 1:
                arr_list_a[i] = temp_a - mean_a
                arr_list_b[i] = temp_b - mean_b

        # Write out decomposition and time values (ignoring m = M)
        if arr_list_a[0].shape[0] < 2 ** M:
            T[ms - 1] = L
            D[ms - 1] = sum_ab * (1 / 2 ** (ms))

        # Write out new means to original arrays
        a = np.array(arr_list_a).flatten()
        b = np.array(arr_list_b).flatten()

    return T, np.flip(D)

def mrd_tau(a, b, M, dt):

    '''
    Return
    '''