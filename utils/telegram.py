from utils.settings import * 
import telegram 
from telegram.ext import Updater


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