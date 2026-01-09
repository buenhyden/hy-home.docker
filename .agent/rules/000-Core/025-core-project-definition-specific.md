---
trigger: always_on
glob: "README.md,docs/**/*.md"
description: "Project Definition Standards: Structure and content for README and documentation."
---
# Project Definition Standards

## 1. README Structure

- **Purpose**: Clearly state *why* the project exists and what problem it solves.
- **Tech Stack**: List key technologies and versions.
- **Quick Start**: Provide a copy-pasteable "Getting Started" or "Installation" section.

### Example: Sections

**Good**

```markdown
# My Project

## Purpose
A high-performance web scraper.

## Tech Stack
- Python 3.12
- Scrapy
- PostgreSQL

## Quick Start
```bash
pip install -r requirements.txt
scrapy crawl myspider
```

```

## 2. Folder Structure

- **Map**: Include a logical map of the folder structure in `README.md` or `docs/structure.md`.
- **Explanation**: Briefly explain the purpose of top-level directories.

## 3. Customization & Libraries

- **Dependencies**: Explicitly list major 3rd-party libraries.
- **Custom Logic**: Document any non-standard architectural decisions or custom modules.
