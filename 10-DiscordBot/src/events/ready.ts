import { Client } from "discord.js";
import { slashCommandRegistration } from "../util/slashCommands";

export default function () {
    console.log('Beep Boop 🤖 \nI am ready 🐇');

    slashCommandRegistration()
    // send wakeup message to status channel
    /* if (typeof process.env.DISCORD_STATUS_CHANNEL_ID === "string") {
        client.channels.fetch(process.env.DISCORD_STATUS_CHANNEL_ID).then((channel: any) => {
            channel.send("I am awake :) Hey everyone I love you")
        }).catch(console.error);
    } */
};
