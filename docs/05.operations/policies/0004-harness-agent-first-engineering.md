---
title: "Harness / Agent-first Engineering Operations Policy"
version: "1.1.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "operations"
artifact_id: "POL-0004"
parent_ids:
- "SPEC-0094"
created: "2026-06-04"
---

# Harness / Agent-first Engineering Operations Policy

## Overview

이 운영 정책은 `hy-home.docker`의 하네스 엔지니어링과 Agent-first Engineering 계약을 유지하기 위한 통제 기준을 정의한다.

Canonical agent governance lives in `.agents/`: the governance policies own the
rules, the Provider Registry owns provider identity, model and permission
translation, and the roles own their own tier and work profile. This document
owns the operational side only — when the harness is exercised, how it is
checked, and what to do when a check fails.

Controls below therefore point at their owner instead of restating it. Every
control that summarised a canonical rule in prose eventually disagreed with it:
the model row named a hierarchy the registry never expressed, and the Codex row
still forbade a catalog the registry had already adopted. A control that names
its owner cannot drift that way.

## Policy Scope

- Agent entry shims.
- Governance policies, roles, skills, and provider registry.
- Claude runtime mirror.
- Codex hook/context surface.
- Stage documentation and validators.
- `AGENTS.md`, `CLAUDE.md`
- `.claude/**`
- `.codex/**`
- `.agents/**`
- `docs/03.specs/**`
- `docs/03.specs/[0-9][0-9][0-9][0-9]-*/plan.md`
- `docs/03.specs/[0-9][0-9][0-9][0-9]-*/tasks/tsk-[0-9][0-9][0-9][0-9]-*.md`
- `docs/05.operations/guides/[0-9][0-9][0-9][0-9]-*.md`
- `docs/05.operations/policies/[0-9][0-9][0-9][0-9]-*.md`
- `docs/05.operations/runbooks/[0-9][0-9][0-9][0-9]-*.md`
- `scripts/validation/check-*.sh`, `scripts/hardening/check-all-hardening.sh`, `scripts/validation/validate-docker-compose.sh`

## Controls

| Control | Requirement |
| --- | --- |
| Thin root shims | Root files delegate detailed policy to `.agents/` and runtime overlays. |
| Runtime mirror parity | Native role adapters and thin Claude skill pointers stay synchronized with authored `.agents` sources; canonical files are never renderer output. |
| Runtime parity scope | Repository checks prove catalog, model, scope import, and protocol-reference parity; they do not prove semantic parity of every runtime document. |
| Model selection | Each role declares a `work_profile` and the Provider Registry maps that profile to a provider model. This document does not restate the mapping: summarising it as one supervisor model and one worker model was wrong for six of the thirteen workers, because `adversarial-review` roles resolve to the same tier as the supervisor and `routine-validation` resolves below the others. |
| Scope imports | Each runtime agent imports exactly one primary scope. |
| Hook safety | Runtime hooks must parse real payload shapes without shell command substitution side effects. |
| Codex boundary | Governance has adopted a Codex catalog: the Provider Registry declares the native agent pattern and the renderer writes one adapter per role beside the hook configuration. The registry, not this document, decides what the Codex surface contains. |
| Template-first docs | New stage docs use `docs/99.templates/` and update parent README files. |
| Source-label prevention | Active runtime/governance files must not reference external harness source labels. |
| Graph context health | Graphify is a navigation aid only when health is clean; contaminated output remains advisory and must be corroborated against tracked source and canonical docs. |
| Infra validation scope | HAFE completion may rely on default/core Compose and supported hardening tiers; non-included profiles such as `10-communication` require separate infra remediation. |
| AI Agent limits | Owned by the [Agentic Engineering Policy](../../../.agents/governance/agentic.md#execution-rules) and, for Graphify, [Environment Constraints](../../../.agents/governance/environment-constraints.md#4-graphify). |

## Exceptions

- Historical Stage 90 or Stage 98 evidence may mention prior source labels when it is clearly non-authoritative.
- `bash scripts/knowledge/report-graphify-health.sh` may report `status=advisory`; that is evidence for downgraded confidence, not a repository validation failure.
- `graphify` refresh may be skipped when the CLI is unavailable, but the skip must be reported.
- `rtk` may be bypassed when it is unavailable in the active shell.
- `10-communication` compose/include/IP remediation is outside HAFE unless explicitly scoped into an infra change.

## Verification

Every hook, runtime, and repository contract check listed in [Runbook §Procedure](../runbooks/0004-harness-agent-first-engineering.md#procedure) must pass before a harness or Agent-first change is accepted.

## Review Cadence

- Run repository contract checks after any root, governance, runtime, provider, script, or stage documentation change.
- Re-run the full verification bundle before declaring a broad harness or Agent-first migration complete.
- Review this policy when `.claude`, `.codex`, or the canonical canonical agent governance role/skill catalogs change.
- Record out-of-scope infra profile failures separately instead of expanding HAFE acceptance criteria silently.

## Traceability

- Declared parent: [Harness and Agent-first Engineering Outcome](../../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md) (`SPEC-0094`)
- Subject peers: [Guide](../guides/0004-harness-agent-first-engineering.md) (`GDE-0004`), [Runbook](../runbooks/0004-harness-agent-first-engineering.md) (`RUN-0004`)

## Related Documents

- [Operations index](../README.md)
- [Usage guide](../guides/0004-harness-agent-first-engineering.md)
