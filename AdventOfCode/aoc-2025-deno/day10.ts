import { distinct } from "@std/collections";

const input = Deno.readTextFileSync("./day10.txt").trim().split("\n")

const binaryInput = input.map(l => l.split(" ").map((v) => {
    if (v.startsWith("[")) {
        // As binary number from right to left
        return parseInt(v.slice(1,-1).split("").map(e => e == "#" ? "1" : "0").reverse().join(""),2)
    } else if (v.startsWith("{")) {
        return v.slice(1,-1).split(",").map(e => parseInt(e))
    } else {
        // Binary number combining all lights a button toggles
        return v.slice(1,-1).split(",").map(e => parseInt(e)).reduce((p,c) => p ^ (1 << c), 0)
    }
})) as [number, number[], number[]][]

let sum = 0

for (const machine of binaryInput) {
    const lights = machine[0]
    const buttons = machine.slice(1,-1) as number[]

    const combinationsInBinary = Array.from({length: 2**buttons.length -1}, (_, i) => i + 1).sort((a,b) => countBinaryOnes(a) - countBinaryOnes(b))

    let min = Infinity
    for (const combination of combinationsInBinary) {
        let test = lights
        const steps = countBinaryOnes(combination)
        for (const [i, v] of combination.toString(2).split("").reverse().entries()) {
            if (v == "1") {
                test ^= buttons[i]
            }
        }
        if (test == 0) {
            min = steps
            break
        }
    }

    sum += min
}

console.log(sum)

// Start for part 2 - Doesn't takes forever! I didn't get that part
const joltageInput = input.map(l => l.split(" ").map((v) => {
    if (v.startsWith("[")) {
        return v
    } else if (v.startsWith("{")) {
        return v.slice(1,-1).split(",").map(e => parseInt(e))
    } else {
        return v.slice(1,-1).split(",").map(e => parseInt(e))
    }
})) as [string, number[][], number[]][]

sum = 0

for (const [i, machine] of joltageInput.entries()) {
    console.log("Machine: " + (i+1))

    const joltages = machine.at(-1)! as number[]
    const buttons = machine.slice(1,-1).sort((a,b) => b.length - a.length) as number[][]

    sum += minimumSteps(joltages, buttons, 0, new Map<string, number>())
}

function minimumSteps(joltages:number[], buttons: number[][], steps: number, cache: Map<string, number>): number {
    // Check if in cache
    if (cache.has(joltages.toString())) return steps + cache.get(joltages.toString())!

    // Check if one button can end it all
    if (distinct(joltages).length == 2 && joltages.includes(0)) {
        const index = buttons.findIndex(button => button.every(b => joltages.map((v,i) => v == 1 ? i: -1).includes(b)))
        if (index != 1) return steps + joltages[buttons[index][0]]
    } 
    
    // Check if we overshot
    if (joltages.some(v => v < 0)) return Infinity
    
    // Check if we arrived at a solution
    if (joltages.every(v => v == 0)) return steps

    steps++
    const minSteps = Math.min(...buttons.map(button => {
        const copy = [...joltages]
        for (const pos of button) {
            copy[pos]--
        }
        return minimumSteps(copy, buttons, steps, cache)
    }));

    cache.set(joltages.toString(), minSteps-(steps-1))
    return minSteps
}

console.log(sum)

function countBinaryOnes(n: number) {
  let c = 0;
  do { c += n & 1 } while ((n >>= 1) != 0)
  return c;
}