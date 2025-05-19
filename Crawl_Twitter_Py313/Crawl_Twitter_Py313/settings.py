# Scrapy settings for Crawl_Twitter_Py313 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "Crawl_Twitter_Py313"

SPIDER_MODULES = ["Crawl_Twitter_Py313.spiders"]
NEWSPIDER_MODULE = "Crawl_Twitter_Py313.spiders"

ADDONS = {}

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
]


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "Crawl_Twitter_Py313 (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   "Crawl_Twitter_Py313.middlewares.CrawlTwitterPy313SpiderMiddleware": 543,
}
URLLENGTH_LIMIT = 0
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "Crawl_Twitter_Py313.middlewares.CrawlTwitterPy313DownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "Crawl_Twitter_Py313.pipelines.CrawlTwitterPy313Pipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
KEY =[
    "HzC0o6dVjghXa9cgf8e9x/jdyTYmrg8qA6gcnZIZaLwgx3sP/o+VPoy+5pPbm1durHN6xBwr4w432i6aL10TKviopASLHA",
    "i0dihp9IZPe2mTkEVNHZLlKq63EI5W88CvE1AQHVZ38x6gjtjusLfJSx4JCqVtp0jfjuUIjqoCgiLjyAMnJqtdsbhITiiA",
    "xwnSap59d+TX7UjRdBEf0FllFNoPOj3WhvHSFGZ1pQyaAyTvBBZrg/Zou5tgfs9Oa76iHMQdqbCQ/Ywh67nS/PJD9R5VxA",
    "jF+/gmFh0NlAHvkTjr+GAvaDB5284vWq77QS+eRJoSA5wKljzdoOUX3ktCsu7kCnqwzpV4+OXxAyevB2Coz7b2vTEqK1jw",
    "a8krkUlLdg6MDqvLpCrG2N7tDWKKi5T7siRmeDW1rgRRCNTediKUX56HyYYRMivHWe0OsGhoqPNuYiajQPCOL/itWC64aA",
    "kwwGfklkvEY+E3e0pgrYEwKmcOVo17rUjikoTAxoOsk+Nui50M8ELZFgGeJP736rLx/2SJCgj/bYxwID3Gk0KQ69KraZkA",
    "OhmnXLV5X/1MkQg8PpQnr5lTnwGT2JJkXgT03Ba4yGqoLhuG0BQg3SujMLdBDsJZlqlf4TlevcMYwXpnEVIaXrpHsmnkOQ",
    "BZvbYbwlhObjNs2ZGzdoqlYdDphkDGNLPP+UQ/xJko4JX0lGAq7h0VwYAP0q6wM2KZxg3ga3O1JIxTETGWhFRYBLpWkHBg",
    "55vazW5/rwS+5rcorL7ux3hKhKfUQ/C0OuCRHDsDJYZVUUzt/z5/iRAQS9xEGn7tkUeCPOSv6NMIilbGUUJXCCdYz8VS5A",
    "P3DYTy3InKOP9Ja/+DkfV0SGwnfmSVPmlC4SuOuWkw2ojNou/XebRlAMFS2IckEvupha5DxynbFKIakzPHC9jixi7mrQPA",
    "8YwO13LUcpD/WPI1qWr6PJdyVDjsOto++eaXYqTJU87H9br88cb+Tf5fmQ8vYwMHO12UKvJPTtrdAySlP7nyyf/cCR0L8g",
    "mWyY6AlTkEdH/vCnk7tUpaDxwRsAD+LPuHIa4e2ea38wbwTEs6IQN+saSMwzrogbzyr8QprfwoXSg8irZYp4aiayAeNDmg",
    "1Ivlho1/d0zYC1ueH2eJs0qPmUk0xD4zHievbBQJ8SIKVcFjSqf2SDC83NC5WdwhBG2xD9eCbRDA1UUQQilHaNSWVT7G1w",
    "ENjz/f1cXP9v3NZGtEQwRsWPenv+tmR7TzEj4C9CpRLPOJ9YakWez1nQMX0uVwuLPK51yxMSgVzBMoz7BqgrqZe4PcVLEw",
    "YNGPCay+ackv5dePiv8UfzveY1AMuVknBfWiGXlm4cD2fWdaibUcpJv7sx6bB0aYV6UFu2PUc5I0uFXO9/F/7+m9InbFYw",
    "o1jdOWuxh2kvZnaKB7UMd/8e7EXWcELdJdxcU9VJyK5gd8AZ0nfno40lgR+JHOJqLGrGeKD5+AUPDoeizIW81PXeteVXoA",
    "+d2Se/SlEbNjkJGVjUtMx5EPsV76oVAeXrDQwH+sgBKfJ6FVUKMlcGDan5vYTohg5zacIvqM0a0GVOIWQF4DRPKvxuEq+g",
    "hj+PpcXMfpsYzwIcJlZwGl3Wo+dwCsb7noCuOgQ5f1CcfWdP3gfjPqe5zHohJIbDK1LjXYXLKWqCB0plikaOOCdQQnpChQ",
    "p4qLIv3gz94EzeixIZLG3RSFB/w4FfFN2IKoZVAgxKuaYESYBYs2BIWf0DDMIojCAH3CfKSj7ojWBBSWp00B1wT1lOH2pA",
    "YO+hnRLalIXSKeuD4PPd1QInVA0yg4pEwtnTKleg0B7I9mhLskptfl0jq9gT6ULz578Fu2NuhFhKkROm3W6nHNqgshOsYw",
    "x5M++Ans8NojK/v3+mDVbiLUoOKTKVuZQjQjx0eNRvl0Vs2U4sgUYo7YcUVjPW5tECKiHMSPD0LGQrHlOrUXlz/O0KydxA",
    "8e++ztHYgDZgutRb6SNMUddfQjmwI8MWQ2fHrPoZxDRkc8oEQdCwSyoK3nek6Q6p0BuUKvJ3prc67Qw5mmDVHN3FrMLa8g",
    "FG997lDo9ue0/EYKl72UeiXE4WZgEXL5rorb8/df+IvxvhR7mGyPZgiqGAnFYcpA7ORxzxeHO9XfRAjmyggDLlYyEHtMFw",
    "+5xTAz7Km82kPP9raZqj+xqQwPjs1fPZ4T2X2BxRCTuHdRwYatnvGr2JLBd7GVvgfg6eIPiNP+p7e++dFVgKnZuFf5KU+A",
    "tYp6M9AqT7UFYEUR9paQdBcz6zWWduKUp25Z5elr8bOiTFYkn5kOUn9p2cjtp3TQzk7QbrYHHrqVv+Z8W2wVdI96oIcutg",
    "nnfoap7TgCsufAOW/PAYjMIjvLW5QkpMDAQqFjHv7VNIUT8ky2PULzeXIDopDnqhRZ74RZ2p0UoDmqYAxxtKJmZCNOgjnQ",
    "CDQGa64LqR+rcGWOsTLZZrXqtmINQslM5LEJhqrac5+ITJyrZSXpJ7RLDbO8V2jkqQ5u0wsaGzZK6PhFI1e68YWg4VRVCw",
    "PeR5LggObL85sppWLew7HmgXcpqU+mu4evZNt4olVkzhbstJ5XxlvM/wr1tGqFeQfjZb5j7XZjQIvvd4HzSauBPw8IacPg",
    "f3ZzYo/HSUu1y2mXT+Fb1wVTK/DpSKutH4d0xOv489CuQqk+XRWEFt+NCHIE/N3+rG8ZpHwxVQNvmhxX585dq/sofZoEfA",
    "GV3CqVO9LHkxG3ZuKKBE/rY1T2xvukS/m5pQQQ3H/EJmQHm8gTRWX7Jm9o0BghXF4g9/whp/b8GQ95ZjXQ9/L55Z1hjCGg"
]