---
trigger: always_on
glob: "**/*.py,**/*.js"
description: "Web Scraping: Resilience, Ethics, Legal, and Headless Browsers."
---
# Web Scraping Standards

## 1. Resilience

- **Selectors**: Attribute-based (`[data-testid="price"]`) > Structural (`div > div > span`).
- **Retries**: Exponential backoff on 5xx or Network errors.

### Example: Selectors

**Good**

```python
soup.select_one('h1.product-title')
```

**Bad**

```python
soup.select_one('body > div:nth-child(2) > h1') // Breaks on layout shift
```

## 2. Ethics

- **Rate Limiting**: Random sleep intervals (1-5s) between requests.
- **Identification**: Set User-Agent to identify your bot with contact info.

### Example: User-Agent

**Good**

```python
headers = {'User-Agent': 'MyBot/1.0 (+https://mysite.com/bot)'}
```

**Bad**

```python
headers = {'User-Agent': 'Mozilla/5.0 ...'} // Spoofing browser
```

## 3. Legal Compliance

- **robots.txt**: Respect `Disallow` directives.
- **ToS**: Check Terms of Service before scraping.
- **Rate**: Respect `Crawl-delay` if present.

### Example: robots.txt

**Good**
> Check `https://example.com/robots.txt` before scraping `/api/` paths.

**Bad**
> Ignoring robots.txt completely.
