import asyncio
import discord

async def mother_russia(message, stripped_text, language, ffmpeg_path):
    if stripped_text is "stop" and message.guild.voice_client.is_connected():
        await message.guild.voice_client.disconnect()
    
    else:
        await message.channel.send(language['mother_russia'], file = discord.File("assets/images/motherrussia.jpg"))

        if not message.author.voice.channel is None:
            voice_client = await message.author.voice.channel.connect()
            ffmpegaudio = discord.FFmpegPCMAudio("assets/audio/motherrussia.mp3", executable = ffmpeg_path)

            voice_client.play(ffmpegaudio)