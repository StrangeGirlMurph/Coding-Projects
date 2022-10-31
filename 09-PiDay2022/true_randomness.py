PiNumbers = []


def PiRandom():
    return PiNumbers.pop()


def loadPiNumbers():
    global PiNumbers

    with open("numbers/pi-million.txt", "r") as f:
        PiNumbers = f.readlines()[0][2:]
    PiNumbers = [int(PiNumbers[i : i + 5]) for i in range(0, len(PiNumbers), 5)]


randomOrgNumbers = []


def RandomOrgRandom():
    return randomOrgNumbers.pop()


def loadRandomOrgNumbers():
    global randomOrgNumbers

    with open("numbers/random.org.txt", "r") as f:
        lines = f.readlines()
    randomOrgNumbers = [int(line) for line in lines]
