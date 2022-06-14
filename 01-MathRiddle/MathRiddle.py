from turtle import pos
import numpy as np
from MathRiddleUtils import primes, sumsOfCombinations, productsOfCombinations

N = 10

primes = primes(N)
notPrimes = np.setdiff1d(np.arange(2, N+1), primes)

pairs = np.array([(x, y) for x in range(2, N+1) for y in range(2, N+1)])
pairsPrimesOnly = np.array([(x, y) for x in primes for y in primes])
pairsNoPrimesOnly = np.setdiff1d(pairs, pairsPrimesOnly)

allSums = np.unique([x + y for (x, y) in pairs])
allProducts = np.unique([x * y for (x, y) in pairs])

# STATEMENT 1
# finding 1: p is not a prime number (already done because a,b are greater then 1)
# finding 2: p can't be factorized into two primes
possibleProducts = np.setdiff1d(allProducts, np.unique([x * y for x in primes for y in primes]))

# STATEMENT 2
# finding 3: s is not a sum that can only be formed by two primes
print(np.setdiff1d(sumsOfCombinations(pairsPrimesOnly), sumsOfCombinations(pairsNoPrimesOnly)))
