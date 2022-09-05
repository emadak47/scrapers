import logging
import os 
from dotenv import load_dotenv
load_dotenv()


TG_GROUP = os.getenv("TG_GROUP")
TG_TOKEN = os.getenv("TG_TOKEN")

DH_USERNAME = os.getenv("DH_USERNAME")
DH_PASSWORD = os.getenv("DH_PASSWORD")

TW_CONSUMER_KEY = os.getenv("TW_CONSUMER_KEY")
TW_CONSUMER_SECRET = os.getenv("TW_CONSUMER_SECRET")
TW_ACCESS_TOKEN = os.getenv("TW_ACCESS_TOKEN")
TW_ACCESS_TOKEN_SECRET = os.getenv("TW_ACCESS_TOKEN_SECRET")


logging.basicConfig(
    filename="logger.log", 
    format='%(asctime)s %(message)s', 
    filemode='w', 
    level=logging.INFO
)