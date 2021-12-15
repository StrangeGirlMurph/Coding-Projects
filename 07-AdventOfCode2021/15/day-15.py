import numpy as np

with open('input.txt', 'r') as f:
    lines = f.readlines()
lines = np.array([list(line[:-1]) for line in lines])
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
