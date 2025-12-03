const input = Deno.readTextFileSync("./day03.txt").trim().split("\n").map(l => l.split("").map(i => parseInt(i)))

let total = 0

for (const bank of input)  {
    const first = Math.max(...bank.slice(0,-1))
    const pos = bank.findIndex(v => v == first)
    const second = Math.max(...bank.slice(pos+1))
    total += first * 10 + second
}

console.log(total)

total = 0

for (const bank of input)  {
    let lastpos = -1;
    for (let i = 1; i <= 12; i++) {
        const slice = bank.slice(lastpos + 1, i == 12 ? undefined : -(12-i))
        const next = Math.max(...slice)
        lastpos = lastpos + 1 + slice.findIndex(v => v == next)
        total += next * Math.pow(10,12-i)
    }
}

console.log(total)

