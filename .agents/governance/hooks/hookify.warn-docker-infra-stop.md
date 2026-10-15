---
title: "WARNING: Docker infrastructure completion routing"
version: "1.0.2"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-15"
action: "warn"
enabled: true
event: "stop"
name: "warn-docker-infra-stop"
pattern: ".*"
---

# WARNING: Docker infrastructure completion routing

## Overview

Apply the declared `warn` action for warn-docker-infra-stop.

## Scope

`stop` 이벤트의 `warn-docker-infra-stop` 규칙에 적용한다. 정확한 matcher는 이 문서의 frontmatter가 소유한다.

## Rules

**Docker infrastructure completion routing (project rule)**

This hook warns that infra-layer work has conditional completion gates. Apply
only the canonical contract in
`.agents/governance/task-checklists.md#before-completion` and
its referenced validators. The hook does not restate pass criteria, blockers,
settings policy, or evidence fields. Record the result in the applicable
co-located Task with the exact command result, rollback, and skipped checks.

## Exceptions

No exception is declared by this rule.

## Verification

The declared `stop` event and `pattern` define the matching scope; native event delivery remains a separate observation.

## Related Documents

- `.agents/README.md`
- `.agents/governance/task-checklists.md`
