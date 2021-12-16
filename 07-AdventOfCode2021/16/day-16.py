import numpy as np

with open('input.txt', 'r') as f:
    hex = f.readline()[:-1]

basis = bin(int('1' + hex, 16))[3:]
sumVersionNumbers = 0


def determinReturnValue(results, typeID):
    if typeID == 0:
        return sum(results)
    elif typeID == 1:
        return np.prod(results)
    elif typeID == 2:
        return min(results)
    elif typeID == 3:
        return max(results)
    elif typeID == 5:
        return int(results[0] > results[1])
    elif typeID == 6:
        return int(results[0] < results[1])
    elif typeID == 7:
        return int(results[0] == results[1])


def readPacket(package):
    global sumVersionNumbers
    version = int(package[0:3], 2)  # packet verion
    typeID = int(package[3:6], 2)  # type ID
    body = package[6:]  # body

    sumVersionNumbers += version

    if typeID == 4:
        # literal value
        value = ""
        i = 0
        while body[i*5] == "1":
            value += body[(i*5)+1:(i+1)*5]
            i += 1
        value += body[(i*5)+1:(i+1)*5]  # include the last one
        value = int(value, 2)

        rest = body[(i+1)*5:]
        return rest, value
    else:
        # operator
        results = []
        lengthtypeID = body[0]

        if lengthtypeID == "0":
            # length in bits
            totalLength = int(body[1:16], 2)
            newbody = body[16:16+totalLength]

            while newbody != "" and "1" in newbody:
                newbody, value = readPacket(newbody)
                results.append(value)

            return body[16+totalLength:], determinReturnValue(results, typeID)
        else:
            # number of sub-packets
            numberSubpackets = int(body[1:12], 2)
            remainder = body[12:]
            for i in range(numberSubpackets):
                remainder, value = readPacket(remainder)
                results.append(value)

            return remainder, determinReturnValue(results, typeID)


remainder, finalvalue = readPacket(basis)

print("What do you get if you add up the version numbers in all packets?", sumVersionNumbers)
print("What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission?", finalvalue)
