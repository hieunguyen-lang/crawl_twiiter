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
class TwitterLatestWeb1Spider(scrapy.Spider):
    name = "twitter_latest_web1"
    handle_httpstatus_list = [403, 404, 200, 401, 429, 500, 504]
    custom_settings = {
        # 'URLLENGTH_LIMIT': 20830,
        "CONCURRENT_REQUESTS": 5,
        "DOWNLOADER_MIDDLEWARES": {
            'Crawl_Twitter_Py313.middlewares.RandomUserAgentMiddleware': 400,
            # 'CrawlerTwitter.middlewares.RandomProxyBuyingTEST': 410,
        },
        # "DOWNLOAD_TIMEOUT": 3,
        # "DELAY": 1,
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
        a=0
        for i in range(1,50):
            a+=i
            #encoded_keyword = quote(keyword, safe=':/')
            url = 'https://api.twitter.com/graphql/BDo3929M41KOm8lE6VqX2g/SearchTimeline?variables=%7B%22includeTweetImpression%22%3Atrue%2C%22query_source%22%3A%22typeahead_click%22%2C%22includeHasBirdwatchNotes%22%3Afalse%2C%22includeEditPerspective%22%3Afalse%2C%22includeEditControl%22%3Atrue%2C%22query%22%3A%22banker%20Peter%20Sands%22%2C%22timeline_type%22%3A%22Latest%22%7D&features=%7B%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22grok_android_analyze_trend_fetch_enabled%22%3Afalse%2C%22super_follow_badge_privacy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22super_follow_user_api_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22super_follow_tweet_api_enabled%22%3Atrue%2C%22articles_api_enabled%22%3Atrue%2C%22profile_label_improvements_pcf_label_in_profile_enabled%22%3Atrue%2C%22premium_content_api_read_enabled%22%3Afalse%2C%22android_graphql_skip_api_media_color_palette%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22subscriptions_verification_info_enabled%22%3Atrue%2C%22blue_business_profile_image_shape_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22immersive_video_status_linkable_timestamps%22%3Atrue%2C%22profile_label_improvements_pcf_label_in_post_enabled%22%3Atrue%2C%22super_follow_exclusive_tweet_notifications_enabled%22%3Atrue%7D'

            headers = {
                "accept": "*/*",
                "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
                "authorization": 'OAuth realm="http://api.twitter.com/", oauth_version="1.0", oauth_token="1918725811877953536-5a8XfJh0UM8imSGWqu8VdVvbPuQutr", oauth_nonce="32448723943943412300748591506664", oauth_timestamp="1747216783", oauth_signature="62HSwHa6Ivr83JCcdJHaY%2B00ENA%3D", oauth_consumer_key="3nVuSoBZnx6U4vzUxf5w", oauth_signature_method="HMAC-SHA1"',
                "content-type": "application/json",
            }

        

            yield scrapy.Request(method="GET", url=url, headers=headers, meta={'keyword': "keyword"},dont_filter=True)

    def parse(self, response):
        self.countRequest += 1

        #API Error
        if response.status != 200:
            print("[ERROR] API STATUS: " + str(response.status))

        
        if response.status == 200:
            print("[INFO] API STATUS: " + str(response.status))
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