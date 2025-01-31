# Memes Bot

This is a simple bot that sends memes to a Telegram group in random intervals.

## Installation

1. Clone the repository
2. Install the requirements (tested with Python 3.12)
3. Create a `.env` file with the following content:
```
TELEGRAM_BOT_TOKEN=your_api_id
TELEGRAM_CHAT_ID=your_chat_id
MODE=DEVELOPMENT
```
4. Populate the memes folder with images
5. Run the bot with `python3 main.py`

## Usage

The bot will send a meme and wait a random interval before sending another one. By default, it sends a message indicating when the next meme will be sent.