import numpy as np
from tqdm import tqdm
targetX = np.arange(156, (202)+1)
targetY = np.arange(-110, (-69)+1)
print(targetX)
print(targetY)

# This isn't the most beautiful code I've ever written
# For this code to work and that in resonable time you have to tweak the numbers in the ranges based on your target and stuff


def highestY():
    global targetY
    global targetX

    for y in tqdm(range(200, 0, -1)):
        for x in range(1, 50):
            coordinates = [[0, 0]]

            while coordinates[-1][0] < max(targetX) and coordinates[-1][1] > min(targetY):
                numCoordinate = len(coordinates) - 1

                dy = y - (numCoordinate)
                dx = x - (numCoordinate)
                lastx = coordinates[-1][0]
                lasty = coordinates[-1][1]

                if dx >= 0:
                    coordinates.append([lastx + dx, lasty + dy])
                else:
                    coordinates.append([lastx, lasty + dy])

                if coordinates[-1][0] in targetX and coordinates[-1][1] in targetY:
                    return max(pos[1] for pos in coordinates), coordinates


def allHits():
    global targetY
    global targetX
    hits = 0

    for y in tqdm(range(120, -120, -1)):
        for x in range(5, 210):
            coordinates = [[0, 0]]

            while coordinates[-1][0] < max(targetX) and coordinates[-1][1] > min(targetY):
                numCoordinate = len(coordinates) - 1

                dy = y - (numCoordinate)
                dx = x - (numCoordinate)
                lastx = coordinates[-1][0]
                lasty = coordinates[-1][1]

                if dx >= 0:
                    coordinates.append([lastx + dx, lasty + dy])
                else:
                    coordinates.append([lastx, lasty + dy])

                if coordinates[-1][0] in targetX and coordinates[-1][1] in targetY:
                    hits += 1
                    break
    return hits


biggestY, coordinates = highestY()
print("What is the highest y position it reaches on this trajectory?", biggestY)

num = allHits()
print("How many distinct initial velocity values cause the probe to be within the target area after any step?", num)
