import { Client, Message } from "discord.js";
import { commands } from "../init";
import { getFiles } from "./getFiles";

export async function textCommandLoader(client: Client) {
    const textCommands = await getFiles("./src/commands/textCommands/", "", "sample");

    for (const file of textCommands) {
        const cmdName = file.split('.')[0];

        console.log(`Registering text command: ${cmdName}`);

        const command = await import(`../commands/textCommands/${cmdName}`);
        commands.textCommands[cmdName] = command.default;
    };
}

export function textCommandHandler(msg: Message, cmdName: string, args: string) {
    const execute = commands.textCommands[cmdName];

    if (execute === undefined) {
        //msg.reply("I don't know that command :(")
        return
    }

    execute(msg, args);
}