import numpy as np


def getListOfPrimes(n):
    primes = np.arange(3, n+1, 2)
    for i in primes:
        primes = list(filter(lambda x: x % i != 0 or i == x, primes))
    return [2] + primes


primes = getListOfPrimes(50)
print(primes)
