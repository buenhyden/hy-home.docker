---
status: completed
---

<!-- Target: docs/03.specs/106-workspace-support-surface-contract/spec.md -->

# Workspace Support Surface Contract Technical Specification

## Overview

This document defines the implementation contract for `_workspace` as an
isolated, repository-local support surface.

The workspace already references `_workspace` in Stage 00 agent and subagent
handoff guidance, but the directory does not currently exist as a tracked
surface and `.gitignore` does not define its protection rules. This spec closes
that gap by making `_workspace/repo-support/` the only allowed temporary
repo-support staging area and by prohibiting diagnostics, local logs, auth
files, tokens, shell history, raw logs, credentials, private keys, and secret
values from the tracked `_workspace` surface.

## Strategic Boundaries & Non-goals

- This specification owns the `_workspace` support-surface boundary and its
  validation contract.
- `_workspace` is not an active documentation stage, template target, runtime
  config surface, or long-term evidence store.
- `_workspace/repo-support/` may hold short-lived, non-secret generated
  analysis, dry-run previews, migration ledgers, and subagent handoff artifacts
  during a task.
- Durable findings must be promoted to canonical stages such as
  `docs/04.execution/tasks/`, `docs/90.references/`, or Stage 00 memory.
- The work does not inspect, print, rotate, or move secret values.
- The work does not change Docker Compose runtime, provider adapters, hooks,
  model policy, CI workflow behavior, or remote GitHub state.

## Related Inputs

- **User approval**: 2026-07-05 approval for Approach A, `_workspace` contract
  first, with broader repo-wide cleanup decomposed as follow-up.
- **Subagent protocol**:
  [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Workflow routing**:
  [../../00.agent-governance/rules/workflows.md](../../00.agent-governance/rules/workflows.md)
- **Environment constraints**:
  [../../00.agent-governance/rules/environment-constraints.md](../../00.agent-governance/rules/environment-constraints.md)
- **Security scope**:
  [../../00.agent-governance/scopes/security.md](../../00.agent-governance/scopes/security.md)
- **Template governance**:
  [../../99.templates/support/template-governance.md](../../99.templates/support/template-governance.md)
- **Frontmatter contract**:
  [../../99.templates/support/frontmatter-contract.md](../../99.templates/support/frontmatter-contract.md)
- **Git ignore pattern source**:
  [gitignore documentation](https://www.kernel.org/pub/software/scm/git/docs/gitignore.html)
- **GitHub ignore guidance**:
  [Ignoring files](https://docs.github.com/articles/ignoring-files)
- **OWASP source**:
  [Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

## Contracts

| Contract | Required Behavior |
| --- | --- |
| Allowed root | `_workspace/` is a repository-local support surface, not a documentation stage. |
| Allowed tracked files | Track only `_workspace/README.md`, `_workspace/repo-support/README.md`, and future explicitly approved non-secret contract markers. |
| Allowed runtime artifacts | Use `_workspace/repo-support/` for short-lived non-secret generated analysis, dry-run previews, migration ledgers, and subagent handoffs. |
| Prohibited artifacts | Do not place diagnostics dumps, local logs, auth files, tokens, shell history, raw logs, credentials, private keys, or secret values in `_workspace`. |
| Evidence promotion | Promote durable results to `docs/04.execution/tasks/`, `docs/90.references/`, or Stage 00 memory before completion. |
| Ignore posture | Ignore `_workspace/**` by default and re-include only the approved tracked contract files. |
| Validator posture | Fail repo contracts if tracked `_workspace` files fall outside the allowlist or if tracked `_workspace` paths contain prohibited path segments. |

## Core Design

### Target Structure

```text
_workspace/
├── README.md              # tracked role and safety contract
└── repo-support/
    └── README.md          # tracked allowed artifact profile
```

Short-lived runtime artifacts may be created below `_workspace/repo-support/`
while work is active, but those files remain ignored unless a future approved
task explicitly promotes a non-secret artifact to a canonical documentation
stage.

### Repository Boundary

`_workspace` is a staging surface for the repository workflow, not a user-local
home for debugging or authentication material. The protected boundary is stricter
than ordinary temporary files because agentic workflows may create many
intermediate artifacts while coordinating subagents.

### Git Ignore Model

The root `.gitignore` must ignore `_workspace/**` and then re-include the
tracked contract files. This follows the Git ignore model where patterns are
shared through the repository and negated with `!` for approved exceptions.

## Data Modeling & Storage Strategy

| Artifact Type | Location | Tracking Policy | Promotion Rule |
| --- | --- | --- | --- |
| Generated analysis summary | `_workspace/repo-support/<task>/...` | Ignored by default | Promote curated outcome to Stage 04 task evidence or Stage 90 reference. |
| Dry-run preview | `_workspace/repo-support/<task>/dry-run/...` | Ignored by default | Keep only command, ID, and path evidence in Stage 04; do not preserve raw logs. |
| Migration ledger | `_workspace/repo-support/<task>/ledger/...` | Ignored by default | Promote final migration table to task evidence or reference report. |
| Subagent handoff | `_workspace/repo-support/<phase>-<agent>/...` | Ignored by default | Summarize decisions in canonical task evidence. |
| Diagnostics dump or local log | Not allowed under tracked repo support | Must not be tracked | Use local ignored/private tooling outside this contract. |
| Auth, token, key, shell history, raw secret log | Not allowed | Must not be written, summarized, or committed | Escalate to approved secrets protocol if a task truly requires secret work. |

## Interfaces & Data Structures

### Validator Rule

`scripts/validation/check-repo-contracts.sh` must include a `_workspace`
protected-surface section that:

- lists tracked files under `_workspace`;
- permits only the approved contract files;
- rejects tracked paths with prohibited path segments such as `auth`, `token`,
  `tokens`, `credential`, `credentials`, `secret`, `secrets`, `key`,
  `private-key`, `shell-history`, `history`, `log`, `logs`, `diagnostic`, and
  `diagnostics`;
- verifies that `.gitignore` contains the default ignore and re-include
  patterns.

### Governance Rule

Stage 00 governance must route intermediate agent outputs to
`_workspace/repo-support/` and must state that raw logs, local diagnostics,
auth material, tokens, shell history, and secret values are prohibited.

### Template / Frontmatter Rule

Stage 99 support documents must state that `_workspace` contract files are
repo-support README surfaces, not target-stage documents and not copyable
template outputs. They do not receive lifecycle frontmatter solely to match
Stage 01-05 or Stage 90 documents.

## Agent Role & IO Contract

| Role | Input | Output |
| --- | --- | --- |
| Documentation Specialist | Stage 00 and Stage 99 contracts, current `_workspace` references | Updated spec, plan, task, README, and support-contract text. |
| Security Reviewer | Security scope, OWASP secrets guidance, `.gitignore` rules | Prohibited-surface wording and validator expectations. |
| QA / Validator Maintainer | Existing `check-repo-contracts.sh` sections | `_workspace` protected-surface validation. |

## Tools & Tool Contract

- Use `rg` for repository evidence discovery.
- Use official Git/GitHub/OWASP sources only for external support-surface and
  secret-boundary claims.
- Use `apply_patch` for file edits.
- Use `git diff --check` for patch hygiene.
- Use `bash scripts/validation/check-doc-traceability.sh` for documentation
  link and traceability checks.
- Use `bash scripts/validation/check-repo-contracts.sh` for final repository
  contract validation.

## Guardrails

- Do not read, print, summarize, or commit secret values.
- Do not place raw logs, shell history, local diagnostics, auth files, or token
  material under `_workspace`.
- Do not convert `_workspace` into a docs stage, archive, or permanent evidence
  repository.
- Do not add README-only policy if the rule belongs in Stage 00 or Stage 99
  support contracts.
- Do not use Graphify as sole evidence because the current graph report is
  stale relative to HEAD.

## Verification

```bash
git diff --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-repo-contracts.sh
```

Graphify update is required only after code changes when the CLI is available.
This task changes shell validation logic but not application source code; if
Graphify is unavailable, record the skip in task evidence.

## Success Criteria & Verification Plan

- **VAL-WSC-001**: `_workspace/README.md` and
  `_workspace/repo-support/README.md` define allowed and prohibited surfaces
  without secret values or raw logs.
- **VAL-WSC-002**: `.gitignore` ignores `_workspace/**` by default and
  re-includes only approved tracked contract files.
- **VAL-WSC-003**: Stage 00 routes intermediate artifacts to
  `_workspace/repo-support/` and prohibits diagnostics, auth files, tokens,
  shell history, raw logs, and secrets.
- **VAL-WSC-004**: Stage 99 support contracts describe `_workspace` as a
  repo-support surface outside target-stage and template-source profiles.
- **VAL-WSC-005**: `check-repo-contracts.sh` fails on unapproved tracked
  `_workspace` files and required `.gitignore` drift.
- **VAL-WSC-006**: Documentation traceability and repository contract checks
  pass, or unrelated failures are recorded in task evidence.

## Related Documents

- [spec README](./README.md)
- [docs/03.specs README](../README.md)
- [implementation plan](../../04.execution/plans/2026-07-05-workspace-support-surface-contract.md)
- [task evidence](../../04.execution/tasks/2026-07-05-workspace-support-surface-contract.md)
- [subagent protocol](../../00.agent-governance/subagent-protocol.md)
- [environment constraints](../../00.agent-governance/rules/environment-constraints.md)
- [security scope](../../00.agent-governance/scopes/security.md)
- [template governance](../../99.templates/support/template-governance.md)
- [frontmatter contract](../../99.templates/support/frontmatter-contract.md)
