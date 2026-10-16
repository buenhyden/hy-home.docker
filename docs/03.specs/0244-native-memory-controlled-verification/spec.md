---
title: "Native Memory Controlled Verification"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0244"
parent_ids:
- "REQ-0024"
- "AD-0027"
- "ADR-0049"
created: "2026-10-16"
---

# Native Memory Controlled Verification

## Overview

The owner authorized a bounded continuation of the Claude native-memory and
hook investigation. The earlier sanitized normal-session observation confirmed
that the menus can be opened without an error marker, but did not surface a
non-mutating effective-memory state or individual event receipts. This package
defines one controlled verification route that records that distinction rather
than promoting configured state or menu availability to an effective-off claim.

SPEC-0236 remains the broader shared-memory design and implementation package.
This package neither changes its draft scope nor reads, migrates, or writes a
native or shared memory store.

## Scope

In scope:

- one or more explicitly approved normal Claude sessions that use only a
  written allowlist of non-mutating status, menu, or metadata views;
- the public Codex CLI effective-feature observation and its limits;
- a sanitized comparison between configured native-memory settings, a
  provider-exposed effective-state view if available, and hook menu or receipt
  observations;
- after Claude effective memory-off is proved, one exact ignored-fixture
  provider attempt per independently reviewed Task plan, bounded to the
  plan's two- or three-turn limit and USD 1, with strict empty MCP and no
  Chrome, Bash, or network tools; and
- session-only forced-memory and sandbox fallback controls as separately
  classified proof routes, never as proof of the normal merged setting; and
- a transient, explicitly reviewed provider metadata read through an allowlisted
  control query, retaining only Boolean or enum classifications and no memory
  body; and
- a value-free Task record of session identity, command category, result, and
  stopping condition; and
- independent privacy/security review of the resulting claim boundary.

Out of scope:

- arbitrary private-file or credential access, memory-body reads or writes,
  memory migration, persistent or global configuration changes, user-global
  trust changes, or any provider prompt except the Task-reviewed fixture
  attempt stated above;
- asserting Claude effective memory-off when no non-mutating provider view
  exposes it;
- asserting an individual hook was delivered when no event-specific receipt is
  available; and
- reopening completed SPEC-0212 TSK-0009 or accepting SPEC-0236 criteria.

## Contracts

1. Each controlled session has a written action allowlist. A normal state
   query may only initialize, call its approved metadata view, and end its
   session. A separate fixture attempt may use only its Task-reviewed exact
   fixture action. Any unlisted prompt, tool, setting change, memory-body
   read, arbitrary private-file access, credential access, or extra session
   stops the attempt before that action.
2. The Task records configured state, public CLI effective-feature state,
   provider-exposed effective state, menu availability, and event-specific
   delivery as separate observations. A result may be `UNVERIFIED` or
   `UNKNOWN` in prose; only the Task evidence result domain records executable
   checks.
3. Claude effective memory-off is recorded as verified only when a normal
   session exposes that state through an allowed, non-mutating view. Absence of
   such a view remains unverified, keeps this criterion pending, and does not
   trigger a setting change.
4. Hook configuration or a hooks menu is not evidence of delivery. After
   contract 3 proves memory-off, each independently approved conditional
   fixture attempt may produce sanitized event-specific receipts for
   `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, and `Stop`; otherwise
   delivery remains unknown. A session-only forced-memory flag is a separate
   proof class and cannot establish the normal merged setting.
5. Each conditional fixture attempt discards raw output, uses the exact
   ignored fixture only, clears its approved privacy environment and wrapper
   witness after the run, and records only event names, exit/status, fixture
   hash, and cleanup result. Session-only `sandbox=false` is permitted only
   under its separately reviewed fallback plan and makes no OS-confinement
   claim.
6. The Task contains no authentication material, memory body, prompt content,
   tool payload, private path, or raw provider diagnostic. The execution owner
   stops and escalates if any is about to enter the evidence.

## Acceptance Criteria

1. The Task records the controlled-session allowlist, redaction rules, target,
   and stop conditions before a normal-session attempt.
2. The Task records the public Codex CLI feature boundary and clearly limits
   what that observation establishes.
3. The Task records a sanitized non-mutating normal-session proof that Claude
   effective memory is off, separate from configured state; an unverified
   result keeps this criterion pending and has no state-changing fallback.
4. After criterion 3 passes, the Task records sanitized fixture receipts for
   `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, and `Stop`; a missing
   receipt keeps this criterion pending.
5. Each conditional fixture attempt records its Task-reviewed two- or
   three-turn/USD 1 bound, strict tool boundary, fixture hash, raw-output
   disposal, and cleanup result.
6. A privacy/security review and the selected document checks pass without
   exposing private native-memory or authentication material.

## Failure Conditions

An unavailable effective-state view, an absent event receipt, a rejected
automatic diagnostic, or an unsupported menu action is not a reason to try an
unbounded or mutating alternative. It leaves the relevant state unverified or
unknown, and the relevant criterion remains pending. A conditional fixture
attempt must not run before memory-off proof or without its independently
reviewed Task plan. Any request to inspect a memory body, change persistent or
global native settings, expose authentication or private diagnostic content,
or widen the fixture or tool boundary stops this package and requires
separately scoped authorization.

## Related Documents

- [REQ-0024](../../01.requirements/0024-agent-governance-standardization.md)
- [AD-0027](../../02.architecture/descriptions/0027-agent-governance-canonical-adapter.md)
- [ADR-0049](../../02.architecture/decisions/0049-shared-agent-memory-store.md)
- [SPEC-0236](../0236-shared-agent-memory/spec.md)
- [Plan](plan.md)
- [Task](tasks/tsk-0001-native-memory-controlled-verification.md)
