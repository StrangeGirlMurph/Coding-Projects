# at least 12 beacons

# This isn't working!
# Unable to allocate 7.46 GiB for an array with shape (2001, 2001, 2001) and data type bool!!!!


import numpy as np

with open('input.txt', 'r') as f:
    lines = f.readlines()

# getting the input right
scanners = []
i = 0
for line in lines:
    if line == f"--- scanner {i} ---\n":
        scanners.append([])
        i += 1
    elif line != "\n":
        scanners[-1].append(line[:-1])

scanners = [[[int(item) for item in coordinate.split(",")] for coordinate in scanner] for scanner in scanners]

for scanner in scanners:
    if len(scanner) == 25:
        scanner.append([0, 0, 0])
scanners = np.array(scanners)
print(scanners)


def getCubeRepresentation(scanner):
    cube = np.zeros((2001, 2001, 2001), dtype=np.bool_)

    cube[1000][1000][1000] = 2  # code for scanner

    for coordinate in scanner:
        if coordinate.all():
            x = 1000 + coordinate[0]
            y = 1000 + coordinate[1]
            z = 1000 + coordinate[2]

            cube[x][y][z] = 1  # code for beacon
    return cube


cubes = []
for scanner in scanners:
    cubes.append(getCubeRepresentation(scanner))

print(cubes)
