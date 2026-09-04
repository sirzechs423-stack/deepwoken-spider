import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

class DeepwokenSpider(scrapy.Spider):
    name = "deepwoken"
    allowed_domains = ["deepwoken.fandom.com"]
    start_urls = ["https://deepwoken.fandom.com/wiki/Main_Page"]

    def parse(self, response):
        # follow internal /wiki/ links but skip common namespaces
        for href in response.css("a[href^='/wiki/']::attr(href)").getall():
            # skip namespace links like Special:, Category:, File:, Help:, Talk:
            if any(href.startswith(f"/wiki/{ns}:") for ns in ("Special", "Category", "File", "Help", "Talk")):
                continue
            # use errback to capture network/parsing failures and log them
            yield response.follow(href, callback=self.parse_article, errback=self.errback)

    def parse_article(self, response):
        try:
            title = response.css("h1::text").get()
            summary = response.css("p::text").get()
            yield {
                "url": response.url,
                "title": title,
                "summary": summary,
            }
        except Exception:
            self.logger.exception("Unhandled exception parsing %s", response.url)

    def errback(self, failure):
        # log full failure for debugging
        self.logger.error(repr(failure))

        # in case you want to handle specific failure types
        if failure.check(HttpError):
            # HttpError is raised for non-200 responses
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
