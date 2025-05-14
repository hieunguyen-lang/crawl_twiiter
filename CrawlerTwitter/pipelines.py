# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import print_function
import mysql.connector
import redis
import json
from mysql.connector import errorcode
from elasticsearch import Elasticsearch
from datetime import datetime
from scrapy.conf import settings

class CrawleryoutubePipeline:
    
    def __init__(self, **kwargs):
        print ("[Info] Init Pipeline!")

        # Redis Config
        self.redis_db = redis.Redis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'], db=settings['REDIS_DB_TWITTER_ID'])

        #MySQL
        self.now  = datetime.now()
        self.conn = mysql.connector.connect(user=settings['MYSQL_USERNAME'],
                                    passwd=settings['MYSQL_PASSWD'],
                                    db=settings['MYSQL_DB'],
                                    host=settings['MYSQL_HOST'],
                                    charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def open_spider(self, spider):
        print("Spider open")

    def process_item(self, item, spider):
        print("Saving item into db ...")
        self.save(dict(item))

    def close_spider(self, spider):
        print("Spider close")

    def save(self, row):
        print('Save to Elasticsearch')
        timestamp = int(row['timeCreated'])

        if row['typePost'] == 'post':
            idEs = str(row['brand_id'])+'_'+str(row['object_id'])+'_'+str(row['service_id'])+'_'+str(row['post_id'])
            message = row['title']+' - '+row['description']
            doc = {
                "content_created": row['publishedAt'],
                "per_positive":0,
                "point":3,
                "sub_service_id":0,
                "is_updated":0,
                "fb_id": row['post_id'],
                "sub_parent_service_id":0,
                "brand_id": str(row['brand_id']),
                "tag":7,
                "object_id": str(row['object_id']),
                "per_neutral":0,
                "content_from_id": row['author_id'],
                "brand_service_id":0,
                "message": message,
                "is_delete":0,
                "is_backup":0,
                "total_like": row['likeCount'], #So luong like
                "is_duplicated":0,
                "state":0,
                "page_name": row['author_name'],
                "content_from_name": row['author_name'],
                "concern_point":7,
                "type": 0,
                "child_count": row['commentCount'], #So luong cmt
                "is_pin":0,
                "message_0":"",
                "total_page_like":0,
                "parent_object_id":str(row['parent_object_id']),
                "own_type":0,
                "per_negative":0,
                "mention_type":1,
                "status_9":0,
                "status_8":0,
                "status_7":0,
                "sub_message": row['profileImage'],
                "status_5":0,
                "status_4":2,
                "status_3":0,
                "status_2":0,
                "status_1":0,
                "status_0":0,
                "message_1":"",
                "sub_status":1,
                "message_3":"",
                "message_2":"",
                "message_4":"",
                "created": timestamp,
                "page_id": row['author_id'],
                "fb_parent_id":"",
                "parent_service_id":str(row['parent_service_id']),
                "sub_brand_service_id":0,
                "total_share": row['viewCount'], #Luong view
                "service_id":str(row['service_id']),
                "status_6":0,
                "content_id": row['post_id'],
                "content_updated": row['publishedAt']
            }
            print("Item saved Post to MySQL && Elastic Search")
        else:
            idEs = str(row['brand_id'])+'_'+str(row['object_id'])+'_'+str(row['service_id'])+'_'+str(row['comment_id'])
            message = '['+row['author_name']+']'+row['title']
            doc = {
                "content_created": row['publishedAt'],
                "per_positive":0,
                "point":3,
                "sub_service_id":0,
                "is_updated":0,
                "fb_id": row['comment_id'],
                "sub_parent_service_id":0,
                "brand_id": row['brand_id'],
                "tag":7,
                "object_id": row['object_id'],
                "per_neutral":0,
                "content_from_id": row['author_id'],
                "brand_service_id":0,
                "message": message,
                "is_delete":0,
                "is_backup":0,
                "total_like": row['likeCount'], #So luong like
                "is_duplicated":0,
                "state":0,
                "page_name": row['author_name'],
                "content_from_name": row['author_name'],
                "concern_point":7,
                "type": 1,
                "child_count": row['commentCount'], #So luong cmt
                "is_pin":0,
                "message_0":"",
                "total_page_like":0,
                "parent_object_id": row['parent_object_id'],
                "own_type":0,
                "per_negative":0,
                "mention_type":1,
                "status_9":0,
                "status_8":0,
                "status_7":0,
                "sub_message": row['profileImage'],
                "status_5":0,
                "status_4":2,
                "status_3":0,
                "status_2":0,
                "status_1":0,
                "status_0":0,
                "message_1":"",
                "sub_status":1,
                "message_3":"",
                "message_2":"",
                "message_4":"",
                "created": timestamp,
                "page_id": row['author_id'],
                "fb_parent_id": row['post_id'],
                "parent_service_id": row['parent_service_id'],
                "sub_brand_service_id":0,
                "total_share": row['viewCount'], #Luong view
                "service_id": row['service_id'],
                "status_6":0,
                "content_id": row['post_id'],
                "content_updated": row['publishedAt']
            }
            print("Item saved Comment to MySQL && Elastic Search")

        # Prod
        es = Elasticsearch([{'host': settings['ES_HOST'], 'port': settings['ES_PORT']}])
        es_raw = Elasticsearch([{'host': settings['ES_HOST_RAW'], 'port': settings['ES_PORT_RAW']}])

        try:
            check_duplicate = es.exists(index=settings['ES_INDEX'], doc_type=settings['ES_TYPE'], id=idEs)
            # check_duplicate = False
            if check_duplicate == False:
                res = es.index(index=settings['ES_INDEX'], doc_type=settings['ES_TYPE'], id=idEs, body=doc)
                row_new = row
                self._set_raw(row_new)
                self.insert_key_to_redis(idEs)
                # SAVE DATA RAW
                check_duplicate_raw = self.es_raw.exists(index='twitter_raw', doc_type='filtered', id=doc['fb_id'])
                if check_duplicate_raw == False:
                    doc["brand_id"] = ""
                    doc["object_id"] = ""
                    doc["parent_object_id"] = ""
                    self.es_raw.index(index='twitter_raw', doc_type='filtered', id=doc['fb_id'], body=doc)
            else:
                print("[INFO] ITEM ALREADY EXISTS")

        except Exception:
            print("[INFO] ITEM ERROR")

    def mysql_close(self):
        self.cnx.close()
        
    def insert_key_to_redis(self, key):
        nano = self.redis_db.set(key,"exist")

        print ("================= SET =================")
        print ("=>>>>>>>>>>>> Key: " + key)
        print (nano)
        print ("=======================================")

    def _set_raw(self, data):
        sql = """INSERT INTO dlk_data_posts(post_id, author_id, author_name, tags, title, description, published, data, comments, keyword, type, parent, comment_id) VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        try:
            curr = self.cursor.execute(sql,(str(data['post_id']), str(data['author_id']), data['author_name'], data['tags'], data['title'], data['description'], data['publishedAt'], json.dumps(data['data']), data['comments'], data['keyword'], data['typePost'], data['parent'], data['comment_id']))
            self.conn.commit()
            print ("Save success to DB: "+str(data['post_id']))

        except Exception as e:
            print (e)
            print ("[EXCEPTION] exception in set raw !!!")