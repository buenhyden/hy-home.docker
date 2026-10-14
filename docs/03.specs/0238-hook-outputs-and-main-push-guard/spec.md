---
title: "Hook Outputs and Main Push Guard"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "specs"
artifact_id: "SPEC-0238"
parent_ids:
- "REQ-0024"
- "AD-0027"
- "ADR-0032"
created: "2026-10-13"
---

# Hook Outputs and Main Push Guard

## Overview

Independent security and governance reviews of `.claude/settings.json`,
`.codex/hooks.json` and the shared hook dispatcher on `main` `f1214c839`, and a
check against the Claude Code and Codex hook documentation on 2026-10-13,
found:

- PreCompact emits `hookSpecificOutput` with `hookEventName: "PreCompact"`,
  which Claude Code rejects; neither provider accepts that field for
  PreCompact.
- SessionStart and the PreToolUse guidance send model-facing text as
  `systemMessage`, which both providers show only to the user.
- Codex hooks use 600-second timeouts on every event and list Claude-only
  tool names in their matchers.
- The Codex sandbox cannot start on this host, and that limit is recorded
  nowhere; two Codex claims (project `[memories]`, PreToolUse on
  `apply_patch`) are stated as fact though unobserved.
- The `block-direct-main-push` rule misses most push forms, a plain
  `git push` whose target is `main`, and every push an agent hook never sees.
  `main` was pushed directly twice on 2026-10-13.
- `Bash(grep:*)` and `Bash(rg:*)` auto-approve reading secret files, and
  `rg --pre` runs arbitrary programs; nothing denies reading `secrets/` or
  `.env`.

## Scope

In scope: `scripts/hooks/agent-event-hook.sh`, `scripts/hooks/hook_rules.py`,
the `block-direct-main-push` rule, a new `scripts/hooks/pre-push-guard.sh` and
its `.pre-commit-config.yaml` stage, `.claude/settings.json`,
`.codex/hooks.json`, the Registry `hook_contracts`, both provider adapters,
`environment-constraints.md` §1 and §5, the Storybook guide's Codex MCP
location, the `.github/rulesets/main-protection.md` record, and tests.

Out of scope: remote GitHub protection settings, installing the local git
hook, user-global provider settings, and the review findings the owner did not
choose (more destructive-command denials, removing project `autoMode` and
`"$defaults"`).

Owner decisions on 2026-10-13: fix the PreCompact hook, the Codex hooks and the
direct-push gap ("점검후 수정하고 보완"); remove the grep/rg allows and deny
reads of secrets (AskUserQuestion).

## Contracts

1. PreCompact emits only universal fields; the model receives post-compaction
   context through SessionStart `hookSpecificOutput.additionalContext`.
2. SessionStart and PreToolUse guidance reach the model as
   `additionalContext`; SessionStart names `AGENTS.md` or `CLAUDE.md`.
3. Codex hook timeouts match Claude's per event (Stop 600 s) and its matchers
   name the tools Codex emits. The native hook files equal the Registry
   contract.
4. A PreToolUse `git push` that would update `main` is denied in every
   explicit form, for `HEAD`, `@` and an implicit refspec by the branch and
   push target of the repository it runs in, and when that repository cannot
   be read. A tracked `pre-push` guard refuses a push to `refs/heads/main`
   once installed, within the limits the pre-commit shim imposes; only a
   remote ruleset without bypass enforces the boundary.
5. Claude settings deny the Read and Edit tools on `secrets/**` and `.env`
   under the session directory and at any absolute path, and on `~/.ssh`, deny explicit pushes to `main`, drop
   the grep/rg allows, and set the Registry-owned `on_failure: block` on
   PreToolUse so a timed-out hook is documented to deny the tool.
6. Policy and adapters state the Codex sandbox limit and the unobserved Codex
   claims.

## Acceptance Criteria

1. Tests show PreCompact without `hookSpecificOutput`, SessionStart and
   PreToolUse guidance in `additionalContext`, and the compaction reminder on
   source `compact`; each fails against `main`.
2. A test shows the native hook files equal the Registry contract, and the
   Codex values are aligned.
3. Tests show every listed main-push form denied, feature-branch pushes
   allowed, and the pre-push guard refusing main; the main-push tests fail
   against `main`.
4. Tests show the settings deny rules, the removed allows, and the
   PreToolUse `onFailure` value equal to the Registry binding.
5. The governance contract, renderer check, script manifest, workflow
   contract, changed metadata, corpus lifecycle and links pass, and an
   independent review finds nothing blocking.
6. Hosted `candidate-quality` passes.

## Related Documents

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [ADR-0032](../../02.architecture/decisions/0032-canonical-agent-governance-home.md)
- [Plan](plan.md)
