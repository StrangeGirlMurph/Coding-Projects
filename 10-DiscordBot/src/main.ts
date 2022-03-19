import { Client, Intents } from 'discord.js';

import "dotenv/config"; // config .env
import { setup } from './setup';

// define needed intents for the bot
const intents: number[] = [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_PRESENCES, Intents.FLAGS.GUILD_MESSAGE_REACTIONS, Intents.FLAGS.GUILD_MESSAGE_TYPING]

// initialize the client of the application
export const client = new Client({ intents: intents });

client.login(process.env.DISCORD_BOT_TOKEN); // login

setup(client);