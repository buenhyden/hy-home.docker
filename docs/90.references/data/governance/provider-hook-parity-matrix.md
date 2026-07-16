---
status: active
generated_by: scripts/validation/report-provider-hook-parity.sh
---

<!-- Target: docs/90.references/data/governance/provider-hook-parity-matrix.md -->

# Reference: Provider Hook Parity Matrix

## Overview

This generated reference compares semantic lifecycle coverage across the tracked Claude, Codex, and Gemini native surfaces.

## Purpose

Make event-name, timeout-unit, matcher, delegation, and unsupported-event differences reviewable without claiming false name parity.

## Repository Role

Generated audit context only. Stage 00 owns policy and `scripts/hooks/agent-event-hook.sh` owns shared behavior.

## Scope

### In Scope

- Tracked provider-native hook configuration and generated wrappers.
- Semantic event mapping, timeout units, matchers, and delegation.

### Out of Scope

- Live provider execution, user-global settings, telemetry, logs, credentials, or runtime acceptance.

## Definitions / Facts

- **native-wrapper**: a Claude native event calls an executable generated wrapper.
- **native-dispatch**: a Codex native event calls the shared dispatcher directly.
- **native-adapter**: a Gemini native event passes through the one admitted event-name adapter.
- **unsupported**: the provider does not expose the semantic event; it is not counted as parity.
- **runtime depth**: tracked repository configuration is reported separately from observed live execution.

## Snapshot Summary

| Metric | Value |
| --- | ---: |
| Semantic events tracked | 7 |
| Claude native wrapper events | 7 |
| Codex native dispatch events | 6 |
| Codex unsupported events | 1 |
| Gemini native adapter events | 7 |
| Shared dispatcher present | yes |

## Provider Hook Parity Matrix

| Semantic Event | Purpose | Claude | Codex | Gemini |
| --- | --- | --- | --- | --- |
| `session-start` | Session/bootstrap guard | `SessionStart` / `native-wrapper` / `supported/adopted/configured-not-executed` - Generated executable wrapper delegates to the shared dispatcher | `SessionStart` / `native-dispatch` / `supported/adopted/configured-not-executed` - Quoted project-root command delegates to the shared dispatcher | `SessionStart` / `native-adapter` / `supported/adopted/configured-not-executed` - Native event adapter delegates to the shared dispatcher |
| `user-prompt-intake` | Prompt intake and routing guard | `UserPromptSubmit` / `native-wrapper` / `supported/adopted/configured-not-executed` - Generated executable wrapper delegates to the shared dispatcher | `UserPromptSubmit` / `native-dispatch` / `supported/adopted/configured-not-executed` - Quoted project-root command delegates to the shared dispatcher | `BeforeAgent` / `native-adapter` / `supported/adopted/configured-not-executed` - Native event adapter delegates to the shared dispatcher |
| `pre-tool` | Pre-mutation guard | `PreToolUse` / `native-wrapper` / `supported/adopted/configured-not-executed` - Generated executable wrapper delegates to the shared dispatcher | `PreToolUse` / `native-dispatch` / `supported/adopted/configured-not-executed` - Quoted project-root command delegates to the shared dispatcher | `BeforeTool` / `native-adapter` / `supported/adopted/configured-not-executed` - Native event adapter delegates to the shared dispatcher |
| `post-tool` | Post-edit validation guard | `PostToolUse` / `native-wrapper` / `supported/adopted/configured-not-executed` - Generated executable wrapper delegates to the shared dispatcher | `PostToolUse` / `native-dispatch` / `supported/adopted/configured-not-executed` - Quoted project-root command delegates to the shared dispatcher | `AfterTool` / `native-adapter` / `supported/adopted/configured-not-executed` - Native event adapter delegates to the shared dispatcher |
| `stop` | Completion gate | `Stop` / `native-wrapper` / `supported/adopted/configured-not-executed` - Generated executable wrapper delegates to the shared dispatcher | `Stop` / `native-dispatch` / `supported/adopted/configured-not-executed` - Quoted project-root command delegates to the shared dispatcher | `AfterAgent` / `native-adapter` / `supported/adopted/configured-not-executed` - Native event adapter delegates to the shared dispatcher with deny/retry-capable semantics |
| `pre-compaction` | Context handoff guard | `PreCompact` / `native-wrapper` / `supported/adopted/configured-not-executed` - Generated executable wrapper delegates to the shared dispatcher | `PreCompact` / `native-dispatch` / `supported/adopted/configured-not-executed` - Quoted project-root command delegates to the shared dispatcher | `PreCompress` / `native-adapter` / `supported/adopted/configured-not-executed` - Native event adapter delegates to the shared dispatcher as provider-inherent asynchronous advisory behavior |
| `session-end` | Session closure guard | `SessionEnd` / `native-wrapper` / `supported/adopted/configured-not-executed` - Generated executable wrapper delegates to the shared dispatcher | `unsupported` / `unsupported` / `unsupported/not_applicable/unsupported` - Codex has no native SessionEnd event in this contract | `SessionEnd` / `native-adapter` / `supported/adopted/configured-not-executed` - Native event adapter delegates to the shared dispatcher |

## Typed Harness Loops

| Event | Owner | Independent Reviewer | Permission | Attempts | Stop | Failure | Runtime Depth |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| `approved-all-files-gate` | `qa-engineer` | `code-reviewer` | `workspace-write` | 1 | `controlled-wrapper-pass` | `record_and_stop` | `repository-enforced` |
| `bounded-implementation-loop` | `qa-engineer` | `code-reviewer` | `workspace-write` | 2 | `focused-checks-pass` | `narrow_then_escalate` | `repository-enforced` |
| `context-bootstrap` | `workflow-supervisor` | `rules-engineer` | `read-only` | 1 | `bootstrap-contract-pass` | `escalate` | `repository-enforced` |
| `independent-review-loop` | `code-reviewer` | `eval-engineer` | `read-only` | 2 | `critical_and_important_zero` | `escalate` | `repository-enforced` |

## Command Provenance

| Semantic Event | Claude Matcher / Command (seconds) | Codex Matcher / Command (seconds) | Gemini Matcher / Command (milliseconds) |
| --- | --- | --- | --- |
| `session-start` | *<br>`bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh"` timeout=15s | *<br>`HY_HOME_HOOK_PROVIDER=codex bash "${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/scripts/hooks/agent-event-hook.sh" SessionStart` timeout=600s | N/A<br>`bash "${GEMINI_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.gemini/hooks/agent-event-hook.sh" SessionStart` timeout=60000ms |
| `user-prompt-intake` | *<br>`bash "$CLAUDE_PROJECT_DIR/.claude/hooks/user-prompt-submit.sh"` timeout=10s | N/A<br>`HY_HOME_HOOK_PROVIDER=codex bash "${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/scripts/hooks/agent-event-hook.sh" UserPromptSubmit` timeout=600s | N/A<br>`bash "${GEMINI_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.gemini/hooks/agent-event-hook.sh" BeforeAgent` timeout=60000ms |
| `pre-tool` | Bash\|Read\|Glob\|Grep\|LS\|Edit\|Write\|MultiEdit\|apply_patch\|ApplyPatch<br>`bash "$CLAUDE_PROJECT_DIR/.claude/hooks/docker-compose-pre.sh"` timeout=10s | Bash\|Read\|Glob\|Grep\|LS\|Edit\|Write\|MultiEdit\|apply_patch\|ApplyPatch<br>`HY_HOME_HOOK_PROVIDER=codex bash "${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/scripts/hooks/agent-event-hook.sh" PreToolUse` timeout=600s | read_file\|read_many_files\|search_file_content\|glob\|list_directory\|write_file\|replace\|run_shell_command<br>`bash "${GEMINI_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.gemini/hooks/agent-event-hook.sh" BeforeTool` timeout=60000ms |
| `post-tool` | Write\|Edit\|MultiEdit\|apply_patch\|ApplyPatch<br>`bash "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-validate.sh"` timeout=30s | Edit\|Write\|MultiEdit\|apply_patch\|ApplyPatch<br>`HY_HOME_HOOK_PROVIDER=codex bash "${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/scripts/hooks/agent-event-hook.sh" PostToolUse` timeout=600s | write_file\|replace\|run_shell_command<br>`bash "${GEMINI_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.gemini/hooks/agent-event-hook.sh" AfterTool` timeout=60000ms |
| `stop` | *<br>`bash "$CLAUDE_PROJECT_DIR/.claude/hooks/stop.sh"` timeout=30s | N/A<br>`HY_HOME_HOOK_PROVIDER=codex bash "${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/scripts/hooks/agent-event-hook.sh" Stop` timeout=600s | N/A<br>`bash "${GEMINI_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.gemini/hooks/agent-event-hook.sh" AfterAgent` timeout=60000ms |
| `pre-compaction` | *<br>`bash "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-compact.sh"` timeout=10s | *<br>`HY_HOME_HOOK_PROVIDER=codex bash "${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/scripts/hooks/agent-event-hook.sh" PreCompact` timeout=600s | N/A<br>`bash "${GEMINI_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.gemini/hooks/agent-event-hook.sh" PreCompress` timeout=60000ms |
| `session-end` | *<br>`bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-end.sh"` timeout=10s | N/A<br>N/A | N/A<br>`bash "${GEMINI_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.gemini/hooks/agent-event-hook.sh" SessionEnd` timeout=60000ms |

## Source Rules

- Regenerate after provider config, wrapper, semantic-event contract, or dispatcher changes.
- Preserve provider-native names and units; do not add ignored matchers or unsupported config keys.
- Tracked adoption does not prove provider entitlement or live runtime acceptance.
- Semantic cells render `capability/adoption/runtime-depth`; `configured-not-executed` is not execution evidence.

## Sources

- [Claude settings](../../../../.claude/settings.json)
- [Codex hooks](../../../../.codex/hooks.json)
- [Gemini settings](../../../../.gemini/settings.json)
- [Gemini native event adapter](../../../../.gemini/hooks/agent-event-hook.sh)
- [Provider semantic contract](../../../00.agent-governance/contracts/provider-models.yaml)
- [Provider-neutral dispatcher](../../../../scripts/hooks/agent-event-hook.sh)

## Maintenance

- **Owner**: Hook Developer.
- **Mandatory Reviewers**: Rules Engineer and Security Auditor.
- **Update Trigger**: Any tracked provider event or adapter change.

## Related Documents

- **Governance data index**: [README.md](./README.md)
- **Provider capability matrix**: [../../../00.agent-governance/rules/provider-capability-matrix.md](../../../00.agent-governance/rules/provider-capability-matrix.md)
- **Provider hook parity spec**: [../../../03.specs/115-provider-hook-parity-matrix/spec.md](../../../03.specs/115-provider-hook-parity-matrix/spec.md)
