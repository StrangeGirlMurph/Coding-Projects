const input = Deno.readTextFileSync("./day07.txt").trim().split("\n").map(v => v.split(""))

let count = 0

const manifolds = deepCopy(input)
manifolds[0][manifolds[0].indexOf("S")] = "|"

for (let row = 1; row < manifolds.length; row++) {
    const above = manifolds[row-1]

    for (const [column, value] of manifolds[row].entries()) {
        if (above[column] == "|") {
            if (value == ".") {
                manifolds[row][column] = "|"
            } else if (value == "^") {
                count++
                manifolds[row][column-1] = "|"
                manifolds[row][column+1] = "|"
            }
        }
    }
}

console.log(count)

const quantumManifolds: (number | "^")[][] = deepCopy(input).map(l => l.map(v => v == "." ? 0: "^"))
quantumManifolds[0][input[0].indexOf("S")] = 1

for (let row = 1; row < quantumManifolds.length; row++) {
    const above = quantumManifolds[row-1]    

    for (const [column, value] of quantumManifolds[row].entries()) {
        const valueAbove = above[column]

        if (typeof valueAbove == "number") {
            if (value == "^") {
                (quantumManifolds[row][column-1] as number) += valueAbove;
                (quantumManifolds[row][column+1] as number) += valueAbove
            } else {
                (quantumManifolds[row][column] as number) += valueAbove
            }
        }
    }
}

const paths = (quantumManifolds.at(-1)! as number[]).reduce((p,c) => p+c,0)

console.log(paths)

function deepCopy(a: string[][]): string[][] {
    const b: string[][] = []
    a.forEach(l => {b.push([...l])})
    return b
}