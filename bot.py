import os
import sys
import time
import json
import random
import requests
from dotenv import dotenv_values

MEME_FOLDER = 'memes'
USED_MEMES_FILE = 'used_memes.json'

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

def load_used_memes():
    if not os.path.exists(USED_MEMES_FILE):
        return set()
    with open(USED_MEMES_FILE, 'r') as f:
        return set(json.load(f))

def save_used_memes(used_memes):
    with open(USED_MEMES_FILE, 'w') as f:
        json.dump(sorted(used_memes), f)

def get_random_meme():
    """ Return a random meme that hasn't been used yet """
    all_memes = {
        os.path.join(MEME_FOLDER, f)
        for f in os.listdir(MEME_FOLDER)
        if os.path.isfile(os.path.join(MEME_FOLDER, f))
    }

    used_memes = load_used_memes()

    available_memes = list(all_memes - used_memes)

    if not available_memes:
        bot.send_message("All memes have been used. Meme bot signing off 🫡")
        sys.exit(0)

    chosen = random.choice(available_memes)
    used_memes.add(chosen)
    save_used_memes(used_memes)

    return chosen


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
        bot.send_message('Meme bot started in testing mode')
        min_sleep, max_sleep = 1, 60
    else:
        bot.send_message('Meme bot started')
        min_sleep, max_sleep = 1 * 24 * 3600, 3 * 24 * 3600

    while True:
        sleep_time = random_sleep_time(min_sleep, max_sleep)
        bot.send_message(f'The next meme will appear in {sleep_time} seconds')

        time.sleep(sleep_time)

        bot.send_message('Meme incoming...')
        for _ in reversed(range(3)):
            bot.send_message(f'{_+1}!')
            time.sleep(1)

        with open(get_random_meme(), 'rb') as photo:
            bot.send_photo(photo)