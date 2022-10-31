import numpy as np

with open('input.txt', 'r') as f:
    lines = f.readlines()
lines = np.array([list(line[:-1]) for line in lines])
<<<<<<< HEAD
baseGrid = lines.astype(np.uint16)

baseGrid[0][0] = 0  # dont visit the start again

print(baseGrid)

# distances = np.zeros((100, 100))
# for (x, y), val in np.ndenumerate(distances):
#     distances[x][y] = x + y

# distances = distances[::-1, ::-1]  # flip
# print(distances)

bestScore = float("inf")


def searchPath(grid, posy, posx, currentscore):
    # search the adjacent sides recursively
    if posx + posy == 200:  # reached the end
        global bestScore
        if currentscore < bestScore:
            bestScore = currentscore
    else:
        # go through all neighbors
        for (dy, dx), val in np.ndenumerate(grid[posy-1:posy+2, posx-1:posx+2]):

            # if legal step (not already visited (val != 0) + (dy+dx) % 2 != 0 filters the diagonals)
            # dy+dx
            # 0 1 2
            # 1 2 3
            # 2 3 4
            if val != 0 and (dy+dx) % 2 != 0:
                newy = posy - 1 + dy
                newx = posx - 1 + dx

                currentscore += val

                tempGrid = grid
                tempGrid[newy][newx] = 0
                searchPath(tempGrid, newy, newx)


startingGrid = np.pad(baseGrid, 1, mode="constant", constant_values=0)
searchPath(startingGrid, posy=1, posx=1, currentscore=0)

print(bestScore)
=======
baseGrid = lines.astype(np.float32)
size = len(baseGrid)

# !!! This doesn't cover most cases. This probably only works for my input and the example Input. !!!


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


def doubleCheckFirstHalf(grid, costs, NrDiagonal):
    for element in range(0, NrDiagonal+1):
        xpos = (NrDiagonal-element) + 1  # position in the grid
        ypos = element + 1  # position in the grid
        up = costs[ypos-1][xpos]
        left = costs[ypos][xpos-1]

        if costs[ypos][xpos] + grid[ypos-1][xpos] < up:
            # print(grid)  # [ypos-2:ypos+3, xpos-2:xpos+3]
            # print(costs)  # [ypos-2:ypos+3, xpos-2:xpos+3]

            costs[ypos-1][xpos] = costs[ypos][xpos] + grid[ypos-1][xpos]
            costs = checkValue(grid, costs, xpos+1, ypos-1)

        if costs[ypos][xpos] + grid[ypos][xpos-1] < left:
            # print(grid)  # [ypos-2:ypos+3, xpos-2:xpos+3]
            # print(costs)  # [ypos-2:ypos+3, xpos-2:xpos+3]

            costs[ypos][xpos-1] = costs[ypos][xpos] + grid[ypos][xpos-1]
            costs = checkValue(grid, costs, xpos-1, ypos+1)

    return costs


def doubleCheckSecondHalf(grid, gridSize, costs, NrDiagonal):
    for element in range(0, gridSize-NrDiagonal):
        xpos = (element + NrDiagonal) + 1
        ypos = (gridSize-1-element) + 1
        up = costs[ypos-1][xpos]
        left = costs[ypos][xpos-1]

        if costs[ypos][xpos] + grid[ypos-1][xpos] < up:
            # print(grid)  # [ypos-2:ypos+3, xpos-2:xpos+3]
            # print(costs)  # [ypos-2:ypos+3, xpos-2:xpos+3]

            costs[ypos-1][xpos] = costs[ypos][xpos] + grid[ypos-1][xpos]
            costs = checkValue(grid, costs, xpos+1, ypos-1)

            # print(costs)  # [ypos-2:ypos+3, xpos-2:xpos+3]

        if costs[ypos][xpos] + grid[ypos][xpos-1] < left:
            costs[ypos][xpos-1] = costs[ypos][xpos] + grid[ypos][xpos-1]
            costs = checkValue(grid, costs, xpos-1, ypos+1)

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
        costs = doubleCheckFirstHalf(grid, costs, NrDiagonal)

    # loops through all the diagonals in second half
    for NrDiagonal in range(1, gridSize):
        costs = checksSecondhalf(grid, gridSize, costs, NrDiagonal)
        costs = doubleCheckSecondHalf(grid, gridSize, costs, NrDiagonal)

    print("Costs to reach every point:")
    print(costs[1:gridSize+1, 1:gridSize+1].astype(np.uint16))
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
>>>>>>> d799cf755a9d999e18230c9724332022f5601f15
