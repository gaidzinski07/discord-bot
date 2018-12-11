import discord
import asyncio
import random

async def say(channel, language):
    try:
        with open("config/phrases", 'r') as file:
            list = file.read().splitlines()
    
    except FileNotFoundError:
        print("{}: {}".format(__name__, language['phrases_not_found']))
        return

    random.seed()
    phrase = random.choice(list)

    await channel.send(phrase, tts = True)

async def fucking_string(channel, stripped_text, language):
    try:
        length = int(stripped_text)

        if length > 256:
            await channel.send(language['fuckingstring_length'])
        
        else:
            string = ""
            acceptable_characters = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            
            random.seed()
            for _ in range(length):
                string += random.choice(acceptable_characters)

            await channel.send("{}".format(string))
        
    except ValueError:
        await channel.send(language['int_value_error'])

async def rm(message, stripped_text, language):
    if message.channel.permissions_for(message.author).manage_messages:
        try:
            number = int(stripped_text) + 1
            deleted = await message.channel.purge(limit = number)

            await message.channel.send(language['rm_success'].format(len(deleted) - 1))

        except ValueError:
            await message.channel.send(language['int_value_error'])
    
    else:
        await message.channel.send(language['permission_error'])