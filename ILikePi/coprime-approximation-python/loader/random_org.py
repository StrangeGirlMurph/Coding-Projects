random_org_numbers = []

def get_random_org_number():
    return random_org_numbers.pop()

def load_random_org_numbers():
    global random_org_numbers

    with open("data/random-org-numbers.txt", "r") as f:
        lines = f.readlines()
    random_org_numbers = [int(line) for line in lines]