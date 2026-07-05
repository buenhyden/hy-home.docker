---
status: completed
---

<!-- Target: docs/03.specs/106-workspace-support-surface-contract/README.md -->

# Workspace Support Surface Contract Specification

> Design contract for the `_workspace` repo-support and protected-surface boundary.

## Overview

`docs/03.specs/106-workspace-support-surface-contract` defines the technical
contract for the repository-local `_workspace` staging surface.

The contract separates short-lived, non-secret repo-support artifacts from
diagnostics, local logs, auth files, tokens, shell history, raw logs, and secret
values. It also defines the Stage 00, Stage 99, `.gitignore`, and validation
updates required to keep that boundary enforceable.

## Audience

This README is for:

- Repository Maintainers
- Documentation Writers
- AI Agents
- Security Reviewers

## Status

This specification is a completed design contract implemented on 2026-07-05.

## Scope

### In Scope

- `_workspace` role and purpose definition
- `_workspace/repo-support` allowed artifact boundary
- prohibited local diagnostics, auth, token, shell-history, raw-log, and secret
  surfaces
- Stage 00 governance updates
- Stage 99 support-contract updates
- `.gitignore` tracked-surface protection
- repository validator enforcement

### Out of Scope

- Moving existing secret files or reading secret values
- Runtime Docker Compose changes
- Provider adapter, hook, model-policy, or remote GitHub changes
- Broad repo-wide frontmatter normalization outside direct fallout

## Structure

```text
106-workspace-support-surface-contract/
├── README.md  # This file
└── spec.md    # `_workspace` contract design
```

## How to Work in This Area

1. Read [spec.md](./spec.md) before changing `_workspace`, Stage 00, Stage 99,
   `.gitignore`, or repository validators.
2. Keep executable implementation evidence in the Stage 04 task document.
3. Keep durable support-surface rules in Stage 00 or Stage 99 support
   documents, not in README-only prose.
4. Treat Graphify as advisory for this change because the current graph was
   built from an older commit.

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs README](../README.md)
- [implementation plan](../../04.execution/plans/2026-07-05-workspace-support-surface-contract.md)
- [task evidence](../../04.execution/tasks/2026-07-05-workspace-support-surface-contract.md)
- [subagent protocol](../../00.agent-governance/subagent-protocol.md)
- [environment constraints](../../00.agent-governance/rules/environment-constraints.md)
- [template governance](../../99.templates/support/template-governance.md)
