import { Client } from "discord.js";
import { getFiles } from "./getFiles";

export default async (client: Client) => {
    const events = getFiles("./src/events/", "", "sample");

    for (const file of events) {
        const eventName = file.split('.')[0];

        console.log(`Registering event: ${eventName}`);

        const event = await import(`../events/${eventName}`);
        client.on(eventName, event.default);
    };
};