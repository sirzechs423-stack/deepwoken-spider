# Deepwoken Spider

A web scraper for the [Deepwoken Fandom Wiki](https://deepwoken.fandom.com) built with [Scrapy](https://scrapy.org).

## Overview

This spider crawls the Deepwoken Wiki starting from the main page and follows internal `/wiki/` links, scraping every article it finds. It intelligently excludes namespace pages (Special:, Category:, File:, Talk:, User:, Template:, Forum:, User_blog:, etc.) to collect only real content articles.

## Features

- **Smart crawling**: Follows internal wiki links while respecting namespace restrictions
- **Respectful scraping**: Implements rate limiting and automatic throttling
- **Rich data extraction**:
  - Article title and URL
  - Content text with proper formatting
  - Categories
  - Infobox data (key-value pairs)
  - Article summary (first paragraph)
  - Last revision timestamp

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sirzechs423-stack/deepwoken-spider.git
   cd deepwoken-spider
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the spider:

```bash
scrapy crawl deepwoken -o output.json
```

This will crawl the wiki and export the scraped data to `output.json`.

## Configuration

The spider includes several custom settings for respectful crawling:

- **USER_AGENT**: Identifies the bot and provides contact information
- **ROBOTSTXT_OBEY**: Respects the site's robots.txt
- **DOWNLOAD_DELAY**: 1 second delay between requests
- **AUTOTHROTTLE**: Automatically adjusts request rate based on server load
- **CONCURRENT_REQUESTS_PER_DOMAIN**: Limited to 4 concurrent requests
- **HTTPCACHE**: Caches responses to avoid re-downloading

## Output Format

Each scraped article yields an item with the following fields:

```json
{
  "url": "https://deepwoken.fandom.com/wiki/ArticleName",
  "title": "Article Title",
  "categories": ["Category1", "Category2"],
  "infobox": {
    "Field1": "Value1",
    "Field2": "Value2"
  },
  "summary": "First paragraph of the article...",
  "content": "Full article text with proper formatting...",
  "last_revision": "Timestamp of last edit"
}
```

## Text Cleaning

The `_clean_text()` function handles common web scraping issues:
- Joins fragmented text nodes from inline HTML tags
- Removes excessive whitespace
- Properly formats punctuation (no space before periods, commas, etc.)
- Handles brackets and parentheses correctly

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

This project is open source and available under the MIT License.
