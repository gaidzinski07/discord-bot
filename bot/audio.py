import asyncio, discord

async def mother_russia(client, message, stripped_text):
    if stripped_text == "stop" and message.guild.voice_client.is_connected():
        await message.guild.voice_client.disconnect()
        return
    
    await message.channel.send(client.language['mother_russia'], file = discord.File("assets/images/motherrussia.jpg"))

    if not message.author.voice.channel == None:
        voice_client = await message.author.voice.channel.connect()
        ffmpegaudio = discord.FFmpegPCMAudio("assets/audio/motherrussia.mp3", executable = client.config['ffmpeg_path'])

        voice_client.play(ffmpegaudio)
    
# Future function to play audio from a websource (Youtube and mp3?)
async def play(client, message, url):
    return

async def stop(client, message):
    return

async def playlist(client, message):
    return

async def rm_audio(client, message, stripped_text):
    return