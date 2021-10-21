# # Tweet Listener class set up
# Source: https://ch-nabarun.medium.com/easy-to-play-with-twitter-data-using-spark-structured-streaming-76fe86f1f81c


from multiprocessing.connection import Listener
import json
import configparser
import logging

c = configparser.ConfigParser()
c.read('config.ini')

access_token = c['twitterAuth']['access_token']
access_token_secret = c['twitterAuth']['access_token_secret']
consumer_key = c['twitterAuth']['consumer_key']
consumer_secret = c['twitterAuth']['consumer_secret']


class TweetsListener(Listener):
    # initialized the socket constructor
    def __init__(self, csocket, logger=logging):
        self.client_socket = csocket
        self.logger = logging.basicConfig(filename='tweet_stream.log', filemode='w',
                                          format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def on_data(self, data):
        try:
            # read the Twitter data which comes as a JSON format
            msg = json.loads(data)
            logging.info('Twitter JSON data read')
            # JSON file 'text' contains actual tweet
            # encode to remove emojis & other symbols
            print(msg['text'].encode('utf-8'))
            # the actual tweet data is sent to the client socket
            self.client_socket.send(msg['text'].encode('utf-8'))
            logging.info('Tweet data sent to client socket')
            return True  # to keep going; akin to continue/break

        except BaseException as e:
            # Error handling
            logging(f"Exception : {str(e)}")  # TODO file/module logging
            print(f'Exception: {e}')
            return True

    def on_error(self, status):
        logging.error(status)
        print(f'Error: {status}')
        return True
