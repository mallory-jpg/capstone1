from TikTokAPI import TikTokAPI
import configparser
import pandas as pd
from news import *
from database import *


c = configparser.ConfigParser()
c.read('sm-political-analysis/config.ini')

host = c['database']['host']
username = c['database']['user']
password = c['database']['password']
db = c['database']['database']

news_api_key = c['newsAuth']['api_key']
tiktok_sv_id = c['tiktokAuth']['s_v_web_id']
tiktok_tt_id = c['tiktokAuth']['tt_webid']

tiktok_auth = {
    "s_v_web_id": tiktok_sv_id,  # references variables saved from config file
    "tt_webid": tiktok_tt_id
}

class TikToks(TikTokAPI):

    def __init__(self, cookie, logger=logging, api=None):
        super(TikTokAPI, self).__init__()
        self.cookie = cookie
        self.tiktok_count = 0
        self.logger = logging.basicConfig(filename='tiktok.log', filemode='w',
                                          format='%(asctime)s - %(levelname)s - %(message)s')
    def getVideosByHashtag(self, hashtags, count=3000):
        try:
            for hashTag in hashtags:
                try:
                    hashTag = hashTag.replace("#", "")
                    hashTag_obj = self.getHashTag(hashTag)
                    hashTag_id = hashTag_obj["challengeInfo"]["challenge"]["id"]
                except (KeyError, ReferenceError) as err:
                    logging.error(err)
                    continue
                else:
                    url = self.base_url + "/challenge/item_list/"
                    req_default_params = {
                        "secUid": "",
                        "type": "3",
                            "minCursor": "0",
                            "maxCursor": "0",
                            "shareUid": "",
                            "recType": ""
                        }
                    params = {
                        "challengeID": str(hashTag_id),
                            "count": str(count),
                            "cursor": "0",
                        }
                    for key, val in req_default_params.items():
                            params[key] = val
                    for key, val in self.default_params.items():
                            params[key] = val
                    extra_headers = {
                            "Referer": "https://www.tiktok.com/tag/" + str(hashTag)
                            }
                    self.tiktok_count += 1
                    tok = self.send_get_request(url, params, extra_headers=extra_headers)
                    # write tiktoks to json file
                    with open("tiktoks.json", "a") as f:
                        json.dump(tok, f)
                    print(self.tiktok_count)
                    return tok
        except KeyboardInterrupt as ex:
            raise ex
        finally:
            self.tiktok_df = pd.read_json('tiktoks.json') # columns=['postID', 'createTime', 'userID', 'description', 'musicId', 'soundId', 'tags'])
            logging.info(f'This run scraped {self.tiktok_count} TikToks')
            return self.tiktok_df

# instantiate news class
# news = News(news_api_key)
# news_df = news.get_all_news() # TODO assert that df has information in it

# # instantiate TikTok API
# api = TikTokAPI(cookie=tiktok_auth)
# api.tiktok_df = news_df['keywords'].map(api.getVideosByHashtag)

