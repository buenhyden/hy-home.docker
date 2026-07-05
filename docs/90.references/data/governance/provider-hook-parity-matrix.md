---
status: active
generated_by: scripts/validation/report-provider-hook-parity.sh
---

<!-- Target: docs/90.references/data/governance/provider-hook-parity-matrix.md -->

# Reference: Provider Hook Parity Matrix

## Overview

This generated reference compares the repository's Claude, Codex, and Gemini
hook surfaces. Claude and Codex expose programmatic hook configuration;
Gemini is represented as a behavioral reminder checklist because the Stage 00
provider capability matrix treats Gemini hooks as a non-native capability.

## Purpose

The matrix helps reviewers inspect provider hook parity without manually
opening every hook config, wrapper script, and provider note.

## Repository Role

Use this document as generated audit context only. Active provider policy
remains in `docs/00.agent-governance/`, and executable hook behavior remains
in `.claude/`, `.codex/`, `.agents/`, and `scripts/hooks/`.

## Scope

### In Scope

- Tracked `.claude/settings.json` hook configuration.
- Tracked `.codex/hooks.json` hook configuration.
- Claude wrapper delegation to `scripts/hooks/agent-event-hook.sh`.
- Codex provider-neutral hook dispatch commands.
- Gemini behavioral checklist derived from Stage 00 provider notes.

### Out of Scope

- Personal settings such as `.claude/settings.local.json`.
- Live provider runtime state, telemetry, shell history, or raw hook logs.
- New native Gemini hook claims beyond the current Stage 00 contract.
- Mutating provider configuration, model policy, secrets, credentials, or remote state.

## Definitions / Facts

- **native-wrapper**: Claude event is configured and delegates through a tracked wrapper script.
- **native-dispatch**: Codex event is configured and dispatches directly through `scripts/hooks/agent-event-hook.sh`.
- **behavioral-reminder**: Gemini has no tracked native hook event and must manually follow the shared hook contract.
- **needs-contract-review**: A required Stage 00 Gemini behavioral contract literal is missing.

## Snapshot Summary

| Metric | Value |
| --- | ---: |
| Hook events tracked | 7 |
| Claude native wrapper events | 7 |
| Codex native dispatch events | 7 |
| Gemini behavioral reminder events | 7 |
| Provider-neutral dispatcher present | yes |
| Gemini contract literals missing | 0 |

## Provider Hook Parity Matrix

| Event | Purpose | Claude | Codex | Gemini |
| --- | --- | --- | --- | --- |
| `SessionStart` | Session/bootstrap guard | `native-wrapper` - Configured native hook wrapper delegates to provider-neutral dispatcher | `native-dispatch` - Configured hook dispatches through provider-neutral event hook | `behavioral-reminder` - Load `AGENTS.md`, provider notes, bootstrap, persona, checklist, one scope, and progress memory before repository mutation. |
| `UserPromptSubmit` | Prompt intake and routing guard | `native-wrapper` - Configured native hook wrapper delegates to provider-neutral dispatcher | `native-dispatch` - Configured hook dispatches through provider-neutral event hook | `behavioral-reminder` - Classify task scope, resolve risky ambiguity, and route to the canonical stage before editing. |
| `PreToolUse` | Pre-mutation guard | `native-wrapper` - Configured native hook wrapper delegates to provider-neutral dispatcher | `native-dispatch` - Configured hook dispatches through provider-neutral event hook | `behavioral-reminder` - Review requirements, guardrails, protected surfaces, and template-first rules before mutating files. |
| `PostToolUse` | Post-edit validation guard | `native-wrapper` - Configured native hook wrapper delegates to provider-neutral dispatcher | `native-dispatch` - Configured hook dispatches through provider-neutral event hook | `behavioral-reminder` - Run relevant style, docs, generated-output, and repository contract checks after edits. |
| `Stop` | Completion gate | `native-wrapper` - Configured native hook wrapper delegates to provider-neutral dispatcher | `native-dispatch` - Configured hook dispatches through provider-neutral event hook | `behavioral-reminder` - Confirm completion checklist, logical commit discipline, progress memory, and residual gaps before declaring completion. |
| `PreCompact` | Context handoff guard | `native-wrapper` - Configured native hook wrapper delegates to provider-neutral dispatcher | `native-dispatch` - Configured hook dispatches through provider-neutral event hook | `behavioral-reminder` - Record durable progress and handoff context before compaction or context transition. |
| `SessionEnd` | Session closure guard | `native-wrapper` - Configured native hook wrapper delegates to provider-neutral dispatcher | `native-dispatch` - Configured hook dispatches through provider-neutral event hook | `behavioral-reminder` - Update progress evidence and leave the worktree/validation state explicit at session closure. |

## Command Provenance

| Event | Claude Matcher | Claude Command | Codex Matcher | Codex Command |
| --- | --- | --- | --- | --- |
| `SessionStart` | * | `bash $CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh` timeout=15s | * | `bash scripts/hooks/agent-event-hook.sh SessionStart` timeout=15s |
| `UserPromptSubmit` | * | `bash $CLAUDE_PROJECT_DIR/.claude/hooks/user-prompt-submit.sh` timeout=10s | * | `bash scripts/hooks/agent-event-hook.sh UserPromptSubmit` timeout=10s |
| `PreToolUse` | Bash\|Read\|Glob\|Grep\|LS\|Edit\|Write\|MultiEdit\|apply_patch\|ApplyPatch | `bash $CLAUDE_PROJECT_DIR/.claude/hooks/docker-compose-pre.sh` timeout=10s | Bash\|Read\|Glob\|Grep\|LS\|Edit\|Write\|MultiEdit\|apply_patch\|ApplyPatch | `bash scripts/hooks/agent-event-hook.sh PreToolUse` timeout=10s |
| `PostToolUse` | Write\|Edit\|MultiEdit\|apply_patch\|ApplyPatch | `bash $CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-validate.sh` timeout=30s | Edit\|Write\|MultiEdit\|apply_patch\|ApplyPatch | `bash scripts/hooks/agent-event-hook.sh PostToolUse` timeout=30s |
| `Stop` | * | `bash $CLAUDE_PROJECT_DIR/.claude/hooks/stop.sh` timeout=30s | * | `bash scripts/hooks/agent-event-hook.sh Stop` timeout=30s |
| `PreCompact` | * | `bash $CLAUDE_PROJECT_DIR/.claude/hooks/pre-compact.sh` timeout=10s | * | `bash scripts/hooks/agent-event-hook.sh PreCompact` timeout=10s |
| `SessionEnd` | * | `bash $CLAUDE_PROJECT_DIR/.claude/hooks/session-end.sh` timeout=10s | * | `bash scripts/hooks/agent-event-hook.sh SessionEnd` timeout=10s |

## Gemini Behavioral Reminder Checklist

| Event | Manual Reminder |
| --- | --- |
| `SessionStart` | Load `AGENTS.md`, provider notes, bootstrap, persona, checklist, one scope, and progress memory before repository mutation. |
| `UserPromptSubmit` | Classify task scope, resolve risky ambiguity, and route to the canonical stage before editing. |
| `PreToolUse` | Review requirements, guardrails, protected surfaces, and template-first rules before mutating files. |
| `PostToolUse` | Run relevant style, docs, generated-output, and repository contract checks after edits. |
| `Stop` | Confirm completion checklist, logical commit discipline, progress memory, and residual gaps before declaring completion. |
| `PreCompact` | Record durable progress and handoff context before compaction or context transition. |
| `SessionEnd` | Update progress evidence and leave the worktree/validation state explicit at session closure. |

## Source Rules

- Regenerate this file after changing Claude/Codex hook configs, Claude hook
  wrappers, Gemini provider notes, provider capability matrix rules, or
  `.agents/` runtime guidance.
- Treat Gemini rows as manual behavioral reminders until Stage 00 provider
  governance is updated with verified native hook support.
- Do not read personal settings, hook logs, shell history, credentials,
  tokens, `.env` values, or live provider runtime state.

## Sources

- [Claude settings](../../../../.claude/settings.json) - tracked Claude hook configuration.
- [Codex hooks](../../../../.codex/hooks.json) - tracked Codex hook configuration.
- [Gemini provider notes](../../../00.agent-governance/providers/gemini.md) - Gemini behavioral hook contract.
- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - provider hook capability boundary.
- [Gemini shared runtime README](../../../../.agents/README.md) - `.agents/` rules and workflows surface.
- [Provider-neutral dispatcher](../../../../scripts/hooks/agent-event-hook.sh) - shared hook event implementation.

## Maintenance

- **Owner**: Agentic Workflow Specialist / QA Engineer.
- **Review Cadence**: Review after provider hook, adapter, or provider-note changes.
- **Update Trigger**: Run the generator after tracked provider hook surfaces change.

## Related Documents

- **Governance data index**: [README.md](./README.md)
- **Provider semantic parity spec**: [../../../03.specs/107-provider-semantic-parity-validator/spec.md](../../../03.specs/107-provider-semantic-parity-validator/spec.md)
- **Provider hook parity spec**: [../../../03.specs/115-provider-hook-parity-matrix/spec.md](../../../03.specs/115-provider-hook-parity-matrix/spec.md)
- **Automation candidates**: [../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
