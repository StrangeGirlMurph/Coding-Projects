lines = open("input.txt", "r").readlines()

# part 1
start = [0, 0]  # horizontal pos, depth
for line in lines:
    line = line[:-1].split()
    if line[0] == "up":
        start[1] -= int(line[1])
    elif line[0] == "down":
        start[1] += int(line[1])
    elif line[0] == "forward":
        start[0] += int(line[1])
print("Ending horizontal position:", start[0])
print("Ending depth:", start[1])
print("What do you get if you multiply your final horizontal position by your final depth?", start[0]*start[1])

# part 2
start = [0, 0, 0]  # horizontal pos, depth, aim
for line in lines:
    line = line[:-1].split()
    if line[0] == "up":
        start[2] -= int(line[1])
    elif line[0] == "down":
        start[2] += int(line[1])
    elif line[0] == "forward":
        start[0] += int(line[1])
        start[1] += start[2] * int(line[1])

print("Ending horizontal position:", start[0])
print("Ending depth:", start[1])
print("Ending aim:", start[2])
print("What do you get if you multiply your final horizontal position by your final depth?", start[0]*start[1])
