---
title: "QA and CI Legacy Cleanup Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0253"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-11-04"
---

# QA and CI Legacy Cleanup Specification

## Overview

### Intent

QA and CI still carry boundaries and labels that name records the repository
no longer has. This change removes them and checks QA, CI and scripts for
one-off items that only served a finished operation.

### Background

The user directed that legacy and deprecated items in QA and CI/CD be deleted,
and that one-off scripts, tests and QA be deleted. After Stage 98 lost its
records, the pre-commit `frozen_archive_payloads` boundary matches no file,
the CI gate evidence owner names a deleted Task, and the DATA-0096 README
names run-specific files in a runnable command.

## Scope

### In Scope

- The pre-commit frozen archive boundary, the PostToolUse hook code that reads
  it, and their tests.
- The CI gate evidence `owner` label in the workflow contract, its readers and
  their tests.
- The DATA-0096 command block and stale wording in `scripts/README.md`,
  `.agents/governance/agentic.md` and `docs/99.templates/README.md`.
- An inventory of scripts, tests, workflows and QA exceptions for one-off and
  legacy items, deleting only items with no current caller.

### Out of Scope

- Lifecycle-generation migration and identity-history code, owned by the
  legacy document status work and the SPEC-0209/0231 proof move.
- Registry archive profiles and lifecycle vocabulary.

## Contracts

### Normal Behavior

The PostToolUse hook normalizes changed text files without reading a frozen
boundary. CI gate evidence names
`.agents/governance/quality-standards.md#7-local-qaci-orchestration` as its
owner. The `commands` link mode reports no finding.

### Error Behavior

A script, test or exception entry is deleted only when it has no current
caller, its purpose ended with a finished operation, and it is not a reusable
operator tool; anything else stays and is listed in the Task.

### Boundary Behavior

The workflow contract is a protected surface; the user's cleanup instruction
authorizes the owner label change, and the Task records it.

### Constraints

No runtime, remote or secret state changes.

## Acceptance Criteria

1. No QA or CI configuration, hook or contract names a frozen archive boundary
   or a deleted Task.
2. Every script, test and QA exception was checked for one-off or legacy use,
   and the Task records each candidate with its decision.
3. Gate, CI routing, manifest and hook tests, the document gates, the agent
   governance contract and renderer parity pass locally, with actual results in
   the Task.

## Failure Conditions

### Observable Failures

A deleted item still has a caller, or a check that read the removed boundary
now fails.

### Stop Boundaries

This Task pushes and merges nothing; the coordinator pushes and opens the pull
request, and the user merges.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-qa-ci-legacy-cleanup.md)
