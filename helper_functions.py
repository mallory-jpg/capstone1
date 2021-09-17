

import logging
import numpy as np

def read_hashtags(tag_list):
    """Tweet cleaning helper functions"""
    hashtags = []
    for tag in tag_list:
        hashtags.append(tag['text'])
    return hashtags

def get_random_ua(browser):
    # make sure you've done: git clone https://github.com/tamimibrahim17/List-of-user-agents.git at this point so the txt files are in your directory
    random_ua = ''
    ua_file = f'{browser}.txt'.title()

    try:
        with open(ua_file) as f:
            lines = f.readlines()
        if len(lines) > 0:
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            random_proxy = lines[int(idx)]
    except Exception as ex:
        logging('Exception in random_ua')
        print(str(ex))
    finally:
        return random_ua
