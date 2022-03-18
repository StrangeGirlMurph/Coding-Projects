import requests, json
import numpy as np

ANUnumbers = []  # np.empty(np.uint16)


def ANURandom():
    return ANUnumbers.pop()


def loadANUNumbers(num):
    print("Getting random ANU numbers...")

    global ANUnumbers
    while len(ANUnumbers) < 2 * num:
        respond = requests.get(
            f"https://qrng.anu.edu.au/API/jsonI.php?length=1024&type=uint16"
        ).text
        ANUnumbers += json.loads(respond)["data"]
        # print(int(100 * len(ANUnumbers) / (2 * num)), "%", end="\r")
