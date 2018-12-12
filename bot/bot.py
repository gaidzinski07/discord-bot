import discord
import asyncio
import json
import datetime
from . import audio
from . import image
from . import text
from . import job

class MarshallBot(discord.Client):

    def __init__(self, ffmpeg_path, language, prefix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ffmpeg_path = ffmpeg_path
        self.language = json.load(language)
        self.prefix = prefix
        self.wednesday_task = self.loop.create_task(job.wednesday(self))
        self.vac_task = self.loop.create_task(job.vac(self))

    def choose_text_channel(self, guild):
        for channel in guild.text_channels:
            if channel.name == "general":
                if channel.permissions_for(guild.me).send_messages:
                    return channel
                
                break

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                return channel

    async def on_ready(self):
        print(self.language['init'].format(self.user.name, self.user.id))

        for guild in self.guilds:
            channel = self.choose_text_channel(guild)

            await channel.send(self.language['returning'])

    async def on_guild_join(self, guild):
        channel = self.choose_text_channel(guild)

        await channel.send(self.language['entering'])

    async def on_member_join(self, member):
        channel = self.choose_text_channel(member.guild)

        await channel.send(self.language['welcome'].format(member.mention))
    
    async def on_member_remove(self, member):
        channel = self.choose_text_channel(member.guild)

        await channel.send(self.language['kick'].format(member.mention), file = discord.File("assets/images/homerun.gif"))

    async def on_member_ban(self, guild, user):
        channel = self.choose_text_channel(guild)

        await channel.send(self.language['ban'].format(user.mention), file = discord.File("assets/images/ban.gif"))

    async def on_member_unban(self, guild, user):
        channel = self.choose_text_channel(guild)

        await channel.send(self.language['unban'].format(user.mention), file = discord.File("assets/images/chim.jpg"))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("{}say".format(self.prefix)):
            await text.say(message.channel, self.language)

        elif message.content.startswith("{}crusade".format(self.prefix)):
            await image.crusade(message.channel)

        elif message.content.startswith("{}respeta".format(self.prefix)):
            await image.respeta(message)

        elif message.content.startswith("{}fuckingstring".format(self.prefix)):
            stripped_text = message.content.replace("{}fuckingstring ".format(self.prefix), "")
            await text.fucking_string(message.channel, stripped_text, self.language)

        elif message.content.startswith("{}rm".format(self.prefix)):
            stripped_text = message.content.replace("{}rm ".format(self.prefix), "")
            await text.rm(message, stripped_text, self.language)
        
        elif message.content.startswith("{}motherrussia".format(self.prefix)):
            stripped_text = message.content.replace("{}motherrussia ".format(self.prefix), "")
            await audio.mother_russia(message, stripped_text, self.language, self.ffmpeg_path)