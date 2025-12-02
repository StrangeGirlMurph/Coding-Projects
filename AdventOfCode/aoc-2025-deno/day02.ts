const input = Deno.readTextFileSync("./day02.txt").trim().split(",").map(s => s.split("-").map(t => parseInt(t))) as [number, number][]

let sum = 0;

for (const range of input) {
    const start = range[0]
    const end = range[1]

    for (let i = start; i <= end; i++) {
        const s = i.toString()
        const len = s.length
        if (len % 2 != 0) continue
        else if (s.slice(0, len/2) == s.slice(len/2)) sum += i
    }
}

console.log(sum)

sum = 0;

for (const range of input) {
    const start = range[0]
    const end = range[1]

    for (let i = start; i <= end; i++) {
        const s = i.toString()
        if (/^([1-9]\d*)\1+$/.test(s)) sum += i
    }
}

console.log(sum)

