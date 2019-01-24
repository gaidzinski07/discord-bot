import discord
import asyncio
import praw
import json
import random
import datetime
import re

import exception

class Config():
    def __init__(self):
        try:
            step = 1
            with open("config/config.json", "r") as file:
                self.settings = json.load(file)

            step = 2
            with open("config/language/{}.json".format(self.settings['language']), "r") as file:
                self.language = json.load(file)

            step = 3
            with open("config/phrases.json", "r") as file:
                self.phrases = json.load(file)
            
            self.reddit = None

            if not self.settings['reddit']['client_secret'] == "":
                self.reddit = praw.Reddit(client_id = self.settings['reddit']['client_token'],
                                            client_secret = self.settings['reddit']['client_secret'],
                                            password = self.settings['reddit']['password'],
                                            user_agent = 'discordbot',
                                            username = self.settings['reddit']['user'])
        
        except FileNotFoundError:
            if step == 1:
                print("{}: Config file not found".format(__name__))
        
            elif step == 2:
                print("{}: Language file not found".format(__name__))
            
            elif step == 3:
                print("{}: {}".format(__name__, self.language['phrases_not_found']))

            # ConfigException with message here

class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # __init__ needs to catch ConfigException

        self.config = Config()
        self.wednesday_task = self.loop.create_task(self.wednesday())
        self.vac_task = self.loop.create_task(self.vac())

    def choose_text_channel(self, guild):
        for channel in guild.text_channels:
            if channel.name in ("general", "text"):
                if channel.permissions_for(guild.me).send_messages:
                    return channel
                
                break

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                return channel

        return None

    def command(self, name):
        string = "{}{}".format(self.config.settings['command_prefix'], name)

        return string

    async def wednesday(self):
        await self.wait_until_ready()

        while not self.is_closed():
            now = datetime.datetime.now()

            if now.weekday() == 2 and now.hour == 0:
                for guild in self.guilds:
                    channel = self.choose_text_channel(guild)

                    await channel.send("", file = discord.File("assets/images/wednesday.jpg"))
                
                await asyncio.sleep(86400)
                continue
            
            await asyncio.sleep(10)

    async def vac(self):
        await self.wait_until_ready()

        await asyncio.sleep(86400)

        vac_day = datetime.datetime(2014, 11, 24)
        while not self.is_closed():
            now = datetime.datetime.now()
            diff = now - vac_day
            string = self.config.language['vac_count'].format(diff.days)

            if now.day == 24 and now.month == 11:
                string += self.config.language['vac_anniversary']

            else:
                next_anniversary = vac_day.replace(now.year)
                if now > next_anniversary:
                    next_anniversary = vac_day.replace(now.year + 1)
                
                diff_next_anniversary = next_anniversary - now
                string += self.config.language['vac_count_next'].format(diff_next_anniversary.days)
            
            for guild in self.guilds:
                channel = self.choose_text_channel(guild)

                await channel.send(string)
            
            await asyncio.sleep(86400)

    async def on_ready(self):
        print(self.config.language['init'].format(self.user.name, self.user.id))

        for guild in self.guilds:
            channel = self.choose_text_channel(guild)

            await channel.send(self.config.language['returning'])

    async def on_guild_join(self, guild):
        channel = self.choose_text_channel(guild)

        await channel.send(self.config.language['entering'])

    async def on_member_join(self, member):
        channel = self.choose_text_channel(member.guild)

        await channel.send(self.config.language['welcome'].format(member.mention))
    
    async def on_member_remove(self, member):
        channel = self.choose_text_channel(member.guild)

        await channel.send(self.config.language['kick'].format(member.mention), file = discord.File("assets/images/homerun.gif"))

    async def on_member_ban(self, guild, user):
        channel = self.choose_text_channel(guild)

        await channel.send(self.config.language['ban'].format(user.mention), file = discord.File("assets/images/ban.gif"))

    async def on_member_unban(self, guild, user):
        channel = self.choose_text_channel(guild)

        await channel.send(self.config.language['unban'].format(user.mention), file = discord.File("assets/images/chim.jpg"))

    async def on_message(self, message):
        if message.author == self.user:
            return

        elif message.content.startswith(self.command("say")):
            await self.say(message.channel)

        elif message.content.startswith(self.command("rm")):
            stripped_text = message.content.replace("{} ".format(self.command("rm")), "")

            await self.rm(message, stripped_text)

        elif message.content.startswith(self.command("fuckingstring")):
            stripped_text = message.content.replace("{} ".format(self.command("fuckingstring")), "")

            await self.fucking_string(message.channel, stripped_text)

        elif message.content.startswith(self.command("commands")):
            await self.commands(message.channel)

        elif message.content.startswith(self.command("crusade")):
            await self.crusade(message.channel)

        elif message.content.startswith(self.command("respeta")):
            await self.respeta(message)

        elif message.content.startswith(self.command("animemes")):
            await self.animemes(message)

        elif message.content.startswith(self.command("motherrussia")):
            stripped_text = message.content.replace("{} ".format(self.command("motherrussia")), "")

            await self.mother_russia(message, stripped_text)

    async def say(self, channel):
        random.seed()
        phrase = random.choice(self.config.phrases)

        await channel.send(phrase, tts = True)

    async def rm(self, message, stripped_text):
        if message.channel.permissions_for(message.author).manage_messages:
            try:
                number = int(stripped_text) + 1

            except ValueError:
                await message.channel.send(self.config.language['int_value_error'])
                return
                
            deleted = await message.channel.purge(limit = number)

            await message.channel.send(self.config.language['rm_success'].format(len(deleted) - 1))
            return

        await message.channel.send(self.config.language['permission_error'])
    
    async def fucking_string(self, channel, stripped_text):
        try:
            length = int(stripped_text)
        
        except ValueError:
            await channel.send(self.config.language['int_value_error'])
            return

        if length > 256:
            await channel.send(self.config.language['fuckingstring_length'])
            return
            
        string = ""
        acceptable_characters = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        
        for _ in range(length):
            # ?
            random.seed()
            string += random.choice(acceptable_characters)

        await channel.send("{}".format(string))

    async def commands(self, channel):
        await channel.send("https://github.com/felpesm/discord-bot/blob/master/COMMANDS.md")

    async def crusade(self, channel):
        await channel.send("@everyone\nGET OVER HERE", file = discord.File("assets/images/crusade.jpg"))

    async def respeta(self, message):
        string = ""

        for i in message.mentions:
            string += "{} ".format(i.mention)
        
        await message.channel.send(string, file = discord.File("assets/images/respeta.jpg"))

    async def animemes(self, message):
        if self.config.reddit is None:
            await message.channel.send(self.config.language['reddit_not_logged_send'])
            print(self.config.language['reddit_not_logged'].format("animemes"))
            return
        
        subreddit = self.config.reddit.subreddit("Animemes")
        hot_submissions = list(subreddit.hot(limit = 50))
        
        while True:
            random.seed()
            submission = random.choice(hot_submissions)

            if re.match(r".*\.(jpg|png)", submission.url):
                break

        embed = discord.Embed(title="Animemes", description=submission.title, color=discord.Colour.dark_red())
        embed.set_footer(text="Created by {}".format(submission.author.name), icon_url=submission.author.icon_img)
        embed.set_image(url=submission.url)

        await message.channel.send(submission.permalink, embed=embed)

    async def mother_russia(self, message, stripped_text):
        if message.guild.voice_client.is_connected():
            if stripped_text == "stop":
                await message.guild.voice_client.disconnect()
                
            return
        
        if not message.author.voice.channel == None:
            voice_client = await message.author.voice.channel.connect()
            ffmpeg_audio = discord.FFmpegPCMAudio("assets/audio/motherrussia.mp3", executable = self.config.settings['ffmpeg_path'])
            
            await message.channel.send(self.config.language['mother_russia'], file = discord.File("assets/images/motherrussia.jpg"))
            voice_client.play(ffmpeg_audio)