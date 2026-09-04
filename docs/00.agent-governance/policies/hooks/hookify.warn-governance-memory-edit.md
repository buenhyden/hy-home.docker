---
title: "WARNING: Stage 00 root authority edit"
version: "1.0.0"
type: "governance/hook-policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
action: "warn"
conditions:
- field: "file_path"
  operator: "regex_match"
  pattern: "(^|/)docs/00\\.agent-governance/(README|sdlc)\\.md$"
enabled: true
event: "file"
name: "warn-stage00-root-edit"
---

<!-- markdownlint-disable MD041 MD040 -->

**Stage 00 root authority edit detected**

Confirm that the change preserves the six-entry Stage 00 inventory, routes
document shapes to Stage 99, records evidence in the co-located Task, and
regenerates provider projections when their inputs change.

## Related Documents

- `docs/00.agent-governance/README.md`
- `docs/00.agent-governance/sdlc.md`
