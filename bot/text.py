import discord
import asyncio
import random

async def say(channel):
    with open("config/phrases", 'r') as file:
        list = file.read().splitlines()
    
    random.seed()
    phrase = random.choice(list)

    await channel.send(phrase, tts = True)