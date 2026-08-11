---
status: archived
artifact_id: plan-0050
artifact_type: archive
parent_ids: []
archived_from: docs/04.execution/plans/2026-05-26-workspace-audit-gap-closure.md
archived_at: 2026-08-11
archive_reason: "Move baseline completed source to stable typed target docs/98.archive/changes/chg-0050-workspace-audit-gap-closure/plan.md; migrate 6 resolved inbound link(s) with it."
archive_disposition: evidence-preserve
archived_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
archived_blob: 2da189b37a52ac2e1b42da1a494d82fa3c70d734
preservation_class: git-history
---
<!-- Target: docs/04.execution/plans/2026-05-26-workspace-audit-gap-closure.md -->

# Workspace Audit Gap Closure Plan

## Overview

This document is the implementation plan for the 2026-05-26 workspace audit second session. It defines low-risk changes, verification criteria, and deferred items for closing newly identified gaps (GAP-NEW-03 through GAP-NEW-10) from the previous audit session (`2026-05-26-workspace-audit.md`).

## Context

After the first audit session completed 18 skills, env/secrets comparison, and stage README reinforcement, the second session found additional gaps:

- Missing `UserPromptSubmit` event in `.codex/hooks.json` (hook parity contract violation)
- Skill count mismatch in `.claude/CLAUDE.md` (11 vs actual 18)
- Missing stage mappings for 7 new skills in `stage-authoring-matrix.md`
- Missing skill count statement in AGENTS.md section 3
- Missing Stage Handoff section in `docs/90.references/README.md`
- Drift in `infra/tech-stack.versions.json` (16 components, Dependabot PR not reflected)
- Stale `docs/90.references/llm-wiki/llm-wiki-index.md`

## Goals & In-Scope

- **Goals**: Immediately close low-risk gaps GAP-NEW-05 through GAP-NEW-07 and GAP-NEW-09; record the GAP-NEW-03 block.
- **In Scope**: `.codex/hooks.json`, `AGENTS.md`, `stage-authoring-matrix.md`, `docs/90.references/README.md`, `infra/tech-stack.versions.json`, and LLM Wiki regeneration.

## Non-Goals & Out-of-Scope

- **Non-goals**: Docker runtime behavior changes, secret value changes, or `.env` value changes.
- **Out of Scope**: GAP-NEW-08 (ops orphan file classification), GAP-NEW-10 (pre-commit integration), deferred as medium/high risk.

## Work Breakdown

| Task              | Description                           | Files / Docs Affected                  | Validation Criteria                  |
| ----------------- | ------------------------------------- | -------------------------------------- | ------------------------------------ |
| PLN-001           | Add `UserPromptSubmit` hook parity | `.codex/hooks.json`                    | All 7 events exist; JSON is valid |
| PLN-002           | State skill count | `AGENTS.md`                            | "18 skills" string exists |
| PLN-003           | Add Stage Authoring Matrix skills section | `stage-authoring-matrix.md`            | Section 4 exists with 7 skill mappings |
| PLN-004           | Add 90.references Stage Handoff section | `docs/90.references/README.md`         | "Stage Handoff" section exists |
| PLN-005           | Correct tech-stack drift | `infra/tech-stack.versions.json`       | `check-repo-contracts.sh` failures=0 |
| PLN-006           | Regenerate LLM Wiki index | `docs/90.references/llm-wiki/llm-wiki-index.md` | `check-repo-contracts.sh` failures=0 |
| PLN-007 (BLOCKED) | Correct `.claude/CLAUDE.md` skill count | `.claude/CLAUDE.md`                    | Blocked; user manual edit required |

## Verification Plan

| ID      | Level      | Description                     | Command / How to Run                                 | Pass Criteria            |
| ------- | ---------- | ------------------------------- | ---------------------------------------------------- | ------------------------ | ----------- |
| VAL-001 | Structural | repo contracts                  | `bash scripts/validation/check-repo-contracts.sh`    | failures=0               |
| VAL-002 | Structural | doc traceability                | `bash scripts/validation/check-doc-traceability.sh`  | failures=0               |
| VAL-003 | Structural | Compose validation              | `bash scripts/validation/validate-docker-compose.sh` | No errors                |
| VAL-004 | Structural | UserPromptSubmit in Codex hooks | `jq '.hooks                                          | keys' .codex/hooks.json` | 7 keys confirmed |

## Risks & Mitigations

| Risk                                   | Impact | Mitigation                                                   |
| -------------------------------------- | ------ | ------------------------------------------------------------ |
| `.claude/CLAUDE.md` self-modification is blocked | Low    | Record GAP-NEW-03 block and tell the user manual correction is required |
| tech-stack.versions.json drift recurs | Medium | Manual JSON update is needed when Dependabot PRs merge; future ADR recommended |

## Completion Criteria

- [x] GAP-NEW-05: stage-authoring-matrix.md Section 4 added
- [x] GAP-NEW-06: AGENTS.md skill count stated
- [x] GAP-NEW-07: 90.references Stage Handoff section added
- [x] GAP-NEW-09: `.codex/hooks.json` UserPromptSubmit added
- [x] tech-stack drift closure (PLN-005, PLN-006)
- [ ] GAP-NEW-03: `.claude/CLAUDE.md` manual correction (user pending)
- [ ] GAP-NEW-08 (deferred): document ops orphan file tier classification
- [ ] GAP-NEW-10 (deferred): integrate pre-commit validation script

## Related Documents

- **Previous Audit Plan**: [2026-05-26-workspace-audit](../chg-0051-workspace-audit/plan.md)
- **Previous Audit Task**: [2026-05-26-workspace-audit task](../chg-0051-workspace-audit/task.md)
- **Gap Closure Task**: [2026-05-26-workspace-audit-gap-closure task](task.md)
- **Operations**: [Operations index](../../../05.operations/README.md)
