random_book_numbers = []

def get_random_book_number():
    return random_book_numbers.pop()

def load_random_book_numbers():
    global random_book_numbers

    with open("data/a-million-random-digits.txt", "r") as f:
        lines = f.readlines()
    lines = [line[8:-1].split() for line in lines]
    random_book_numbers = [int(i) for line in lines for i in line]