from bot import MarshallBot

ffmpeg_path = "/usr/bin/ffmpeg"
token_path = "token"

client = MarshallBot(ffmpeg_path)
file = open(token_path, "r")

client.run(file.read())