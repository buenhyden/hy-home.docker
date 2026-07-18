---
status: active
artifact_id: task:2026-07-18-target-surface-contract-convergence
artifact_type: task
parent_ids:
  - plan:2026-07-18-target-surface-contract-convergence
---

# Task: Target Surface Contract Convergence

## Overview

This is the execution/evidence ledger for Spec 133 and its six-unit Plan. It
records RED/GREEN results, protected-surface approval, manifest reviews,
destructive dispositions, logical commits, independent reviews, controlled
all-files QA, deviations, and closure. `not_run` is replaced only after the
corresponding command executes.

Execution branch: `codex/target-surface-contract-convergence`.
Execution worktree: `.worktrees/target-surface-contract-convergence`.
Immutable baseline: `32c40e11747bc0bd03789c24861d2e5d60c0e999`.

## Inputs

- Spec: `docs/03.specs/133-target-surface-contract-convergence/spec.md`
- Plan:
  `docs/04.execution/plans/2026-07-18-target-surface-contract-convergence.md`
- Parent: Spec 131 and the promoted Foundation manifest
- Work units: `T-TSC-001` through `T-TSC-006`
- Target roots: `.github`, `archive`, `examples`, `infra`, `projects`,
  `scripts`, `secrets`, and `tests`
- Canonical Stage 99 metadata, README, archive, and corpus contracts
- Canonical July 5 research and audit packs
- Controlled QA: `scripts/validation/run-agent-precommit-all-files.sh`

## Goals and Non-goals

Goals:

- classify the complete target corpus before mutation;
- activate distinct content/SDLC archive and typed example/README rules;
- retire approved InfluxDB 2 source and active direct consumers;
- remove only consumer-proven duplicate and phantom surfaces;
- activate deterministic static QA/CI regressions; and
- close with reviews, generated freshness, logical commits, and controlled QA.

Non-goals:

- live data migration, service startup, deployment, release, or remote GitHub
  mutation;
- secret-value access or raw rendered/log evidence;
- bulk README normalization or historical wording deletion;
- push, PR, merge, or worktree deletion without later explicit authority.

## Scope and Change Boundaries

Allowed paths are the eight target roots, direct Stage 00/01/02/03/04/05/90/99
consumers named in the Plan, `.env.example`, `.pre-commit-config.yaml`, and
`.prettierignore`. Generated changes are limited to canonical owners.

Forbidden actions: user-global config; credentials/tokens/private keys/auth
files/shell history/raw logs; service startup; live queries/data movement;
deployment/release/remote mutation; unmanifested deletion; direct all-files
pre-commit; `--no-verify`; history rewriting; destructive Git cleanup.

Compose impact: source-only InfluxDB 2 removal and unused k6/Locust v2 wiring
removal. InfluxDB 3 remains. No service starts.

Security impact: contract, workflow, secret-metadata, and evidence hardening;
no secret value or runtime security resource changes.

Operations impact: current InfluxDB, k6, Locust, OpenSearch, and SeaweedFS
guidance aligns with static source; no procedure executes.

Runtime impact: approved tracked Compose source changes only; live acceptance
remains unverified.

## Approval Evidence

Approval source:

- The user approved destructive contract/governance remediation, protected
  local surfaces, external research, logical commits, and Subagent-Driven work.
- The user directed deprecated implementations to be removed and approved
  InfluxDB 2 server/direct-consumer removal.
- The user approved Spec 133 and continued execution.

Protected surfaces: Stage 99 contracts/templates, Stage 00 routing, Stage 01-05
truth, workflows, Compose source, validators, secret metadata, research/audit,
and generated indexes may change only as named in the Plan.

Approval boundary: local tracked changes, read-only discovery/research, static
validation, commits, and final controlled wrapper are authorized. Live runtime,
data, remote, push, PR, merge, and worktree deletion are excluded.

Rollback/recovery: revert logical commits in reverse order and regenerate only
owned output. The pinned Git objects preserve withdrawn/archive source.

Redaction boundary: record commands, exit states, safe paths, counts, Git
objects/commits, approved generated hashes, and verdicts only. Never record
values from `secrets/**`, expanded Compose values, or raw logs.

## Work Breakdown

| Work unit | Responsibility | State |
| --- | --- | --- |
| T-TSC-001 | Archive, metadata, wave, and manifest foundation | not_run |
| T-TSC-002 | README, typed example, and Storybook cleanup | not_run |
| T-TSC-003 | Root content archive provenance migration | not_run |
| T-TSC-004 | Deprecated runtime and duplicate disposition | not_run |
| T-TSC-005 | Validator, QA routing, and static CI enforcement | not_run |
| T-TSC-006 | Research, audit, generated evidence, and closure | not_run |

## Work Log

| Date | Work unit | Agent role | Result |
| --- | --- | --- | --- |
| 2026-07-18 | Planning | Controller | Converted approved Spec 133 into a six-unit Plan and this evidence ledger. |
| 2026-07-18 | Planning discovery | Three read-only subagents | Contract/profile, corpus/runtime, and QA/evidence file maps were source-corroborated. No target implementation changed. |
| 2026-07-18 | Planning review | Independent read-only reviewer | Initial review found one Critical ordering defect and four Important ambiguities: target tests were created after first use, Spec status lagged Plan status, workflow test ownership/artifact policy was conditional, schema v2 was underspecified, and 74 manual versus 75 automated README coverage was conflated. |
| 2026-07-18 | Planning remediation | Controller | Moved target regression creation to Task 2, fixed Task 5 to the existing workflow owner, retained the artifact-upload prohibition, activated Spec 133, defined schema v2/CLI behavior, and separated automated 75-file from manual 74-file evidence. Fresh re-review is required before implementation. |
| 2026-07-18 | Planning re-review | Fresh read-only reviewer | No Critical remained; four Important precision gaps remained in Task 4 test ownership, the Spec body status, workflow-owner wording, and wave-only manifest/summary path resolution. |
| 2026-07-18 | Planning re-review remediation | Controller | Added the Task 4 regression path, aligned both Spec status surfaces, removed the conditional workflow owner, and bound wave-only read checks to registry manifest/summary paths while retaining explicit-output writes. Fresh terminal planning review remains required. |
| 2026-07-18 | Terminal planning review | Fresh read-only reviewer | Spec/Plan/Task status, schema v2/CLI, README evidence boundary, protected constraints, and task order passed. Two Important findings remained: duplicate workflow-policy ownership and non-fail-closed absence scans. |
| 2026-07-18 | Terminal planning remediation | Controller | Kept artifact-upload prohibition solely in the existing repository-contract owner and replaced both plain/masked grep commands with explicit fail-closed absence assertions. Final zero-finding review remains required before implementation. |
| 2026-07-18 | Zero-review follow-up | Fresh read-only reviewer | Workflow ownership passed. One Important shell edge remained because grep exit codes above 1 were treated like the expected no-match code 1. |
| 2026-07-18 | Zero-review remediation | Controller | Both absence scans now capture the false-branch status, accept only no-match code 1, and propagate every execution error. Final confirmation remains required. |
| 2026-07-18 | Planning terminal confirmation | Independent read-only reviewer | PASS and READY with C0/I0/M0. Both absence scans fail on matches, pass only on no-match code 1, propagate execution errors, and remain correct under `set -e`; workflow policy has one canonical owner. |
| 2026-07-18 | Linked-worktree baseline repair | Controller | After planning commit `5c4e1d55`, the new Plan became a tracked consumer of the promoted frontmatter contract and exposed one stale Foundation consumer row plus three generated-owner freshness gaps that pre-commit index state had hidden. Added only the exact Plan consumer and regenerated the Foundation summary, LLM Wiki index/coverage, and metadata inventory before any implementation task. |

## Verification Evidence

| Work unit | RED evidence | GREEN/aggregate evidence | Result |
| --- | --- | --- | --- |
| T-TSC-001 | not_run | not_run | not_run |
| T-TSC-002 | not_run | not_run | not_run |
| T-TSC-003 | not_run | not_run | not_run |
| T-TSC-004 | not_run | not_run | not_run |
| T-TSC-005 | not_run | not_run | not_run |
| T-TSC-006 | not_run | not_run | not_run |

Prospective commands and expected results live in the Plan. Record actual exit
state, bounded result, and skip rationale here without raw logs or secret data.

## Controlled Agent Pre-commit Evidence

- Command: not_run; Task 6 only.
- Allowed prefixes: not_finalized; must equal actual changed surfaces.
- Hook exit: not_run.
- Snapshot result: not_run.
- Observation boundary: Git-visible, non-ignored repository status only; the
  wrapper does not observe ignored or outside-worktree writes.
- Before/after/changed/unexpected path sets: not_run.
- Disposition: not_run.

## Review Evidence

| Work unit | Self-review | Specification review | Quality review | Findings/disposition |
| --- | --- | --- | --- | --- |
| T-TSC-001 | not_run | not_run | not_run | not_run |
| T-TSC-002 | not_run | not_run | not_run | not_run |
| T-TSC-003 | not_run | not_run | not_run | not_run |
| T-TSC-004 | not_run | not_run | not_run | not_run |
| T-TSC-005 | not_run | not_run | not_run | not_run |
| T-TSC-006 | not_run | not_run | not_run | not_run |
| Whole branch | N/A | not_run | not_run | exact final range pending |

Reviewers are separate fresh agents. A destructive row cannot pass until both
independent verdicts and all finding dispositions are recorded.

## Commit Ledger

| Work unit | Intended logical commit | Identity | Validation |
| --- | --- | --- | --- |
| Planning | `docs(plan): define target surface convergence execution` | `5c4e1d55` | metadata 10/0; traceability 46/0; alignment 656/5,251/141/0; aggregate 0 before the tracked-consumer baseline recheck |
| Planning repair | `docs(plan): repair tracked planning consumers` | pending | promoted manifest and generated freshness recheck pending |
| T-TSC-001 | `feat(docs): establish target corpus migration contracts` | pending | not_run |
| T-TSC-002 | `docs(examples): align sample and storybook contracts` | pending | not_run |
| T-TSC-003 | `docs(archive): preserve Windows network note provenance` | pending | not_run |
| T-TSC-004a | `refactor(infra): retire InfluxDB 2 compatibility` | pending | not_run |
| T-TSC-004b | `chore(infra): remove unconsumed duplicate scaffolds` | pending | not_run |
| T-TSC-005 | `feat(qa): enforce target surface contracts` | pending | not_run |
| T-TSC-006 | `docs(execution): close target surface convergence` | pending | not_run |

Material review fixes and generated-only fallout receive additional rows.

## Deferred and Blocked Items

- Live InfluxDB data/query migration, service acceptance, deployment, release,
  remote enforcement, secrets, and runtime security remain deferred.
- SeaweedFS security scaffold activation remains a separate approved runtime
  and security chain.
- Any executable InfluxDB 2 data/query consumer blocks T-TSC-004 and routes to
  a new runtime/data Spec and Plan.
- Remote/local CI differences remain `needs_revalidation` unless dated
  read-only evidence is actually collected; no remote repair occurs.

Deferral destination: a new Stage 03 Spec and Stage 04 Plan/Task chain for the
specific runtime, data, security, deployment, or remote surface.

## Related Documents

- [Spec 133](../../03.specs/133-target-surface-contract-convergence/spec.md)
- [Implementation Plan](../plans/2026-07-18-target-surface-contract-convergence.md)
- [Spec 131](../../03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md)
- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Canonical audit pack](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Task checklists](../../00.agent-governance/rules/task-checklists.md)
