import discord
import asyncio
import random

async def say(channel, language):
    try:
        with open("config/phrases", 'r') as file:
            list = file.read().splitlines()
    
    except FileNotFoundError:
        print(language['phrases_not_found'])
        return

    random.seed()
    phrase = random.choice(list)

    await channel.send(phrase, tts = True)

async def fucking_string():
    return