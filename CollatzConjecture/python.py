import time

calcUpTo = 1000000


def python(max):
    # a version to just brute force everything while being as fast as possible
    for i in range(1, max + 1):
        n = i
        while n != 1:
            if n % 2 == 0:
                n = n//2
            else:
                n = ((3 * n) + 1) // 2
        next


# testing
print("calculating the collatz conjecture up to", "{:,}".format(calcUpTo))

start = time.time()
python(calcUpTo)  # <-
end = time.time()

print("time (normal python) \t", end - start)
