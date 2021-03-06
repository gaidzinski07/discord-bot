import json
from bot.bot import DiscordBot

def main():
    try:
        step = 1
        with open("config/config.json", "r") as file:
            config_dict = json.load(file)

        step = 2
        with open("config/language/{}.json".format(config_dict['language']), "r") as file:
            language_dict = json.load(file)

        step = 3
        with open("config/phrases.json", "r") as file:
            phrase_list = json.load(file)

        client = DiscordBot(config_dict, language_dict, phrase_list)
    
        client.run(client.config['token'])

    except FileNotFoundError:
        if step == 1:
            print("{}: Config file not found".format(__name__))
        
        elif step == 2:
            print("{}: Language file not found".format(__name__))
        
        elif step == 3:
            print("{}: {}".format(__name__, language_dict['phrases_not_found']))
        
        exit(1)
    
    except KeyboardInterrupt:
        if not client.is_closed:
            client.close()
            
        exit(0)

if __name__ == '__main__': 
    main()