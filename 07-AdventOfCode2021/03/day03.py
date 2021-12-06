import numpy as np
lines = open("input.txt", "r").readlines()
lines = [line[:-1] for line in lines]

# part 1


def part1():
    columns = [[], [], [], [], [], [], [], [], [], [], [], []]
    for entry in lines:
        columns = np.column_stack((columns, list(entry)))

    gamma_rate = ""
    epsilon_rate = ""
    for column in columns:
        if np.count_nonzero(column == "1") > len(column)/2:
            gamma_rate += "1"
            epsilon_rate += "0"
        else:
            gamma_rate += "0"
            epsilon_rate += "1"

    print(gamma_rate)
    print(epsilon_rate)

    print(int(gamma_rate, 2))
    print(int(epsilon_rate, 2))

    print("What is the power consumption of the submarine?", int(gamma_rate, 2)*int(epsilon_rate, 2))

# part 2


def part2():
    temp_lines = lines
    oxCriteria = ""

    for i in range(12):
        temp_lines = [l for l in temp_lines if l.startswith(oxCriteria)]  # filter all the crap out
        columns = [[], [], [], [], [], [], [], [], [], [], [], []]

        if len(temp_lines) == 1:
            break

        for entry in temp_lines:
            columns = np.column_stack((columns, list(entry)))

        if np.count_nonzero(columns[i] == "1") >= len(columns[i])/2:
            oxCriteria += "1"
        else:
            oxCriteria += "0"

    ox = temp_lines[0]
    print("oxygen criteria", oxCriteria)
    print(ox)

    temp_lines = lines
    co2Criteria = ""

    for i in range(12):
        temp_lines = [l for l in temp_lines if l.startswith(co2Criteria)]  # filter all the crap out
        columns = [[], [], [], [], [], [], [], [], [], [], [], []]

        if len(temp_lines) == 1:
            break

        for entry in temp_lines:
            columns = np.column_stack((columns, list(entry)))

        if np.count_nonzero(columns[i] == "0") <= len(columns[i])/2:
            co2Criteria += "0"
        else:
            co2Criteria += "1"

    co2 = temp_lines[0]
    print("CO2 criteria", co2Criteria)
    print(co2)

    print("What is the life support rating of the submarine?", int(ox, 2)*int(co2, 2))


part1()
part2()
