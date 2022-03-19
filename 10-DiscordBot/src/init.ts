import { Client } from "discord.js"

import events from "./util/events";
import { slashCommandLoader } from "./util/slashCommands";
import { textCommandLoader } from "./util/textCommands"


export const commands: {
    textCommands: { [name: string]: Function },
    slashCommands: { [name: string]: Function }
} = {
    textCommands: {},
    slashCommands: {}
}

export function init(client: Client) {
    textCommandLoader(client);
    slashCommandLoader(client);
    events(client);
}

