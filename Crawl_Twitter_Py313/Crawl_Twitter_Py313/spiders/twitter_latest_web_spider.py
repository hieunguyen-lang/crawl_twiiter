# -*- coding: utf-8 -*-
__author__ = 'DuyLK'

import scrapy
import json
import random
import time
import sys
import redis
import mysql.connector
#from CrawlerTwitter.items import CrawlerTwitterItem
# from .helper import Helper
from scrapy import signals
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings
from scrapy.loader import ItemLoader
from scrapy import signals
from pydispatch import dispatcher
from urllib.parse import quote
from datetime import datetime, timedelta
from mysql.connector import errorcode
# from dispatcherLib import DispatcherLibrary
#from CrawlerTwitter.proxy import *
settings = get_project_settings()
from dotenv import load_dotenv
import os

# Load biến môi trường từ file .env
load_dotenv()
class TwitterLatestWebSpider(scrapy.Spider):
    name = "twitter_latest_web"
    handle_httpstatus_list = [403, 404, 200, 401, 429, 500, 504]
    custom_settings = {
        # 'URLLENGTH_LIMIT': 20830,
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOADER_MIDDLEWARES": {
            'Crawl_Twitter_Py313.middlewares.RandomUserAgentMiddleware': 400,
            # 'CrawlerTwitter.middlewares.RandomProxyBuyingTEST': 410,
        },
        "DOWNLOAD_TIMEOUT": 3,
        "DOWNLOAD_DELAY" : 10,
        "RETRY_ENABLED": False,
        "RETRY_TIMES": 1
    }
    def __init__(self, *args, **kwargs):
        print('Init Spider ...')
        self.countRequest = 0
        self.countNewItem = 0
        self.DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        self.created = datetime.today().strftime(self.DATETIME_FORMAT)

        #Redis Config
        self.redis_db = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB_ID'))

        self.conn = mysql.connector.connect(user=os.getenv('MYSQL_USERNAME'),
                                    passwd=os.getenv('MYSQL_PASSWD'),
                                    db=os.getenv('MYSQL_DB'),
                                    host=os.getenv('MYSQL_HOST'),
                                    charset="utf8mb4", use_unicode=True)
        
        self.cursor = self.conn.cursor()

        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.spider_opened, signals.spider_opened)

    def get_keyword(self):
        query = "SELECT id, keyword FROM data_keywords WHERE status = 1 ORDER BY RAND() LIMIT 30"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def insert_data(self, data):
        insert_query = """
            INSERT IGNORE INTO data_posts_twitter(post_id, keyword, user_id, user_name, content_created, status, type, url_post, content, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = self.conn.cursor()
        cursor.executemany(insert_query, data)
        self.conn.commit()
        print("[INFO] DONE {} RECORD".format(str(len(data))))

    def start_requests(self):
        list_keyword = self.get_keyword()
        
        for row in list_keyword:
            id, keyword = row
            encoded_keyword = quote(keyword, safe=':/')
            print(encoded_keyword)
            url = 'https://x.com/i/api/graphql/nKAncKPF1fV1xltvF3UUlw/SearchTimeline?variables=%7B%22rawQuery%22%3A%22{}%22%2C%22count%22%3A20%2C%22querySource%22%3A%22recent_search_click%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22rweb_video_screen_enabled%22%3Afalse%2C%22profile_label_improvements_pcf_label_in_post_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22premium_content_api_read_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22responsive_web_grok_analyze_button_fetch_trends_enabled%22%3Afalse%2C%22responsive_web_grok_analyze_post_followups_enabled%22%3Atrue%2C%22responsive_web_jetfuel_frame%22%3Afalse%2C%22responsive_web_grok_share_attachment_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22responsive_web_grok_show_grok_translated_post%22%3Afalse%2C%22responsive_web_grok_analysis_button_from_backend%22%3Atrue%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_grok_image_annotation_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'.format(encoded_keyword)

            headers = {
                    "accept": "*/*",
                    "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
                    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                    "content-type": "application/json",
                    "dnt": "1",
                    "priority": "u=1, i",
                    "referer": "https://x.com/",
                    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"Windows\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                    "x-client-transaction-id": "e8kjs3ndx2o4RO52SwylI+EdQQQRlWhoDmGNqt8IwzYJKbkHI8IrAZguCeARWHN8aXQroHiJ+ghXOts/PBmSmVftUPz3eA",
                    "x-client-uuid": "99c4895d-141a-48a8-8a5b-344e56cd76f1",
                    "x-csrf-token": "9f5f4c079e7f555653aefe6496f10c467dc043c3784ce2814b2d7f6da9e8ba73f0e47f8f21e144a100ecf0dbe234b94ad600708a88b55df44acc044c9d87342b9ec046b62b7c7e49fbb4e4955abbbe0f",
                    "x-twitter-active-user": "yes",
                    "x-twitter-auth-type": "OAuth2Session",
                    "x-twitter-client-language": "en"
                }

            cookies = {
                    "guest_id": "v1%3A174659106509384187",
                    "night_mode": "2",
                    "guest_id_marketing": "v1%3A174659106509384187",
                    "guest_id_ads": "v1%3A174659106509384187",
                    "g_state": "{\"i_l\":0}",
                    "kdt": "PWBkW58Bkv24SyKFEmRBVqzYSsmRkxMXkO914nkw",
                    "auth_token": "c63738f7fed343378353c20d5973fa768ff12f8d",
                    "ct0": "9f5f4c079e7f555653aefe6496f10c467dc043c3784ce2814b2d7f6da9e8ba73f0e47f8f21e144a100ecf0dbe234b94ad600708a88b55df44acc044c9d87342b9ec046b62b7c7e49fbb4e4955abbbe0f",
                    "twid": "u%3D1919969636952768512",
                    "personalization_id": "v1_vso0/8LANYanmeekinOuww==",
                    "lang": "vi",
                    "_ga": "GA1.1.205388427.1746772689",
                    "_ga_RJGMY4G45L": "GS2.1.s1747030841$o3$g0$t1747030844$j57$l0$h0",
                    "external_referer": "8e8t2xd8A2w%3D|0|GlWr2u5wzZgGipXRLxmupQ%3D%3D",
                    "__cf_bm": "OEthQEJK3arbEbrIImEDTAR2g905NralOiqCMQwn22I-1747628815-1.0.1.1-fQJtivTAecIefUPG5qhBDZgHTAQyrIFgeVwDvSZKlZuNak486NUi5dLtaMAlJNNmSFGBp17BH700e6QH2Un8Bi.ITZrTB1.DJMIvT.Y1P8Q"
                }

            yield scrapy.Request(method="GET", url=url, headers=headers, cookies=cookies, meta={'keyword': keyword})

    def parse(self, response):
        self.countRequest += 1

        #API Error
        if response.status != 200:
            print("[ERROR] API STATUS: " + str(response.status) + " - keyword: " + response.meta['keyword'])

        
        if response.status == 200:
            self.countNewItem += 1 
            #Response Meta
            metas = response.meta
            keyword = response.meta['keyword']
            res = json.loads(response.body)
            data_push  = []
            if "data" in res:
                data = res["data"]
                if "search_by_raw_query" in data:
                    data_search = data["search_by_raw_query"]
                    if "search_timeline" in data_search:
                        search_timeline = data_search["search_timeline"]
                        if "timeline" in search_timeline:
                            timeline = search_timeline["timeline"]
                            if "instructions" in timeline:
                                instructions = timeline["instructions"]
                                data_posts = instructions[0]["entries"]
                                for post in data_posts:
                                    if "content" in post:
                                        try:
                                            result = post["content"]["itemContent"]["tweet_results"]["result"]
                                            data_auth = result["core"]["user_results"]["result"]["legacy"]
                                            data_post = result["legacy"]
                                            post_id = int(result['rest_id'])
                                            print("[INFO] POST ID: {}".format(post_id))
                                            user_id = data_post['user_id_str']
                                            user_name = data_auth["screen_name"]
                                            user_name_show = data_auth["name"]
                                            content_created = self.convert_id_to_created(post_id)
                                            url_post = "/{_user_id}/status/{_post_id}".format(_user_id=user_id, _post_id=post_id)
                                            content = data_post['full_text']
                                            data_push.append((post_id, keyword, user_name, user_name_show, content_created, 0, 1, url_post, content, self.created))
                                        except Exception as e:
                                            print("[ERROR] Error: {}".format(e))
                                            print("[INFO] Content: {}".format(post["content"]))
                else:
                    print("[INFO] No data")

            if len(data_push) > 0:
                print("[INFO] PUSH DATA MYSQL ({} ITEM)".format(len(data_push)))
                self.insert_data(data_push)    
                self.countNewItem += len(data_push)
                data_push = []
            else:
                print("[INFO] No push data")

    def convert_id_to_created(self, post_id):
        timestamp = (post_id>>22) + 1288834974657
        content_created = datetime.fromtimestamp(timestamp/1000).strftime("%Y-%m-%d %H:%M:%S")
        return content_created 

    #Check Redis
    def redis_exists(self,key):
        val = self.redis_db.get(key)
        if val == "exist":
            return True
        return False

    #Insert Key to Redis
    def insert_key_to_redis(self, key):
        nano = self.redis_db.set(key,"exist")

    def spider_opened(self,spider):
        print("Spider - Open")

    def spider_closed(self, spider, reason):
        print("================================================")
        print("NUMBER REQUESTS: "+ str(self.countRequest))
        print("NUMBER OF NEW ITEMS: "+ str(self.countNewItem))
        print("DONE!")
        print("================================================")