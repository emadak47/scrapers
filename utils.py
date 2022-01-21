import logging
import telegram 
import os 
from telegram.ext import Updater
from dotenv import load_dotenv
load_dotenv()


TG_GROUP = os.getenv("TG_GROUP")
TG_TOKEN = os.getenv("TG_TOKEN")
DH_USERNAME = os.getenv("DH_USERNAME")
DH_PASSWORD = os.getenv("DH_PASSWORD")


logging.basicConfig(
    filename="logger.log", 
    format='%(asctime)s %(message)s', 
    filemode='w', 
    level=logging.INFO
)


class Bot:
    def __init__(self, chat_id = TG_GROUP, token = TG_TOKEN):
        self.chat_id = chat_id
        self.bot = telegram.Bot(token)
    
    def send_message(self, msg):
        self.bot.send_message(chat_id = self.chat_id, text = msg)
    
    def get_updates(self):
        return self.bot.get_updates() 


class CommandBot():
    def __init__(self, bot_token: str = TG_TOKEN) -> None:
        self.updater = Updater(bot_token, use_context=True)
        self.dispatcher = self.updater.dispatcher