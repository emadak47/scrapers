from utils.settings import *
from utils.twitter import TweetListener, create_api

class Twitter: 
    def __init__(self) -> None:
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG) 
        self.api = create_api()
        self.me = self.api.me()
        

    def initiate_listener(self, keywords: list = ["crypto", "nft"]) -> None: 
        tweets_listener = TweetListener(self.api)
        stream = tweepy.Stream(self.api.auth, tweets_listener)
        stream.filter(track=keywords, languages=["en"])