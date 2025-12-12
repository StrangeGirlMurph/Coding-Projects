const input = Deno.readTextFileSync("./day12.txt").trim().split("\n\n")

const shapes = input.slice(0,-1).map(s => s.split(":\n")[1].split("\n").map(l => l.split("").map(v => v == "#" ? 1 : 0))).map(s => ({area: s.reduce<number>((p,c) => p + c.reduce<number>((pp,cc) => pp+cc, 0),0), mask: s}))

// Because presents can be rotated and flipped I can freely flip width and length here
const regions = input.at(-1)!.split("\n").map(l => l.split(": ").map((v,i) => i == 0 ? v.split("x").map(v => parseInt(v)).sort((a,b) => a-b) : v.split(" ").map(v => parseInt(v))))

console.log(`There are ${shapes.length} shapes and ${regions.length} regions`)

// Regions are sorted by region area first and by are of all the shapes second
regions.sort((a,b) => (a[0][0] * a[0][1] - b[0][0] * b[0][1]) || (a[1].reduce((p,c,i) => p+(c * shapes[i].area), 0) - b[1].reduce((p,c,i) => p+(c * shapes[i].area), 0)))

// Compress all regions with the same width and length into one object
const compressedRegions: {h: number, w: number, quantities: number[][]}[] = [];
for (const region of regions) {
    const h = region[0][0];
    const w = region[0][1];
    
    let existing = compressedRegions.find(r => r.h === h && r.w === w);
    if (!existing) {
        existing = { h, w, quantities: [] };
        compressedRegions.push(existing);
    }
    existing.quantities.push(region[1]);
}

// Generate all rotated and mirrored versions
const shapeVariants: {area: number, orientations: [number, number][][]}[] = []

for (const shape of shapes) {
    const baseOffsets: [number, number][] = []
    
    // Translate the mask into offsets
    for (let i = 0; i < shape.mask.length; i++) {
        for (let j = 0; j < shape.mask[i].length; j++) {
            if (shape.mask[i][j] == 1) baseOffsets.push([i,j])
        }
    }

    const allVariants = [baseOffsets]

    // All rotations
    for (let i = 0; i < 3; i++) {
        // Transpose + flip along y = 90° clockwise rotation
        allVariants.push(allVariants[i].map(v => [...v].reverse() as [number, number]).map(v => [v[0], -v[1]+2]))
    }

    // All mirror images
    for (let i = 0; i < 4; i++) {
        allVariants.push(allVariants[i].map(v => [v[0], -v[1]+2]))
    }

    // Remove duplicates
    const distinctVariants: [number, number][][] = []
    for (const variant of allVariants) {
        if (!distinctVariants.some(distinctVariant => distinctVariant.every(testOffset => variant.findIndex(offset => testOffset[0] == offset[0] && testOffset[1] == offset[1]) != -1))) {
            distinctVariants.push(variant)
        }
    }

    shapeVariants.push({area: shape.area, orientations: distinctVariants})
}

let count = 0

for (const region of compressedRegions) {
    const h = region.h
    const w = region.w
    const s = h * w

    for (const quantities of region.quantities) {
        // Remove all the ones that don't even fit by area size
        if (s < quantities.map((v,i) => v * shapes[i].area).reduce((p,c) => p + c,0)) break

        count++
    }
}

console.log(count)