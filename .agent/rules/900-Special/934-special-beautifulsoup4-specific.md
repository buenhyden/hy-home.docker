---
trigger: always_on
glob: "**/*.py"
description: "BeautifulSoup4: HTML Parsing Standards."
---
# BeautifulSoup4 Standards

## 1. Parser Selection

- **lxml**: Prefer `lxml` parser (`features="lxml"`) for speed.
- **html5lib**: Use `html5lib` only if extremely lenient parsing is needed for broken HTML (it is slower).

### Example: Parser

**Good**

```python
soup = BeautifulSoup(html_content, 'lxml')
```

## 2. Selectors

- **CSS Selectors**: Use `soup.select()` and `soup.select_one()` with CSS selectors. They are generally more readable and familiar than `find()` / `find_all()`.

### Example: Selection

**Good**

```python
title = soup.select_one('h1.main-title').get_text(strip=True)
links = [a['href'] for a in soup.select('div.content a')]
```

## 3. Resilience

- **None Handling**: Always check if elements exist before accessing attributes or text to prevent `AttributeError`.

**Good**

```python
element = soup.select_one('.price')
price = element.get_text(strip=True) if element else None
```

**Bad**

```python
# Crashes if element is missing
price = soup.select_one('.price').text
```
