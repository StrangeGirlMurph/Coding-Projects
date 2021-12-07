# change in horizontal position costs 1 fuel
import numpy as np

line = open("input.txt", "r").read()
line = line[:-1].split(",")
grabs = [int(num) for num in line]

leastFuel = float("inf")
for i in range(min(grabs), max(grabs)+1):
    totalFuel = sum([abs(grab - i) for grab in grabs])
    if totalFuel < leastFuel:
        leastFuel = totalFuel

print("How much fuel must they spend to align to that position?", leastFuel)

# part2
leastFuel = float("inf")
for i in range(min(grabs), max(grabs)+1):
    totalFuel = sum([(abs(grab - i)*((abs(grab - i)+1))/2) for grab in grabs])  # gaussian sum formula
    if totalFuel < leastFuel:
        leastFuel = int(totalFuel)

print("How much fuel must they spend to align to that position?", leastFuel)
