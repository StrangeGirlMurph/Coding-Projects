import numpy as np

with open('input.txt', 'r') as f:
    lines = f.readlines()
lines = np.array([list(line[:-1]) for line in lines])
baseGrid = lines.astype(np.float32)
size = len(baseGrid)

# !!! This doesn't cover most cases. Both parts currently only work for the example input. !!!
# For my input it only works for part 1


def checkValue(grid, costs, xpos, ypos):
    up = costs[ypos-1][xpos]
    left = costs[ypos][xpos-1]

    if grid[ypos][xpos] != float("inf"):
        if up < left:
            costs[ypos][xpos] = up + grid[ypos][xpos]
        else:
            costs[ypos][xpos] = left + grid[ypos][xpos]
    return costs


def checksFirsthalf(grid, costs, NrDiagonal):
    # goes through all the elements in that diagonal from the upper right to the bottom left corner
    for element in range(0, NrDiagonal+1):
        xpos = (NrDiagonal-element) + 1  # position in the grid
        ypos = element + 1  # position in the grid

        costs = checkValue(grid, costs, xpos, ypos)
    return costs


def checksSecondhalf(grid, gridSize, costs, NrDiagonal):
    # goes through all the elements in that diagonal from the bottom left to the upper right corner
    for element in range(0, gridSize-NrDiagonal):
        xpos = (element + NrDiagonal) + 1
        ypos = (gridSize-1-element) + 1

        costs = checkValue(grid, costs, xpos, ypos)
    return costs


def findCheapestPath(grid):
    gridSize = len(grid)
    grid = np.pad(grid, 1, mode="constant", constant_values=float("inf"))

    costs = np.zeros((gridSize, gridSize))
    costs = costs + float("inf")
    costs[0][0] = 0
    costs = np.pad(costs, 1, mode="constant", constant_values=float("inf"))

    # loops through all the diagonals
    for NrDiagonal in range(1, gridSize):
        costs = checksFirsthalf(grid, costs, NrDiagonal)

    # loops through all the diagonals in second half
    for NrDiagonal in range(1, gridSize):
        costs = checksSecondhalf(grid, gridSize, costs, NrDiagonal)

    print("Costs to reach every point:")
    print(costs[1:gridSize+1, 1:gridSize+1])
    print("What is the lowest total risk of any path from the top left to the bottom right?", int(costs[-2][-2]))


# part 1
Grid1 = np.copy(baseGrid)
Grid1[0][0] = 0  # dont visit the start again
findCheapestPath(Grid1)

# modifying the grid for part 2
Grid2 = np.tile(baseGrid, (5, 5))
for (dy, dx), val in np.ndenumerate(np.zeros((5, 5))):
    Grid2[(dy*size):((dy+1)*size), (dx*size):((dx+1)*size)] += dy+dx  # chunks
    Grid2[(dy*size):((dy+1)*size), (dx*size):((dx+1)*size)] = Grid2[(dy*size):((dy+1)*size), (dx*size):((dx+1)*size)] % 9

Grid2[Grid2 == 0] = 9
Grid2[0][0] = 0
findCheapestPath(Grid2)
