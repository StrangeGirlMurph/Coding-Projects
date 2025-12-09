import { minBy } from "@std/collections/min-by";

const positions = Deno.readTextFileSync("./day09.txt").trim().split("\n").map(l => l.split(",").map(i => parseInt(i))) as [number, number][]

let max = -Infinity

for (let i = 0; i < positions.length; i++) {
    const a = positions[i]
    for (let j = positions.length-1; i < j; j--) {
        const b = positions[j]

        const s = size(a,b)
        if (s > max) max = s
    }
}

console.log(max)

// Part 2 takes about 50s!
max = -Infinity

const xValues = positions.map(v => v[0])
const yValues = positions.map(v => v[1])

const xMin = Math.min(...xValues)
const xMax = Math.max(...xValues)
const yMin = Math.min(...yValues)
const yMax = Math.max(...yValues)

// Generate edges
const horizontalEdges: [number,[number,number]][] = []
const verticalEdges: [number,[number,number]][] = []

for (let i = -1; i < positions.length - 1; i++) {
    const a = positions.at(i)!;
    const b = positions.at(i+1)!;
    
    if (a[0] == b[0]) {
        verticalEdges.push([a[0], a[1] <= b[1] ? [a[1], b[1]] : [b[1], a[1]]])
    } else {
        horizontalEdges.push([a[1], a[0] <= b[0] ? [a[0], b[0]] : [b[0], a[0]]])
    }
}

horizontalEdges.sort((a,b) => a[0] - b[0])
verticalEdges.sort((a,b) => a[0] - b[0])

// Check all rectangles
for (let i = 0; i < positions.length; i++) {
    const a = positions[i]
    const [ax, ay] = a

    let lastNotInside: [number, number] | null = null;
    for (let j = i+1; j < positions.length; j++) {
        const b = positions[j]
        const [bx, by] = b
        const s = size(a,b)

        // Only check if its even worth it
        if (s <= max) continue 

        // if it contains a smaller rectangle inside that isn't inside you can skip 
        if (lastNotInside && bx >= lastNotInside[0] && by >= lastNotInside[1]) continue
        
        // These cases are always inside
        if (j == i+1) {
            max = s
            continue
        }

        // Check the two corners first
        if (!(isInside([ax, by]) && isInside([bx, ay]))) continue

        // Check the edges of the rectangle
        let failed = false

        const edges: {
            start: number,
            end: number,
            getPoint: (i:number, a:[number, number],b:[number, number]) => [number, number],
        }[] = [
            {
                start: ax < bx ? ax : bx,
                end: ax < bx ? bx : ax,
                getPoint: (i,a,_b) => [i, a[1]]
            },
            {
                start: ax < bx ? ax : bx,
                end: ax < bx ? bx : ax,
                getPoint: (i,_a,b) => [i, b[1]]
            },
            {
                start: ay < by ? ay : by,
                end: ay < by ? by : ay,
                getPoint: (i,a,_b) => [a[0], i]
            },
            {
                start: ay < by ? ay : by,
                end: ay < by ? by : ay,
                getPoint: (i,_a,b) => [b[0], i]
            }
        ]

        edges:
        for (const edge of edges) {
            // Optimization idea: first go over every second pos and only then do the ones in between
            for (let i = edge.start+1; i < edge.end; i++) {
                if (!isInside(edge.getPoint(i,a,b))) {
                    failed = true
                    break edges
                }
            }
        }
        if (failed) {
            lastNotInside = b
            continue
        }

        // Is inside so update max :)
        max = s
    }
}

console.log(max)

function isInside(a: [number, number]): boolean {
    const [x,y] = a

    // The red tiles are always inside
    if (positions.findIndex(v => v[0] == x && v[1] == y) != -1) return true

    // Check if on an edge
    if (horizontalEdges.findIndex(v => v[0] == y && v[1][0] < x && x < v[1][1]) != -1) return true
    if (verticalEdges.findIndex(v => v[0] == x && v[1][0] < y && y < v[1][1]) != -1) return true

    const directions = [
        {dir: "-", axes: "y", diff: y - yMin},
        {dir: "+", axes: "x", diff: xMax - x},
        {dir: "+", axes: "y", diff: yMax - y},
        {dir: "-", axes: "x", diff: x - xMin}
    ]

    const direction = minBy(directions, el => el.diff)!

    // parallel and cross are both relative to the vector from x,y to the closest floor edge
    let crossEdges: [number,[number,number]][];
    let parallelEdges: [number,[number,number]][];
    let crossCoordinate: number;
    let parallelCoordinate: number;

    if (direction.axes == "y") {
        crossEdges = horizontalEdges
        parallelEdges = verticalEdges
        crossCoordinate = x
        parallelCoordinate = y
    } else {
        crossEdges = verticalEdges
        parallelEdges = horizontalEdges
        crossCoordinate = y
        parallelCoordinate = x
    }

    // Filter out all the parallel edges that are not on the right height
    parallelEdges = parallelEdges.filter(el => el[0] == crossCoordinate)

    // If we are going in + direction we will start checking from the highest values on
    if (direction.dir == "+") crossEdges.reverse()

    let crossings = 0

    // Count cross crossings
    for (let i = 0; i < crossEdges.length; i++){
        const edge = crossEdges[i]
        const edgeRange = edge[1]
        if (direction.dir == "+" ? edge[0] < parallelCoordinate : edge[0] > parallelCoordinate) break

        if (edgeRange[0] <= crossCoordinate && crossCoordinate <= edgeRange[1]) crossings++
    }

    // Count parallel crossings
    for (let i = 0; i < parallelEdges.length; i++){
        const edgeRange = parallelEdges[i][1]

        if (direction.dir == "+" ? parallelCoordinate <= edgeRange[0] && parallelCoordinate <= edgeRange[1] : edgeRange[0] <= parallelCoordinate && edgeRange[1] <= parallelCoordinate) crossings++        
    }

    // Undo the reverse
    if (direction.dir == "+") crossEdges.reverse()

    return crossings % 2 == 1
}

function size([ax,ay]: [number, number], [bx,by]: [number,number]): number {
    return (Math.abs(bx-ax) + 1) * (Math.abs(by-ay) + 1)
}
