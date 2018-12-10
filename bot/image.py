import asyncio
import discord

async def respeta(message):
    string = ""

    for i in message.mentions:
        string += "{} ".format(i.mention)

    await message.channel.send(string, file = discord.File("assets/images/respeta.jpg"))

async def crusade(channel):
    await channel.send("@everyone\nGET OVER HERE", file = discord.File("assets/images/crusade.jpg"))