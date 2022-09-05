from __future__ import annotations
from utils.settings import * 
import tweepy 


def create_api(rate_limit: bool = True, rate_limit_notify: bool = True):
    consumer_key: str = TW_CONSUMER_KEY
    consumer_secret: str = TW_CONSUMER_SECRET
    access_token: str = TW_ACCESS_TOKEN
    access_token_secret: str = TW_ACCESS_TOKEN_SECRET

    auth = tweepy.OAUthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(
        auth, 
        wait_on_rate_limit = rate_limit,
        wait_on_rate_limit_notify = rate_limit_notify
    )

    try: 
        api.verify_credentials()
    except Exception as e: 
        print("****** Error initiating twitter API")
        raise e 
    
    # print ("====== Twitter API created")
    return api 



class TweetListener(tweepy.StreamListener): 
    def __init__(self, api) -> None:
        self.api = api
        self.me = self.api.me()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG) 
    
    # logic
    def on_status(self, tweet):
        self.logger.info(tweet)

    # handle error
    def on_error(self, status): 
        self.logger.error(status)