---
title: "Scripts Agent Guide"
version: "1.0.0"
type: "common/agent-guide"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: Scripts Agent Guide
  layer: agent
updated: "2026-11-20"
---

# Scripts Agent Guide

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the agent-guide payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Allowed Scope

###### Allowed Surface
<!-- core-payload-level:4 -->

`scripts/` holds the executable gates: validators, hardening checks, hooks,
operation commands and their shared libraries. This guide routes an agent that
changes or runs them. The human guide is [README.md](README.md).

`scripts/validation/`, `scripts/hardening/`, `scripts/hooks/`,
`scripts/knowledge/`, `scripts/operations/`, `scripts/security/`,
`scripts/lib/<domain>/` and `scripts/manifest.yaml`.

###### Non-goals
<!-- core-payload-level:4 -->

Policy text is out of scope; a script implements a canonical rule and never
becomes its owner.

##### Instruction Precedence

When this guide and the owner of a rule it summarizes disagree, the owner wins
and this guide is corrected
([documentation protocol](../docs/00.workspace/03.process/documentation-protocol.md#readme-and-agentsmd)).
[Bootstrap](../.agents/governance/bootstrap.md#authority-and-precedence)
sets the full precedence order; a folder guide routes only and never overrides
canonical governance or a Stage contract.

#### Workflow

##### Intake

- [Bootstrap](../.agents/governance/bootstrap.md),
  [quality standards](../docs/00.workspace/04.quality/quality-standards.md),
  [approval boundaries](../docs/00.workspace/04.quality/approval-boundaries.md),
  [GitHub governance](../docs/00.workspace/03.process/github-governance.md).
- Roles: [`qa-engineer`](../.agents/roles/qa-engineer.md),
  [`ci-cd-engineer`](../.agents/roles/ci-cd-engineer.md),
  [`hook-developer`](../.agents/roles/hook-developer.md).
- Skills: [`ci-cd-patterns`](../.agents/skills/ci-cd-patterns/SKILL.md),
  [`style-validation`](../.agents/skills/style-validation/SKILL.md),
  [`test-authoring`](../.agents/skills/test-authoring/SKILL.md).
- Hook rule: [`warn-pre-commit-manual`](../.agents/governance/hooks/hookify.warn-pre-commit-manual.md).
- Native hooks: `.claude/hooks/` and `.codex/hooks.json` call
  `scripts/hooks/agent-event-hook.sh`, which calls
  `scripts/hooks/post-tool-validate.sh` for post-edit validation.
- Provider loading: [Claude adapter](../.claude/provider.md),
  [Codex adapter](../.codex/provider.md).

##### Execution

###### Inspect and Change
<!-- core-payload-level:4 -->

- Inspect the selected gates with
  `python3 scripts/validation/run-ci-gate.py --profile changed --explain`
  before running them.

###### Local Obligations
<!-- core-payload-level:4 -->

- Register every new, moved or retired script in `scripts/manifest.yaml`; the
  Script Manifest check rejects an unregistered or orphaned script.
- Give a change to `scripts/lib/<domain>/` a behavior test in
  `tests/lib/<domain>/`, and a CLI or entrypoint change a test in
  `tests/validation/`.

#### Boundaries

##### Authority

Stop and report when this guide and its canonical owner disagree (the owner
wins and this guide is corrected), when an action needs an approval that
[approval boundaries](../docs/00.workspace/04.quality/approval-boundaries.md)
has not granted, or when a required check fails.

##### Secrets and External Effects

- Let the installed hooks check the reviewed index and message on an ordinary
  commit when their delivery has been confirmed. If delivery is unconfirmed or
  a diagnosis is needed, use
  `scripts/validation/run-ci-precommit.sh --mode local-staged` for the reviewed
  index, then commit normally. Never run `pre-commit run` directly.
- An all-files run follows the
  [execution boundary](../docs/00.workspace/04.quality/quality-standards.md#4-execution-boundary)
  and its `scripts/validation/run-agent-precommit-all-files.sh` route.
- Generated provider surfaces under `.claude/` and `.codex/`, and each folder
  `CLAUDE.md` import shim beside a folder `AGENTS.md`, come from
  `scripts/operations/provider_surface_renderer.py`; re-render them, never
  hand-edit them.
- A script never prints, logs or writes a secret value.

#### Verification

##### Checks

- `python3 scripts/validation/check-script-manifest.py`
- `python3 scripts/operations/provider_surface_renderer.py --check`
- `python3 scripts/validation/check-agent-governance-contract.py`

##### Reporting

###### Evidence and Limits
<!-- core-payload-level:4 -->

Record each check's command, revision and exit in the current Task. These
checks are static or local; they do not prove runtime state, native provider
delivery, remote enforcement or owner acceptance.

###### Handoff
<!-- core-payload-level:4 -->

Record progress, decisions and evidence in the current Task, and leave the
next owner named there. Human-facing and related documents:

- [Scripts README](README.md)
- [Tests agent guide](../tests/AGENTS.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
