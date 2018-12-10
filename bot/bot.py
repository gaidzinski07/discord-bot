import discord
import asyncio
import json
from . import image
from . import text
from . import job

class MarshallBot(discord.Client):

    def __init__(self, ffmpeg_path, language, prefix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ffmpeg_path = ffmpeg_path
        self.language = json.load(language)
        self.prefix = prefix
        self.bg_task = self.loop.create_task(job.wednesday(self))

    async def on_ready(self):
        print(self.language['init'].format(self.user.name, self.user.id))

    def choose_text_channel(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                return channel

    async def on_message(self, message):
        if message.author is self.user:
            return

        if message.content.startswith("{}say".format(self.prefix)):
            await text.say(message.channel, self.language)

        elif message.content.startswith("{}crusade".format(self.prefix)):
            await image.crusade(message.channel)

        elif message.content.startswith("{}respeta".format(self.prefix)):
            await image.respeta(message)