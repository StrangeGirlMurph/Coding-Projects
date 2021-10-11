from numba import njit, prange
import time

calcUpTo = 1000000000000


@njit(cache=True, parallel=True, fastmath=True, nogil=True)
def speeeed(max):
    # a version to just brute force everything while being as fast as possible
    for i in prange(1, max + 1):
        n = i
        while n != 1:
            if n % 2 == 0:
                n = n//2
            else:
                n = ((3 * n) + 1) // 2
        next


# testing
print("calculating the collatz conjecture up to", "{:,}".format(calcUpTo))

start = time.time()
speeeed(calcUpTo)  # <-
end = time.time()

print("time (without the number of steps) \t", end - start)
