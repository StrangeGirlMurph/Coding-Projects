# This code isn't used in any way.
# These are some of my attemps to make my algorithm work.
# This is just my storage unit for when I might get back to this.


def doubleCheckFirstHalf(grid, costs, NrDiagonal):
    allGood = True

    for element in range(0, NrDiagonal+1):
        xpos = (NrDiagonal-element) + 1  # position in the grid
        ypos = element + 1  # position in the grid
        up = costs[ypos-1][xpos]
        left = costs[ypos][xpos-1]

        if costs[ypos][xpos] + grid[ypos-1][xpos] < up:
            print("UP")
            print(grid)  # [ypos-2:ypos+3, xpos-2:xpos+3]
            print(costs)  # [ypos-2:ypos+3, xpos-2:xpos+3]

            costs[ypos-1][xpos] = costs[ypos][xpos] + grid[ypos-1][xpos]
            costs = checkValue(grid, costs, xpos+1, ypos-1)

            print("result")
            print(costs)  # [ypos-2:ypos+3, xpos-2:xpos+3]
            allGood = False

        if costs[ypos][xpos] + grid[ypos][xpos-1] < left:
            print("LEFT")
            print(grid)  # [ypos-2:ypos+3, xpos-2:xpos+3]
            print(costs)  # [ypos-2:ypos+3, xpos-2:xpos+3]

            costs[ypos][xpos-1] = costs[ypos][xpos] + grid[ypos][xpos-1]
            costs = checkValue(grid, costs, xpos-1, ypos+1)

            print("result")
            print(costs)  # [ypos-2:ypos+3, xpos-2:xpos+3]
            allGood = False

    if not allGood:
        costs, allGood = doubleCheckFirstHalf(grid, costs, NrDiagonal-1)

    return costs


def doubleCheckSecondHalf(grid, costs, NrDiagonal):
    gridSize = len(grid)
    allGood = True

    for element in range(0, gridSize-NrDiagonal):
        xpos = (element + NrDiagonal) + 1
        ypos = (gridSize-1-element) + 1
        up = costs[ypos-1][xpos]
        left = costs[ypos][xpos-1]

        if costs[ypos][xpos] + grid[ypos-1][xpos] < up:
            print("UP")
            print(grid)  # [ypos-2:ypos+3, xpos-2:xpos+3]
            print(costs)  # [ypos-2:ypos+3, xpos-2:xpos+3]

            costs[ypos-1][xpos] = costs[ypos][xpos] + grid[ypos-1][xpos]
            costs = checkValue(grid, costs, xpos+1, ypos-1)

            print("result")
            print(costs)  # [ypos-2:ypos+3, xpos-2:xpos+3]
            allGood = False
        if costs[ypos][xpos] + grid[ypos][xpos-1] < left:
            costs[ypos][xpos-1] = costs[ypos][xpos] + grid[ypos][xpos-1]
            costs = checkValue(grid, costs, xpos-1, ypos+1)
            allGood = False

    return costs
