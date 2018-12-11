from bot.bot import MarshallBot

def main():
    ffmpeg_path = "/usr/bin/ffmpeg"
    token_path = "config/token"
    language = "en_us"
    prefix = ";"

    try:
        with open("config/language/{}.json".format(language), 'r') as file:
            client = MarshallBot(ffmpeg_path, file, prefix)
        
    except FileNotFoundError:
        print("{}: Language file not found".format(__name__))
        exit(1)

    try:
        with open(token_path, 'r') as file:
            client.run(file.read())
    
    except FileNotFoundError:
        print("{}: {}".format(__name__, client.language['token_not_found']))
        exit(1)

if __name__ == '__main__':
    main()