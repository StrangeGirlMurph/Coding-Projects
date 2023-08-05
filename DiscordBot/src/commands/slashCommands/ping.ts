import { CommandInteraction } from "discord.js";
import { slashCommandInfo } from "../../util/slashCommands";

export default function (interaction: CommandInteraction) {
    interaction.reply('Pong!');
}

export const info: slashCommandInfo = {
    name: "ping",
    description: "Lets you play ping pong",
    type: "CHAT_INPUT",
    options: [],
};