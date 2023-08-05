import time
# all the finished versions
from speed import speeeed
#from smart import smort
from steps import steps_qwq

# number to calculate up to
calcUpTo = 1000000000

print("calculating the collatz conjecture up to", "{:,}".format(calcUpTo))

start = time.time()
speeeed(calcUpTo)
end = time.time()
print("time (without steps) \t", end - start)

start = time.time()
steps_qwq(calcUpTo)
end = time.time()
print("time (with steps) \t", end - start)

