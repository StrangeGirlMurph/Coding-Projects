import numpy as np

with open('input.txt', 'r') as f:
    hex = f.readline()[:-1]

testLiteral = "D2FE28"  # 2021
testOperatorID0 = "38006F45291200"
testOperatorID1 = "EE00D40C823060"
test = "8A004A801A8002F478"
test2 = "620080001611562C8802118E34"

basis = bin(int('1' + hex, 16))[3:]

sumVersionNumbers = 0
result = 0


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
        return rest
    else:
        # operator

        lengthtypeID = body[0]

        if lengthtypeID == "0":
            # length in bits
            totalLength = int(body[1:16], 2)
            newbody = body[16:16+totalLength]
            while newbody != "" and "1" in newbody:
                newbody = readPacket(newbody)

            return body[16+totalLength:]
        else:
            # number of sub-packets
            numberSubpackets = int(body[1:12], 2)
            remainder = body[12:]
            for i in range(numberSubpackets):
                remainder = readPacket(remainder)
            return remainder


def main(basis):
    remainder = basis

    while remainder != "" and "1" in remainder:
        remainder = readPacket(remainder)


main(basis)

print("What do you get if you add up the version numbers in all packets?", sumVersionNumbers)
print("What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission?", result)
