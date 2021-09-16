import pandas as pd
import numpy as np

primesTo50 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
notPrimesTo50 = np.arange(2, 51)[~np.in1d(np.arange(2, 51), primesTo50)]
data = pd.DataFrame()

# numbers
data["numbers"] = np.arange(2, 51)

# primes
temp = np.in1d(data["numbers"], primesTo50)
data["primes"] = np.where(temp == True, data["numbers"], temp)
data["primes"].replace(0, "", inplace=True)

# not primes
data["not primes"] = np.where(temp == False, data["numbers"], temp)
data["not primes"].replace(1, "", inplace=True)

# sums primes
allSumsFromPrimes = []
for i in primesTo50:
    for k in primesTo50:
        allSumsFromPrimes.append(i + k)
uniqueSumsFromPrimes = np.unique(allSumsFromPrimes)

# products primes
allProductsFromPrimes = []
for i in primesTo50:
    for k in primesTo50:
        allProductsFromPrimes.append(i * k)
uniqueProductsFromPrimes = np.unique(allProductsFromPrimes)

# sums not primes
allSumsFromNotPrimes = []
for i in notPrimesTo50:
    for k in notPrimesTo50:
        allSumsFromNotPrimes.append(i + k)
uniqueSumsFromNotPrimes = np.unique(allSumsFromNotPrimes)

# products not primes
allProductsFromNotPrimes = []
for i in notPrimesTo50:
    for k in notPrimesTo50:
        allProductsFromNotPrimes.append(i * k)
uniqueProductsFromNotPrimes = np.unique(allProductsFromNotPrimes)

print(data)

print(uniqueSumsFromPrimes)
print(uniqueProductsFromPrimes)
