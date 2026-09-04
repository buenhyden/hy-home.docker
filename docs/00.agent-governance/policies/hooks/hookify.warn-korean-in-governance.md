---
title: "WARNING: Korean text in governance documentation"
version: "1.0.0"
type: "governance/hook-policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
action: "warn"
conditions:
- field: "file_path"
  operator: "regex_match"
  pattern: "docs/00\\.agent-governance/.*\\.md$"
- field: "new_text"
  operator: "regex_match"
  pattern: "[\\uac00-\\ud7a3\\u3131-\\u318e]"
enabled: true
event: "file"
name: "warn-korean-in-governance"
---

<!-- markdownlint-disable MD041 MD040 -->

**Korean text detected in governance documentation (project rule)**

This hook is an advisory detector. Resolve the file's language through the sole
document-role authority at
`docs/00.agent-governance/policies/documentation-protocol.md#authoring-rules`;
the hook does not publish a second language table or exception rule.

## Related Documents

- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/policies/documentation-protocol.md`
