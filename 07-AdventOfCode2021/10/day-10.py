# A corrupted line is one where a chunk closes with the wrong character
# the first illegal character
# ): 3 points.
# ]: 57 points.
# }: 1197 points.
# >: 25137 points.

import numpy as np

lines = open("input.txt", "r").readlines()
lines = [line[:-1] for line in lines]
lines = [list(line) for line in lines]

closingBrackets = [")", "]", "}", ">"]
matching = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}
points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}
score = {
    ")": 0,
    "]": 0,
    "}": 0,
    ">": 0
}

filteredLines = []  # for part 2
for lineidx, line in enumerate(lines):
    while line:  # list is not empty
        somethingiswrong = False

        if set(closingBrackets).isdisjoint(line):
            # checks if line is incomplete
            filteredLines.append(line)  # for part 2
            break
        else:
            for idx, i in enumerate(line):
                if idx != len(line) - 1:
                    if line[idx + 1] in closingBrackets:
                        if matching[i] == line[idx + 1]:
                            del line[idx:idx+2]
                            break
                        else:
                            score[line[idx + 1]] += 1
                            somethingiswrong = True
                            break
        if somethingiswrong:
            break

for bracket in points:
    points[bracket] *= score[bracket]


print("What is the total syntax error score for those errors?", sum(points.values()))

# part 2
autocompletePoints = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}

scores = []
for line in filteredLines:
    score = 0
    for i in line[::-1]:
        score *= 5
        score += autocompletePoints[i]
    scores.append(score)

print("What is the middle score?", sorted(scores)[int((len(scores)-1)/2)])
