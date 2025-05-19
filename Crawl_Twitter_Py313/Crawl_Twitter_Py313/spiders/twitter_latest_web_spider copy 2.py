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
class TwitterLatestWeb2Spider(scrapy.Spider):
    name = "twitter_latest_web2"
    handle_httpstatus_list = [403, 404, 200, 401, 429, 500, 504]
    custom_settings = {
        # 'URLLENGTH_LIMIT': 20830,
        "CONCURRENT_REQUESTS": 5,
        "DOWNLOADER_MIDDLEWARES": {
            'Crawl_Twitter_Py313.middlewares.RandomUserAgentMiddleware': 400,
            # 'CrawlerTwitter.middlewares.RandomProxyBuyingTEST': 410,
            'Crawl_Twitter_Py313.middlewares.Rotate_Trans_Clien_Id_SearchMiddleware': 410,
        },
        "DOWNLOAD_TIMEOUT": 3,
        "DOWNLOAD_DELAY" : 1,
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

            
            yield scrapy.Request(method="GET", url=url, meta={'keyword': keyword})

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