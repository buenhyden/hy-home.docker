---
title: "WARNING: Docker infrastructure completion routing"
version: "1.0.1"
type: "governance/hook-policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
action: "warn"
enabled: true
event: "stop"
name: "warn-docker-infra-stop"
pattern: ".*"
---

<!-- markdownlint-disable MD041 MD040 -->

**Docker infrastructure completion routing (project rule)**

This hook warns that infra-layer work has conditional completion gates. Apply
only the canonical contract in
`.agents/governance/task-checklists.md#before-completion` and
its referenced validators. The hook does not restate pass criteria, blockers,
settings policy, or evidence fields. Record the result in the applicable
co-located Task with the exact command result, rollback, and skipped checks.

## Related Documents

- `.agents/README.md`
- `.agents/governance/task-checklists.md`
