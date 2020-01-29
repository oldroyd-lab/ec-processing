import numpy as np
import pandas as pd

def find_pow2(n):
    """
    Calculate the highest power of 2

    Args:
        n (int) : length of timeseries

    Returns:
        M (int) : largest power of 2 that is less than n
    """

    return int(np.floor(np.log2(n)))

def interp_dt(dt0, N, M):
    """
    Calculate new dt based on Vickers and Mahrt, 2003 eq. 8
    """

    dt_new = ((N - 1) * dt0) / (2**M - 1)

    return dt_new

def mrd(a, b, M=None):
    """
    Calculate the Multiresolution Decomposition for a given timeseries of two variables
    Howell and Mahrt, 1997; Vickers and Mahrt, 2003; Vickers and Mahrt 2006

    Args:
        a (array) : 1D array for timeseries "a"
        b (array) : 1D array for timeseries "b"
        M (int) : Number of points in the MRD (2^M points)

    Returns:
        D (array) : Decomposition array
        T (array) : Time array
    """

    if M is None:

        N = a.shape[0]
        M = find_pow2(N)

    # Ensure that both timeseries are of length 2**M
    a = a[:2**M]
    b = b[:2**M]

    # Pre-allocate time and decomposition arrays
    T = np.zeros(M)
    D = np.zeros(M)

    # Loop through M - 0 values (reversed)
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
        if ms > 0:
            T[ms - 1] = L
            D[ms - 1] = sum_ab * (1 / 2 ** (ms))

        # Write out new means to original arrays
        a = np.array(arr_list_a).flatten()
        b = np.array(arr_list_b).flatten()

    return T, np.flip(D)

def mrd_tau(a, b, dt, M=None, interp=False):
    """
    Similar to the mrd() function, but returns time scale "tau" instead of T
    Also allows for interpolation of points in timeseries not of length 2**M
    with the "interp" argument

    Args:
        a (array) : 1D array for timeseries "a"
        b (array) : 1D array for timeseries "b"
        dt (float or int) : timestep in timeseries "a" and "b" [s]
        M (int) : (optional) number of points in the MRD (2^M points)
        interp (bool) : decide if a and b are interpolated to 2^M points (True) or
                        truncated to the first 2**M points (False)

    Returns:
        D (array) : decomposition array
        tau (array) : time scale array
    """

    if M is None:

        N = a.shape[0]
        M = find_pow2(N)

    dt = interp_dt(dt0, N, M)

    return