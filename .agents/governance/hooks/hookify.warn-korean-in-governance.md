---
title: "WARNING: Korean text in governance documentation"
version: "1.1.3"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)(\\.agents/(?:[^/]+/)*(?!README\\.md$)[^/]+\\.md|\\.(claude|codex)/provider\\.md)$"
- "field": "new_text"
  operator: "regex_match"
  pattern: "[\\uac00-\\ud7a3\\u3131-\\u318e]"
enabled: true
event: "file"
name: "warn-korean-in-governance"
---

# WARNING: Korean text in governance documentation

## Overview

Apply the declared `warn` action for warn-korean-in-governance.

## Scope

The `warn-korean-in-governance` rule applies on the `file` event and matches file edits whose path and text meet every structured `conditions` entry ("WARNING: Korean text in governance documentation"). The frontmatter owns the exact matcher.

## Rules

**Korean text detected in governance documentation (project rule)**

This hook is an advisory detector. It skips `README.md` files, whose language
the documentation protocol owns; the negative lookahead in the path pattern is
what excludes them, so keep it when editing the pattern. Resolve the file's language through the sole
document-role authority at
`.agents/governance/documentation-protocol.md#document-language`;
the hook does not publish a second language table or exception rule.

## Exceptions

No exception is declared by this rule.

## Verification

Native event delivery is a separate observation from the frontmatter match.

## Related Documents

- `.agents/README.md`
- `.agents/governance/documentation-protocol.md`
