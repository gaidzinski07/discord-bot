import discord
import asyncio
import commands

class MarshallBot(discord.Client):
    
    def __init__(self, ffmpeg_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ffmpeg_path = ffmpeg_path

    def choose_text_channel(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                return channel

    async def on_message(self, message):
        if message.author == self.user:
            return