import discord, asyncio, random

async def say(client, channel):
    random.seed()
    phrase = random.choice(client.phrases)

    await channel.send(phrase, tts = True)

async def fucking_string(client, channel, stripped_text):
    try:
        length = int(stripped_text)
    
    except ValueError:
        await channel.send(client.language['int_value_error'])
        return

    if length > 256:
        await channel.send(client.language['fuckingstring_length'])
        return
        
    string = ""
    acceptable_characters = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    
    random.seed()
    for _ in range(length):
        string += random.choice(acceptable_characters)

    await channel.send("{}".format(string))

async def rm(client, message, stripped_text):
    if message.channel.permissions_for(message.author).manage_messages:
        try:
            number = int(stripped_text) + 1

        except ValueError:
            await message.channel.send(client.language['int_value_error'])
            return
            
        deleted = await message.channel.purge(limit = number)

        await message.channel.send(client.language['rm_success'].format(len(deleted) - 1))
        return

    await message.channel.send(client.language['permission_error'])

async def about(channel):
    await channel.send("https://github.com/felpesm/discord-bot/blob/master/COMMANDS.md")