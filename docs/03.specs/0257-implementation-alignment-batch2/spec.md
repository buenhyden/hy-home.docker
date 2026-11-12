---
title: "Implementation Alignment Batch 2 Specification"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
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

### Owning Requirements

The user directed that README, AGENTS.md and the Stage 01, 02, 05 and 99
documents be checked against the implementation and corrected, including
missing owners. SPEC-0255 listed the remaining findings as batch 2; PR #733
has merged, so the infra READMEs are free to edit.

SPEC-0257 has parent_ids REQ-0026 and AD-0030. It makes concrete REQ-0026 (document retention and retirement) and the AD-0030 document lifecycle architecture constraint by finishing the deferred alignment findings of SPEC-0255. The body cites no REQ-0026-FR or NFR identifier.

## Scope

### In Scope

- Backticked operations paths in infra READMEs that omit the domain folder.
- The Grafana README Compose link and the `infra/09-platform-ops` audience.
- Registry `common.root_exceptions` and `common.inventory_excludes` entries
  whose paths no longer exist.
- Compose secret names that no owning guide lists.

### Non-goals

- Stage 01–03 lifecycle statuses and validator code (PR #730).
- Secret values, runtime state and terminal Task bodies.

## Behavior Contract

### Normal Behavior

Every backticked operations path in an infra README resolves to a file, and
every Compose secret name appears in the guide that owns its service.

Paths stay inline code: a document outside `docs/` does not link an
individual stage document.

### Failure and Edge Cases

A corrected document that breaks metadata, lifecycle or link alignment fails
the document gates.

Only secret names are written; no secret value is read or recorded.

**Observable failures.** A path still misses its file, or a secret name is missing from every guide.

**Stop boundaries.** This Task pushes and merges nothing. The coordinator pushes the branch and
opens the pull request.

## Acceptance Criteria

### Criteria

1. No backticked `docs/` path in an infra README is missing.
2. The Grafana Compose link resolves and the `infra/09-platform-ops` audience
   names people only.
3. The Registry names no missing path in `root_exceptions` or
   `inventory_excludes`.
4. Each Compose secret name appears in an operations guide or README.
5. The document gates pass locally, with actual results in the Task.

### Evidence Requirements

- Criteria 1 and 2 are observed by checking backticked paths and the Grafana link in the infra READMEs; criterion 3 by checking the Registry paths exist; criterion 4 by checking each Compose secret name against the guides.
- Criterion 5 is verified by running the document gates locally; the actual results go in the Task.
- The frontmatter owner judges each criterion and records the decision in the Task's Criterion Acceptance table.

## References

### Normative and Evidence

- [Plan](plan.md)
- [Task](tasks/tsk-0001-implementation-alignment-batch2.md)

### Historical and Navigation

No historical or navigation link applies; the package links only its Plan and Task.
