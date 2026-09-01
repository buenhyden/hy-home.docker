---
profile_id: data
status: active
artifact_id: DATA-0072
artifact_type: data
parent_ids: []
created: '2026-08-21'
updated: '2026-08-28'
observed_at: '2026-08-21'
generated_by: scripts/validation/report-provider-hook-parity.sh
---

# Provider Hook Parity Matrix

## Overview

Generated comparison of tracked Claude and Codex semantic-event adoption.
Configured entries prove repository adoption, not observed live execution.

## Purpose

Expose deterministic provider-event configuration parity without claiming live execution.

## Repository Role

This generated Stage 90 datum supports validation and cannot override Stage 00 policy.

## Scope

Tracked Claude and Codex event configuration only; runtime observation is out of scope.

## Definitions / Facts

Configured means a tracked native hook entry exists; unsupported means no native mapping is registered.

## Data

| Semantic Event | Claude | Status | Codex | Status |
| --- | --- | --- | --- | --- |
| `session-start` | `SessionStart` | `configured` | `SessionStart` | `configured` |
| `pre-tool-use` | `PreToolUse` | `configured` | `PreToolUse` | `configured` |
| `post-tool-use` | `PostToolUse` | `configured` | `PostToolUse` | `configured` |
| `stop` | `Stop` | `configured` | `Stop` | `configured` |
| `session-end` | `SessionEnd` | `configured` | `N/A` | `unsupported` |
| `pre-compact` | `PreCompact` | `configured` | `PreCompact` | `configured` |
| `user-prompt-submit` | `UserPromptSubmit` | `configured` | `UserPromptSubmit` | `configured` |

## Sources

- `docs/00.agent-governance/providers/registry.yaml`
- `.claude/settings.json`
- `.codex/hooks.json`

## Maintenance

Regenerate after provider registry or native hook configuration changes.

## Related Documents

- [Provider capability matrix](../../../00.agent-governance/policies/provider-capability-matrix.md)
- [Provider registry](../../../00.agent-governance/providers/registry.yaml)

## Schema

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Provenance

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Inventory

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Refresh

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Consumers

This package preserves its existing data evidence under the Stage 99 `data` contract.

## Traceability

This package preserves its existing data evidence under the Stage 99 `data` contract.
