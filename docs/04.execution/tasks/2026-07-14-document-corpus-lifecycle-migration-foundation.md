---
status: active
artifact_id: task:2026-07-14-document-corpus-lifecycle-migration-foundation
artifact_type: task
parent_ids:
  - plan:2026-07-14-document-corpus-lifecycle-migration-foundation
---

# Task: Document Corpus Lifecycle Migration Foundation

## Overview

This Task is the durable execution ledger for Spec 131 and its six-unit
Foundation Plan. It records the approved baseline, bounded file responsibility,
fresh-agent assignments, RED/GREEN commands, independent reviews, logical
commits, generated evidence, controlled all-files result, and final closure.

Planning evidence was created on branch
codex/document-corpus-lifecycle-migration in linked worktree
.worktrees/document-corpus-lifecycle-migration. Implementation results remain
not run until recorded under the matching work unit.

## Inputs

- Spec: docs/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md
- Plan: docs/04.execution/plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md
- Approved baseline: e00e1483
- Foundation work units: T-DCLM-001 through T-DCLM-006
- Current canonical audit:
  docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md
- Machine metadata owner:
  docs/99.templates/support/document-metadata-profiles.yaml
- Controlled QA owner:
  scripts/validation/run-agent-precommit-all-files.sh

## Goals and Non-goals

Goals:

- establish the migration, archive, retention, manifest, directory-budget, and
  review-signal control plane;
- add tested metadata and lifecycle validators with deterministic safe output;
- align Stage 00, Stage 98, Stage 99, local QA, and tracked CI definitions;
- publish the approved Foundation manifest and generated evidence;
- close with independent task and whole-branch reviews plus controlled
  all-files evidence.

Non-goals:

- migrate the active, operations, historical, archive, reference, generated,
  or README corpus;
- move Stage 04 leaves into year partitions;
- create immutable snapshot payloads;
- change Compose, infrastructure, deployment, secrets, provider-global
  settings, model policy, remote GitHub state, releases, or environments.

## Scope and Change Boundaries

Allowed authored paths:

- docs/00.agent-governance rules and progress memory directly required by
  Foundation;
- Spec 131 and its Stage 03 routing;
- this Plan, this Task, and existing Stage 04 routing;
- docs/90.references data/governance lifecycle evidence, canonical generated
  outputs, and routing;
- docs/98.archive/README.md only;
- Stage 99 support contracts and the common archive template;
- .github/workflows/document-corpus-lifecycle.yml;
- .pre-commit-config.yaml existing repo-contract routing only;
- scripts/README.md and Foundation validation/QA scripts;
- tests/validation focused Foundation tests.

Prohibited paths and actions:

- existing Stage 01 through Stage 05 corpus leaves;
- all 20 existing Stage 98 tombstones and any archive snapshot payload;
- broad Stage 90 authored corpus rewrites;
- _workspace diagnostics, local logs, auth files, tokens, credentials, private
  keys, shell history, raw logs, or secret values;
- runtime Compose, infra, deployment, environment, release, provider-global,
  or remote GitHub mutation;
- direct pre-commit run --all-files, --no-verify, history rewriting, or
  destructive Git cleanup.

Compose impact: none.

Security impact: validation and redaction hardening only. No credential,
secret-store, identity, network, runtime policy, or security-resource change.

Operations impact: documentation lifecycle governance only. No service,
incident, release, deployment, or on-call behavior changes.

Runtime impact: none. The tracked workflow is read-only quality automation and
does not deploy or mutate third-party state.

## Approval Evidence

Approval source:

- The user approved the hybrid archive model: provenance tombstone plus
  immutable Git commit/blob by default, with checksum-backed full snapshots
  only for audit, legal, or evidence-preserve cases.
- The user approved the six-package program and explicitly instructed
  continued implementation.
- The user approved Subagent-Driven execution with a fresh implementation agent
  and separate review agents.

Protected surfaces:

- Stage 00 and Stage 99 contracts may be changed within the approved
  Foundation scope.
- Existing archive tombstones, snapshot payloads, runtime surfaces, secrets,
  provider-global configuration, and remote GitHub state remain protected.

Approval boundary:

- Foundation contracts, validators, tests, local QA routing, and tracked
  read-only workflow definitions are authorized.
- Later Waves A through E, snapshot admission, runtime work, and remote
  mutation require their own approved Spec or explicit user approval.
- Local merge to main is excluded until finishing and separate user approval.

Rollback or recovery:

- Revert one logical Foundation task commit range in reverse order.
- Regenerate only derived outputs owned by the reverted task.
- Never use git reset --hard or rewrite branch history.

Redaction boundary:

- Evidence records commands, exit codes, stable finding codes, bounded paths,
  counts, and Git object identities.
- It never records body payloads, snapshot bytes, secret values, tokens,
  credentials, auth files, private keys, shell history, or raw logs.

## Work Breakdown

| Work unit | Responsibility | State |
| --- | --- | --- |
| T-DCLM-001 | Machine migration contract and static archive metadata | Not run |
| T-DCLM-002 | Lifecycle companion, Git provenance, deterministic data | Not run |
| T-DCLM-003 | Human contracts, archive template, Stage 98/00 routing | Not run |
| T-DCLM-004 | Repository contracts, local QA, tracked workflow | Not run |
| T-DCLM-005 | Foundation manifest and generated evidence | Not run |
| T-DCLM-006 | Full QA, wrapper, whole-branch review, closure | Not run |

## Work Log

| Date | Work unit | Agent role | Result |
| --- | --- | --- | --- |
| 2026-07-14 | Planning | Controller | Spec 131 approved and activated; Plan and Task evidence shell authored. |

Each implementation row will record the fresh agent identity, exact bounded
assignment, changed paths, self-review, deviations, and handoff. Reviewer rows
will be separate from implementation rows.

## Verification Evidence

Planned exact command families:

- metadata registry and changed/new checks;
- focused metadata and lifecycle unittest suites;
- Python compile and Bash syntax checks;
- Foundation contract, manifest, provenance, budget, duplicate, and ledger
  checks;
- repository contracts, document traceability, and implementation alignment;
- canonical security, audit-matrix, LLM Wiki, and metadata-inventory
  generation/check modes;
- Graphify refresh and advisory health corroboration;
- controlled all-files wrapper from a clean linked worktree.

Expected evidence:

- RED before each behavior implementation and GREEN after;
- zero Foundation blocking findings;
- legacy full-corpus debt reported as advisory until Wave E;
- deterministic write/check equality;
- no payload leakage or unexpected changed path;
- clean Git status after final closure.

Actual evidence: not run.

Verification results: not run.

## Controlled Agent Pre-commit Evidence

Controlled wrapper command:

scripts/validation/run-agent-precommit-all-files.sh with this tracked Task and
the explicit allow-prefix set in the Plan.

Allowed prefixes:

- .github/workflows/document-corpus-lifecycle.yml
- .pre-commit-config.yaml
- docs/00.agent-governance/rules
- docs/00.agent-governance/memory/progress.md
- docs/03.specs/131-document-corpus-lifecycle-migration-foundation
- docs/03.specs/README.md
- docs/04.execution
- docs/90.references/data/governance/document-corpus-lifecycle
- docs/90.references/data/governance/audit-implementation-matrix.md
- docs/90.references/data/security/security-automation-readiness.md
- docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
- docs/90.references/llm-wiki/llm-wiki-index.md
- docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
- docs/98.archive/README.md
- docs/99.templates/support
- docs/99.templates/templates/common
- scripts/README.md
- scripts/validation/check-document-corpus-lifecycle.py
- scripts/validation/check-document-metadata.py
- scripts/validation/check-repo-contracts.sh
- scripts/validation/recommend-qa-gates.sh
- scripts/validation/run-local-qa-gates.sh
- tests/validation/test_document_metadata.py
- tests/validation/test_document_corpus_lifecycle.py

Exit status: not run.

Snapshot result: not run.

Observation boundary: Git-visible path sets and safe hook summaries only.

Path sets: not run.

Disposition: not run.

## Review Evidence

Implementation review verdict: not run for T-DCLM-001 through T-DCLM-006.

Specification review verdict: not run for T-DCLM-001 through T-DCLM-006.

Quality review verdict: not run for T-DCLM-001 through T-DCLM-006.

Review findings and disposition: none recorded before implementation.

## Commit Ledger

Planning baseline:

- 15fdac5d — docs(spec): define corpus lifecycle migration foundation
- 313c36ed — docs(generated): refresh corpus design indexes
- c6b3d9bc — docs(spec): clarify canonical stage routing

Foundation logical commits: none recorded before implementation.

Commit validation: each entry must name its work unit, review verdicts, focused
GREEN commands, and generated fallout before closure.

## Deferred and Blocked Items

Deferred:

- Spec 132 — active SDLC graph migration;
- Spec 133 — operations document migration;
- Spec 134 — completed/superseded evidence and Stage 04 year partition;
- Spec 135 — existing tombstone provenance and approved snapshots;
- Spec 136 — Stage 90, README, generated, _workspace, .github, and final
  full-corpus enforcement.

Blocked items: none at planning time.

Deferral destination: the named later-wave Specs and their separately approved
Plans/Tasks.

## Related Documents

- [Foundation Spec](../../03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md)
- [Foundation Plan](../plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md)
- [Stage 04 Tasks](./README.md)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [Metadata registry](../../99.templates/support/document-metadata-profiles.yaml)
- [Controlled all-files wrapper](../../../scripts/validation/run-agent-precommit-all-files.sh)
