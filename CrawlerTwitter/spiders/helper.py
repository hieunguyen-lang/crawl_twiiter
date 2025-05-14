# -*- coding: utf-8 -*-
__author__ = 'DuyLK'


# //
# //                            _
# //                         _ooOoo_
# //                        o8888888o
# //                        88" . "88
# //                        (| -_- |)
# //                        O\  =  /O
# //                     ____/`---'\____
# //                   .'  \\|     |//  `.
# //                  /  \\|||  :  |||//  \
# //                 /  _||||| -:- |||||_  \
# //                 |   | \\\  -  /'| |   |
# //                 | \_|  `\`---'//  |_/ |
# //                 \  .-\__ `-. -'__/-.  /
# //               ___`. .'  /--.--\  `. .'___
# //            ."" '<  `.___\_<|>_/___.' _> \"".
# //           | | :  `- \`. ;`. _/; .'/ /  .' ; |
# //           \  \ `-.   \_\_`. _.'_/_/  -' _.' /
# // ===========`-.`___`-.__\ \___  /__.-'_.'_.-'================



from datetime import datetime,date
import time
import os
from datetime import timedelta
import calendar
import unidecode
import re
import requests
import json
from CrawlerTwitter.helper import HelperKeys
from CrawlerTwitter.items import CrawlerTwitterItem

class Helper:
    def __init__(self, *args, **kwargs):
        self.DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        self.DATE_REGEX =   '\d+/\d+/\d+'
        self.TIME_REGEX = '\d+:\d+'
        self.filepath = os.getcwd()
        getAllKeyLimit = json.load(open(self.filepath + '/CrawlerTwitter/key.json'))
        self.arrKeysLimit = [str(i) for i in getAllKeyLimit]
        self.arrKeys = HelperKeys.ApiKeyHelper.key
        #Telegram Config
        self.bot_token = '1373128266:AAGLzdOlNKAx8TK31XfKzW6Od2mgemsc0Yc'
        self.bot_chatID = '-472318322'

    def getServerVersion(self):
        return "SV01"

    def _join_data(self, separator=None, data=None):
        if(separator != None and data != None):
            if len(data) > 0:
                s = data[0]
                for i in range(1, len(data)):
                    if(data[i]):
                        words = data[i].strip().split(" ")
                        if len(words) > 15:
                            s = s + " <br><br> " + data[i] 
                        else:
                            s = s + separator + data[i].strip()
                s=re.sub(r"(<br>){2,}", " <br><br> ",s)
                s=re.sub(r"\s{2,}", " ",s)
                return s
        return ''

    def _to_dict(self, data):
        d = {}
        if(len(data) > 0):
            for i in range(0, len(data)):
                d[i] = data[i]
        return d

    def getItem(self):
        item = CrawleryoutubeItem()
        item['video_id'] = ""
        item['url'] = ""
        item['channel_id'] = ""
        item['title'] = ""
        item['description'] = ""
        item['publishedAt'] = ""
        item['tags'] = ""
        item['author_id'] = ""
        item['author_name'] = ""
        item['author_username'] = ""
        item['data'] = ""
        item['comments'] = ""
        item['keyword'] = ""
        item['company'] = ""
        item['typePost'] = ""
        item['parent'] = ""
        item['timeCreated'] = ""
        item['comment_id'] = ""
        item['likeCount'] = ""
        item['commentCount'] = ""
        item['profileImage'] = ""
        item['viewCount'] = ""

        return item


    def format_classic(self,input_str):
        # dateformat example: 20/11/2016
        # time format: 15:00
        input_str = input_str.strip()
        try:
            date_rex = "\d+/\d+/\d+"
            time_rex = "\d+:\d+"
            date_str = re.findall(date_rex,input_str)[0]
            time_str = re.findall(time_rex,input_str)[0]
            stripped = time_str + " " + date_str
            return datetime.strptime(stripped, "%H:%M %d/%m/%Y").strftime(self.DATETIME_FORMAT)
        except Exception:
            print "[EXCEPTION] datetime converting exception, classic1 prototype datetime parsing"
            return datetime.today().strftime(self.DATETIME_FORMAT)

    def format_time(self, input_str):
        #sample string : "2020-12-22T10:59:53+07:00"
        input_str = str(unidecode.unidecode(input_str)).strip()
        print "------------------------------"
        print "Time in: "+input_str
        try:
            date_rex = "\d+-\d+-\d+"
            time_rex = "\d+:\d+:\d+"
            date_str = re.findall(date_rex,input_str)[0]
            time_str = re.findall(time_rex,input_str)[0]
            stripped = time_str + " " + date_str
            print "Time out: "+stripped
            return datetime.strptime(stripped, "%H:%M:%S %Y-%m-%d").strftime(self.DATETIME_FORMAT)
        except Exception:
            # print "[EXCEPTION] datetime converting exception, Not format: 2020-12-22T10:59:53+07:00 "
            try:
                # sample string : "1 gio truoc", "1 ngay truoc"
                stamp = None
                if "phut truoc" in input_str:
                    string = input_str.replace(" phut truoc","")
                    m = int(string)
                    stamp = str(datetime.now() + timedelta(minutes=-m))
                if "gio truoc" in input_str:
                    string = input_str.replace(" gio truoc","")
                    h = int(string)
                    stamp = str(datetime.now() + timedelta(hours=-h))
                if "ngay" in input_str:
                    string = input_str.replace(" ngay truoc","")
                    d = int(string)
                    stamp = str(datetime.now() + timedelta(days=-d))
                if stamp != None:
                    print stamp
                    date_rex = "\d+-\d+-\d+"
                    time_rex = "\d+:\d+:\d+"
                    date_str = re.findall(date_rex,stamp)[0]
                    time_str = re.findall(time_rex,stamp)[0]
                    stripped = time_str + " " + date_str
                    print "Time out: "+datetime.strptime(stripped, "%H:%M:%S %Y-%m-%d").strftime(self.DATETIME_FORMAT)
                    return datetime.strptime(stripped, "%H:%M:%S %Y-%m-%d").strftime(self.DATETIME_FORMAT)
                else:
                    print "[EXCEPTION] datetime converting exception, Format Fail"
                    print "Time out: "+datetime.today().strftime(self.DATETIME_FORMAT)
                    return datetime.today().strftime(self.DATETIME_FORMAT)
            except Exception:
                print "[EXCEPTION] datetime converting exception, None Imput String"
                print "Time out: "+datetime.today().strftime(self.DATETIME_FORMAT)
                return datetime.today().strftime(self.DATETIME_FORMAT)

    #Remove Key Limit
    def removeKeyLimit(self, key):
        print "Remove Key Limit"
        # print self.arrKeys
        # print self.arrKeysLimit
        if key in self.arrKeys:
            self.arrKeys.remove(key)
            self.arrKeysLimit.append(key)
            temp_path = self.filepath + '/' + 'CrawlerTwitter' + '/' + 'helper.py'
            temp_path_key_limit = self.filepath + '/' + 'CrawlerTwitter' + '/' +'/key.json'

            # Check Leng Arr Key Active
            if len(self.arrKeys) > 0:
                keys = ", \n\t\t\t".join(str("'" + x + "'") for x in self.arrKeys)
            else:
                keys = ''
                print('Empty Youtube API Key!')
                print('---------*0*----------')

            # Check Leng Arr Key Die
            if len(self.arrKeysLimit) > 0:
                keys_limit = ", \n\t".join(str('"' + x + '"') for x in self.arrKeysLimit)
            else:
                keys_limit = ''
                print('Empty Key Limit!')
                print('---------*0*----------')

            #Remove helper
            file = open(temp_path, 'w')
            file.write('''
# -*- coding: utf-8 -*-
__author__ = 'DuyLK'

class HelperKeys():
    class ApiKeyHelper():
        key = [
            '''+keys+''' 
        ]
''')
            file.close()

            #Add Key Limit to Keys.json
            file = open(temp_path_key_limit, 'w')
            file.write('''
[
    '''+keys_limit+'''
]
''')
            file.close()
            print('Update Key Success!')
        else:
            print ('Key not in Array')

    def sendTelegram(self, urls=[]):
        print '=>>>>>>>>>>>Send Telegram!'
        dataUrlText = ''
        for url in urls:
            dataUrlText += "\n -"+url +"\n"

        bot_message = " \n Date: "+str(datetime.now())+" \n New item count: "+str(len(urls))+" \n List Urls New:"+dataUrlText+" \n --------------------------------------------------------------------"
        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        print '[Crawler Youtube Notification] =>>>>>>>>>>>Send Telegram Success!'

    def sendMessageTelegram(self, message):
        print '=>>>>>>>>>>>Send Message Telegram!'
        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.bot_chatID + '&parse_mode=Markdown&text=' + message
        response = requests.get(send_text)
        print '[Crawler Youtube Notification] =>>>>>>>>>>>Send Telegram Success!'


    def getDataFormUrl(self, url):
        print '=>>>>>>>>>>>Get Data Form URL!'
        url_request = "http://123.30.186.133:5000/api/v1/resources?url="+url
        response = requests.get(url_request)
        return response.content