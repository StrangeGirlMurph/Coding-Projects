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


def checkWinning(idx):
    for boardNum, board in enumerate(marks):
        if 5 in np.sum(board, axis=0) or 5 in np.sum(board, axis=1):
            # checks both the columns and rows (based on the axis)
            calcScore(boardNum, idx)
            return True
    return False


def calcScore(boardNum, idx):
    board = boards[boardNum]
    marked = marks[boardNum]
    print(board)
    print(marked)
    sum = 0
    for (x, y), num in np.ndenumerate(board):
        if marked[x][y] == 0:
            sum += num

    print("What will your final score be if you choose that board?", sum * numbers[idx])


i = 0
for idx, num in enumerate(numbers):
    for (x, y, z), val in np.ndenumerate(boards):
        if num == val:
            marks[x][y][z] = 1

    if checkWinning(idx):
        break


# print(marks)
# print(boards)
# print(numbers)
