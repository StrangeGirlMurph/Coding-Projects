# 5x5
# mark number on every board
# a full row/column wins
# score: sum of all unmarked numbers on the board times the winning number
import numpy as np

lines = open("input.txt", "r").readlines()
lines = [line[:-1] for line in lines]

numbers = lines[0].split(",")
numbers = [int(num) for num in numbers]

lines = lines[1:]  # remove numbers
lines = [line for line in lines if line != ""]

boards = np.array_split(lines, len(lines)/5)
# from 2d array based on strings to 3d with the numbers
boards = [list(([int(num) for num in row.split()]) for row in board) for board in boards]

marks = np.zeros((len(boards), 5, 5))  # stores the marked places

score = 0


for num in numbers:
    # set marks
    for (x, y, z), val in np.ndenumerate(boards):
        if num == val:
            marks[x][y][z] = 1

    # check if one wins
    deletion = []
    for markedboardNum, markedboard in enumerate(marks):
        if 5 in np.sum(markedboard, axis=0) or 5 in np.sum(markedboard, axis=1):
            # checks both the columns and rows (based on the axis)

            sum = 0
            print(len(boards[markedboardNum]))
            for (x, y), number in np.ndenumerate(boards[markedboardNum]):
                if markedboard[x][y] == 0:
                    sum += number

            score = sum * num
            deletion.append(markedboardNum)

    dew = 0
    for i in deletion:
        del boards[i-dew]
        marks = np.delete(marks, i-dew, 0)
        dew += 1


print("Once it wins, what would its final score be?", score)


# print(marks)
# print(boards)
# print(numbers)
