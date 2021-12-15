import numpy as np

with open('input.txt', 'r') as f:
    lines = f.readlines()
lines = np.array([list(line[:-1]) for line in lines])
grid = lines.astype(np.uint16)
print(grid)

distances = np.zeros((100, 100))
for (x, y), val in np.ndenumerate(distances):
    distances[x][y] = x + y

distances = distances[::-1, ::-1]  # flip
print(distances)
