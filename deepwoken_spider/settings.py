# Scrapy settings for deepwoken_spider project

BOT_NAME = "deepwoken_spider"

SPIDER_MODULES = ["deepwoken_spider.spiders"]
NEWSPIDER_MODULE = "deepwoken_spider.spiders"

# Identification
USER_AGENT = "deepwoken-spider (+https://github.com/sirzechs423-stack/deepwoken-spider)"
ROBOTSTXT_OBEY = True

# Concurrency & polite crawling
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# Auto-throttle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10

# HTTP cache
HTTPCACHE_ENABLED = True

# If you use scrapy-splash, keep these. Remove if not using Splash.
SPLASH_URL = "http://localhost:8050"
DOWNLOADER_MIDDLEWARES = {
    "scrapy_splash.SplashCookiesMiddleware": 723,
    "scrapy_splash.SplashMiddleware": 725,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
}
DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"
HTTPCACHE_STORAGE = "scrapy_splash.SplashAwareFSCacheStorage"
