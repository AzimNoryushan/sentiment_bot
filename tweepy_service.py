import tweepy
from dotenv import load_dotenv
import os
import traceback

class Tweepy_service:

    def __init__(self):
        self.topic = ""

    async def getTweets(self, topic):
        try:
            load_dotenv()

            consumer_key = os.getenv('consumer_key')
            consumer_secret = os.getenv('consumer_secret')

            access_token = os.getenv('access_token')
            access_token_secret = os.getenv('access_token_secret')

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            api = await tweepy.API(auth, wait_on_rate_limit=True)

            count = 0
            max_count = 1000
            topic = topic
            geocode = '3.10559,101.6427,100km'
            tweets = []

            for tweet in await tweepy.Cursor(api.search_tweets, q=topic, geocode=geocode, count=100).items():
                tweets.append(tweet.text)
                count += 1

                if count >= max_count:
                    break

            return tweets

        except:
            traceback.print_exc

#print(api.verify_credentials().screen_name)