---
title: "Folder Guide Delivery Specification"
version: "0.2.0"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0264"
parent_ids:
- "REQ-0024"
- "AD-0027"
created: "2026-11-06"
---

# Folder Guide Delivery Specification

## Overview

### Intent

Nine folders carry an `AGENTS.md` guide, but neither Codex nor Claude Code reads
them when an agent works below the folder. This Spec contracts one shared hook
that delivers the nearest folder guide to the agent before it touches a file.

### Background

The owner requested on 2026-11-06 that Codex and Claude read each folder's
`AGENTS.md`, and chose one shared hook over folder `CLAUDE.md` shims.

- Codex merges `AGENTS.md` only from the repository root down to the working
  directory (`codex-rs/core/src/agents_md.rs` in openai/codex).
- Claude Code reads `AGENTS.md` only where no `CLAUDE.md` is on the path. Root
  `CLAUDE.md` exists here, and the setting to read both is ignored in project
  settings (code.claude.com/docs/en/memory).

So neither provider reads the folder guides.

## Scope

### In Scope

- `scripts/lib/hooks/folder_guides.py` and `scripts/hooks/agent-event-hook.sh`.
- The tests in `tests/lib/hooks/test_folder_guides.py` and the script manifest
  entry.
- The `.claude/provider.md` and `.codex/provider.md` descriptions.
- The audit of the folder `AGENTS.md` files in the same branch.

### Out of Scope

- Folder `CLAUDE.md` shims.
- Delivery on a Codex shell read; only `apply_patch` triggers delivery.
- Changing what a guide says beyond the audit.

## Contracts

### Normal Behavior

The PreToolUse hook adds the nearest folder `AGENTS.md` to `additionalContext`
for edit targets (Claude Write, Edit and MultiEdit; Codex `apply_patch`) and
for Claude Read. Each guide is delivered once per session. SessionStart clears
that record. The root `AGENTS.md` is never delivered.

### Error Behavior

The hook never blocks a tool call. Any failure in guide lookup, state access or
reading leaves the tool call allowed and delivers nothing.

### Boundary Behavior

A guide larger than 16 KiB is capped. State lives under
`$XDG_STATE_HOME/hy-home/folder-guides`, default `~/.local/state`, and is
replaced atomically.

### Constraints

The state directory must be owned by the current user with mode 0700, else it
is not used. The hook adds no tool permission or approval.

## Acceptance Criteria

1. Before an edit below a folder with an `AGENTS.md`, both Claude (Write, Edit,
   MultiEdit, and Read) and Codex (`apply_patch`) receive that guide in
   `additionalContext`.
2. A guide is delivered once per session and again after SessionStart.
3. The root `AGENTS.md` is never delivered.
4. The hook never blocks a tool call, including on state or read failure.
5. State is kept in a per-user directory owned by the user with mode 0700, and
   written by atomic replace.
6. `.claude/provider.md` and `.codex/provider.md` describe the delivery and its
   limits.
7. The folder `AGENTS.md` files are audited in the same branch.
8. The delivery is observed in a new Claude session and a new Codex
   session started at the repository root: editing or reading a file under
   `infra/` shows the "Folder guide `infra/AGENTS.md`" context once.

## Failure Conditions

### Observable Failures

- A guide missing before an edit, or repeated within a session.
- The root guide delivered.
- A tool call blocked by the hook.
- State in a directory not owned by the user or not mode 0700.

### Stop Boundaries

A Codex shell read does not trigger delivery. Native delivery in a live
session is not yet observed; only dispatcher tests exist until criterion 8 is
accepted.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-deliver-folder-guides.md)
- [README and AGENTS.md split](../0251-readme-and-agents-guide-split/spec.md)
- [Claude adapter](../../../.claude/provider.md)
- [Codex adapter](../../../.codex/provider.md)
