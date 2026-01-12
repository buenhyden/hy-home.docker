---
trigger: always_on
glob: "mkdocs.yml,**/*.md"
description: "MkDocs: Material Theme, Admonitions, Tabs, and Code Annotations."
---
# MkDocs Standards

## 1. Admonitions

- **Usage**: Use standard `!!! type` blocks.
- **Types**: `note`, `warning`, `tip`, `danger`, `info`.

### Example: Admonition

**Good**

```markdown
!!! warning "Breaking Change"
    version 2.0 drops support for Python 3.8.
```

**Bad**

```markdown
**WARNING**: version 2.0 drops support... (Just bold text)
```

## 2. Navigation

- **Structure**: Explicit `nav` in `mkdocs.yml` or `awesome-pages` plugin.
- **Links**: Relative links only. Never absolute URLs to your own site.

## 3. Material Theme Features

- **Tabs**: Use content tabs for multi-language examples.
- **Code Annotations**: Use `(1)` annotations to explain complex code.
- **Diagrams**: Enable `mermaid` extension for architecture diagrams.

### Example: Tabs

**Good**

```markdown
=== "Python"
    ```python
    print("Hello")
    ```
=== "JavaScript"
    ```javascript
    console.log("Hello");
    ```
```

**Bad**

```markdown
Python:
... (code) ...

JavaScript:
... (code) ...
```

## 4. Configuration & Plugins

- **Readability**: Ensure all `mkdocs.yml` configurations are optimized for readability and maintainability.
- **Plugins**: Use appropriate plugins to enhance functionality (e.g., `mkdocs-minify-plugin`, `mkdocs-git-revision-date-localized-plugin`, `mkdocstrings`).
- **Optimization**: Minify HTML/CSS/JS in production builds to improve page load speed.
- **Validation**: Periodically check for broken links and invalid YAML syntax.
