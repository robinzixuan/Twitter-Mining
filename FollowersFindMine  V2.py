# Gather the recent 50 tweets from all 32,525 followers of @MIGOP on twitter
# Retrieve the followers first, then worry about the tweets
# Add a main function to this later
import tweepy
import csv
import time
from multiprocessing.pool import ThreadPool
from textblob import TextBlob
import nltk.corpus
import re

def create_api( consumer_key,consumer_secret,access_token,access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

def get_followers(api, user_account):
    followers = []
    if(api.verify_credentials):
        print("We successfully logged in.")
        try:
            for page in tweepy.Cursor(api.followers, screen_name=user_account, count=200).pages():
                followers.extend(page)
        except:
            time.sleep(15*60)
            for page in tweepy.Cursor(api.followers, screen_name=user_account, count=200).pages():
                followers.extend(page)
    return followers

emoji_pattern = re.compile(
   u"(\ud83d[\ude00-\ude4f])|"  # emoticons
   u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
   u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
   u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
   u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
   "+", flags=re.UNICODE)

def remove_emoji(text):
   return emoji_pattern.sub(r'', text)



def clean_tweet(tweet):
    tweet=remove_emoji(tweet)
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_emotion(tweet):
    analyze=TextBlob(clean_tweet(tweet))
    if analyze.sentiment.polarity>0:
        return 'positive'
    elif analyze.sentiment.polarity == 0:
           return 'neutral'
    else:
           return 'negative'


def get_tweets(api, user_account):
    user_tweets = api.user_timeline(id=user_account, count=10)
    tweets = []
    for status in user_tweets:
        tweets.append(status.text)
        tweets.append(get_emotion(status.text))
    return tweets


def write_csv(api,followers_list):
    with open("TrumpFollowersData.csv", "w", encoding='utf-8-sig', newline='') as outfile:
        writer = csv.writer(outfile)
        
        writer.writerow(("id_str", "name", "screen_name", "location", "url", 
                          "description", "protected", "verified", 
                          "followers_count", "friends_count", "listed_count", 
                          "favourites_count", "statuses_count", "created_at", 
                          "geo_enabled", "lang"))
        
        for follower in followers_list:
            def task1():
                new_row = []
                new_row.append(follower.id_str)
                new_row.append(follower.name)
                new_row.append(follower.screen_name)
                new_row.append(follower.location)
                new_row.append(follower.url)
                new_row.append(follower.description)
                new_row.append(follower.protected)
                new_row.append(follower.verified)
                new_row.append(follower.followers_count)
                new_row.append(follower.friends_count)
                new_row.append(follower.listed_count)
                new_row.append(follower.favourites_count)
                new_row.append(follower.statuses_count)
                new_row.append(follower.created_at)
                new_row.append(follower.geo_enabled)
                new_row.append(follower.lang)
                return new_row
            def task2():
                a=get_tweets(api,follower.screen_name)
                return a
            pool = ThreadPool(processes=2)
            async_result=pool.apply_async(task1)
            new_row=async_result.get()
            async_result=pool.apply_async(task2)
            a=async_result.get()
            new_row.extend(a)
            writer.writerow(new_row)
          
    
pool1 = ThreadPool(processes=2)

def task3(a):
    consumer_key = "i6kXNkUFB2Kx4LQwOmLrMOcmE"
    consumer_secret = "uHVPm6aoO4VDxRZQSKHJOb9KEzcVx4QE8dErkNYvcmQAhBiQac"
    access_token = "1015231719853748225-WzoFQq4miICR7oNt71Yrx5u6mAVwh0"
    access_token_secret = "6SeVgsAwwMnPLDt0LH1p6L0YtmTkNx3782zsDxsWjQHpJ"
    api=create_api( consumer_key,consumer_secret,access_token,access_token_secret)   
    Trump_followers = get_followers(api, a)
    write_csv(api,Trump_followers)
    
def task4(b):
    consumer_key1 = "x3JKz59Zp7uebM2hNtVtpHP2K"
    consumer_secret1 = "xCm2jZJlFjHp7bFS0s75KAxHSQU3UphSQNlCSnZQCcOm8vrgXr"
    access_token1 = "739688302387728386-C60FQMOkeh2D5ztmUEm7azJhe057NCp"
    access_token_secret1 = "amhjVlzdvJKWjrACtjwpsFKlsFAQmICw2Y2LU2z89hvk1"
    api1=create_api( consumer_key1,consumer_secret1,access_token1,access_token_secret1)  
    Trump_followers1 = get_followers(api1, a)
    write_csv(api1,Trump_followers1)



c=input('1/2:')
if int(c)==2:
    a=input('name:')
    b=input('name2:')    
    async_result=pool1.apply_async(target=task3,args=(a,))
    async_result=pool1.apply_async(target=task4,args=(b,))
elif int(c)==1:
    a=input('name:')
    async_result=pool1.apply_async(target=task3,args=(a,))
else: 
    raise RuntimeError('Error Input')

    