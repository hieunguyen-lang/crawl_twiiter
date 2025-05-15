# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import random
import requests
from scrapy.utils.project import get_project_settings
settings = get_project_settings()    
class CrawlTwitterPy313SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class CrawlTwitterPy313DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class RandomUserAgentMiddleware(object):
    def process_request(self, request,spider):
        userAgent = random.choice(settings['USER_AGENT_LIST'])
        if userAgent:
            request.headers.setdefault("User-Agent", userAgent)
            request.headers['User-Agent']=userAgent
        else:
            request.headers.setdefault("User-Agent",settings['USER_AGENT_LIST'][0])
            request.headers['User-Agent']=settings['USER_AGENT_LIST'][0]
class RotateCookieMiddleware:
    def __init__(self):
        
        self.request_count = 0
        self.current_index = 0
        self.change_every = 10  # sá»‘ request sau Ä‘Ã³ Ä‘á»•i
        self.current_token_guest = "1922108278525591995"
    def get_guest_token(self):
        headers={
                "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
            }
        response = requests.post("https://api.twitter.com/1.1/guest/activate.json",headers=headers)
        print(response.status_code)
        return response
    def process_request(self, request, spider):
        # Äá»•i token request láº§n Ä‘áº§u tiÃªn
        if self.request_count ==0:
            response =self.get_guest_token()
            if response.status_code == 200:
                res = json.loads(response.text)
                self.current_token_guest = str(res["guest_token"])
                print("Guest token: " +self.current_token_guest)
        self.request_count += 1
        
        # Äá»•i cookie sau má»—i N request
        if self.request_count % self.change_every == 0:
            # self.current_index = (self.current_index + 1) % len(self.cookies_list)
            response =self.get_guest_token()
            if response.status_code == 200:
                    
                    res = json.loads(response.text)
                    self.current_token_guest = str(res["guest_token"])
                    print("Guest token: " +self.current_token_guest)
        
            
        cookie_info = {
                "headers": {
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                    "content-type": "application/json",
                    "x-guest-token": self.current_token_guest,
                    "origin": "https://x.com",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-dest": "empty"
                },
                "cookies": {}
            }
        request.headers.update(cookie_info['headers'])
        request.cookies = cookie_info['cookies']

        return None


class Rotate_Trans_Clien_Id_SearchMiddleware:
    def __init__(self):
        # Danh sách các user-agent
        self.List_X_Client_Key = settings['KEY']
        # Đảm bảo chỉ số bắt đầu từ 0
        self.current_x_client_key = 0

    def process_request(self, request, spider):
        # Lấy user-agent theo chỉ số hiện tại
        x_client_key = self.List_X_Client_Key[self.current_x_client_key]
        print("Using x-client-transaction-id:" + x_client_key)
        cookie_info = {
                "headers": {
                "accept": "*/*",
                "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
                "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                "content-type": "application/json",
                "dnt": "1",
                "priority": "u=1, i",
                "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                "x-client-transaction-id": x_client_key,
                "x-client-uuid": "99c4895d-141a-48a8-8a5b-344e56cd76f1",
                "x-csrf-token": "9f5f4c079e7f555653aefe6496f10c467dc043c3784ce2814b2d7f6da9e8ba73f0e47f8f21e144a100ecf0dbe234b94ad600708a88b55df44acc044c9d87342b9ec046b62b7c7e49fbb4e4955abbbe0f",
                "x-twitter-active-user": "yes",
                "x-twitter-auth-type": "OAuth2Session",
                "x-twitter-client-language": "en"
            },
                "cookies": {
                "_ga": "GA1.2.931018832.1736396588",
                "_ga_KEWZ1G5MB3": "GS1.2.1736396588.1.0.1736396588.60.0.0",
                "guest_id": "173691187390724780",
                "night_mode": "2",
                "guest_id_marketing": "v1%3A173691187390724780",
                "guest_id_ads": "v1%3A173691187390724780",
                "g_state": "{\"i_l\":0}",
                "kdt": "xNAnvGRG00ld5bHzS52Bw0vjbzuJaI6v83rOU58n",
                "__cf_bm": "12QDKLXslRqAVtSsNoHA5jlEE3W0EkvXgLCx6.jL7rU-1745490230-1.0.1.1-go9b2iVoWHeZcnoHvNXnKTMoUqof.RQY0TVOF1hZfFRs7aKwn5qkxBkeE39NHeCmuWUthwCjUtJAg9j39ra.EQRztzWB3xtoo8Q8ifpbbJU",
                "personalization_id": "\"v1_tmFgnymYmrYHYlkn9dwn2g==\"",
                "gt": "1915350966121226286",
                "external_referer": "padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D",
                "auth_token": "c63738f7fed343378353c20d5973fa768ff12f8d",
                "ct0": "9f5f4c079e7f555653aefe6496f10c467dc043c3784ce2814b2d7f6da9e8ba73f0e47f8f21e144a100ecf0dbe234b94ad600708a88b55df44acc044c9d87342b9ec046b62b7c7e49fbb4e4955abbbe0f",
                "lang": "en",
                "twid": "u%3D1915351017878925312"
            }
            }
        request.headers.update(cookie_info['headers'])
        request.cookies = cookie_info['cookies']

        
        # Cập nhật chỉ số user-agent cho lần tiếp theo
        self.current_x_client_key = (self.current_x_client_key + 1) % len(self.List_X_Client_Key)
        return None
