import discord
import asyncio
import datetime
import praw
from . import audio
from . import image
from . import text
from . import job

class MarshallBot(discord.Client):
    def __init__(self, config_dict, language_dict, phrase_list, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = config_dict
        self.language = language_dict
        self.phrases = phrase_list['phrases']
        self.reddit = None

        if self.config['reddit']['client_secret'] != "":
            self.reddit = praw.Reddit(client_id = self.config['reddit']['client_token'],
                                    client_secret = self.config['reddit']['client_secret'],
                                    password = self.config['reddit']['password'],
                                    user_agent = 'marshallbot',
                                    username = self.config['reddit']['user'])

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

        elif message.content.startswith("{}say".format(self.config['command_prefix'])):
            await text.say(self, message.channel)

        elif message.content.startswith("{}crusade".format(self.config['command_prefix'])):
            await image.crusade(message.channel)

        elif message.content.startswith("{}respeta".format(self.config['command_prefix'])):
            await image.respeta(message)

        elif message.content.startswith("{}fuckingstring".format(self.config['command_prefix'])):
            stripped_text = message.content.replace("{}fuckingstring ".format(self.config['command_prefix']), "")
            await text.fucking_string(self, message.channel, stripped_text)

        elif message.content.startswith("{}rm".format(self.config['command_prefix'])):
            stripped_text = message.content.replace("{}rm ".format(self.config['command_prefix']), "")
            await text.rm(self, message, stripped_text)
        
        elif message.content.startswith("{}motherrussia".format(self.config['command_prefix'])):
            stripped_text = message.content.replace("{}motherrussia ".format(self.config['command_prefix']), "")
            await audio.mother_russia(self, message, stripped_text)