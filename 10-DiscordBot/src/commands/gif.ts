import { Message } from "discord.js";
import fetch from "node-fetch";

export async function gif(msg: Message, args: string): Promise<void> {
    let search = "cute cat";
    if (args.length > 0) {
        search = args
    }
    let url = `https://g.tenor.com/v1/search?q=${search}&key=${process.env.TENORKEY}&limit=10`;
    let response = await fetch(url);
    let responsejson: any = await response.json();

    if (responsejson.results.length > 0) {
        const index = Math.floor(Math.random() * responsejson.results.length)
        msg.reply(`${responsejson.results[index].url}`);
    } else {
        msg.reply("I found no GIF's for that :(")
    }
}