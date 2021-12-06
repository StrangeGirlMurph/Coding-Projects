import numpy as np

line = open("input.txt", "r").read()
line = line[:-1].split(",")
fish = [int(num) for num in line]

groupedfish = []
for i in range(0, 9):
    groupedfish.append(len([f for f in fish if f == i]))
groupedfish = np.array(groupedfish)

for i in range(256):
    groupedfishtemp = np.empty((9), np.uint64)

    for l in range(8):
        groupedfishtemp[l] = groupedfish[l + 1]
    groupedfishtemp[6] += groupedfish[0]
    groupedfishtemp[8] = groupedfish[0]

    groupedfish = groupedfishtemp

print("How many lanternfish would there be after 256 days?", np.sum(groupedfish))
