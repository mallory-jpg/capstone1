from news import *

import tweepy  # python package for accessing Tweet streaming API
from tweepy import API
import json
import logging
import pandas as pd
import configparser
import geocoder
import sys


config = configparser.ConfigParser()
config.read('config.ini')

access_token = config['twitterAuth']['access_token']
access_token_secret = config['twitterAuth']['access_token_secret']
consumer_key = config['twitterAuth']['consumer_key']
consumer_secret = config['twitterAuth']['consumer_secret']

news_api_key = config['newsAuth']['api_key']

# instantiate News class
news = News(news_api_key)
# get all news - takes about 30 seconds
news.get_all_news()


class Tweets():

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, logger=logging):
        self.logger = logging.basicConfig(filename='tweets.log', filemode='w',
                                          format=f'%(asctime)s - %(levelname)s - %(message)s')
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        self.location = sys.argv[1]  # user location as argument variable
        # object with latitude & longitude of user location
        self.geo = geocoder.osm(self.location)

    def tweepy_auth(self):
        """Authorize tweepy API
        :return self.api: authorized tweepy api object"""

        self.auth = tweepy.OAuthHandler(
            self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

        # create API object
        # user_agent=get_random_ua('Chrome'), wait_on_rate_limit_notify=True)
        self.api = API(self.auth, wait_on_rate_limit=True)

        try:
            self.api.verify_credentials()
            logging.info("Tweepy API Authenticated")
            print('Tweepy authentication successful')
        except Exception as e:
            logging.error(f"Error during Tweepy authentication: {e}")
            raise e
        return self.api

    # def get_tweets(self, news_keywords, news_instance): # TODO add stream listening stuff to params
    #     searched_tweets = self.tweet_search(news_keywords)
        # stream_tweets = TwitterStreamListener.on_status(listener, tweet_stream)

    def tweet_search(self, news_keywords):
        """
        Search for tweets within previous 7 days & write results to JSON file
        :param news_keywords: tuple of keywords to query from keywords df column
        """
        api = self.api

        # unpack keyword tuples
        print('Searching for tweets matching keywords')
        for keys in news_keywords:
            keywords = list(keys)  # TODO add itertools combinations
            for word in keywords:
                try:
                    result = api.search(q=str(
                        word) + " -filter:retweets", lang='en')
                    # print(type(result))
                    status = result[0]
                    # print(type(status))
                    tweet = status._json
                    search_tweet_count = len(tweet)
                    #self.file.write(json.dumps(tweets)+ '\\n')
                    tweet = json.dumps(tweet)  # tweet to json string
                    if (type(tweet) != str):
                        raise AssertionError(
                            "Tweet must be converted to JSON string")
                    tweet = json.loads(tweet)  # tweet to dict
                    if (type(tweet) != dict):
                        raise AssertionError(
                            "Tweet must be converted from JSON string to type dict")
                except (TypeError) as e:
                    logging('Error: ', e)
                    print('Error: keyword not found in tweet search')
                    break
                else:
                    # write tweets to json file
                    with open("tweets.json", "a") as f:
                        json.dump(tweet, f)
        logging.info('Tweet search successful')
        print('Tweet search by keyword was successful')

        # finally:
        # TODO add tweet unpacking & cleaning?
        # pass
        # TODO put tweets into db
        # TODO

    def clean_tweets(self, tweets):
        # use slang.txt
        # https://www.geeksforgeeks.org/python-efficient-text-data-cleaning/
        pass
