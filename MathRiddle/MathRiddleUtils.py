import numpy as np


def primes(n):
    s = np.arange(3, n+1, 2)
    for m in range(3, int(n ** 0.5)+1, 2):
        if s[(m-3)//2]:
            s[(m*m-3)//2::m] = 0
    return np.append(2, s[s > 0])


def sumsOfCombinations(l):
    return np.unique([x + y for x in l for y in l])


def productsOfCombinations(l):
    return np.unique([x + y for x in l for y in l])
