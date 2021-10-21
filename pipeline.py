# import dependencies
import configparser
import json
import logging
import math
import re
import socket
import urllib.parse
from datetime import date, datetime, timedelta
from operator import itemgetter

import numpy as np
import pandas as pd
import psycopg2  # alts: SQLalchemy
import requests
import tweepy  # python package for accessing Tweet streaming API
from bs4 import BeautifulSoup
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from numpy import datetime64
from psycopg2 import Error
from TikTokAPI import TikTokAPI
from tweepy import API, Stream

# import program modules
from database import *
from news import *
from tiktok import *
from timer import Timer
from tweet_search import *
from tweet_stream_listener import *

c = configparser.ConfigParser()
c.read('config.ini')

# config credentials
host = c['database']['host']
username = c['database']['user']
password = c['database']['password']
db = c['database']['database']

news_api_key = c['newsAuth']['api_key']
tiktok_sv_id = c['tiktokAuth']['s_v_web_id']
tiktok_tt_id = c['tiktokAuth']['tt_webid']

# twitter auth
access_token = c['twitterAuth']['access_token']
access_token_secret = c['twitterAuth']['access_token_secret']
consumer_key = c['twitterAuth']['consumer_key']
consumer_secret = c['twitterAuth']['consumer_secret']

logging.basicConfig(filename='pyPipeline.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if '__name__' == '__main__':

    postgres_db = DataBase(host, username, password)
    logging.info('Database initialized')

    # connect to server
    postgres_server = postgres_db.create_server_connection()
    logging.info('Database server connected')

    # connect to social media news db
    connection = postgres_db.create_db_connection(db)
    logging.info('Postres connection created')

    # execute defined queries to create db tables if needed
    try:
        postgres_db.execute_query(connection, create_article_table)
        postgres_db.execute_query(connection, create_article_text_table)
        postgres_db.execute_query(connection, create_tweets_table)
        postgres_db.execute_query(connection, create_political_event_table)
        postgres_db.execute_query(connection, create_users_table)
        postgres_db.execute_query(connection, create_tiktok_sounds_table)
        postgres_db.execute_query(connection, create_tiktok_music_table)
        postgres_db.execute_query(connection, create_tiktok_stats_table)
        postgres_db.execute_query(connection, create_tiktok_tags_table)
        postgres_db.execute_query(connection, create_tiktoks_table)
        logging.info('Database queries executed successfully')
    except (ConnectionError) as e:
        logging.error({e}, 'Check SQL create queries')

    # add foreign keys
    try:
        postgres_db.execute_query(connection, alter_tiktoks_table)
        postgres_db.execute_query(connection, alter_tiktok_stats_table)
        logging.info('Database relationships created successfully')
    except (ConnectionError) as e:
        logging.error({e}, 'Check table relationships')

    # instantiate News class
    news = News(news_api_key)
    # get all news & keywords - takes about 30 seconds
    keywords = news.get_all_news()
    logging.info('News dataframe created')

    # create a socket object
    s = socket.socket()
    # Get local machine name : host and port
    host = "127.0.0.1"
    # TODO catch errors and exceptions for port
    # Will reject if already in use
    port = 3350
    # Bind to the port
    s.bind((host, port))
    logging.info(f'Port bound to host. Listening on port {port}')
    print(f"Listening on port: {str(port)}")
    # Wait to establish the connection with client
    s.listen(5)
    logging.info('Connected to client')
    # Returns tuple of data & origin
    c, addr = s.accept()
    # Confirmation printed on command line
    logging.info('Socket request recieved')
    print("Received request from: " + str(addr))

    # instantiate Tweets class
    t = Tweets(consumer_key, consumer_secret,
               access_token, access_token_secret)
    # authenticate Tweepy
    auth = t.tweepy_auth()
    logging.info('Tweepy authenticated')
    # twitter_stream will get the actual live tweet data
    # This is a stream object
    twitter_stream = Stream(auth, TweetsListener(c))
    # filter tweet feeds using keywords
    for keys in news.all_news_df['keywords']:
        keywords = list(keys)  # TODO add itertools combinations
        for word in keywords:
            twitter_stream.filter(track=word)
    logging.info('Tracking keywords in Twitter stream')

    tiktok_auth = {
        "s_v_web_id": tiktok_sv_id,  # references variables saved from config file
        "tt_webid": tiktok_tt_id
    }

    api = TikToks(cookie=tiktok_auth)
    logging.info('TikTokAPI authorized')
    tiktok_df = news.all_news_df['keywords'].map(api.getVideosByHashtag)

    # add late-arriving twitter data
    # tweet search instead of stream
    tw = t.tweet_search(keywords)

    # mogrify stream
    # postgres_db.execute_mogrify(connection, filtered_stream, 'stream_tweets')
    # mogrify batch tweets
    postgres_db.execute_mogrify(connection, tw, 'batch_tweets')
    # execute mogrify - insert news df into database
    postgres_db.execute_mogrify(connection, news.all_news_df, 'articles')
    # mogrify
    postgres_db.execute_mogrify(connection, tiktok_df, 'tiktoks')
    logging.info('Data added to database successfully')
