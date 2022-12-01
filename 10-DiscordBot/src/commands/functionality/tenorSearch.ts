import fetch from "node-fetch";

export async function search(query: string | null): Promise<string> {
    let defaultSearch = "cute cat";
    if (query === null) {
        query = defaultSearch;
    }

    let url = `https://g.tenor.com/v1/search?q=${query}&key=${process.env.TENOR_API_KEY}&limit=10`;
    let response = await fetch(url);
    let responsejson: any = await response.json();

    if (responsejson.results.length > 0) {
        const index = Math.floor(Math.random() * responsejson.results.length)
        return `${responsejson.results[index].url}`;
    } else {
        return "I found no GIF's for that :(";
    }
}