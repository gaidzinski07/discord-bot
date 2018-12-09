from bot.bot import MarshallBot

def main():
    ffmpeg_path = "/usr/bin/ffmpeg"
    token_path = "config/token"
    prefix = ";"

    client = MarshallBot(ffmpeg_path, prefix)
    with open(token_path, 'r') as file:
        client.run(file.read())

if __name__ == '__main__':
    main()