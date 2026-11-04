---
title: "Agent Guide Follow-ups Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0254"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-11-04"
---

# Agent Guide Follow-ups Specification

## Overview

### Intent

SPEC-0251 added the folder `AGENTS.md` guides and left four follow-ups open:
`infra` READMEs linking individual stage documents, a CI selection gap for
guide-only edits, a type name that put a routing guide in the governance
family, and guides that started at `draft`. This change closes them.

### Background

The user approved handling the entrypoint findings, the CI selection gap,
ADR-0002 and the type name on 2026-11-04, and earlier approved moving the
guides to `active`.

## Scope

### In Scope

- Plain-text identities in place of the nine individual stage links in
  `infra` READMEs.
- A workflow-contract rule that selects the agent-governance suite for an
  edit to a folder guide.
- Renaming the folder guide type to `common/agent-guide`.
- Moving the nine folder guides to `active`.

### Out of Scope

- Editing the accepted ADR-0002 decision body.
- The root `AGENTS.md` and `CLAUDE.md` shims.

## Contracts

### Normal Behavior

`check-document-links.py --mode entrypoint` reports no finding. A change to
any folder guide the Registry `folder-agent-guide` profile lists selects the
agent-governance suite. Folder guides use the `common/agent-guide` type and the
`active` status.

### Error Behavior

A folder guide path that no longer selects the agent-governance suite fails
the CI routing test.

### Boundary Behavior

The type rename changes no permission or authority: a folder guide stays
routing only and ranks below canonical governance.

### Constraints

An accepted decision body is not rewritten.

## Acceptance Criteria

1. The entrypoint link check reports no finding.
2. A folder-guide-only change selects the agent-governance suite, and a test
   enforces it for every profile path.
3. Folder guides use `common/agent-guide` and `active`, and the stage
   authoring matrix and documentation protocol name that type.
4. The document gates, the document-governance suite, the agent governance
   contract and the CI routing suites pass locally, with actual results in the
   Task.

## Failure Conditions

### Observable Failures

A stage link remains outside `docs/`, a guide edit misses the
agent-governance suite, or a guide still names the governance family.

### Stop Boundaries

This Task pushes and merges nothing; the coordinator pushes and opens the pull
request under the user's instruction, and the user merges.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-agent-guide-follow-ups.md)
