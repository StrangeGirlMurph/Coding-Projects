import { Client, Message } from "discord.js";
import { textCommandHandler } from "../util/textCommands";

export default function (msg: Message) {
    if (msg.author.bot) return;

    // checks for a limiting category and only reacts to those messages in it
    if (msg.inGuild() && process.env.DISCORD_CATEGORY_ID !== undefined &&
        msg.channel.parentId === process.env.DISCORD_CATEGORY_ID) {

        const tokens = msg.content.split(" "); // i.e. ["!gif", "cat"]
        let command = tokens.shift();
        let args = tokens.join(" ");

        if (command?.charAt(0) === "!") {
            // valid text command format
            command = command.slice(1); // remove the ! ("gif")

            textCommandHandler(msg, command, args)
        }
    }
}