---
status: active
---

<!-- Target: docs/90.references/data/governance/gap-to-stage-routing.md -->

# Reference: Gap-to-Stage Routing

## Overview

This reference summarizes the Stage 00 gap-to-stage routing contract and the
local advisory recommender that helps classify audit, review, validation, and
agent-handoff gaps.

## Purpose

Provide a quick, source-linked routing reference so that discovered gaps are
assigned to one canonical owner before edits begin.

## Repository Role

This document supports audit and validation workflows. It does not replace
`docs/00.agent-governance/rules/documentation-protocol.md`, create policy, or
authorize changes to runtime, remote, credential, secret, or provider surfaces.

## Scope

### In Scope

- Canonical gap owner categories from Stage 00 documentation protocol.
- Advisory use of `scripts/validation/recommend-gap-routing.sh`.
- Examples for text and path based routing suggestions.

### Out of Scope

- Automatic edits to the suggested owner.
- Runtime, CI, provider, secret, credential, deployment, or remote mutation.
- Replacing human review for ambiguous gaps.

## Definitions / Facts

- **Gap**: an audit, review, validation, or handoff finding that needs a
  canonical owner before edits.
- **Canonical owner**: the first stage or surface responsible for deciding the
  change, such as Stage 00 governance, Stage 03 specs, Stage 04 tasks, or
  Stage 90 references.
- **Advisory recommendation**: a non-mutating suggestion. The user or agent must
  still confirm the owner before editing.

## Routing Reference

| Gap Type | Canonical Owner |
| --- | --- |
| Governance, provider behavior, agent execution rule, approval boundary, or memory contract | `docs/00.agent-governance/` |
| User value, scope, acceptance criteria, or product intent | `docs/01.requirements/` |
| Architecture shape, major technical decision, quality attribute, or tradeoff | `docs/02.architecture/` |
| Interface, data model, service contract, agent contract, or verification contract | `docs/03.specs/` |
| Work sequencing, approval gates, rollback strategy, or implementation backlog | `docs/04.execution/plans/` |
| Completed work evidence, validation output, deviation, or implementation disposition | `docs/04.execution/tasks/` |
| Operator usage, operational control, recovery procedure, incident, or postmortem | `docs/05.operations/` |
| Source-backed research, audit snapshot, data reference, learning note, or LLM navigation | `docs/90.references/` |
| Obsolete or implementation-conflicting document that must leave the active chain | `docs/98.archive/` |
| Template, frontmatter, lifecycle, or authoring contract | `docs/99.templates/` |
| Runtime, secret value, credential, remote GitHub mutation, deployment, or uncertain implementation drift | Stage 04 task/audit gap first |

## Advisory Tool Contract

Use the recommender to classify descriptions or related paths without mutating
the repository:

```bash
bash scripts/validation/recommend-gap-routing.sh --text "runbook recovery procedure is missing rollback evidence"
bash scripts/validation/recommend-gap-routing.sh --files docs/03.specs/108-compose-profile-service-coverage-snapshot/spec.md
bash scripts/validation/recommend-gap-routing.sh --list
```

The script parses the Stage 00 routing table from
`docs/00.agent-governance/rules/documentation-protocol.md` and applies simple
path-prefix and keyword heuristics. Low-confidence output means the gap should
be recorded as a Stage 04 task or audit gap before editing.

## Source Rules

- Treat Stage 00 documentation protocol as the source of truth.
- Keep this reference synchronized when Stage 00 gap routing changes.
- Do not include secret values, credentials, tokens, private keys, shell
  history, raw logs, or local auth output in recommender input examples.

## Sources

- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - canonical gap-to-stage routing table.
- [Task checklists](../../../00.agent-governance/rules/task-checklists.md) - pre-task and gap routing checklist.
- [Gap routing recommender](../../../../scripts/validation/recommend-gap-routing.sh) - local advisory classifier.
- [Automation candidates](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md) - `AEA-AUTO-004` implementation context.

## Maintenance

- **Owner**: Documentation Specialist / QA Engineer.
- **Review Cadence**: Review after Stage 00 documentation protocol changes.
- **Update Trigger**: Update when routing categories, canonical owner paths, or
  recommender behavior changes.

## Related Documents

- [governance data index](./README.md)
- [reference data index](../README.md)
- [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- [automation candidates](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
