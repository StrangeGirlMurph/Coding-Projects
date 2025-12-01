const day = (Deno.readDirSync(".").filter(v => v.name.startsWith("day") && v.name.endsWith("ts")).map(v => parseInt(v.name.slice(3,5))).toArray().sort().at(-1) || 0) + 1

new Deno.Command("xdg-open", {args: [`https://adventofcode.com/2025/day/${day}`]}).output()

const response = await fetch(`https://adventofcode.com/2025/day/${day}/input`, {
    headers: {
        Cookie: `session=${Deno.env.get("SESSION_COOKIE")}`,
    },
});

const path = "./day" + day.toString().padStart(2,"0")

if (response.body) {
    const file = await Deno.open(path + ".txt", { write: true, create: true });
    await response.body.pipeTo(file.writable);
}

Deno.writeTextFileSync(path + ".ts", 
`const input = Deno.readTextFileSync("${path}.txt")
`)