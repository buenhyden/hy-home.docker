---
trigger: always_on
glob: "**/*.py"
description: "Selenium: Web Scraping and Automation Best Practices."
---
# Selenium Standards

## 1. Robustness

- **Explicit Waits**: ALWAYS use `WebDriverWait` with `expected_conditions` (EC). NEVER use `time.sleep()`.
- **Locators**: Prefer CSS Selectors or ID/TestID over XPath (unless necessary for text matching).

### Example: Explicit Wait

**Good**

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "myDynamicElement"))
)
```

**Bad**

```python
import time
time.sleep(5) # Flaky!
driver.find_element(By.ID, "myDynamicElement")
```

## 2. Driver Management

- **Context Manager**: Use a context manager/try-finally block to ensure `driver.quit()` is called.
- **Headless**: Run in headless mode (`--headless`) for CI/CD or server-side execution.
- **Options**: Configure options (User-Agent, window size) to mimic real users and avoid bot detection checks (e.g., `blink-settings=imagesEnabled=false` for speed).

## 3. Page Object Model (POM)

- **Abstraction**: For complex projects, use POM. Create classes representing pages (e.g., `LoginPage`) with methods for interactions (`login()`), separating logic from locators.
