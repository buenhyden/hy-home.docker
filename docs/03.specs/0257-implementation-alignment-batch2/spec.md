---
title: "Implementation Alignment Batch 2 Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0257"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-04"
---

# Implementation Alignment Batch 2 Specification

## Overview

### Intent

Correct the audit findings SPEC-0255 deferred because open branches held the
files, so documents and the Registry state what the repository holds now.

### Background

The user directed that README, AGENTS.md and the Stage 01, 02, 05 and 99
documents be checked against the implementation and corrected, including
missing owners. SPEC-0255 listed the remaining findings as batch 2; PR #733
has merged, so the infra READMEs are free to edit.

## Scope

### In Scope

- Backticked operations paths in infra READMEs that omit the domain folder.
- The Grafana README Compose link and the `infra/09-platform-ops` audience.
- Registry `common.root_exceptions` and `common.inventory_excludes` entries
  whose paths no longer exist.
- Compose secret names that no owning guide lists.

### Out of Scope

- Stage 01–03 lifecycle statuses and validator code (PR #730).
- Secret values, runtime state and terminal Task bodies.

## Contracts

### Normal Behavior

Every backticked operations path in an infra README resolves to a file, and
every Compose secret name appears in the guide that owns its service.

### Error Behavior

A corrected document that breaks metadata, lifecycle or link alignment fails
the document gates.

### Boundary Behavior

Only secret names are written; no secret value is read or recorded.

### Constraints

Paths stay inline code: a document outside `docs/` does not link an
individual stage document.

## Acceptance Criteria

1. No backticked `docs/` path in an infra README is missing.
2. The Grafana Compose link resolves and the `infra/09-platform-ops` audience
   names people only.
3. The Registry names no missing path in `root_exceptions` or
   `inventory_excludes`.
4. Each Compose secret name appears in an operations guide or README.
5. The document gates pass locally, with actual results in the Task.

## Failure Conditions

### Observable Failures

A path still misses its file, or a secret name is missing from every guide.

### Stop Boundaries

This Task pushes and merges nothing. The coordinator pushes the branch and
opens the pull request.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-implementation-alignment-batch2.md)
