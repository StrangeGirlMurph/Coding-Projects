import { Client, Interaction } from "discord.js";

export default function (interaction: Interaction) {
    console.log("Interaction created")
    /* if (!interaction.isCommand()) return
    if (!interaction.inGuild()) return interaction.reply("This command can only be used in a server")

    const slashcmd = client.slashcommands.get(interaction.commandName)

    if (!slashcmd) return interaction.reply("Invalid slash command")

    if (slashcmd.perm && !interaction.member.permissions.has(slashcmd.perm))
        return interaction.reply("You do not have permission for this command")

    slashcmd.run(client, interaction)


    // if (interaction.isCommand()) {
    //     const cmd = commands.get(interaction.commandName);
    //     if (!cmd) {
    //         interaction.reply({ content: 'I\'m sorry an error occurred!', ephemeral: true });
    //         return;
    //     }
    //     cmd.execute(client, interaction);
    // } else {
    //     interaction.reply({ content: `I'm sorry, an error occurred.`, ephemeral: true });
    // } */
}; 
