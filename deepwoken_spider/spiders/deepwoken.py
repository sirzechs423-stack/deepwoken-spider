import scrapy

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
            yield response.follow(href, self.parse_article)

    def parse_article(self, response):
        title = response.css("h1::text").get()
        summary = response.css("p::text").get()
        yield {
            "url": response.url,
            "title": title,
            "summary": summary,
        }
