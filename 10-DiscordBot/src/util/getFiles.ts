import fs from "fs"

// returnes an array of all the files at the path with the specified ending without the ones that start with ignore
export function getFiles(path: string, ending: string = "", ignore: string = "") {
    return fs.readdirSync(path).filter(f => f.endsWith(ending) && !f.startsWith(ignore))
}