import { Interaction } from "discord.js";
import { slashCommandHandler } from "../util/slashCommands";

export default function (interaction: Interaction) {
    if (!interaction.isCommand()) {
        return;
    }

    if (!interaction.inGuild()) {
        return interaction.reply({ content: `This command can only be used in a server.`, ephemeral: true });
    }

    slashCommandHandler(interaction);
}; 
