__author__ = 'DuyLK'
# -*- coding: utf-8 -*-

import configparser
from scrapy.utils.project import get_project_settings
from datetime import datetime
from datetime import timedelta
import time
import mysql.connector
import os
from helper import Helper
settings = get_project_settings()

class DispatcherLibrary:
    def __init__(self, *args, **kwargs):
        self.process_id = os.getpid()
        self.limit = 10

    def mysqConnect(self):
        self.conn = mysql.connector.connect(user=settings['MYSQL_USERNAME'],
                                    passwd=settings['MYSQL_PASSWD'],
                                    db=settings['MYSQL_DB'],
                                    host=settings['MYSQL_HOST'],
                                    charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()


    def mysqlQuery(self, sql, params=()):
        try:
            self.mysqConnect()
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            # self.conn.commit()
        except mysql.connector.Error as e:
            print ('exception generated during sql connection: ', e)
            self.mysqConnect()
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
        return cursor

    def mysqlQuery_One(self, sql):
        try:
            self.mysqConnect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            # self.conn.commit()
        except mysql.connector.Error as e:
            print ('exception generated during sql connection: ', e)
            self.mysqConnect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
        return cursor

    def spider_open(self):
        print ('spider_open', self)

    def spider_close(self, reason):
        print ('spider_close', self)

    def getKeywords(self, id=''):
        if id != '':
            print ("Get ALL Keywords in Company")
            sql = """SELECT id, keyword, campaign, company_id, brand_id, object_id, service_id, parent_object_id, parent_service_id, status FROM dlk_data_keywords WHERE company_id = '%s' and status = 1 """
            curr = self.mysqlQuery(sql % id)
        else:
            print ("Get ALL Keywords")
            sql = """SELECT id, keyword, campaign, company_id, brand_id, object_id, service_id, parent_object_id, parent_service_id, status FROM dlk_data_keywords WHERE status = 1 """
            curr = self.mysqlQuery_One(sql)

        if curr :
            return curr.fetchall()
        else:
            return []

    def get_data_by_id(self):
        sql = """SELECT id, uid_post, username, brand_id, object_id, service_id, parent_object_id, parent_service_id, status FROM `dlk_data_by_ids` WHERE `status` = 0 """
        curr = self.mysqlQuery(sql)
        if curr:
            return curr.fetchall()
        else:
            return []

    def update_data_by_id(self, uid_post):
        try:
            sql = """UPDATE `dlk_data_by_ids` SET status = 1 WHERE `uid_post` = %s """
            curr = self.mysqlQuery(sql, (uid_post,))
            self.conn.commit()
            print ("UPDATE SUCCESS uid_post: " + uid_post)
        except Exception as e:
            print (e)
            print ("UPDATE ERROR")

    def get_data_by_user(self):
        sql = """SELECT id, uid, username, brand_id, object_id, service_id, parent_object_id, parent_service_id, status FROM `dlk_data_by_users` WHERE `status` = 1 """
        curr = self.mysqlQuery(sql)
        if curr:
            return curr.fetchall()
        else:
            return []


    def getUrlLeechByGroup(self, group, page):
        start = (page - 1) * self.limit
        sql = """SELECT id, domain_url, category_name, domain_name, domain_group, status, created, pay_position_1, pay_position_2, pay_position_3, pay_position_4, pay_position_5, pay_position_6 FROM web_url WHERE domain_group = %s AND status = 1 ORDER BY id DESC LIMIT %s,%s"""
        curr = self.mysqlQuery(sql,(group, start,self.limit))
        if curr :
            return curr.fetchall()
        else:
            return []

    def insertLog(self, action, message):
        current_time = time.time()
        try:
            sql = """INSERT INTO dlk_data_logs(action, message) VALUE (%s, %s)"""
            curr = self.mysqlQuery(sql,(action, message))
            self.conn.commit()
            print ("=>>>>>>>>>>>>> Save Log")
        except Exception as e:
            print (e)
            print ("[EXCEPTION] exception in save log")
