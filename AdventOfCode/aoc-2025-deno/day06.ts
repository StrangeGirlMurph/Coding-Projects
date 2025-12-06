const input = Deno.readTextFileSync("./day06.txt").trim().split("\n")

const split = input.map(l => l.split(/ +/))

let total = 0

for (let column = 0; column < split[0].length; column++) {
    const operation = split[4][column]

    let result = operation == "*" ? 1 : 0
    for (let i = 0; i < 4; i++) {
        const value = parseInt(split[i][column])
        if (operation == "*") {
            result *= value
        } else {
            result += value
        }
    }
    total += result
}

console.log(total)

total = 0

const operators = split[4]
const columnWise: number[][] = [[]]

for (let column = 0; column < input[0].length; column++) {
    let topToBottom = ""
    for (let row = 0; row < 4; row++) [
        topToBottom += input[row][column]
    ]

    const value = parseInt(topToBottom.trim())
    if (Number.isNaN(value)) {
        columnWise.push([])
    } else {
        columnWise[columnWise.length-1].push(value)
    }
} 

for (const [i, operator] of operators.entries()) {
    let result = operator == "*" ? 1 : 0
    for (const v of columnWise[i]) {
        if (operator == "*") {
            result *= v
        } else {
            result += v
        }
    }
    total += result
}

console.log(total)