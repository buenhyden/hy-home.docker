---
title: "SPEC-0209 and SPEC-0231 Retirement Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-04"
layer: "specs"
artifact_id: "SPEC-0260"
parent_ids:
- "REQ-0026"
- "AD-0030"
created: "2026-11-04"
---

# SPEC-0209 and SPEC-0231 Retirement Specification

## Overview

### Intent

Delete the completed packages SPEC-0209 and SPEC-0231. They stayed only
because the Spec Package loader read their lifecycle generation 5 and 6
Contract Migration proofs from the working tree. Under generation 7 the
loader reads those proofs from the last generation 6 revision instead.

### Background

The generation 5 proof (source `8b85e88fe2dfef54f4cc125ee2687982c86c1942`)
lives in SPEC-0209-TSK-0001 and the generation 6 proof (source
`2a57d4122dc8dac954afca364b838e4bf97fd44a`) in SPEC-0231-TSK-0001. Both
Tasks are terminal and unchanged at the last generation 6 revision
`49f8dd661acf37bf292ee0aa59abfe1af16cde10`, which
`previous_generation_revision(root, 7)` already resolves from Git history.

## Scope

### In Scope

- `load_spec_packages` passes the generation 6 tree's packages as the proof
  source to the generation 5, 6 and 7 historical admission paths.
- Tests for the proof source and its fail-closed behavior.
- Deleting both package directories, reserving 209 and 231 in the Registry
  `spec` space, and removing their index rows.
- Rewording current documents that said the two packages stay as proof.

### Out of Scope

- Changing which Tasks are admitted or how their Evidence is read.
- Terminal Task bodies and other packages' Task records.

## Contracts

### Normal Behavior

With lifecycle generation 7 or later, each migration proof is read from the
packages at `previous_generation_revision(root, 7)`; the current tree still
supplies the Tasks being admitted. The same historical Tasks are admitted
after the two packages leave the tree.

### Error Behavior

A missing generation 6 revision or a missing proof package in it fails the
loader with an error; nothing falls back to the working tree.

### Boundary Behavior

Generations 5 and 6 keep reading proofs from the given packages.

### Constraints

Prose may name a retired identity to explain lineage (ADR-0051).

## Acceptance Criteria

1. With the two packages deleted, `load_spec_packages` loads the current tree
   and reads both migration proofs from the generation 6 revision.
2. A missing proof package or proof revision fails closed, proven by tests.
3. Numbers 209 and 231 are reserved, the index has no row for them, and no
   current document says they stay as proof.
4. The document gates and the document governance tests pass locally, with
   actual results in the Task.

## Failure Conditions

### Observable Failures

The loader fails on the current tree, a historical Task loses admission, or a
link into a deleted package breaks outside a terminal Task.

### Stop Boundaries

This Task pushes and merges nothing. The coordinator pushes the branch and
opens the pull request, and the user merges.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-spec-0209-0231-retirement.md)
