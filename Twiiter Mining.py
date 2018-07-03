#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 09:10:01 2018

@author: luohaozheng
"""
from urllib import request
import re
import nltk
import string
#from nltk.corpora import stopwords
'''
import psycopg2
conn = psycopg2.connect(database="", user="postgres", password="postgres", host="192.168.10.80", port="5432")
cur = conn.cursor()
cur.execute("CREATE TABLE result(id serial PRIMARY KEY,Name varchar(32),Status varchar(32),Description text,Refer text,Phase text,other text);")
def tablewrite(n,b,c,d):
    cur.execute("INSERT INTO test(Name,age,location,Twitter)VALUES(%s, %s, %s, %s, %s, %s)", (n,b,c,d))
 '''   
import tweepy
consumer_key = "x3JKz59Zp7uebM2hNtVtpHP2K"
consumer_secret = "xCm2jZJlFjHp7bFS0s75KAxHSQU3UphSQNlCSnZQCcOm8vrgXr"
access_token = "739688302387728386-C60FQMOkeh2D5ztmUEm7azJhe057NCp"
access_token_secret = "amhjVlzdvJKWjrACtjwpsFKlsFAQmICw2Y2LU2z89hvk1"

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth) 

# Using the API object to get tweets from your timeline, and storing it in a variable called public_tweets
public_tweets = api.home_timeline()
# foreach through all tweets pulled
D=dict()
for tweet in public_tweets:
   # printing the text stored inside the tweet object
   b=tweet.text

   token=nltk.word_tokenize(b)
   
 #  print(token)
   a=tweet.user.location
   if a in D:
       D[a]+=1
   else:
       D[a]=1
   reg3=r'''((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+'''
   imgre3 = re.compile(reg3)
   imglist3 = re.findall(imgre3, b)
   print(imglist3)
    
       
   