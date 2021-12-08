# four digit seven segment display
# a,b,c,d,e,f,g
# connections are randomly
# note where every input lands on all the 10 unique patterns
#  0:6     1:2     2:5     3:5     4:4
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#  5:5     6:6     7:3     8:7     9:6
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg
# unique: 1:2, 7:3, 4:4, 8:7

import numpy as np

lines = open("input.txt", "r").readlines()
lines = [line[:-1] for line in lines]
lines = [line.split(" | ") for line in lines]
lines = [list(i.split() for i in line) for line in lines]

# part 1
num = 0
for line in lines:
    for i in line[1]:
        if len(i) in [2, 3, 4, 7]:
            num += 1
print("In the output values, how many times do digits 1, 4, 7, or 8 appear?", num)

# part 2
# sort the input segments by amount of signals
for line in lines:
    line[0].sort(key=len)


print(lines)
print("What do you get if you add up all of the output values?")
