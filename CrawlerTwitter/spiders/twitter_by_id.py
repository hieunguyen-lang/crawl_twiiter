# -*- coding: utf-8 -*-
__author__ = 'DuyLK'

import scrapy
import json
import mysql.connector
import random
import time
import sys
import redis
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

class TwitterSpider(scrapy.Spider):
    name = "twitter_by_id"
    handle_httpstatus_list = [403, 404, 200, 401]

    def __init__(self, lang='', timeStart='', timeGet=5, *args, **kwargs):
        print('Init Spider ...')
        self.lang = lang
        self.timeGet = int(timeGet)
        self.countRequest = 0
        self.countNewItem = 0
        self.DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

        #Redis Config
        self.redis_db = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], db=settings['REDIS_DB_ID'])
        self.redis_Twitter_db = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], db=settings['REDIS_DB_TWITTER_ID'])

        # Get Time
        if timeStart:
            self.timeStart = str(timeStart) + 'T23:59:59.000Z'
            timeFormatStart = datetime.strptime(self.timeStart, "%Y-%m-%dT%H:%M:%S.%fZ")
            self.timeEnd = str(timeFormatStart.date() - timedelta(days=self.timeGet)) + 'T00:00:00.000Z'
        else:
            self.timeStart = str(datetime.utcnow().date()) + 'T'+ str(datetime.utcnow().hour) +':'+ str(datetime.utcnow().minute - 1) + ':00.000Z'
            self.timeEnd = str(datetime.utcnow().date() - timedelta(days=self.timeGet)) + 'T00:00:00.000Z'

        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.spider_opened, signals.spider_opened)

    def start_requests(self):
        # list_data = DispatcherLibrary().getKeywords()
        # list_data = [
        #     (1, '1596794423643320322', 'KhoongTrang', 1, 38411, 0, 38411, 0, 1),
        #     (2, '1593811534307676161', 'TinoChuynGia1', 1, 38721, 0, 38721, 0, 1)
        # ]
        list_data = DispatcherLibrary().get_data_by_id()

        for row in list_data:
            id, uid_post, username, brand_id, object_id, service_id, parent_object_id, parent_service_id, status = row
            headers = self.getHeaderRandom()
            print("[INFO] ID: " + str(id) + " -- USERNAME: " + str(username))
            if headers != '':
                url = 'https://api.twitter.com/2/tweets/'+uid_post+'?tweet.fields=public_metrics,author_id,created_at,entities,geo,in_reply_to_user_id,lang,possibly_sensitive,referenced_tweets,source'
                yield scrapy.Request(url=url, headers=headers, meta={'headers': headers, 'uid_post': uid_post, 'brand_id': brand_id, 'object_id': object_id, 'service_id': service_id, 'parent_object_id': parent_object_id, 'parent_service_id': parent_service_id })
            else:
                print('[Error] Headers 1 -> Empty!')
                print('---------*0*----------')

    def parse(self, response):
        self.countRequest += 1
        #Response Meta
        posts = json.loads(response.body)
        print('=======================================')
        print posts
        print('=======================================')
        metas = response.meta
        uid_post = response.meta['uid_post']
        brand_id = response.meta['brand_id']
        object_id = response.meta['object_id']
        service_id = response.meta['service_id']
        parent_object_id = response.meta['parent_object_id']
        parent_service_id = response.meta['parent_service_id']
        DispatcherLibrary().update_data_by_id(uid_post)

        #API Error
        if response.status == 403 or response.status == 404:
            print "[ERROR] 403 or 404 API: " + response.url
            print self.countHeader()
            if self.countHeader() > 0:
                headers = self.getHeaderRandom()
                newUrl = 'https://api.twitter.com/2/users/'+uid_post+'/tweets?tweet.fields=public_metrics,author_id,created_at,entities,geo,in_reply_to_user_id,lang,possibly_sensitive,referenced_tweets,source'
                print "=>>>>>>>>>>>> Again Request to Twitter <<<<<<<<<<<<<<="
                yield scrapy.Request(url=newUrl, callback=self.parse, headers=headers, meta={'brand_id': brand_id, 'object_id': object_id, 'service_id': service_id, 'parent_object_id': parent_object_id, 'parent_service_id': parent_service_id })
            else:
                print('[Error] Headers 2 -> Empty!')

        #API Empty
        if response.status == 400:
            print "[ERROR] 400 API: " + response.url

        if response.status == 401:
            print "[ERROR] 401 API: Unauthorized"

        if response.status == 200:
            self.countNewItem += 1
            if "data" in posts:
                post = posts['data']
                # for post in datas:
                post_id = post['id']
                
                # Check Duplicate
                idRedis = str(brand_id)+'_'+str(object_id)+'_'+str(service_id)+'_'+str(post_id)
                duplicate = self.redis_exists(idRedis)
                # duplicate = False

                if duplicate == True:
                    print('\n')
                    print ("=======================================")
                    print "[INFO] ITEM ALREADY EXISTS DON'T REQUEST AGAIN"
                    print "[INFO] THE ID: " + post_id
                    print "[INFO] THE WEB LINK : https://www.twitter.com/"+str(uid_post)+"/status=" + post_id
                    print ("=======================================")
                    print('\n')
                else:
                    print('\n')
                    print "============= VIDEO NOT DUPLICATE ============="
                    print "[INFO] THE WEB LINK : https://www.twitter.com"+str(uid_post)+"/status=" + post_id
                    print "[INFO] THE ID: "+ post_id                     
                    print "=============================================="
                    datas = {"data": post, "meta": metas}
                    if self.countHeader() > 0:
                        headers = self.getHeaderRandom()
                        url_user = "https://api.twitter.com/2/users/"+post['author_id']+"?user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
                        yield scrapy.Request(url=url_user, callback=self.parseUser, headers=headers, meta=datas)
                    else:
                        print('[Error] Headers 3 -> Empty!')
            else:
                print('[ERROR] EMPTY RESURT!')
                print('---------*0*----------')
        else:
            print('[INFO] STATUS NOT 200')
            print('---------*0*----------')           

    def parseUser(self, response):
        print "==="
        print "[INFO] PARSER USER!"
        print "==="
        users = json.loads(response.body)
        #API Empty
        if response.status == 400:
            print "[ERROR] 400 API: " + response.url

        if response.status == 401:
            print "[ERROR] 401 API: Unauthorized"

        if response.status == 200:
            datas = response.meta
            if "data" in users:
                item = self.detailPost(datas,users['data'])
                if item != '':
                    # print item
                    yield item
                print('\n')
            else:
                print "==="
                print "[INFO] NOT REQUEST DATA USER!!!"
                print "==="
        else:
            print "==="
            print "[INFO] STATUS NOT 2O0!!!"
            print "==="           

    def detailPost(self, datas, users):
        print "==="
        print "[INFO] DETAIL POST!"
        print "==="
        data = datas['data']
        metas = datas['meta']
        time = data['created_at']
        timeFormat = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        timeCreated = (timeFormat + timedelta(hours=7)).strftime('%s')
        timeFormat =  (timeFormat + timedelta(hours=7)).strftime(self.DATETIME_FORMAT) 
        url = "https://twitter.com/"+users['username']+"/status/"+data['id']
        item = CrawlerTwitterItem()
        item['post_id'] = data['id']
        item['url'] = url
        item['brand_id'] = metas['brand_id']
        item['object_id'] = metas['object_id']
        item['service_id'] = metas['service_id']
        item['parent'] = ''
        item['parent_object_id'] = metas['parent_object_id']
        item['parent_service_id'] = metas['parent_service_id']
        item['author_id'] = data['author_id']
        item['author_name'] = users['name']  
        item['author_username'] = users['username']      
        item['title'] = ''
        item['description'] = data['text']
        item['publishedAt'] = timeFormat
        item['data'] = data
        item['comment_id'] = ''
        item['comments'] = 'null'
        item['keyword'] = users['username']
        item['company'] = 0
        item['typePost'] = 'post'
        item['likeCount'] = data['public_metrics']['like_count'] #Like
        item['commentCount'] = data['public_metrics']['reply_count'] #Reply
        item['viewCount'] = data['public_metrics']['retweet_count'] #RT      
        item['timeCreated']=  timeCreated
        item['profileImage'] = users['profile_image_url']
        item['tags'] = '' 

        return item    

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
        val = self.redis_Twitter_db.get(key)
        if val == "exist":
            return True
        return False

    #Insert Key to Redis
    def insert_key_to_redis(self, key):
        nano = self.redis_Twitter_db.set(key,"exist")

        print ("================= SET =================")
        print ("=>>>>>>>>>>>> Key: " + key)
        print (nano)
        print ("=======================================")

    #Count Key
    def countHeader(self):
        keys = HelperKeys.ApiKeyHelper.key
        return len(keys)

    def spider_opened(self,spider):
        print "Spider - Open"

    def spider_closed(self, spider, reason):
        print("NUMBER REQUESTS: "+ str(self.countRequest))
        print("NUMBER OF NEW ITEMS: "+ str(self.countNewItem))
        print("DONE!")