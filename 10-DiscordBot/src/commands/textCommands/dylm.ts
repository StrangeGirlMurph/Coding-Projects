import { Message } from "discord.js";
import { iLove } from "./ily";

export default function (msg: Message, args: any): void {
    msg.reply(`I love ${iLove.join(", ")} 🦄💕🌹`);
}