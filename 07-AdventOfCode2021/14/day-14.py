import numpy as np
from tqdm import tqdm

with open('input.txt', 'r') as f:
    lines = f.readlines()
lines = [line[:-1].split(" -> ") for line in lines]

insertionRules = dict(lines)
TEMPLATE = list("SNVVKOBFKOPBFFFCPBSF")

# old part 1 now also works with part 2
template = list(TEMPLATE)  # copy

for i in range(1, 11):
    tempStr = template[0]

    for idx, val in enumerate(template[:-1]):
        if val + template[idx+1] in insertionRules:
            tempStr += insertionRules[val + template[idx+1]] + template[idx+1]
        else:
            tempStr += template[idx+1]
    template = list(tempStr)

count = [template.count(x) for x in set(template)]
print(sorted(count))
print("What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?", sorted(count)[-1] - sorted(count)[0])

# part 2
count = dict([(x, template.count(x)) for x in set(TEMPLATE)])

pairdict = {}
# creates a dict with the pairs and their number of pairs
for idx, char in enumerate(template[:-1]):
    pair = char + template[idx + 1]
    if pair in pairdict:
        pairdict[pair] += 1
    else:
        pairdict[pair] = 1

# print("Starting pairs:", pairdict)
# print("Starting count:", count)
# print("Rules", insertionRules)


def increasePair(dict, key, insertion, numtimes):
    pair1 = key[0] + insertion
    pair2 = insertion + key[1]

    dict.setdefault(pair1, 0)
    dict[pair1] += numtimes
    dict.setdefault(pair2, 0)
    dict[pair2] += numtimes

    dict[key] -= numtimes
    return dict


for i in range(1, 41):
    tempdict = dict(pairdict)

    for key in dict(pairdict):

        if key in insertionRules:
            tempdict = increasePair(tempdict, key, insertionRules[key], pairdict[key])

            count.setdefault(insertionRules[key], 0)
            count[insertionRules[key]] += pairdict[key]

    pairdict = tempdict

count = sorted(count.values())
print("What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?", count[-1] - count[0])
