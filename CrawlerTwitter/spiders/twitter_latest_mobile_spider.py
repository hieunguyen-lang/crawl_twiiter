# -*- coding: utf-8 -*-
__author__ = 'DuyLK'

import scrapy
import json
import random
import time
import sys
import redis
import mysql.connector
from scrapy.conf import settings
from CrawlerTwitter.items import CrawlerTwitterItem
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from CrawlerTwitter.helper import HelperKeys
from helper import Helper
from scrapy.loader import ItemLoader
from datetime import datetime, timedelta
from scrapy.loader import ItemLoader
from mysql.connector import errorcode
from dispatcherLib import DispatcherLibrary
reload(sys)
sys.setdefaultencoding('utf8')

class TwitterLatestMobileSpider(scrapy.Spider):
    name = "twitter_latest_mobile"
    handle_httpstatus_list = [403, 404, 200, 401]

    def __init__(self, *args, **kwargs):
        print('Init Spider ...')
        self.countRequest = 0
        self.countNewItem = 0
        self.DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        self.created = datetime.today().strftime(self.DATETIME_FORMAT)

        #Redis Config
        self.redis_db = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], db=settings['REDIS_DB_ID'])
        
        self.conn = mysql.connector.connect(user="root",
                                    passwd="vuduchong123",
                                    db="monitaz_crawler_twitter",
                                    host="192.168.1.11",
                                    charset="utf8mb4", use_unicode=True)
        
        self.cursor = self.conn.cursor()

        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.spider_opened, signals.spider_opened)

    def insert_data(self, data):
        insert_query = """
            INSERT IGNORE INTO data_posts_extension(post_id, keyword, user_id, user_name, content_created, status, type, url_post, content, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = self.conn.cursor()
        cursor.executemany(insert_query, data)
        self.conn.commit()
        print("[INFO] DONE {} RECORD".format(str(len(data))))

    def start_requests(self):
        keyword = "techcombank"
        url = 'https://api.twitter.com/graphql/tD6PM3q0jJijkK_go6Lkuw/SearchTimeline?variables=%7B%22includeTweetImpression%22%3Atrue%2C%22query_source%22%3A%22typed_query%22%2C%22includeHasBirdwatchNotes%22%3Afalse%2C%22includeEditPerspective%22%3Afalse%2C%22includeEditControl%22%3Atrue%2C%22query%22%3A%22'+keyword+'%22%2C%22timeline_type%22%3A%22Latest%22%7D&features=%7B%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22super_follow_badge_privacy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22super_follow_user_api_enabled%22%3Atrue%2C%22unified_cards_ad_metadata_container_dynamic_card_content_query_enabled%22%3Atrue%2C%22super_follow_tweet_api_enabled%22%3Atrue%2C%22articles_api_enabled%22%3Atrue%2C%22android_graphql_skip_api_media_color_palette%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22subscriptions_verification_info_enabled%22%3Atrue%2C%22blue_business_profile_image_shape_enabled%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22immersive_video_status_linkable_timestamps%22%3Atrue%2C%22super_follow_exclusive_tweet_notifications_enabled%22%3Atrue%7D'

        headers = {
            'Accept': 'application/json',
            # 'Accept-Encoding': 'br, gzip, deflate',
            'Accept-Language': 'vi-VN',
            'Authorization': 'OAuth realm="http://api.twitter.com/", oauth_version="1.0", oauth_token="1223100884030083074-eAWlkSE6QkFWF5YGIF9BkiW1mp0RIm", oauth_nonce="68095804350284873847358207963122", oauth_timestamp="1727083621", oauth_signature="pB1OShCYiHuvIw1154WJTQP6XEk%3D", oauth_consumer_key="3nVuSoBZnx6U4vzUxf5w", oauth_signature_method="HMAC-SHA1"',
            'Cache-Control': 'no-store',
            'Connection': 'Keep-Alive',
            # 'Cookie': 'guest_id_marketing=v1%3A172708330055731920; guest_id_ads=v1%3A172708330055731920; personalization_id=v1_FmGXShX32r8WjO2Iz7dSKw==; guest_id=v1%3A172708330055731920; lang=en',
            'Geolocation': '0',
            'Host': 'api-46-0-0.twitter.com',
            'kdt': 'KOPV9jBjWQOS77Gu21xJOV7OG9In2qXDIDBEi3V8',
            'Optimize-Body': 'true',
            'OS-Security-Patch-Level': '2019-07-05',
            'Timezone': 'Asia/Ho_Chi_Minh',
            'User-Agent': 'TwitterAndroid/10.32.0-release.0 (310320000-r-0) SM-G970N/9 (samsung;SM-G970N;samsung;SM-G970N;0;;1;2013)',
            'X-B3-TraceId': '920e921ff6c21491',
            'X-Client-UUID': '37c7a7b6-20e0-4832-94d2-2d6845bf7dad',
            'X-Twitter-Active-User': 'yes',
            'X-Twitter-API-Version': '5',
            'X-Twitter-Client': 'TwitterAndroid',
            'X-Twitter-Client-AdID': '33f4d8e9-c599-4727-83e0-98fe2936f7b1',
            'X-Twitter-Client-DeviceID': '720348ed50271912',
            'X-Twitter-Client-Flavor': 'X-Twitter-Client-Language:vi-VN',
            'X-Twitter-Client-Limit-Ad-Tracking': '0',
            'X-Twitter-Client-Version': '10.32.0-release.0'
        }

        yield scrapy.Request(url=url, headers=headers, meta={'keyword': keyword})

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
            if "data" in res:
                data = res["data"]
                if "search" in data:
                    data_search = data["search"]
                    if "timeline_response" in data_search:
                        timeline_response = data_search["timeline_response"]
                        if "timeline" in timeline_response:
                            timeline = timeline_response["timeline"]
                            if "instructions" in timeline:
                                instructions = timeline["instructions"]
                                data_posts = instructions[0]["entries"]
                                for post in data_posts:
                                    if "content" in post and "content" in post["content"] and "legacy" in post["content"]["content"]["tweetResult"]["result"]:
                                        data_auth = post["content"]["content"]["tweetResult"]["result"]["core"]["user_result"]["result"]["legacy"]
                                        data_post = post["content"]["content"]["tweetResult"]["result"]["legacy"]
                                        post_id = int(data_post['conversation_id_str'])
                                        print("====")
                                        print("[INFO] POST ID: {}".format(post_id))
                                        print("====")
                                        user_id = data_post['user_id_str']
                                        user_name = data_auth["screen_name"]
                                        user_name_show = data_auth["name"]
                                        content_created = self.convert_id_to_created(post_id)
                                        url_post = "/{_user_id}/status/{_post_id}".format(_user_id=user_id, _post_id=post_id)
                                        content = data_post['full_text']
                                        data_push.append((post_id, keyword, user_name, user_name_show, content_created, 0, 1, url_post, content, self.created))
            # PUSH DATA MYSQL
            # self.insert_data(data_push)                            

    def convert_id_to_created(self, post_id):
        timestamp = (post_id>>22) + 1288834974657
        content_created = datetime.fromtimestamp(timestamp/1000).strftime("%Y-%m-%d %H:%M:%S")
        return content_created 

    #Get Key Random
    def getHeaderRandom(self):
        keys = HelperKeys.ApiKeyHelper.key
        if len(keys) > 0:
            key = keys[random.randint(0, len(keys) - 1)]
            return key
        else:
            return ''

    #Check Redis
    def redis_exists(self,key):
        val = self.redis_db.get(key)
        if val == "exist":
            return True
        return False

    #Insert Key to Redis
    def insert_key_to_redis(self, key):
        nano = self.redis_db.set(key,"exist")

    #Count Key
    def countHeader(self):
        keys = HelperKeys.ApiKeyHelper.key
        return len(keys)

    def spider_opened(self,spider):
        print("Spider - Open")

    def spider_closed(self, spider, reason):
        print("NUMBER REQUESTS: "+ str(self.countRequest))
        print("NUMBER OF NEW ITEMS: "+ str(self.countNewItem))
        print("DONE!")