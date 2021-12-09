# height from 9 to 0
# four adjacent locations (up, down, left, and right)

# 21---43210
# 3-878-4-21
# -85678-8-2
# 87678-678-
# -8---65678

import numpy as np
from scipy import ndimage

lines = open("input.txt", "r").readlines()
lines = [line[:-1] for line in lines]
lines = [list(int(item) for item in list(line)) for line in lines]

# part 1
grid = np.pad(lines, 1, mode="constant", constant_values=10)  # surrounds the 2d array with tens
# print(grid)

totalsum = 0
for (x, y), item in np.ndenumerate(grid):
    # filters the side panels
    if x != 0 and x != len(grid)-1 and y != 0 and y != len(grid[x])-1:
        if item < grid[x-1][y] and item < grid[x+1][y] and item < grid[x][y-1] and item < grid[x][y+1]:
            totalsum += item + 1

print("What is the sum of the risk levels of all low points on your heightmap?", totalsum)

# part 2
grid = np.where(np.array(lines) < 9, 1, 0)
labeled_array, num_features = ndimage.label(grid)  # default structure [[0,1,0], [1,1,1], [0,1,0]]

# print(labeled_array)

basin = np.zeros((num_features))
for (x, y), item in np.ndenumerate(labeled_array):
    if (item != 0):
        basin[item - 1] += 1

basin = sorted(basin)
prod = np.prod(basin[-3:])

print("What do you get if you multiply together the sizes of the three largest basins?", int(prod))
