import numba
from numba import njit
import time

calcUpTo = 1000000


@njit(cache=True, parallel=True, fastmath=True, nogil=True)
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
        next

    print("number of steps\t\t", steps)


# testing
print("calculating the collatz conjecture up to", "{:,}".format(calcUpTo))

start = time.time()
steps_qwq(calcUpTo)
end = time.time()
print("time (with the number of steps) \t", end - start)
