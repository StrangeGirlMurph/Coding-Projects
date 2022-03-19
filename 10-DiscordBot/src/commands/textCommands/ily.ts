import { Message } from "discord.js";

export let iLove: string[] = [];

export default function (msg: Message, args: any): void {
    msg.reply(`I love you too ${msg.member?.displayName}! 💕👑🌺`);
    if (msg.member !== null) {
        iLove.push(msg.member.displayName);
    }
}

