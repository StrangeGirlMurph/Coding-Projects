import numba
from numba import njit
import time

calcUpTo = 1000000

# not at all finished didn't do anything


@njit
def smort(max):
    # using logic to be able to skip some calculations
    # allNumbers = []
    for i in range(1, max + 1):
        n = i
        while n != 1:
            if n % 2 == 0:
                n = n//2
            else:
                n = ((3 * n) + 1) // 2
            # allNumbers.append()


# testing
print("calculating the collatz conjecture up to", "{:,}".format(calcUpTo))

start = time.time()  # timer

smort(calcUpTo)

end = time.time()  # timer
print("time (without the number of steps) \t", end - start)
