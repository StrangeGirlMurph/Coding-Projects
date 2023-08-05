pi_numbers = []

def get_pi_number():
    return pi_numbers.pop()

def load_pi_numbers():
    global pi_numbers

    with open("data/million-pi-digits.txt", "r") as f:
        pi_numbers = f.readlines()[0][2:]
    pi_numbers = [int(pi_numbers[i : i + 5]) for i in range(0, len(pi_numbers), 5)]
