# Each octopus slowly gains energy over time and flashes brightly for a moment when its energy is full.
# step:
# First, the energy level of each octopus increases by 1.
# Then, any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. If this causes an octopus to have an energy level greater than 9, it also flashes. This process continues as long as new octopuses keep having their energy level increased beyond 9. (An octopus can only flash at most once per step.)
# Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to flash.

import numpy as np

with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [line[:-1] for line in lines]
lines = [list(line) for line in lines]
grid = np.array([list(int(item) for item in line) for line in lines])

totalFlashes = 0
print(grid)
for step in range(1, 101):
    # 1. increase energy level by 1
    grid += 1

    # 2./3. flashing
    while np.count_nonzero(grid > 9) > 0:
        # loops aslong as there are values greater then 9 in the grid

        for (x, y), val in np.ndenumerate(grid):
            if val > 9:
                grid[x][y] = 0  # octopus flashes
                totalFlashes += 1

                # increases the energy level of all adjacent octopuses by 1
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        # checks which didnt flash this step (padding for the borders)
                        if np.pad(grid, 1, mode="constant", constant_values=0)[1 + x + dx][1 + y + dy] != 0:
                            grid[x + dx][y + dy] += 1

print("How many total flashes are there after 100 steps?", totalFlashes)

# part 2
grid = np.array([list(int(item) for item in line) for line in lines])

numSteps = 0
for step in range(1, 100000):
    # 1. increase energy level by 1
    grid += 1

    # 2./3. flashing
    while np.count_nonzero(grid > 9) > 0:
        # loops aslong as there are values greater then 9 in the grid

        for (x, y), val in np.ndenumerate(grid):
            if val > 9:
                grid[x][y] = 0  # octopus flashes
                totalFlashes += 1

                # increases the energy level of all adjacent octopuses by 1
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        # checks which didnt flash this step (padding for the borders)
                        if np.pad(grid, 1, mode="constant", constant_values=0)[1 + x + dx][1 + y + dy] != 0:
                            grid[x + dx][y + dy] += 1

    if not np.any(grid):
        numSteps = step
        break

print("What is the first step during which all octopuses flash?", numSteps)
