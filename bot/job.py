import datetime
import discord
import asyncio

async def wednesday(client):
    await client.wait_until_ready()

    while not client.is_closed():
        now = datetime.datetime.now()

        if now.weekday() is 2 and now.hour is 0:
            for guild in client.guilds:
                channel = client.choose_text_channel(guild)

                await channel.send("", file = discord.File("assets/images/wednesday.jpg"))
            
            await asyncio.sleep(86400)
        
        else:
            await asyncio.sleep(10)