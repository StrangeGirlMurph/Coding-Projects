import { Message } from "discord.js";

let iLove: string[] = [];

export function ily(msg: Message, args: any): void {
    msg.reply(`I love you too ${msg.author.username}! 💕👑🌺`);
    iLove.push(msg.author.username);
}

export function dylm(msg: Message, args: any): void {
    msg.reply(`I love ${iLove.join(", ")} 🦄💕🌹`);
}