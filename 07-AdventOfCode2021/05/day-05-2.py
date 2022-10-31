import numpy as np

lines = open("input.txt", "r").readlines()
lines = [line[:-1] for line in lines]
lines = [line.split(" -> ") for line in lines]
lines = [list(([int(num) for num in coordinate.split(",")]) for coordinate in line) for line in lines]

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

# first do everything like in part 1
# filter all diagonal
straightlines = []
for idx, line in enumerate(lines):
    if (line[0][0] == line[1][0] or line[0][1] == line[1][1]):

        # the I don't want to come up with a smart solution so I'll just sort the coordinates part
        difference = np.diff([line[0], line[1]], axis=0)
        if np.sum(difference) < 0:
            straightlines.append(line[::-1])
        else:
            straightlines.append(line)

# "draw" lines in grid
for line in straightlines:
    # x fixed
    if line[0][0] == line[1][0]:
        for i in range(abs(line[0][1] - line[1][1]) + 1):
            grid[line[0][1] + i-1][line[0][0]-1] += 1  # y,x

    # y fixed
    if line[0][1] == line[1][1]:
        for i in range(abs(line[0][0] - line[1][0]) + 1):
            grid[line[0][1]-1][line[0][0] + i-1] += 1  # y,x

# now do it with the diagonal lines
# filter all straight lines
diagonallines = []
for idx, line in enumerate(lines):
    if not (line[0][0] == line[1][0] or line[0][1] == line[1][1]):
        # the I don't want to come up with a smart solution so I'll just sort the coordinates part
        if line[0][0]-line[1][0] > 0:
            diagonallines.append(line[::-1])
        else:
            diagonallines.append(line)

# "draw" lines in grid
for line in diagonallines:
    # always walk in x direction
    for i in range((line[1][0] - line[0][0]) + 1):
        if (line[0][1] - line[1][1]) < 0:
            grid[line[0][1] + i-1][line[0][0] + i - 1] += 1  # y,x
        else:
            grid[line[0][1] - i-1][line[0][0] + i - 1] += 1  # y,x

twoOverlaps = 0

for line in grid:
    for item in line:
        if item >= 2:
            twoOverlaps += 1

print("At how many points do at least two lines overlap?", twoOverlaps)

with open("output.txt", "w") as f:
    strgrid = []
    for line in grid:
        strline = ""
        for item in line:
            if item == 0:
                strline += "."
            else:
                strline += str(int(item))
        strgrid.append(strline + "\n")
    f.writelines(strgrid)

print(grid.shape)
