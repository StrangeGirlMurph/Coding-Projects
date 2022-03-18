
import { Message } from "discord.js";
import { gif } from "./commands/gif";
import { ily, dylm } from "./commands/love";

const commands: any = {
    gif, ily, dylm
}

export function commandHandler(msg: Message) {
    const tokens = msg.content.split(" ");
    let command = tokens.shift();
    let args = tokens.join(" ");

    if (command?.charAt(0) === "!") {
        command = command.slice(1);
        if (command in commands) {
            commands[command](msg, args)
        }
    }

}