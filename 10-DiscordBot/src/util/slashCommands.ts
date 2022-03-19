import { Client, CommandInteraction } from "discord.js";
import { commands } from "../init";
import { client } from "../main";
import { getFiles } from "./getFiles";


export interface slashCommandInfo {
    name: string, // must be lower case
    description: string,
    type: string
    options: slashCommandOption[]
}

export interface slashCommandOption {
    name: string,
    description: string // cant be empty string
    type: string,
    required: boolean
}


const toRegister: any[] = [];

export async function slashCommandLoader(client: Client) {
    const slashCommands = await getFiles("./src/commands/slashCommands/", "", "sample");

    if (slashCommands.length === 0) {
        console.log("No slash commands available")
        return
    }


    for (const file of slashCommands) {
        const cmdName = file.split('.')[0];

        console.log(`Loading command: ${cmdName}`);

        const command = await import(`../commands/slashCommands/${cmdName}`);

        commands.slashCommands[command.info.name] = command.default;
        toRegister.push(command.info);
    }

}

export async function slashCommandRegistration() {
    const guildId = process.env.DISCORD_GUILD_ID;

    if (client.application === null || guildId === undefined) return

    let registeredCommands = await client.application.commands.fetch(undefined, { guildId });


    for (const command of toRegister) {
        const cmd = registeredCommands.find(c => c.name === command.name);

        if (cmd === undefined) {
            // there is no command under the registered commands with the same name
            console.log(`Registering slash command: ${command.name}`);
            await client.application.commands.create(command, guildId); // register it
        } else {
            // there is a command with the same name

            // delete it from the list to prevent it from getting unregistered
            registeredCommands.delete(cmd.id)

            if (cmd.description !== command.description || JSON.stringify(cmd.options) !== JSON.stringify(command.options)) {
                // the command is different
                console.log(`Updating slash command: ${command.name}`);
                await client.application.commands.edit(cmd.id, command, guildId);
            }
        }
    }

    // deleting all the left over commands
    for (const regcommand of registeredCommands) {
        client.application.commands.delete(regcommand[0], guildId)
    }
}


export function slashCommandHandler(interaction: CommandInteraction) {
    const name = interaction.commandName;
    const cmd = commands.slashCommands[name];
    if (!cmd) {
        interaction.reply({ content: 'I\'m sorry an error occurred!', ephemeral: true });
        return;
    }
    cmd(interaction);
}



