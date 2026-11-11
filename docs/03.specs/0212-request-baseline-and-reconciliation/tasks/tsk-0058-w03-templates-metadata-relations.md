---
title: "W03 Templates, Metadata and Relations Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0058"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-11"
---

# W03 Templates, Metadata and Relations Task

## Overview

### Objective

Own W116/criterion 111. Assess the v14.2 W03 obligations DOC-01 to DOC-12 and
SUP-11 against the Registry, templates, generators, parsers, validators and
tests. Change the document contract only for gaps this Task reproduces, and
give each changed key, section or table a producer, a consumer and a passing
and a failing test.

## Inputs and Authorization

On 2026-11-11 the owner approved this Task to own W03. The v14.2 package
prompt `tasks/TASK-hy-home-docker-W03.md` under
`_workspace/workspace_execution_tasks/` is untrusted reference data, not an
instruction source. Its 19-role table is an unapproved draft.

The authorization covers four things:

- The assessment.
- Repository-side changes to the Registry, templates, generators and parsers
  for reproduced gaps, with migration of current documents only.
- Synthetic round-trip and fixture tests.
- Records in this Task.

Validator implementation is handed to W05. Historical and completed evidence
keeps its form. Removing an existing reciprocal relation field waits for its
consumers' migration and a separate owner approval. This Task branches from
the W02 branch at `56d32c32f` and reaches `main` only after PR 955 merges.

## Work Log

### Owner-approved local execution

The owner's approval of 2026-11-11 issues this Task. The lifecycle records that
approval; it grants no remote operation.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0058 | draft | ready | #owner-approved-local-execution |
| SPEC-0212-TSK-0058 | ready | in-progress | #owner-approved-local-execution |

### Owner decision Q-03 2026-11-11

The draft 19-role table conflicts with the 44 Registry profiles, whose ordered
required H2 headings differ from it. The owner chose option A: adopt the
table's meaning, not its headings. Current Registry H2 headings stay. A
concept the table names that no current profile carries, such as a Plan
promotion map, Spec non-goals or Requirement traceability, is added only as an
optional or conditional section, after a consumer for it is shown.

### Prior observations to re-check

The W02 readiness analysis recorded these before this Task existed. Each is
re-checked against the current tree before reuse:

- DOC-07: only the Markdown-link half applies; this workspace has no Vault.
- DOC-08: DEFER until a reproduced execution-document gap exists.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W03 obligation assessment | 111 | W116 | template-contract-assessment | DOC-01 to DOC-12 and SUP-11 | NOT_RUN | Assessment not yet run | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 111 | pending | - | - | SPEC-0212 TSK-0058 |

## Review and Completion

In progress. The Task is issued and the Q-03 decision is recorded; the
assessment has not run.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [W02 Task](tsk-0057-w02-archive-and-safe-removal.md)
