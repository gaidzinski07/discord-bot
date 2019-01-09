import discord
import asyncio
import random

async def say(marshall, channel):
    random.seed()
    phrase = random.choice(marshall.phrases)

    await channel.send(phrase, tts = True)

async def fucking_string(marshall, channel, stripped_text):
    try:
        length = int(stripped_text)
    
    except ValueError:
        await channel.send(marshall.language['int_value_error'])
        return

    if length > 256:
        await channel.send(marshall.language['fuckingstring_length'])
        return
        
    string = ""
    acceptable_characters = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    
    random.seed()
    for _ in range(length):
        string += random.choice(acceptable_characters)

    await channel.send("{}".format(string))

async def rm(marshall, message, stripped_text):
    if message.channel.permissions_for(message.author).manage_messages:
        try:
            number = int(stripped_text) + 1

        except ValueError:
            await message.channel.send(marshall.language['int_value_error'])
            return
            
        deleted = await message.channel.purge(limit = number)

        await message.channel.send(marshall.language['rm_success'].format(len(deleted) - 1))
        return

    await message.channel.send(marshall.language['permission_error'])