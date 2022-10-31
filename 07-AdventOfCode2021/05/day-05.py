import numpy as np

lines = open("input.txt", "r").readlines()
lines = [line[:-1] for line in lines]
lines = [line.split(" -> ") for line in lines]
lines = [list(([int(num) for num in coordinate.split(",")]) for coordinate in line) for line in lines]

# filter all diagonal
templines = []
for idx, line in enumerate(lines):
    if (line[0][0] == line[1][0] or line[0][1] == line[1][1]):

        # the I don't want to come up with a smart solution so I'll just sort the coordinates part
        difference = np.diff([line[0], line[1]], axis=0)
        if np.sum(difference) < 0:
            templines.append(line[::-1])
        else:
            templines.append(line)

lines = templines

# print(lines)

# find biggest values
biggestX = 0
biggestY = 0
for line in lines:
    for coordinate in line:
        if coordinate[0] > biggestX:
            biggestX = coordinate[0]
        if coordinate[1] > biggestY:
            biggestY = coordinate[1]
grid = np.zeros((biggestY, biggestX))

# "draw" lines in grid
for line in lines:
    # x fixed
    if line[0][0] == line[1][0]:
        for i in range(abs(line[0][1] - line[1][1]) + 1):
            grid[line[0][1] + i-1][line[0][0]-1] += 1  # y,x

    # y fixed
    if line[0][1] == line[1][1]:
        for i in range(abs(line[0][0] - line[1][0]) + 1):
            grid[line[0][1]-1][line[0][0] + i-1] += 1  # y,x

twoOverlaps = 0

for line in grid:
    for item in line:
        if item >= 2:
            twoOverlaps += 1

# print(grid)

print("At how many points do at least two lines overlap?", twoOverlaps)
