import numpy as np

with open('testinput.txt', 'r') as f:
    lines = f.readlines()
lines = np.array([list(line[:-1]) for line in lines])
baseGrid = lines.astype(np.uint16)
size = len(baseGrid)


def findCheapestPath(grid):
    gridSize = len(grid)

    costs = np.zeros((gridSize, gridSize), dtype=np.uint32)
    costs = costs + float("inf")
    costs[0][0] = 0

    # loops through all the diagonals
    for NrDiagonal in range(1, gridSize):

        # goes through all the elements in that diagonal
        for idxY in range(0, NrDiagonal+1):

            # edge cases
            if idxY == 0:
                costs[0][NrDiagonal] = costs[0][NrDiagonal-1] + grid[0][NrDiagonal]
            elif idxY == NrDiagonal:
                costs[NrDiagonal][0] = costs[NrDiagonal-1][0] + grid[NrDiagonal][0]
            else:
                costs[idxY][NrDiagonal-idxY] = min([costs[idxY-1][NrDiagonal-idxY], costs[idxY][NrDiagonal-idxY-1]]) + grid[idxY][NrDiagonal-idxY]

    # loops through all the diagonals second half
    for NrDiagonal in range(1, gridSize):
        # goes through all the elements in that diagonal
        for idxX in range(0, gridSize-NrDiagonal):
            costs[gridSize-1-idxX][NrDiagonal + idxX] = min([costs[gridSize-1-idxX][NrDiagonal + idxX-1], costs[gridSize-1-idxX-1][NrDiagonal + idxX]]) + grid[gridSize-1-idxX][NrDiagonal + idxX]

    print(costs)
    print("What is the lowest total risk of any path from the top left to the bottom right?", int(costs[-1][-1]))


# part 1
Grid1 = np.copy(baseGrid)
Grid1[0][0] = 0  # dont visit the start again
findCheapestPath(Grid1)

# part 2
Grid2 = np.tile(baseGrid, (5, 5))

for (dy, dx), val in np.ndenumerate(np.zeros((5, 5))):
    Grid2[(dy*size):((dy+1)*size), (dx*size):((dx+1)*size)] += dy+dx  # chunks
    Grid2[(dy*size):((dy+1)*size), (dx*size):((dx+1)*size)] = Grid2[(dy*size):((dy+1)*size), (dx*size):((dx+1)*size)] % 9

Grid2[Grid2 == 0] = 9
Grid2[0][0] = 0

# findCheapestPath(Grid2)
