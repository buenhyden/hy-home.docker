---
status: active
observed_at: 2026-08-21
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
| `user-prompt-intake` | `UserPromptSubmit` | `configured` | `UserPromptSubmit` | `configured` |
| `pre-tool` | `PreToolUse` | `configured` | `PreToolUse` | `configured` |
| `post-tool` | `PostToolUse` | `configured` | `PostToolUse` | `configured` |
| `stop` | `Stop` | `configured` | `Stop` | `configured` |
| `pre-compaction` | `PreCompact` | `configured` | `PreCompact` | `configured` |
| `session-end` | `SessionEnd` | `configured` | `N/A` | `unsupported` |

## Sources

- `docs/00.agent-governance/providers/registry.yaml`
- `.claude/settings.json`
- `.codex/hooks.json`

## Maintenance

Regenerate after provider registry or native hook configuration changes.

## Related Documents

- [Provider capability matrix](../../../../00.agent-governance/policies/provider-capability-matrix.md)
- [Provider registry](../../../../00.agent-governance/providers/registry.yaml)
