import numpy as np

pairsTo50 = [(x, y) for x in range(2, 51) for y in range(2, 51)]  # Generate all pairs of numbers from 2 to 50 with order
primesTo50 = [x for x in range(2, 51) if all(x % y != 0 for y in range(2, x))]
antiPrimesTo50 = [x for x in range(2, 51) if not all(x % y != 0 for y in range(2, x))]
allSums = np.unique([x + y for (x, y) in pairsTo50])
allProducts = np.unique([x * y for (x, y) in pairsTo50])
