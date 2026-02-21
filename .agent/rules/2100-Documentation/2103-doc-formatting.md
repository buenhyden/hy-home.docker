---
trigger: model_decision
glob: ["docs/**/*.md", "**/*.md"]
description: "Formatting Standards: Markdown syntax, headers, links, and asset management."
---

# 0810-Documentation-Formatting

- **Role**: Documentation Editor
- **Purpose**: Enforce consistent markdown styling for readability and parsing.
- **Activates When**: Formatting any markdown document.

## 1. Standards

### 1.1 Principles

- **[REQ-FMT-GEN-01] Consistency**: Style MUST be consistent across all files.
- **[REQ-FMT-GEN-02] Standard Markdown**: Use GFM (GitHub Flavored Markdown).
- **[REQ-FMT-GEN-03] Accessibility**: Images MUST have alt text.

### 1.2 Scope

- **In-Scope**: All Markdown files.
- **Out-of-Scope**: Generated code documentation (JSDoc, GoDoc).

### 1.3 Inputs & Outputs

- **Inputs**: Raw text.
- **Outputs**: Formatted Markdown.

### 1.4 Must / Must Not

- **[REQ-FMT-HDR-01] Hierarchy**: Headers MUST nest properly (H1 -> H2 -> H3). No skipping levels.
- **[REQ-FMT-COD-01] Code Blocks**: Fenced code blocks MUST specify language.
- **[REQ-FMT-LNK-01] Relative Links**: Internal links MUST be relative.
- **[BAN-FMT-HTM-01] No HTML**: Avoid raw HTML tags if Markdown suffices.

## 2. Procedures

### 2.1 Formatting Checklist

1. **Headers**: One H1 per file.
2. **Lists**: Use hyphens (`-`) for unordered lists.
3. **Links**: `[Text](./path/to/file.md)`.
4. **Images**: `![Alt Text](./path/to/image.png)`.

## 3. Examples

### 3.1 Good Formatting

```markdown
# Title

## Section 1
Text here.

### Subsection
- Item A
- Item B

[Link to File](./other.md)
```

## 4. Validation Criteria

- [ ] **[VAL-FMT-HDR-01]** Header hierarchy is correct.
- [ ] **[VAL-FMT-COD-01]** Code blocks have languages.
- [ ] **[VAL-FMT-LNK-01]** Links work and are relative.

## 5. References

- None.
