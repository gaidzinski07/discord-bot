# import logging
# Logger is crucial here

from bot import DiscordBot

def main():
    try:
        client = DiscordBot()

        if client == None:
            exit(1)

        client.run()
    
    except KeyboardInterrupt:
        if not client.is_closed:
            client.close()
            
        exit(0)

if __name__ == '__main__': 
    main()
    