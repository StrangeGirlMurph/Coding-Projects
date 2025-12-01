const input = Deno.readTextFileSync("./day01.txt").split("\n").map(v => [v[0], parseInt(v.slice(1))]) as [string, number][]

let pos = 50;
let countAtZero = 0;

for (const i of input) {
    if (i[0] == "R") {
        pos = (pos + i[1]) % 100 
    } else {
        pos = pos - i[1] % 100
        if (pos < 0) pos += 100
    }
    if (pos == 0) countAtZero++
}

console.log(countAtZero)

pos = 50;
countAtZero = 0;

for (const i of input) {
    countAtZero += Math.floor(i[1] / 100)
    const old = pos
    if (i[0] == "R") {
        pos = (pos + i[1]) % 100
        if (pos < old) countAtZero++
    } else {
        pos = pos - i[1] % 100
        if (pos < 0) pos += 100
        if ((pos > old && old != 0)  || (pos == 0 && i[1] % 100 != 0)) countAtZero++
    }
}

console.log(countAtZero)