# the number of times a depth measurement increases
lines = open("input.txt", "r").readlines()

# part 1
i = 0
numIncreases = 0
for line in lines[1:]:
    if int(line[:-1]) > int(lines[i][:-1]):
        numIncreases += 1
    i += 1
print("How many measurements are larger than the previous measurement?", numIncreases)

# part 2
i = 1
numIncreases = 0
for line in lines[1:]:
    if i < len(lines)-2:
        sum1 = int(lines[i-1][:-1]) + int(line[:-1]) + int(lines[i+1][:-1])
        sum2 = int(line[:-1]) + int(lines[i+1][:-1]) + int(lines[i+2][:-1])
        if sum1 < sum2:
            numIncreases += 1
    i += 1
print("Consider sums of a three-measurement sliding window. How many sums are larger than the previous sum?", numIncreases)
