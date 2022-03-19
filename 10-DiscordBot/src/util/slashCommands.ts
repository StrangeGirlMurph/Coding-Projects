import { Client } from "discord.js";

export function slashCommandLoader(client: Client) {



}

export function slashCommandHandler() {

}



/* import { Client, Collection, CommandInteraction } from "discord.js";
import { SlashCommandBuilder } from "@discordjs/builders";
import { client } from "../main";


module.exports = (bot, reload) => {
    const { client } = bot

    let slashcommands = getFiles("./slashcommands/", ".js")

    if (slashcommands.length === 0)
        console.log("No slash commands loaded")

    slashcommands.forEach(f => {
        if (reload) delete require.cache[require.resolve(`../slashcommands/${f}`)]
        const slashcmd = require(`../slashcommands/${f}`)
        client.slashcommands.set(slashcmd.name, slashcmd)
    })
} */