import datetime
import discord
import asyncio

async def wednesday(client):
    await client.wait_until_ready()

    while not client.is_closed():
        now = datetime.datetime.now()

        if now.weekday() == 2 and now.hour == 0:
            for guild in client.guilds:
                channel = client.choose_text_channel(guild)

                await channel.send("", file = discord.File("assets/images/wednesday.jpg"))
            
            await asyncio.sleep(86400)
        
        else:
            await asyncio.sleep(10)

async def vac(client):
    await client.wait_until_ready()

    vac_day = datetime.datetime(2014, 11, 24)
    while not client.is_closed():
        now = datetime.datetime.now()
        diff = now - vac_day
        string = client.language['vac_count'].format(diff.days)

        if now.day == 24 and now.month == 11:
            string += client.language['vac_anniversary']

        else:
            next_anniversary = vac_day.replace(now.year)
            if now > next_anniversary:
                next_anniversary = vac_day.replace(now.year + 1)
            
            diff_next_anniversary = next_anniversary - now
            string += client.language['vac_count_next'].format(diff_next_anniversary.days)
        
        for guild in client.guilds:
            channel = client.choose_text_channel(guild)

            await channel.send(string)
        
        await asyncio.sleep(86400)