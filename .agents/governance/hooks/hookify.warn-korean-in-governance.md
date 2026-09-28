---
title: "WARNING: Korean text in governance documentation"
version: "1.1.0"
type: "governance/hook-policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
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

<!-- markdownlint-disable MD041 MD040 -->

**Korean text detected in governance documentation (project rule)**

This hook is an advisory detector. It skips `README.md` files, whose language
the documentation protocol owns; the negative lookahead in the path pattern is
what excludes them, so keep it when editing the pattern. Resolve the file's language through the sole
document-role authority at
`.agents/governance/documentation-protocol.md#document-language`;
the hook does not publish a second language table or exception rule.

## Related Documents

- `.agents/README.md`
- `.agents/governance/documentation-protocol.md`
