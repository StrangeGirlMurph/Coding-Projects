import { Client } from 'discord.js';

import "dotenv/config";
import { commandHandler } from "./commandHandler";

const client = new Client({ intents: ["GUILDS", "GUILD_MESSAGES", "DIRECT_MESSAGES"] });

client.login(process.env.TOKEN);

const statusChannelId = "954392404813832203"

client.once('ready', () => {
    console.log('Beep Boop 🤖 \nI am ready 🐇');

    // client.channels.fetch("954392404813832203").then((channel: any) => {
    //     channel.send("I am awake :) Hey everyone I love you")
    // }).catch(console.error);
});

client.on("messageCreate", (msg) => {
    if (msg.author.bot) return;
    if (msg.inGuild()) {
        if (msg.channel.parentId === "953313361918042132") {
            commandHandler(msg)
        }
    }
})
