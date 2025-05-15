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
class TwitterLatestMobileSpider(scrapy.Spider):
    name = "twitter_latest_mobile"
    handle_httpstatus_list = [403, 404, 200, 401, 429, 500, 504]
    custom_settings = {
        # 'URLLENGTH_LIMIT': 20830,
        "CONCURRENT_REQUESTS": 5,
        "DOWNLOADER_MIDDLEWARES": {
            'Crawl_Twitter_Py313.middlewares.RandomUserAgentMiddleware': 400,
            # 'CrawlerTwitter.middlewares.RandomProxyBuyingTEST': 410,
        },
        "DOWNLOAD_TIMEOUT": 3,
        "DELAY": 1,
        "RETRY_ENABLED": True,
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
        query = "SELECT id, keyword,authorization FROM data_keywords WHERE status = 1 ORDER BY RAND() LIMIT 30"
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
            id, keyword,authorization = row
            encoded_keyword = quote(keyword, safe=':/')

            url = 'https://api.twitter.com/graphql/BDo3929M41KOm8lE6VqX2g/SearchTimeline?variables=%7B%22includeTweetImpression%22%3Atrue%2C%22query_source%22%3A%22typed_query%22%2C%22includeHasBirdwatchNotes%22%3Afalse%2C%22includeEditPerspective%22%3Afalse%2C%22includeEditControl%22%3Atrue%2C%22query%22%3A%22{}%22%2C%22timeline_type%22%3A%22Latest%22%7D&features=%7B%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22grok_android_analyze_trend_fetch_enabled%22%3Afalse%2C%22super_follow_badge_privacy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22super_follow_user_api_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22super_follow_tweet_api_enabled%22%3Atrue%2C%22articles_api_enabled%22%3Atrue%2C%22profile_label_improvements_pcf_label_in_profile_enabled%22%3Atrue%2C%22premium_content_api_read_enabled%22%3Afalse%2C%22android_graphql_skip_api_media_color_palette%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22subscriptions_verification_info_enabled%22%3Atrue%2C%22blue_business_profile_image_shape_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22immersive_video_status_linkable_timestamps%22%3Atrue%2C%22profile_label_improvements_pcf_label_in_post_enabled%22%3Atrue%2C%22super_follow_exclusive_tweet_notifications_enabled%22%3Atrue%7D'.format(encoded_keyword)

            headers = {
                "accept": "application/json",
                "accept-language": "vi,en-US;q=0.9,en;q=0.8,fr-FR;q=0.7,fr;q=0.6",
                "Accept-Encoding": "br, gzip, deflate",
                "Authorization": authorization.strip(),
                "Cache-Control": "no-store",
                "Connection": "Keep-Alive",
                "Host": "api.twitter.com",
                "kdt": "IZ1DYrjSPytRcPuLXksCPZvAoSqSxwObNpYvZwtc",
                "Optimize-Body": "true",
                "OS-Security-Patch-Level": "2019-07-05",
                "Timezone": "Asia/Bangkok",
                "X-B3-TraceId": "21d563649d58e53c",
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "X-Client-UUID": "5372bff8-6055-4a14-b311-3674f99c740b",
                "X-Twitter-Active-User": "yes",
                "X-Twitter-API-Version": "5",
                "X-Twitter-Client": "TwitterAndroid",
                "X-Twitter-Client-AdID": "b2a6321b-255c-4e95-9261-506cc8541534",
                "x-twitter-client-language": "en"
            }

            cookies = {
                
            }

            yield scrapy.Request(method="GET", url=url, headers=headers, cookies=cookies, meta={'keyword': keyword})

    def parse(self, response):
        self.countRequest += 1

        #API Error
        if response.status == 403 or response.status == 404:
            print("[ERROR] 403 or 404 API: " + response.url)

        #API Empty
        if response.status == 400:
            print("[ERROR] 400 API: " + response.url)

        if response.status == 401:
            print("[ERROR] 401 API: Unauthorized")

        if response.status == 200:
            self.countNewItem += 1 
            #Response Meta
            metas = response.meta
            keyword = response.meta['keyword']
            res = json.loads(response.body)
            data_push  = []
            try:
                if res["data"]["search"]["timeline_response"]["timeline"]["instructions"]["entries"]:
                    for post in res["data"]["search"]["timeline_response"]["timeline"]["instructions"]["entries"]:
                        if "content" in post:
                            try:
                                result = post["content"]["tweetResult"]["result"]
                                data_auth = result["core"]["user_result"]["result"]["legacy"]
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
            except Exception as e:
                print("[ERROR] Error Get data from response:")

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