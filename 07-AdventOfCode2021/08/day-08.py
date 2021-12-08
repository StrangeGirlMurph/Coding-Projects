# four digit seven segment display
# a,b,c,d,e,f,g
# connections are randomly
# note where every input lands on all the 10 unique patterns
#  0:6     1:2!    2:5     3:5     4:4!
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#  5:5     6:6     7:3!    8:7!    9:6
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg
# unique: 1:2, 7:3, 4:4, 8:7
# (3x)5, (3x)6
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

result = 0
for line in lines:
    num = []
    for segment in line[1]:
        # only the 1 has 2 input signals
        if len(segment) == 2:
            num.append("1")
        # only the 7 has 3 input signals
        elif len(segment) == 3:
            num.append("7")
        # only the 4 has 4 input signals
        elif len(segment) == 4:
            num.append("4")
        # only the 8 has 7 input signals
        elif len(segment) == 7:
            num.append("8")
        # left over are 3 digits (2, 3, 5) with 5 input signals
        elif len(segment) == 5:
            # if both signals from 1 are in the 5 input signals
            if set(list(line[0][0])) < set(list(segment)):
                num.append("3")
            # if the signals from 4 - 1 are in the 5 input signals
            elif set([e for e in list(line[0][2]) if e not in list(line[0][0])]) < set(list(segment)):
                # list(line[0][2]).remove(line[0][0][0]).remove(line[0][0][1])
                num.append("5")
            # else it has to be the 2
            else:
                num.append("2")
        # and 3 digits (0, 6, 9) with 6 input signals
        elif len(segment) == 6:
            # if all the signals from 4 are in it
            if set(list(line[0][2])) < set(list(segment)):
                num.append("9")
            # if not! check if the signals from 1 are in it
            elif set(list(line[0][0])) < set(list(segment)):
                num.append("0")
            # else it has to be the 6
            else:
                num.append("6")
    result += int("".join(num))
print("What do you get if you add up all of the output values?", result)
