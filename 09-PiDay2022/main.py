from pseudo_randomness import NumpyRandom, PythonRandom, RandRandom, loadRandNumbers
from ANU_quantum_randomness import ANURandom, loadANUNumbers
from true_randomness import (
    PiRandom,
    loadPiNumbers,
    RandomOrgRandom,
    loadRandomOrgNumbers,
)
from tqdm import tqdm
import math
import numpy as np


def coprime(a, b):
    while b != 0:
        a, b = b, a % b
    return a == 1


def estimatePi(random=PythonRandom, num=10000000):
    coprimecount = 0
    pie = np.longdouble(1)

    # load numbers
    if random == ANURandom:
        num = 1024 * 10
        loadANUNumbers(num)
    elif random == RandRandom:
        loadRandNumbers()
        if num > 200000:
            num = 200000
    elif random == PiRandom:
        loadPiNumbers()
        if num > 200000:
            num = 200000
    elif random == RandomOrgRandom:
        loadRandomOrgNumbers()
        if num > 10000:
            num = 10000

    # calc
    for i in range(1, int(num / 2) + 1):
        if coprime(random(), random()):
            coprimecount += 1
        if coprimecount != 0:
            pie = math.sqrt((6 * i) / coprimecount)
        # print(pie, end="\r")
    return pie


def printPie(randomGenerator):
    Pi = estimatePi(randomGenerator)

    difference = abs(math.pi - Pi)
    print(randomGenerator.__name__, Pi, "Diff:", difference)


# loadRandomNumbers()
printPie(RandomOrgRandom)
printPie(PythonRandom)
printPie(NumpyRandom)
printPie(ANURandom)
printPie(RandRandom)
printPie(PiRandom)
