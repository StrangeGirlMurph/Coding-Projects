import { CommandInteraction } from "discord.js";
import { slashCommandInfo } from "../../util/slashCommands";
import { search } from "../functionality/tenorSearch";

export default async function (interaction: CommandInteraction) {
    const args = interaction.options.getString("search");

    interaction.reply(await search(args));
}

export const info: slashCommandInfo = {
    name: "gif",
    description: "Getting a tenor GIF",
    type: "CHAT_INPUT",
    options: [
        {
            type: "STRING",
            name: "search",
            description: "input for search",
            required: false
        }],
};