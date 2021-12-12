# visit small caves at most once, and can visit big caves any number of times
import numpy as np

with open('input.txt', 'r') as f:
    lines = f.readlines()
lines = [line[:-1] for line in lines]
lines = [line.split("-") for line in lines]

# just for the input
graph = {}
for line in lines:
    for idx, val in enumerate(line):
        if val in graph:
            graph[val].append(line[1-idx])
        else:
            graph[val] = [line[1-idx]]
del graph["end"]  # no need to know where we can go from the end
# we never want to go back to the start (thats why the entries get removed)
for key in graph:
    if "start" in graph[key]:
        graph[key].remove("start")

print(graph)
totalPaths = 0


def pathSearch(currentpoint: str, visited: list):
    global graph

    if currentpoint.islower():
        visited = np.append(currentpoint)

    if currentpoint == "end":
        global totalPaths
        totalPaths += 1
    else:
        for point in graph[currentpoint]:
            if point not in visited:
                pathSearch(point, visited)


pathSearch("start", [])
print("How many paths through this cave system are there that visit small caves at most once?", totalPaths)

# part2
totalPaths2 = 0


def pathSearch2(currentpoint: str, visited: list):
    global graph

    if currentpoint.islower():
        visited = np.append(visited, currentpoint)

    if currentpoint == "end":
        global totalPaths2
        totalPaths2 += 1
    else:
        for point in graph[currentpoint]:
            if point not in visited or len(visited) == len(set(visited)):
                pathSearch2(point, visited)


pathSearch2("start", [])
print("How many paths through this cave system are there?", totalPaths2)
