import numpy as np

with open('input coordinates.txt', 'r') as f:
    coordinates = f.readlines()
coordinates = [line[:-1].split(",") for line in coordinates]
coordinates = [[int(item) for item in line] for line in coordinates]
coordinates = np.array(coordinates)

with open('input folding.txt', 'r') as f:
    foldingInstructions = f.readlines()
foldingInstructions = [line[:-1].split()[2].split("=") for line in foldingInstructions]
foldingInstructions = [[item[0], int(item[1])] for item in foldingInstructions]

paper = np.zeros((np.amax(coordinates[:, 1])+1, np.amax(coordinates[:, 0])+1))
print(paper.shape)

for coordinate in coordinates:
    paper[coordinate[1]][coordinate[0]] = 1

for fold in foldingInstructions:
    if fold[0] == "x":
        x = fold[1]
        lefthalf = paper[:, :x]
        righthalf = paper[:, x:]

        for (row, col), val in np.ndenumerate(lefthalf):
            if righthalf[row][len(righthalf[row])-1-col] == 1:
                lefthalf[row][col] = 1

        paper = lefthalf
    elif fold[0] == "y":
        y = fold[1]
        tophalf = paper[:y]
        bottomhalf = paper[y:]

        for (row, col), val in np.ndenumerate(tophalf):
            if bottomhalf[len(bottomhalf)-1-row][col] == 1:
                tophalf[row][col] = 1

        paper = tophalf
    # break # uncomment for part 1

print("How many dots are visible after completing just the first fold instruction on your transparent paper?", np.count_nonzero(paper))

# part 2
with open("output.txt", "w") as f:
    strgrid = []
    for line in paper:
        strline = ""
        for item in line:
            if item == 0:
                strline += "_"
            else:
                strline += "1"
        strgrid.append(strline + "\n")
    f.writelines(strgrid)
