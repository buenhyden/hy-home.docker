---
trigger: always_on
glob: "**/*.js,**/*.ts"
description: "Puppeteer: Headless Browser Automation Guidelines."
---
# Puppeteer Standards

## 1. Selectors and Waiting

- **Robust Locators**: Use `page.waitForSelector()` before interacting.
- **Async/Await**: Ensure all Puppeteer actions are awaited.

### Example: Waiting

**Good**

```javascript
await page.waitForSelector('.submit-btn');
await page.click('.submit-btn');
```

**Bad**

```javascript
// Race condition risk
page.click('.submit-btn');
```

## 2. Performance

- **Resource Blocking**: Block unnecessary resources (images, fonts, stylesheets) using `page.setRequestInterception(true)` to speed up scraping.
- **Parallelization**: limits concurrency (e.g., with `puppeteer-cluster`) to avoid CPU/Memory exhaustion.

## 3. Anti-Detection

- **Stealth**: Use `puppeteer-extra-plugin-stealth` to evade standard bot detection.
- **Randomization**: Randomize user-agent and add slight delays between actions if needed.

## 4. Resource Management

- **Browser Contexts**: Use Incognito contexts (`browser.createIncognitoBrowserContext()`) for isolation between tasks.
- **Cleanup**: Always ensure `browser.close()` is called in a `finally` block.
