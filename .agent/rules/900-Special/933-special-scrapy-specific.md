---
trigger: always_on
glob: "**/*.py"
description: "Scrapy: High-level Web Crawling Framework Standards."
---
# Scrapy Framework Standards

## 1. Project Structure

- **Items**: Define data structures in `items.py` to enforce schema.
- **Spiders**: Keep spiders focused. Use separate spiders for different domains.
- **Pipelines**: Use pipelines for cleaning, validation, and storage (DB, JSON).

## 2. Robustness

- **Politeness**: Set `DOWNLOAD_DELAY` and `CONCURRENT_REQUESTS_PER_DOMAIN` in `settings.py` to respect target servers.
- **Retries**: Configure `RETRY_ENABLED` and `RETRY_TIMES` for transient network errors.
- **AutoThrottle**: Enable `AUTOTHROTTLE_ENABLED` for dynamic adjustment of scraping speed.

### Example: Settings

**Good**

```python
# settings.py
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1.0
AUTOTHROTTLE_ENABLED = True
```

## 3. Data Processing

- **Item Loaders**: Use `ItemLoader` and input/output processors (e.g., `TakeFirst`, `MapCompose`) for clean data extraction logic within the Spider.

### Example: Item Loader

**Good**

```python
l = ItemLoader(item=Product(), response=response)
l.add_css('name', 'h1.title::text')
l.add_css('price', '.price::text', MapCompose(lambda x: x.replace('$', '')))
return l.load_item()
```
