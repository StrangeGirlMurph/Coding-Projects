from loader.random_org import get_random_org_number, load_random_org_numbers
from loader.ANU_quantum import get_ANU_number, load_ANU_numbers
from loader.random_numbers_book import get_random_book_number, load_random_book_numbers
from loader.pi_digits import get_pi_number, load_pi_numbers

from tqdm import tqdm
import math
import numpy as np
import random

def get_random_python_number(max=1000):
    return random.randrange(1, max)

def get_random_numpy_number(max=1000):
    return np.random.randint(1, max)

def coprime(a, b):
    while b != 0:
        a, b = b, a % b
    return a == 1


def estimatePi(random=get_random_python_number, num=1000000):
    coprimecount = 0
    pie = np.longdouble(1)

    # load numbers
    if random == get_ANU_number:
        num = 1024 * 10
        (num)
    elif random == get_random_book_number:
        load_random_book_numbers()
        if num > 200000:
            num = 200000
    elif random == get_pi_number:
        load_pi_numbers()
        if num > 200000:
            num = 200000
    elif random == get_random_org_number:
        load_random_org_numbers()
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


printPie(get_random_python_number)
printPie(get_random_numpy_number)
printPie(get_pi_number)
# printPie(get_ANU_number)
printPie(get_random_book_number)
printPie(get_random_org_number)




