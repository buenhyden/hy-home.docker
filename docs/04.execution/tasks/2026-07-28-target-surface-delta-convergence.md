---
status: draft
artifact_id: task:2026-07-28-target-surface-delta-convergence
artifact_type: task
parent_ids:
  - spec:135-target-surface-delta-convergence
  - plan:2026-07-28-target-surface-delta-convergence
---

# Task: Target Surface Delta Convergence

## Overview

This ledger records actual implementation, verification, commit, disposition,
review, and closure evidence for Spec 135. The implementation design and
expected commands remain in the
[Plan](../plans/2026-07-28-target-surface-delta-convergence.md).

Evidence in this ledger is bounded and value-free. It must not contain secret
values, credentials, tokens, auth files, shell history, raw workflow logs,
unbounded command output, or inferred remote failure causes.

## Inputs

- [Spec 135](../../03.specs/135-target-surface-delta-convergence/spec.md)
- [Implementation Plan](../plans/2026-07-28-target-surface-delta-convergence.md)
- Feature base
  `19ee47270e3897073ab9a3f86dfd4cce0f4b2e74`
- Spec 133 comparison commit
  `63039b5b0b20c99a10aae7162627afefcd7a1d8b`
- Isolated branch `feat/135-target-surface-delta-convergence`
- Isolated worktree
  `.worktrees/target-surface-delta-convergence`
- Primary roots `.github`, `archive`, `examples`, `infra`, `projects`,
  `scripts`, `secrets`, and `tests`

## Goals and Non-goals

The goal is to close TSDC-001 through TSDC-017 with six logical commits,
complete successor-delta classification, whole-surface validation, document
and static-version convergence, typed local workflow/QA controls, reconciled
canonical evidence, and two independent reviews per task.

Remote mutation, live Compose or deployment work, push, pull request, merge,
workflow dispatch, secret-value access, raw-log access, and direct all-files
pre-commit are not authorized by this ledger.

## Scope and Change Boundaries

Primary changes are restricted to the eight target roots. Direct-impact paths
are allowed only when an approved target change would otherwise leave a Stage
00, Stage 04, Stage 05, Stage 90, Stage 99, validator, generator, test, or
current-memory consumer false or broken.

Native file formats remain native. README files remain path-profiled and
frontmatter-free by default. Typed Markdown uses only registered metadata.
Root content archives and Stage 98 SDLC archives remain distinct. Secret work
is limited to tracked names, paths, and redacted metadata.

Static registry and documentation synchronization to existing Compose image
declarations is in scope. Starting, stopping, probing, deploying, rebuilding,
or otherwise mutating services is out of scope.

Tracked GitHub workflow, ruleset-desire, validator, and governance changes are
in scope after Plan approval. Remote GitHub configuration and execution remain
read-only observation only.

## Approval Evidence

- The user approved the investigation and successor Spec 135 design.
- The user explicitly allowed subagents and selected Subagent-Driven
  execution.
- The user selected local tracked GitHub changes with read-only remote
  observation; remote synchronization requires separate approval.
- The user authorized destructive and protected local changes within the
  approved Plan boundary, subject to consumer, provenance, rollback, tests,
  and review.
- Approval of this exact Plan and Task ledger is pending. No implementation
  task may start until that approval is recorded.
- No current approval authorizes
  `scripts/validation/run-agent-precommit-all-files.sh`. Any future approval
  is one exact attempt from one clean committed checkpoint.

Rollback is one logical task commit at a time after exact-range review. It
never uses `git reset --hard`, discards unrelated user changes, or attempts a
remote/runtime rollback for surfaces this wave does not mutate.

## Work Breakdown

| Task ID | Description | Type | Requirements | Validation owner | Implementation owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| T-TSDC-001 | Establish successor manifest and whole-surface contract | contract/data | TSDC-001–003, 007, 009 | delta contract tests and advisory checker | fresh implementer after Plan approval | pending |
| T-TSDC-002 | Converge README, typed example, archive, and secret inventory | docs/governance | TSDC-003–009 | metadata, target, links, alignment | fresh implementer after Task 1 review | pending |
| T-TSDC-003 | Reconcile static versions and verified active lifecycle drift | infra-support/docs | TSDC-003, 008–009 | version, hardening, supply-chain checks | fresh implementer after Task 2 review | pending |
| T-TSDC-004 | Type workflow triggers, dependencies, and QA ownership | CI/security | TSDC-010–014 | workflow contract and CI script tests | fresh implementer after Task 3 review | pending |
| T-TSDC-005 | Reconcile canonical audit and remote observation evidence | evidence/docs | TSDC-015–016 | audit semantic, generators, links | fresh implementer after Task 4 review | pending |
| T-TSDC-006 | Promote blocking enforcement and close reviews | closure/QA | TSDC-001–017 | final ladder and whole-branch reviews | fresh closure implementer after Tasks 1–5 | pending |

Tasks are serial at their commit/review boundaries. A task may not advance
until its implementation is committed, the Task ledger is current, and a
distinct specification reviewer plus a distinct quality/security reviewer
have no unresolved Critical or Important findings.

## Work Log

| Date | Unit | Actor | Evidence summary |
| --- | --- | --- | --- |
| 2026-07-28 | Bootstrap | Controller | Loaded Stage 00 bootstrap, provider, and memory contracts; inspected root and isolated-worktree state; kept root `main` clean. |
| 2026-07-28 | Discovery | Controller plus read-only inventory agents | Counted 474 target paths and 82 Markdown/MDX files; identified 102 post-closure target changes, 11 exact heading drifts, 26 shared-agent-policy README copies, one duplicated data README purpose, one typed example ambiguity, one redacted secret inventory omission, six static version drifts, and CI trigger/dependency gaps. |
| 2026-07-28 | External verification | Controller | Verified official GitHub workflow/security/protection, Actions runtime, pre-commit, YAML frontmatter, CommonMark, and GFM sources. Confirmed the pinned pre-commit composite uses mutable `actions/cache@v4`. |
| 2026-07-28 | Remote observation | Controller | Read sanitized repository/run/protection metadata only. Observed 12 remote required contexts versus 16 local desired IDs and two recent failed runs; root causes remain unverified. No remote state changed. |
| 2026-07-28 | Spec | Controller | Wrote and committed Spec 135 as `e828745a`; scoped metadata, Markdown, alignment, and diff checks passed. User approved continuing from the Spec. |
| 2026-07-28 | Plan/Task draft | Controller | Activated the approved Spec and drafted this six-task TDD/Subagent-Driven Plan and evidence ledger. Implementation remains pending exact Plan approval. |

## Verification Evidence

### Planning verification

| Check | Expected | Actual |
| --- | --- | --- |
| Spec 135 metadata | one selected document, zero violations | Passed before Plan drafting |
| Spec 135 Markdown | zero errors | Passed before Plan drafting |
| Document implementation alignment | zero failures | Passed before Plan drafting |
| `git diff --check` | zero whitespace errors | Passed before Plan drafting |
| Plan/Task metadata and Markdown | zero failures | Passed: changed metadata selected 3 with 0 violations; explicit three-file markdownlint reported 0 errors |
| Plan/Task cross-links | zero failures | Passed: traceability and implementation alignment reported 0 failures |

### Task execution evidence

| Task | RED evidence | GREEN evidence | Aggregate evidence | Result |
| --- | --- | --- | --- | --- |
| T-TSDC-001 | Not run — Plan approval pending | Not run — Plan approval pending | Not run — Plan approval pending | pending |
| T-TSDC-002 | Not run — Task 1 review pending | Not run — Task 1 review pending | Not run — Task 1 review pending | pending |
| T-TSDC-003 | Not run — Task 2 review pending | Not run — Task 2 review pending | Not run — Task 2 review pending | pending |
| T-TSDC-004 | Not run — Task 3 review pending | Not run — Task 3 review pending | Not run — Task 3 review pending | pending |
| T-TSDC-005 | Not run — Task 4 review pending | Not run — Task 4 review pending | Not run — Task 4 review pending | pending |
| T-TSDC-006 | Not run — Tasks 1–5 pending | Not run — Tasks 1–5 pending | Not run — Tasks 1–5 pending | pending |

### Current evidence boundaries

- Local tracked definitions do not establish remote workflow success,
  required-check enforcement, ruleset enforcement, environment configuration,
  or deployment state.
- Sanitized job/step metadata does not establish a remote failure root cause.
- Static version convergence does not establish a running service version.
- Secret path inventory does not establish the presence, correctness, or
  contents of secret values.
- A skipped, unavailable, or approval-gated command remains `unverified`; it
  is not reported as pass.

## Controlled Agent Pre-commit Evidence

| Field | Current evidence |
| --- | --- |
| Approval | Not approved for this wave |
| Command | Plan defines one exact wrapper command; it has not run |
| Starting commit | Not applicable |
| Allowed prefixes | Not activated |
| Exit status | Not run |
| Snapshot result | Not run |
| Observation boundary | Would be Git-visible non-ignored repository status only |
| Path sets | Not observed |
| Disposition | **NOT AUTHORIZED / DO NOT RUN.** Direct `pre-commit run` remains prohibited. |

The Task 4 CI-only script is not this controlled Agent route and does not
consume or create Agent authorization.

## Review Evidence

| Task | Implementer | Specification reviewer | Quality/security reviewer | Exact range | Verdict | Findings |
| --- | --- | --- | --- | --- | --- | --- |
| T-TSDC-001 | pending | pending | pending | not available | pending | Plan approval pending |
| T-TSDC-002 | pending | pending | pending | not available | pending | Task 1 review pending |
| T-TSDC-003 | pending | pending | pending | not available | pending | Task 2 review pending |
| T-TSDC-004 | pending | pending | pending | not available | pending | Task 3 review pending |
| T-TSDC-005 | pending | pending | pending | not available | pending | Task 4 review pending |
| T-TSDC-006 | pending | pending | pending | not available | pending | Tasks 1–5 pending |
| Whole branch | not applicable | pending fresh reviewer | pending different fresh reviewer | not available | pending | Final implementation not started |

Reviewers are read-only. Any reviewer-created edit or commit is a process
finding and must not be silently accepted as independent review evidence.

## Commit Ledger

| Unit | Logical purpose | Expected commit | Actual commit | Validation |
| --- | --- | --- | --- | --- |
| Planning specification | Define successor convergence design | `docs(spec): define target surface delta convergence` | `e828745a` | metadata, Markdown, alignment, diff hygiene passed |
| Planning activation | Activate Spec and define Plan/Task | `docs(plan): define target surface delta execution` | not committed | Plan review pending |
| T-TSDC-001 | Successor delta contract | `feat(governance): establish target surface delta contract` | not started | Plan approval pending |
| T-TSDC-002 | Document surface convergence | `docs(governance): converge target documentation surfaces` | not started | Task 1 review pending |
| T-TSDC-003 | Static version/lifecycle reconciliation | `fix(infra): reconcile static version and lifecycle drift` | not started | Task 2 review pending |
| T-TSDC-004 | Workflow and QA ownership | `ci(governance): type workflow and qa ownership` | not started | Task 3 review pending |
| T-TSDC-005 | Audit and remote evidence | `docs(audit): reconcile target surface evidence` | not started | Task 4 review pending |
| T-TSDC-006 | Blocking promotion and closure | `docs(task): close target surface delta convergence` | not started | Tasks 1–5 pending |

## Deferred and Blocked Items

| Item | State | Reason | Destination |
| --- | --- | --- | --- |
| Remote branch-protection synchronization | deferred | Observation-only scope; mutation needs separate approval, rollback, and read-back | future approved GitHub control-plane task |
| Push, pull request, workflow dispatch, and merge | deferred | No external-write approval | finishing workflow after explicit user choice |
| Remote failed-run root-cause analysis | unverified | Raw authenticated logs were not approved or read | separately approved bounded investigation |
| Live Compose/runtime validation | deferred | This wave changes static support/evidence only | domain runtime task with separate approval |
| CD, release, and deployment implementation | deferred | Outside Spec 135 | Spec 127 successor work |
| Self-hosted runner compatibility claim | unverified | No authenticated runner inventory | future control-plane inventory |
| Broad dependency/container vulnerability scanning | partial gap | Existing scoped checks do not establish broad SCA/image coverage | Spec 126 successor work |
| Controlled Agent all-files pre-commit | blocked by approval | No exact one-attempt approval for this wave | final Task 6 gate if separately approved |

None of these items blocks Plan review. They prevent only the corresponding
external, runtime, or approval-gated claim.

## Related Documents

- [Spec 135](../../03.specs/135-target-surface-delta-convergence/spec.md)
- [Implementation Plan](../plans/2026-07-28-target-surface-delta-convergence.md)
- [Spec 133](../../03.specs/133-target-surface-contract-convergence/spec.md)
- [Spec 134](../../03.specs/134-agent-governance-canonical-convergence/spec.md)
- [Canonical implementation audit](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md)
- [GitHub governance](../../00.agent-governance/rules/github-governance.md)
- [Document metadata profiles](../../99.templates/support/document-metadata-profiles.yaml)
- [README profile contract](../../99.templates/support/readme-profile-contract.md)
- [Archive and retention contract](../../99.templates/support/archive-retention-contract.md)
- [Existing target-surface manifest](../../90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml)
- [Controlled Agent pre-commit wrapper](../../../scripts/validation/run-agent-precommit-all-files.sh)
