# See https://quantumnumbers.anu.edu.au/

import requests, json

ANU_numbers = []

def get_ANU_number() -> int:
    return ANU_numbers.pop()

def load_ANU_numbers(num):
    print("Getting random ANU numbers...")

    global ANU_numbers
    while len(ANU_numbers) < 2 * num:
        respond = requests.get(
            f"https://qrng.anu.edu.au/API/jsonI.php?length=1024&type=uint16"
        ).text
        ANU_numbers += json.loads(respond)["data"]
        # print(int(100 * len(ANU_number) / (2 * num)), "%", end="\r")
