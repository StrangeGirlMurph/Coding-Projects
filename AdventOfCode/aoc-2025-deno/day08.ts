import {union} from "@std/collections"

const input = Deno.readTextFileSync("./day08.txt").trim().split("\n").map(l => l.split(",").map(v => parseInt(v)))

const distances = []

for (let i = 0; i < input.length; i++) {
    for (let j = 0; j < i; j++) {        
        const a = input[i]
        const b = input[j]
        const distance = Math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)
        distances.push([distance,i,j])
    }
}

distances.sort((a,b) => a[0] - b[0])

const circuits:number[][] = []

for (let n = 0; n < 1000; n++) {
    const distanceObject = distances[n];
    const a = distanceObject[1]
    const b = distanceObject[2]
    const includesA = circuits.findIndex(v => v.includes(a))
    const includesB = circuits.findIndex(v => v.includes(b))

    if (includesA != -1 && includesB != -1) {
        if (includesA == includesB) continue
        const merged = union(circuits[includesA], circuits[includesB])
        circuits.splice(includesA,1)
        circuits.splice(includesB-(includesA < includesB ? 1 : 0),1)
        circuits.unshift(merged)
    } else if (includesA != -1) {
        circuits[includesA].push(b)
    } else if (includesB != -1) {
        circuits[includesB].push(a)
    } else {
        circuits.push([a,b])
    }
}

const sizes = circuits.map(c => c.length)
sizes.sort((a, b) => b-a)

console.log(sizes[0] * sizes[1] * sizes[2])

for (let n = 1000; n < distances.length; n++) {
    const distanceObject = distances[n];
    const a = distanceObject[1]
    const b = distanceObject[2]
    const includesA = circuits.findIndex(v => v.includes(a))
    const includesB = circuits.findIndex(v => v.includes(b))

    if (includesA != -1 && includesB != -1) {
        if (includesA == includesB) continue
        const merged = union(circuits[includesA], circuits[includesB])
        circuits.splice(includesA,1)
        circuits.splice(includesB-(includesA < includesB ? 1 : 0),1)
        circuits.unshift(merged)
    } else if (includesA != -1) {
        circuits[includesA].push(b)
    } else if (includesB != -1) {
        circuits[includesB].push(a)
    } else {
        circuits.push([a,b])
    }

    if (circuits.length == 1 && circuits[0].length == input.length) {
        console.log(input[a][0] * input[b][0])
        break
    }
}