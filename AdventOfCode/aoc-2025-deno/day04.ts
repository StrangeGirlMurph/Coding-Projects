const input = Deno.readTextFileSync("./day04.txt").trim().split("\n").map(v => v.split("").map(c => c == "@" ? 1 : 0))

const height = input.length 
const width = input[0].length

const neighborOffsets = [
    [-1,-1],
    [-1,0],
    [-1,1],
    [0,-1],
    [0,1],
    [1,-1],
    [1,0],
    [1,1],
]

let total = 0;

for (let row = 0; row < height; row++) {
    for (let column = 0; column < width; column++) {
        if (input[row][column] == 0) continue;
        
        let sum = 0;      

        for (const offset of neighborOffsets) {
            const r = row + offset[0]
            const c = column + offset[1]

            if (!(r < 0 || c < 0 || r >= height || c >= width)) {
                sum += input[r][c]
            }
        }

        if (sum < 4) {
            total += 1
        }
    }
}

console.log(total)

total = 0

while (true) {
    const accessible = []

    for (let row = 0; row < height; row++) {
        for (let column = 0; column < width; column++) {
            if (input[row][column] == 0) continue;
            
            let sum = 0;      

            for (const offset of neighborOffsets) {
                const r = row + offset[0]
                const c = column + offset[1]

                if (!(r < 0 || c < 0 || r >= height || c >= width)) {
                    sum += input[r][c]
                }
            }

            if (sum < 4) {
                accessible.push([row,column])
            }
        }
    }

    if (accessible.length == 0) break

    total += accessible.length

    for (const e of accessible) {
        input[e[0]][e[1]] = 0
    }
}

console.log(total)