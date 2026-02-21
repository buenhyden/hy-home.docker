---
trigger: model_decision
glob: ["docs/**/*.md", "README.md", "**/*.md"]
description: "Content Standards: Guidelines for writing READMEs, Tutorials, How-To guides (Diátaxis), and Changelogs."
---

# 0800-Documentation-Content

- **Role**: Technical Writer / Developer
- **Purpose**: Enforce the Diátaxis framework, audience adaptation, and maintenance triggers for all documentation.
- **Activates When**: Writing or updating READMEs, tutorials, guides, or reference docs.

## 1. Standards

### 1.1 Principles

- **[REQ-DOC-CON-01] Diátaxis**: Documentation MUST be classified into Tutorial, How-To, Reference, or Explanation.
- **[REQ-DOC-CON-02] Single Source**: Information MUST NOT be duplicated; reference authoritative sources.
- **[REQ-DOC-CON-03] Intent-Revealing**: Docs MUST explain _why_, not just _what_ (code explains how).

### 1.2 Scope

- **In-Scope**: Markdown documentation, READMEs, Changelogs.
- **Out-of-Scope**: Code comments (inline), specific technical specs (0805).

### 1.3 Inputs & Outputs

- **Inputs**: User needs, Codebase features.
- **Outputs**: Clear, categorized markdown files.

### 1.4 Must / Must Not

- **[REQ-DOC-REA-01] Core Four**: READMEs MUST include Purpose, Tech Stack, Setup, and Usage.
- **[REQ-DOC-LOG-01] Changelog**: MUST follow Keep a Changelog format (Added, Changed, Deprecated, Removed, Fixed, Security).
- **[BAN-DOC-STYL-01] No Passive Voice**: MUST use active voice and imperative verbs ("Run this", not "This should be run").

## 2. Procedures

### 2.1 Diátaxis Workflow

1. **Classify**: Is it for learning (Tutorial), tasks (How-To), information (Reference), or understanding (Explanation)?
2. **Draft**: Write focused content for that quadrant.
3. **Verify**: Ensure code examples work copy-paste.

### 2.2 Maintenance

1. **Trigger**: Code logic change, API update, or new feature.
2. **Action**: Update relevant docs in the same PR.
3. **Check**: Verify links and setup steps.

## 3. Examples

### 3.1 README Sections (Good)

```markdown
# My Project

## Purpose
A high-performance cache wrapper for Redis.

## Usage
`npm install my-cache`

```javascript
const cache = require('my-cache');
cache.set('key', 'value');
```

```

### 3.2 Changelog Entry (Good)

```markdown
## [1.1.0] - 2025-01-15
### Changed
- **BREAKING**: Renamed `auth` config key to `authentication`.
### Fixed
- Crash on login page.
```

## 4. Validation Criteria

- [ ] **[VAL-DOC-STR-01]** Diátaxis classification is clear.
- [ ] **[VAL-DOC-REA-01]** README contains Purpose, Stack, Setup, Usage.
- [ ] **[VAL-DOC-ACC-01]** Code examples are tested and accurate.
- [ ] **[VAL-DOC-LNK-01]** All links are valid.

## 5. References

- Reference: [diataxis.fr](https://diataxis.fr/)
- Related: [0805-documentation-technical.md](./0805-documentation-technical.md)
