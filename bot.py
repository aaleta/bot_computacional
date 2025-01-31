import os
import time
import random
import requests
from dotenv import dotenv_values

MEME_FOLDER = 'memes'

class MemeBot:
    """ A simple class to send messages and photos to a Telegram chat """
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, message):
        try:
            response = requests.post(
                url=f'https://api.telegram.org/bot{self.token}/sendMessage',
                data={'chat_id': self.chat_id, 'text': message, 'parse_mode': 'HTML'},
                timeout=100
            ).json()
            return response
        except Exception as e:
            return str(e)

    def send_photo(self, photo):
        try:
            response = requests.post(
                url=f'https://api.telegram.org/bot{self.token}/sendPhoto',
                data={'chat_id': self.chat_id},
                files={'photo': photo},
                timeout=100
            ).json()
            return response
        except Exception as e:
            return str(e)

def get_random_meme():
    """ Get a random meme from the memes folder """
    memes = os.listdir(MEME_FOLDER)
    return os.path.join(MEME_FOLDER, random.choice(memes))

def random_sleep_time(min_time=1, max_time=20):
    """ Return a random sleep time between 1 and 4 days in seconds """
    return random.randint(min_time, max_time)

if __name__ == '__main__':
    config = dotenv_values(".env")

    BOT_TOKEN = config["TELEGRAM_BOT_TOKEN"]
    CHAT_ID = config["TELEGRAM_CHAT_ID"]
    PRODUCTION = config["MODE"] == 'PRODUCTION'

    bot = MemeBot(BOT_TOKEN, CHAT_ID)

    if not PRODUCTION:
        bot.send_message('Bot started in testing mode')
        min_sleep, max_sleep = 1, 60
    else:
        min_sleep, max_sleep = 1 * 24 * 3600, 4 * 24 * 3600

    while True:
        sleep_time = random_sleep_time(min_sleep, max_sleep)
        bot.send_message(f'The next meme will appear in {sleep_time} seconds')

        time.sleep(sleep_time)

        bot.send_photo(open(get_random_meme(), 'rb'))