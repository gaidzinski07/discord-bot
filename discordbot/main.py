import logging

from bot import DiscordBot

# Logger is crucial here

def main():
    try:
        client = DiscordBot()
    
        client.run(client.config.settings['token'])
    
    except KeyboardInterrupt:
        if not client.is_closed:
            client.close()
            
        exit(0)

if __name__ == '__main__': 
    main()