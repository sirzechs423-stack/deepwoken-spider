# Scrapy settings for deepwoken_spider project

BOT_NAME = "deepwoken_spider"

SPIDER_MODULES = ["deepwoken_spider.spiders"]
NEWSPIDER_MODULE = "deepwoken_spider.spiders"

# Identification: use a realistic browser UA to reduce blocking
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"

# Default request headers to mimic a real browser
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://deepwoken.fandom.com/",
    "Connection": "keep-alive",
}

# Respect robots.txt
ROBOTSTXT_OBEY = True

# Cookies
COOKIES_ENABLED = True

# Concurrency & polite crawling
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# Auto-throttle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10

# HTTP cache
HTTPCACHE_ENABLED = True

# Retry settings (include 403 optionally; use with care)
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 403]

# Logging
LOG_LEVEL = "INFO"

# NOTE: Splash integration is disabled by default because of compatibility issues
# with some Scrapy versions. If you need JS rendering, consider migrating to
# scrapy-playwright or pinning compatible scrapy/scrapy-splash versions.
