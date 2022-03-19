import { Message } from "discord.js";

export let iLove: string[] = [];

export default function (msg: Message, args: any): void {
    msg.reply(`I love you too ${msg.author.username}! 💕👑🌺`);
    iLove.push(msg.author.username);
}

