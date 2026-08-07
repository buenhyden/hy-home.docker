---
status: active
artifact_id: task:2026-08-07-agentic-research-pack-extension
artifact_type: task
parent_ids:
  - spec:123-agentic-engineering-audit-remediation
---

# Task: Agentic Research Pack Extension and Revalidation

## Overview

This Task extends the single canonical agentic research pack at
`docs/90.references/research/2026-07-05-agentic-research-pack-refresh/` with
three new Stage 90 reference leaves and revalidates the fifteen existing
leaves against current repository state and current official external sources.

The Task does not create a new dated research pack. Spec 122 previously
consolidated a duplicate dated pack and demoted
`2026-07-07-agentic-research-pack-update/` to `superseded` precisely to remove
that fragmentation. This Task preserves that outcome by extending the canonical
pack in place.

This Task is the approved successor Task requested by the previous
current-memory handoff. Opening it resolves the current-memory requirement for
an active Task with `draft` or `active` status and releases the lifecycle
boundary that paused
`task:2026-07-26-agent-governance-canonical-convergence`.

## Inputs

- User request to research and record harness engineering, loop engineering,
  workspace application criteria, Claude/Codex implementation status and common
  contract, spec-driven development, Docker Compose, infrastructure, SDLC,
  SDLC document roles, PRD/ARD/ADR roles, guide/incident/postmortem/policy/
  release/runbook roles, documentation architecture including Diataxis,
  LLM-WIKI, CI/CD, GitHub Actions, QA, security, AI agent catalogs, task-fit
  model selection, and memory hierarchy
- Baseline commit `19ee47270e3897073ab9a3f86dfd4cce0f4b2e74`
- Task open time `2026-08-07T12:36:55+09:00`
- Existing canonical pack: fifteen leaves and one folder-index README
- [Research category README](../../90.references/research/README.md)
- [Reference template](../../99.templates/templates/common/reference.template.md)
- [Documentation protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)

## Goals and Non-goals

### Goals

- Add three new canonical pack leaves that close verified coverage gaps:
  documentation architecture including Diataxis, the LLM-WIKI system, and the
  agent memory hierarchy.
- Revalidate the fifteen existing leaves on two axes: repository-local counted
  facts, and current official external sources.
- Update the pack README and the parent research README so structure, current
  references, and reading order match the new leaf set.
- Record exact verification commands and their observed results.

### Non-goals

- Creating a new Stage 03 specification or Stage 04 plan.
- Creating a new dated research pack directory.
- Deleting the superseded `2026-07-07-agentic-research-pack-update/` pack,
  which Spec 122 retains for link continuity and canonical mapping.
- Changing Stage 00 policy, Stage 03 specifications, Stage 05 procedures, or
  any runtime, Compose, provider, or CI configuration.
- Promoting any currently `unverified` claim without new observation.

## Scope and Change Boundaries

### Allowed Paths

- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/**`
- `docs/90.references/research/README.md`
- `docs/04.execution/tasks/2026-08-07-agentic-research-pack-extension.md`
- `docs/00.agent-governance/memory/current.md` (handoff refresh only)

### Forbidden Paths

- `docs/00.agent-governance/rules/**`, `scopes/**`, `providers/**`,
  `contracts/**`
- `docs/01.requirements/**`, `docs/02.architecture/**`, `docs/03.specs/**`
- `docs/05.operations/**`
- `docs/90.references/research/2026-07-07-agentic-research-pack-update/**`
- `infra/**`, `scripts/**`, `.github/**`, `.claude/**`, `.codex/**`,
  `.gemini/**`, `.agents/**`, `secrets/**`

### Compose Impact

None. This Task does not read, modify, start, stop, or validate any Compose
service, and does not inspect any secret value.

### Security Impact

None to runtime posture. The Task records security-governance references only.
No credential, token, private key, shell history, or raw log is written into
any artifact.

### Operations Impact

None. No runbook, incident, policy, or release procedure changes.

### Runtime Impact

None. No provider runtime surface, hook wrapper, or generated adapter changes.

## Approval Evidence

### Approval Source

Direct user instruction opening this session, which authorized sub-agent use,
authorized writing research output under `docs/90.references/research`, and
required logical-unit commits. Three structural decisions were then confirmed
by the user in-session:

1. Extend the existing canonical pack in place rather than create a new dated
   pack.
2. Revalidate on both axes: repository facts and full external sources.
3. Create a Stage 04 Task only, without a new Spec or Plan.

### Protected Surfaces

No protected surface is touched. No remote mutation, no push, no branch
protection change, no workflow change, and no live provider call beyond
read-only public documentation retrieval.

### Approval Boundary

The approval covers local documentation authoring and local commits on the
current branch. It does not cover push, remote mutation, runtime changes,
Compose operations, or execution of the controlled all-files pre-commit
wrapper.

### Rollback or Recovery

Every change is an ordinary tracked Markdown commit on the current branch.
Recovery is a `git revert` of the listed commits. No generated artifact,
runtime state, or external resource requires cleanup.

### Redaction Boundary

Only public documentation URLs, repository-relative paths, counted facts,
command names, and exit results are recorded. No secret value, token,
credential, private environment diagnostic, or raw log stream is written.

## Work Breakdown

| ID         | Unit                                                | Deliverable                                                                                      | Status      |
| ---------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------- |
| T-ARPE-001 | Open Task and fix scope                             | This Task document                                                                               | In progress |
| T-ARPE-002 | Read-only research and fact re-derivation           | Sub-agent findings for three new topics, workspace count drift, and external source revalidation | In progress |
| T-ARPE-003 | New leaf: documentation architecture                | `documentation-architecture.md`                                                                  | Not started |
| T-ARPE-004 | New leaf: LLM-WIKI system                           | `llm-wiki-system.md`                                                                             | Not started |
| T-ARPE-005 | New leaf: memory hierarchy                          | `memory-hierarchy.md`                                                                            | Not started |
| T-ARPE-006 | Revalidate harness, loop, and provider leaves       | Four updated leaves                                                                              | Not started |
| T-ARPE-007 | Revalidate SDLC and document leaves                 | Four updated leaves                                                                              | Not started |
| T-ARPE-008 | Revalidate quality, security, and automation leaves | Four updated leaves                                                                              | Not started |
| T-ARPE-009 | Revalidate baseline, Compose, and catalog leaves    | Three updated leaves                                                                             | Not started |
| T-ARPE-010 | Update pack README and research README              | Two updated indexes                                                                              | Not started |
| T-ARPE-011 | Verification and evidence closure                   | Command results and memory handoff refresh                                                       | Not started |

## Work Log

- `2026-08-07T12:36:55+09:00` — Task opened at baseline
  `19ee47270e3897073ab9a3f86dfd4cce0f4b2e74`.
- Coverage analysis completed before authoring: of twenty-two requested
  research topics, nineteen already have canonical pack coverage across
  fifteen leaves totalling 3,523 lines. Three topics have no coverage:
  Diataxis-based documentation architecture, the LLM-WIKI system, and the
  agent memory hierarchy. `grep -rn -i diataxis docs/` returned zero matches.
- Six read-only sub-agents dispatched for the three new topics, workspace
  count re-derivation, provider source revalidation, and standards source
  revalidation. Sub-agents do not write files; all authoring is performed by
  the controlling session to avoid concurrent-write conflicts.

## Verification Evidence

### Exact Commands

- `bash scripts/validation/check-repo-contracts.sh`
- `python3 scripts/validation/check-document-metadata.py --mode check-changed --base <safe-base>`
- `bash scripts/validation/check-doc-traceability.sh`
- `git diff --check`

### Expected Evidence

- Repository contract check passes for all changed target-stage documents.
- Changed-document metadata validation passes for the three new leaves, the
  fifteen revalidated leaves, both README indexes, and this Task.
- Traceability check resolves every new and updated cross-link.
- No whitespace or newline drift in the final diff.

## Review Evidence

### Specification Review Verdict

Pending.

### Quality Review Verdict

Pending.

### Review Findings and Disposition

Pending.

## Commit Ledger

### Commit Identity

Pending. Each logical unit lands as one Conventional Commit and is recorded
here with its short SHA when created.

### Commit Logical Unit

One commit per work-breakdown unit: Task open, each new leaf, each
revalidation group, index updates, and evidence closure.

### Commit Validation

Each commit is preceded by changed-file validation. Full repository contract
validation runs once at T-ARPE-011.

## Deferred and Blocked Items

### Deferred Items

- A typed domain-memory taxonomy with validator-enforced promotion, retention,
  archival, and deletion remains outside this Task. This Task records the
  research basis for it in `memory-hierarchy.md` but does not implement policy.
- Predecessor runtime drift for Keycloak, Traefik, PostgreSQL, Prometheus,
  Alloy, and Ollama versions remains routed to a separate approved runtime
  Task.

### Blocked Items

- Provider acceptance and entitlement, live comparative model evaluation, and
  authenticated remote GitHub enforcement remain unverified. This Task records
  them as unverified and does not promote them.

### Deferral Destination

- Domain-memory taxonomy: a future Stage 03 memory-governance specification.
- Runtime and Compose drift: a separate approved runtime Task.

## Related Documents

- [Canonical research pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Research category README](../../90.references/research/README.md)
- [Spec 123 audit remediation](../../03.specs/123-agentic-engineering-audit-remediation/spec.md)
- [Predecessor convergence Task](./2026-07-26-agent-governance-canonical-convergence.md)
- [Current project memory](../../00.agent-governance/memory/current.md)
- [Task checklists](../../00.agent-governance/rules/task-checklists.md)
