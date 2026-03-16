---
title: 'Documentation Maintenance Runbook'
status: 'Active'
owner: 'buenhyden'
tags: ['runbook', 'documentation']
layer: ops
---

# Documentation Maintenance Runbook

**Overview (KR):** 저장소의 평면적 문서 구조와 AI Agent용 Lazy-Loading 체계를 유지하고 관리하기 위한 실행 지침서입니다.

## Prerequisites

- Knowledge of YAML frontmatter.
- Understanding of `docs/agentic/gateway.md` structure.

## Procedures

### 1. Adding a New Document

1. Select the correct category subdirectory (`adr/`, `prd/`, `specs/`, etc.).
2. Use the corresponding template from `templates/`.
3. Add `layer:` metadata to frontmatter.
4. Ensure all internal links are relative.

### 2. Updating the Gateway

If a new document category or a major rule file is added:

1. Update the `Lazy-Loading Map` table in `docs/agentic/gateway.md`.
2. Add the corresponding `[LOAD:*]` marker.

### 3. Verifying Integrity

Run the following commands periodically:

```bash
# Find files missing layer metadata
find docs -name "*.md" -exec grep -L "layer:" {} +

# Find potential broken manual links
rg "\]\(" docs/ | grep -v "http"
```

## Verification

- `[VAL-RBK-001]` No files missing `layer:` metadata.
- `[VAL-RBK-002]` All internal documentation links utilize relative paths and pluralized category roots (`plans/`, `specs/`).
