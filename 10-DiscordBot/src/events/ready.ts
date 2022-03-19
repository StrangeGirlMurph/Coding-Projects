import { Client } from "discord.js";

export default function () {
    console.log('Beep Boop 🤖 \nI am ready 🐇');

    // send wakeup message to status channel
    /* if (typeof process.env.DISCORD_STATUS_CHANNEL_ID === "string") {
        client.channels.fetch(process.env.DISCORD_STATUS_CHANNEL_ID).then((channel: any) => {
            channel.send("I am awake :) Hey everyone I love you")
        }).catch(console.error);
    } */
};
