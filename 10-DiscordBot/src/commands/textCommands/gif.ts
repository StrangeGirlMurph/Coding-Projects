import { Message } from "discord.js";
import { search } from "../functionality/tenorSearch";

export default async function (msg: Message, args: string) {
    msg.reply(await search(args))
}