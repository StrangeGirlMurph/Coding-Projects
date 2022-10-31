import numpy as np
import random

# define your own random number generator
def PythonRandom(max=1000):
    return random.randrange(1, max)


def NumpyRandom(max=1000):
    return np.random.randint(1, max)


randNumbers = []


def RandRandom():
    return randNumbers.pop()


def loadRandNumbers():
    global randNumbers

    with open("numbers/RandMillionDigits.txt", "r") as f:
        lines = f.readlines()
    lines = [line[8:-1].split() for line in lines]
    randNumbers = [int(i) for line in lines for i in line]
