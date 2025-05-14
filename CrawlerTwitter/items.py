# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerTwitterItem(scrapy.Item):

    # define the fields for your item here like:
    post_id = scrapy.Field()
    url = scrapy.Field()
    brand_id = scrapy.Field()
    object_id = scrapy.Field()
    service_id = scrapy.Field()
    parent_object_id = scrapy.Field()
    parent_service_id = scrapy.Field()
    channel_id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    publishedAt = scrapy.Field()
    tags = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_username = scrapy.Field()
    data = scrapy.Field()
    comments = scrapy.Field()
    keyword = scrapy.Field()
    company = scrapy.Field()
    typePost = scrapy.Field()
    parent = scrapy.Field()
    timeCreated = scrapy.Field()
    comment_id = scrapy.Field()
    likeCount = scrapy.Field()
    commentCount = scrapy.Field()
    profileImage = scrapy.Field()
    viewCount =  scrapy.Field()
