---
title: "Postflight Routing"
version: "1.0.1"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
---

# Postflight Routing

## Overview

Route completion verification to the actual changed authority surface.

## Scope

Completion verification selected for the changed canonical and protected surfaces.

## Rules

`task-checklists.md` is the completion authority. Apply only validators mapped
to the changed canonical source and protected surface. For provider projections,
run the agent governance contract and renderer check; write mode is used only through
the registered renderer.

Completion evidence belongs in the co-located Stage 03 Task. Git history is the
recovery boundary. Do not create a second handoff or progress authority.

For an approved all-files gate, record that Direct `pre-commit run` was not used
and invoke `scripts/validation/run-agent-precommit-all-files.sh`. Controlled wrapper reports exit 20 for unexpected paths. Use it only with a Git-visible, non-ignored repository state.

## Exceptions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

## Related Documents

- [Task checklists](task-checklists.md)
- [Documentation protocol](documentation-protocol.md)
- [Provider registry](providers/registry.yaml)
