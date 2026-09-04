import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from deepwoken_scraper.items import DeepwokenItem


def _clean_text(fragments):
    """Join text-node fragments into one readable string.

    Handles the common case where inline tags (<a>, <b>, etc.) split a
    sentence into separate text nodes, e.g. ["Deepwoken", "."] -> "Deepwoken.",
    not "Deepwoken .".
    """
    text = " ".join(f.strip() for f in fragments if f.strip())
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([.,;:!?)\]])", r"\1", text)
    text = re.sub(r"([([\[]\s+", r"\1", text)
    return text.strip()


class DeepwokenSpider(CrawlSpider):
    """
    Crawls deepwoken.fandom.com starting from the wiki's main page and
    follows internal /wiki/ links, scraping every article it finds.

    Namespace pages (Special:, Category:, File:, Talk:, User:, Template:,
    Forum:, User_blog:, etc.) are excluded so we only collect real content
    articles.
    """

    name = "deepwoken"
    allowed_domains = ["deepwoken.fandom.com"]
    start_urls = ["https://deepwoken.fandom.com/wiki/Deepwoken_Wiki"]

    # Namespaces / paths we don't want to crawl or scrape.
    _DENY_PATTERNS = (
        r"/wiki/Special:",
        r"/wiki/File:",
        r"/wiki/Category:",
        r"/wiki/Talk:",
        r"/wiki/User:",
        r"/wiki/User_talk:",
        r"/wiki/Template:",
        r"/wiki/Template_talk:",
        r"/wiki/Forum:",
        r"/wiki/Board:",
        r"/wiki/User_blog:",
        r"/wiki/MediaWiki:",
        r"/wiki/Help:",
        r"/wiki/Map:",
        r"\?action=",
        r"/wiki/Local_Sitemap",
    )

    rules = (
        Rule(
            LinkExtractor(
                allow=(r"/wiki/",),
                deny=_DENY_PATTERNS,
                canonicalize=True,
                unique=True,
            ),
            callback="parse_item",
            follow=True,
        ),
    )

    custom_settings = {
        # Be a good citizen: identify ourselves and throttle requests.
        "USER_AGENT": "DeepwokenWikiBot/1.0 (+https://example.com/contact)",
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 1.0,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1.0,
        "AUTOTHROTTLE_MAX_DELAY": 10.0,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 2.0,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
        "HTTPCACHE_ENABLED": True,
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    def parse_item(self, response):
        # Fandom's UCP skin uses h1.page-header__title; older skins use #firstHeading.
        title = (
            response.css("h1.page-header__title::text").get()
            or response.css("#firstHeading::text").get()
            or response.css("#firstHeading *::text").get()
        )
        if not title:
            return  # not an article page (e.g. redirected to a non-content page)
        title = title.strip()

        # Skip pages that are really just redirects or missing content.
        content_root = response.css("div.mw-parser-output")
        if not content_root:
            return

        # Categories are listed at the bottom of the article in most skins,
        # and in a header block on the newer UCP skin.
        categories = response.css(
            ".page-header__categories a::text, "
            "#catlinks li a::text, "
            "div.category-page__title::text"
        ).getall()
        categories = [c.strip() for c in categories if c.strip()]
        # The header chips and the #catlinks footer both list the same visible
        # categories on Fandom's current skin, so dedupe while keeping order.
        categories = list(dict.fromkeys(categories))

        # Portable infobox key/value extraction.
        infobox = {}
        for group in response.css(".portable-infobox .pi-item.pi-data"):
            label = group.css(".pi-data-label::text").get()
            value = " ".join(
                t.strip() for t in group.css(".pi-data-value ::text").getall() if t.strip()
            )
            if label:
                infobox[label.strip()] = value

        # Full body text: walk direct-child <p>/<ul>/<ol> elements of
        # mw-parser-output (skipping infobox/table/navbox noise) and join each
        # element's own text into ONE line. Flattening all text nodes globally
        # (the original approach) breaks a single sentence like "The Trident is
        # a spear-type weapon in Deepwoken." into several fragments, one per
        # inline tag (<b>, <a>) -- so we group by block element instead.
        content_lines = []
        for node in content_root.css(":scope > p, :scope > ul, :scope > ol"):
            tag = node.root.tag
            if tag == "p":
                text = _clean_text(node.css("::text").getall())
                if text:
                    content_lines.append(text)
            else:  # ul / ol
                for li in node.css(":scope > li"):
                    text = _clean_text(li.css("::text").getall())
                    if text:
                        content_lines.append(f"- {text}")
        content_text = "\n".join(content_lines)

        summary = ""
        first_para = content_root.css(":scope > p")
        for p in first_para:
            text = _clean_text(p.css("::text").getall())
            if text:
                summary = text
                break

        last_revision = response.css(
            ".page-footer__timestamp::text, #footer-info-lastmod::text"
        ).get()

        item = DeepwokenItem(
            url=response.url,
            title=title,
            categories=categories,
            infobox=infobox,
            summary=summary,
            content=content_text,
            last_revision=(last_revision or "").strip(),
        )
        yield item
