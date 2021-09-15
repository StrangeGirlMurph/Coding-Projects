import numpy as np
import numba
from numba import njit, vectorize


@vectorize
def calc(num):
    # a vertorized version of to calculation
    while num != 1:
        if num % 2 == 0:
            num = num//2
        else:
            num = ((3 * num) + 1) // 2
    return num
