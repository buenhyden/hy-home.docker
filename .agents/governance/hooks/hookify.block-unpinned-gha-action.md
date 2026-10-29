---
title: "BLOCKED: floating reference"
version: "1.0.3"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
action: "block"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "\\.github/workflows/.*\\.ya?ml$"
- "field": "new_text"
  operator: "regex_match"
  pattern: "uses:\\s+\\S+@(latest|main|master|develop|dev)\\b"
enabled: true
event: "file"
name: "block-unpinned-gha-action"
---

# BLOCKED: floating reference

## Overview

Apply the declared `block` action for block-unpinned-gha-action.

## Scope

Applies to the `block-unpinned-gha-action` rule on the `file` event. The frontmatter of this document owns the exact matcher.

## Rules

**Floating GitHub Actions reference blocked (project rule)**

`.agents/governance/github-governance.md` — GitHub Actions Security Contract: the workflow uses a floating branch or tag reference.

**Detected pattern:** `uses: owner/action@latest` / `@main` / `@master` / `@develop`

**Why this is risky:**

- External actions can change without review.
- Floating refs increase supply-chain attack exposure.
- Builds are not reproducible.

**Safe alternative:**

```yaml
# BLOCKED: floating reference

- uses: actions/checkout@main
- uses: actions/setup-python@latest

# ALLOWED: pinned version or commit SHA
- uses: actions/checkout@v4.2.2
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

Commit SHA pinning is safest. If a version tag is used, prefer digest verification.

The declared action applies when the pattern matches.

## Exceptions

No exception is declared by this rule.

## Verification

The declared `file` event and structured `conditions` define the matching scope; native event delivery remains a separate observation.

## Related Documents

- `.agents/README.md`
