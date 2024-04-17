from crawldata.functions import random_user_agent

BOT_NAME = 'crawldata'
SPIDER_MODULES = ('crawldata.spiders',)
NEWSPIDER_MODULE = 'crawldata.spiders'
USER_AGENT = random_user_agent()

URLLENGTH_LIMIT = 50000
ROBOTSTXT_OBEY = False
HTTPERROR_ALLOW_ALL = True

# CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
TELNETCONSOLE_ENABLED = False

# # pip install scrapy-rotating-proxies
ROTATING_PROXY_LIST_PATH = '/home/hung/proxies.txt'
ROTATING_PROXY_PAGE_RETRY_TIMES=200
CONCURRENT_REQUESTS_PER_IP = 1

DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610, 
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

ITEM_PIPELINES = {
    # 'crawldata.pipelines.CrawldataPipeline': 300,
    'crawldata.pipelines.MongodbPipeline': 300,
    # 'crawldata.pipelines.SQLitePipeline': 300,
}

LOG_ENABLED = True
LOG_LEVEL = 'ERROR'
LOG_FORMAT = '%(levelname)s: %(message)s'

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'

MONGODB_URI = "mongodb://127.0.0.1:27017"
# MONGODB_DATABASE = "forex"
DATABASE_NAME = "pandascb"

# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# REDIS_URL = 'redis://127.0.0.1:6379'