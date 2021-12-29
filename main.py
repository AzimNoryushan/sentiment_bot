from discord import channel
import discord
from discord.ext import commands
from dotenv import load_dotenv
from topic_sentiment import Topic_sentiment
import os
import traceback

from datetime import date
import time
import malaya
import tweepy
import random
import matplotlib.pyplot as plt

load_dotenv()

#ApaKataTwitter
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True
stamp = ""

bot = commands.Bot(command_prefix='#', description='Apakatatwitter', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command(name='topic')
async def tweet_topic(ctx, *, topic):
    stamp = random.randint(1000000000,9999999999)
    result = analyze_tweet(stamp,topic)

    await ctx.send(result)
    #await ctx.send(file=discord.File('img/{stamp}.png'.format(stamp=stamp)))

def analyze_tweet(stamp, topic):
    positive_results = 0
    negative_results = 0
    undetected_results = 0
    
    tweets = getTweets(topic)

    if tweets == None: return "Tweets empty"

    for tweet in tweets:
        try:
            sentiment = listToString(getSentiment([tweet]))
            if(sentiment=='positive'):
                positive_results = positive_results + 1
            elif(sentiment=='negative'):
                negative_results = negative_results + 1
            else:
                undetected_results = undetected_results+1
        except Exception as e:
            traceback.print_exc

    generate_chart(positive_results, negative_results, stamp, topic)

    return { "positive": positive_results, "negative": negative_results }

def getSentiment(message):
    try:
        model = malaya.sentiment.multinomial()
        sentiment = model.predict(message, add_neutral = False)
        message = ' '.join(message)

        return sentiment
    except:
        traceback.print_exc

def generate_chart(positive_results, negative_results, stamp, topic):
    try:
        # result[0] -> positive
        # result[1] -> negative
        today = date.today()
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        sentiment_list = ['positive', 'negative']
        data_count = [positive_results, negative_results]
        colors = ['green', "red"]
        ax.pie(data_count, labels = sentiment_list,autopct='%1.2f%%',colors=colors)
        plt.title("Sentiment of " + topic + " on Twitter on " +  today.strftime("%d/%m/%Y"))
        
        IMAGE_FOLDER = os.path.isdir("img")
        if not IMAGE_FOLDER:
            os.makedirs("img")  
        else:
            pass

        plt.savefig('img/{stamp}.png'.format(stamp=stamp), dpi=300, bbox_inches='tight')
    except Exception as e:
        traceback.print_exc
        print(e)

def getTweets(topic):
    try:
        consumer_key = os.getenv('consumer_key')
        consumer_secret = os.getenv('consumer_secret')

        access_token = os.getenv('access_token')
        access_token_secret = os.getenv('access_token_secret')

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True)

        count = 0
        max_count = 1000
        topic = topic
        geocode = '3.10559,101.6427,300km'
        tweets = []

        for tweet in tweepy.Cursor(api.search_tweets, q=topic, geocode=geocode, count=100).items():
            tweets.append(tweet.text)
            count += 1

            if count >= max_count:
                break

        return tweets

    except Exception as e:
        print(e)
        traceback.print_exc

def listToString(list):
    try:
        string = str(list).replace(' ', '')
        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.replace('\'', '')

        return string
    except:
        traceback.print_exc

bot.run(TOKEN)

