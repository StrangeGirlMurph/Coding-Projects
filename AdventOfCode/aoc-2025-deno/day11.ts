const input = Deno.readTextFileSync("./day11.txt").trim().split("\n").map(l => l.split(": "))

const map = new Map<string, string[]>()

for (const device of input) {
    map.set(device[0], device[1].split(" "))
}

let total = findPaths("you")
console.log(total)

function findPaths(device: string): number {
    if (device == "out") return 1 

    let numberOfPaths = 0
    for (const next of map.get(device)!) {
        numberOfPaths += findPaths(next)
    }

    return numberOfPaths
}

const cache = new Map<string, number>()
total = findPathsWith("svr", false, false, cache)
console.log(total)

function findPathsWith(current: string, seenDAC: boolean, seenFFT: boolean, cache: Map<string, number>): number {
    const argString = current + (seenDAC ? "1" : "0") + (seenFFT ? "1" : "0")
    if (cache.has(argString)) return cache.get(argString)!

    switch (current) {
        case "dac":
            seenDAC = true
            break;
        case "fft":
            seenFFT = true
            break;
        case "out": 
            if (seenDAC && seenFFT) return 1
            else return 0
        default:
            break;
    }

    let numberOfPaths = 0
    for (const device of map.get(current)!) {
        numberOfPaths += findPathsWith(device, seenDAC, seenFFT, cache)
    }

    cache.set(argString, numberOfPaths)
    return numberOfPaths
}