import numpy as np
import numba
from numba import njit, vectorize, int32
import time

calcUpTo = 1000000000


@njit(cache=True, parallel=True, fastmath=True, nogil=True)
def speeeed(max: np.int64):
    # a version to just brute force everything while being as fast as possible
    for i in numba.prange(1, max + 1):
        n = i
        while n != 1:
            if n % 2 == 0:
                n = n//2
            else:
                n = ((3 * n) + 1) // 2
        next


@njit(cache=True, parallel=True, fastmath=True, nogil=True)
def storeAll(max):
    # like speeeed but storing all numbers
    all = np.empty(1)
    print(np.shape(all))
    for i in numba.prange(1, max + 1):
        n = i
        na = np.array()
        while n != 1:
            if n % 2 == 0:
                n = n//2
            else:
                n = (3 * n) + 1
            np.append(na, n)
        np.append(all, na)
    print("steps ", all.size-max)
    print(all)


@njit(cache=True, parallel=True, fastmath=True, nogil=True)
def speeeed3(max: int):
    # a version to just brute force everything while being as fast as possible
    for i in numba.prange(1, max + 1):
        n = i
        while n != 1:
            n = calc(n)
        next


@njit()
def speeeed2(max):
    # a version to just brute force everything while being as fast as possible
    for i in range(1, max + 1):
        n = i
        while n != 1:
            if n % 2 == 0:
                n = n//2
            else:
                n = ((3 * n) + 1) // 2


@njit(cache=True, parallel=True, fastmath=True)
def steps_qwq(max):
    # like speeeed but with the major disadvantage to count the number of steps
    steps = 0

    for i in numba.prange(1, max + 1):
        n = i
        while n != 1:
            if n % 2 == 0:
                n = n//2
                steps += 1
            else:
                n = ((3 * n) + 1) // 2
                steps += 2
        done = True
    print("number of steps\t\t", steps)


@njit
def steps_qwq2(max):
    # like speeeed but with the major disadvantage to count the number of steps
    steps = 0

    for i in range(1, max + 1):
        n = i
        while n != 1:
            if n % 2 == 0:
                n = n//2
                steps += 1
            else:
                n = ((3 * n) + 1) // 2
                steps += 2

    print("number of steps\t\t", steps)


@njit(int32(int32), cache=True, fastmath=True, nogil=True)
def calc(num):
    # a vertorized version of to calculation
    if num % 2 == 0:
        return num//2
    else:
        return ((3 * num) + 1) // 2


print("calculating the collatz conjecture up to", "{:,}".format(calcUpTo))
start = time.time()
speeeed3(calcUpTo)
end = time.time()
print("time 3 \t", end - start)

start = time.time()
speeeed(calcUpTo)
end = time.time()
print("time 1 \t", end - start)

start = time.time()
speeeed2(calcUpTo)
end = time.time()
print("time 2 \t", end - start)
