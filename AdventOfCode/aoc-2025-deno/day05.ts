const input = Deno.readTextFileSync("./day05.txt").trim().split("\n\n")
const ranges = input[0].split("\n").map(r => r.split("-").map(i => parseInt(i)))
const ids = input[1].split("\n").map(i => parseInt(i))

let count = 0

for (const id of ids) {
    for (const range of ranges) {
        if (id >= range[0] && id <= range[1]) {
            count++
            break
        }
    }
}

console.log(count)

count = 0

ranges.sort((a,b) => a[0] != b[0] ? a[0] - b[0] : a[1] - b[1])

/*
Old idea for part 2 I couldn't make work

for (let i = 0; i < ranges.length - 1; i++) {
    const a = ranges[i]
    const b = ranges[i+1]

    if (b[1] <= a[1]) ranges.splice(i+1,1)
    else if (b[0] <= a[1]) ranges[i][1] = b[0] - 1
}

for (const range of ranges) {
    count += range[1] - range[0] + 1
} 
*/

const fresh = []

for (const range of ranges) {
    const start = range[0]
    const end = range[1]

    let incorporated = false
    for (let i = 0; i < fresh.length; i++) {
        const r = fresh[i]
        const rs = r[0]
        const re = r[1]

        if (rs <= start && start <= re && end > re) {
            fresh[i][1] = end
            incorporated = true 
            break
        } else if (rs <= end && end <= re && start < rs) {
            fresh[i][0] = start
            incorporated = true
            break
        } else if (rs <= start && start <= re && rs <= start && start <= re) {
            incorporated = true
            break
        } else if (start < rs && re < end) {
            fresh[i][0] = start
            fresh[i][1] = end
            incorporated = true
            break
        }
    }

    if (!incorporated) {
        fresh.push(range)
    }
}

for (const range of fresh) {
    count += range[1] - range[0] + 1
}

console.log(count)
