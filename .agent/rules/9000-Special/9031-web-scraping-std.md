---
trigger: always_on
glob: "**/*.{py,js,ts}"
description: "Web Scraping Standards: Enforces resilient selectors, ethical rate limiting, and tool-specific best practices (Selenium, Puppeteer, BS4)."
---

# Web Scraping Standards

- **Role**: Data Extraction Engineer
- **Purpose**: Define standards for resilient, ethical, and performant web scraping across multiple language ecosystems (Python/Node.js).
- **Activates When**: Developing scrapers, crawlers, or automation scripts targeting web assets.

**Trigger**: always_on — Apply during the design and execution of data extraction tasks.

## 1. Standards

### Principles

- **[REQ-SCRAPE-01] Resilience via Selectors**
  - Scrapers MUST prioritize attribute-based selectors (e.g., `[data-testid]`) over structural XPath/CSS to withstand layout changes.
- **[REQ-SCRAPE-02] Ethical Identification**
  - Bot agents MUST set a descriptive `User-Agent` that provides identification and contact information.
- **[REQ-SCRAPE-03] Adaptive Backoff**
  - Extraction pipelines MUST utilize exponential backoff for network or server-side (5xx) errors.

### Tool recommendations

| Library | Use Case | Standard |
| --- | --- | --- |
| BeautifulSoup4 | Static HTML | Fast / Lightweight |
| Selenium | Dynamic UI | Robust / Heavy |
| Puppeteer | Headless Chrome | Modern / Performant |
| Scrapy | Large-Scale Crawling | Professional Framework |

### Must

- **[REQ-SCRAPE-04] Explicit Waiting**
  - Dynamic scrapers MUST use explicit wait conditions (e.g., `WebDriverWait`) instead of arbitrary sleep timers.
- **[REQ-SCRAPE-05] Rate Limiting**
  - All automated requests MUST include random jitter (1-5s) to mitigate server-side load and detection.
- **[REQ-SCRAPE-06] robots.txt Compliance**
  - Bot logic MUST check and respect the `robots.txt` and `Crawl-delay` directives of the target domain.

### Must Not

- **[BAN-SCRAPE-01] Blind Sleep**
  - The use of `time.sleep()` for flow control in dynamic scrapers is PROHIBITED (use EC waits).
- **[BAN-SCRAPE-02] Unchecked Elements**
  - Scrapers MUST NOT attempt to access element attributes without first verifying the element's existence.

### Failure Handling

- **Stop Condition**: Stop crawling if the target domain returns repeated 403 (Forbidden) or 429 (Too Many Requests) errors.

## 2. Procedures

- **[PROC-SCRAPE-01] Resilience Testing**
  - IF a target site undergoes a layout change THEN MUST re-verify all attribute-based selectors against the new DOM.
- **[PROC-SCRAPE-02] Compliance Check**
  - Perform a quarterly audit of scrapers to ensure they align with the target site's latest Terms of Service.

## 3. Examples

### Explicit Wait (Python Selenium)

```python
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='content']"))
)
```

## 4. Validation Criteria

- **[VAL-SCRAPE-01] Selector Robustness**
  - [ ] Scraper survives a change in non-target wrapping `<div>` elements.
- **[VAL-SCRAPE-02] Ethical Header Audit**
  - [ ] `User-Agent` string contains the project name and a contact URL.
- **[VAL-SCRAPE-03] Error Resilience**
  - [ ] Log evidence shows successful retry/backoff during transient network failures.
