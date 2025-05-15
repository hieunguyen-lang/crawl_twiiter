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
    "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",
]