---
status: active
artifact_id: plan:2026-07-19-operational-readiness-closure-program
artifact_type: plan
parent_ids:
  - prd:025-operational-readiness-closure
  - ard:0028-operational-readiness-closure
  - adr:0028-local-isolated-readiness-evidence
  - spec:124-compose-runtime-readiness-remediation
  - spec:125-infrastructure-operations-readiness-remediation
  - spec:126-security-supply-chain-remediation
  - spec:127-deployment-release-engineering-remediation
---

# Operational Readiness Closure Program Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox syntax so execution evidence can be reconciled without treating this
> prospective Plan as a Task log.

**Goal:** Close the four local-isolated operational-readiness gaps with
contract-first vertical slices and preserve remote, production, shared-state,
credential, and publication actions as separately approved follow-up work.

**Architecture:** The program coordinates four independent domain Plans. Each
domain owns its implementation and Task evidence. This Plan owns only activation,
execution order, cross-domain handoffs, independent review gates, logical commit
boundaries, controlled all-files QA, and lifecycle reconciliation.

**Tech Stack:** Docker Compose; Bash; Python `unittest`; PostgreSQL 17 and 18;
CycloneDX JSON; SLSA/in-toto provenance; Syft, Grype, Cosign, and OpenSSF
Scorecard containers; repository metadata, traceability, alignment, QA, and
controlled pre-commit validators.

## Global Constraints

- Work only in the linked worktree on
  `codex/stage03-04-unimplemented-closure`; do not mutate the root `main`
  checkout during implementation.
- Runtime is local and isolated. Production/shared services, real data, remote
  deployment, registry publication, GitHub mutation, credentials, OIDC, and
  secret-value inspection are excluded.
- Each domain Task starts with deterministic RED tests, implements the minimum
  GREEN behavior, then receives a fresh specification reviewer and a separate
  quality/security reviewer.
- Raw non-secret runtime artifacts belong under the four ignored paths
  `_workspace/repo-support/task-2026-07-19-compose-runtime-readiness-remediation/`,
  `_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/`,
  `_workspace/repo-support/task-2026-07-19-infrastructure-operations-readiness-remediation/`,
  and
  `_workspace/repo-support/task-2026-07-19-deployment-release-engineering-remediation/`.
  Credentials, private keys, tokens, raw authentication material, raw logs,
  and shell history belong only in `/tmp` or process memory and must not enter
  tracked files.
- The only all-files pre-commit execution is the controlled wrapper from a clean
  linked worktree. Direct `pre-commit run --all-files` is prohibited.
- Specs 124-127 remain active until their own acceptance evidence and reviews
  pass. Local completion must retain explicit remote/live exclusions.

---

## Overview

The active design chain establishes one local closure program and four bounded
implementation lanes. This program Plan sequences those lanes without merging
their requirements or evidence ownership. The approved order is:

1. Stage 04 Task scaffolding and contract reconciliation.
2. Compose five-service runtime readiness.
3. Sample-service supply-chain verification.
4. Synthetic PostgreSQL logical recovery.
5. Sample-service local promotion and rollback.
6. Whole-branch review, controlled QA, and lifecycle closure.

## Context and Inputs

Canonical inputs:

- [PRD 025](../../01.requirements/025-operational-readiness-closure.md)
- [ARD 0028](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- [Spec 124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md)
- [Spec 125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- [Spec 126](../../03.specs/126-security-supply-chain-remediation/spec.md)
- [Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
- the four domain Plans linked under Related Documents.

The safe documentation comparison base for this program is commit `758aa0d2`,
the design-chain activation commit. Implementation Tasks must record their own
commit identities after each logical unit lands.

### Cross-domain coordination contracts

| Producer | Exact transient artifact | Required consumer fields | Consumer rule |
| --- | --- | --- | --- |
| Spec 124 / Task 2 | Ready handoff `_workspace/repo-support/task-2026-07-19-compose-runtime-readiness-remediation/compose/readiness-verdict.json`; scenario evidence `readiness-verdict.<scenario>.json` in the same directory | Schema v2: producer Spec/Task, approval, scenario, target class, project, start/end, exact five-service states, endpoint verdicts, observed state, recovery/teardown, overall, elapsed, cleanup, redaction | Task 5 accepts only a ready canonical record with exact services, `scenario=vault-restart-recovery`, `recovery_status=passed`, and cleanup/redaction passed. Negative evidence remains scenario-specific and is never promoted as readiness. |
| Spec 126 / Task 3 | `_workspace/repo-support/task-2026-07-19-security-supply-chain-remediation/supply-chain/verification-verdict.baseline.json` and `verification-verdict.candidate.json` | `schema_version`, `producer_spec`, `role`, `source_revision`, image config digest, OCI archive SHA-256, policy ID, `verdict`, exception ID, verification time, redaction status | Task 5 requires two distinct subjects, matching source revision, `verdict=accepted`, no exception, and successful redaction. |
| Spec 125 / Task 4 | `_workspace/repo-support/task-2026-07-19-infrastructure-operations-readiness-remediation/postgres/recovery-verdict.json` | `schema_version`, `producer_spec`, source/target pins, fixture/dump checksums, integrity verdict, observed timings, cleanup status, `scope=synthetic-local` | Task 5 records this as a data-recovery boundary only; the stateless sample service must declare `data_impact=none` and must not claim database recovery. |
| Spec 127 / Task 5 | `_workspace/repo-support/task-2026-07-19-deployment-release-engineering-remediation/delivery/rehearsal-record.json` | both upstream artifact references, readiness reference, baseline/canary projects, promotion decision, rollback decision, post-rollback health, data impact, cleanup status | Task 6 copies only concise typed fields and checksums into Stage 04 Task evidence. |

All JSON artifacts use UTF-8, sorted-key serialization, RFC 3339 UTC
timestamps, and lowercase enum values. Task 2 uses its reviewed schema v2;
Tasks 3–5 use their declared schema v1 until a reviewed successor is approved.
Where checksums apply, SHA-256 strings are prefixed with `sha256:`. Missing or
unknown fields fail closed; producers and consumers share no raw evidence files.

## Goals and Non-goals

Goals:

- Create five active Task documents whose metadata, parents, scope, approvals,
  evidence boundaries, reviews, and commit ledgers are valid before runtime.
- Implement each domain as an independently testable vertical slice.
- Bind Spec 126's accepted artifact verdict into Spec 127 without copying raw
  supply-chain evidence.
- Bind Spec 124 readiness and Spec 125 recovery boundaries into Spec 127 without
  turning local delivery rehearsal into a real release claim.
- Close with reproducible focused tests, whole-repository contract checks,
  independent branch review, and controlled all-files QA evidence.

Non-goals:

- No production readiness certification or broad service rollout.
- No live Supabase/Spilo/PostgreSQL cluster mutation or production backup test.
- No image push, remote attestation, GitHub Environment/Release, workflow
  mutation, branch-protection mutation, deployment, or credential change.
- No SLSA level claim and no Scorecard score used as a deterministic blocker.

## Work Breakdown

### Task 1: Activate Stage 04 execution evidence contracts

**Files:**

- Create: `docs/04.execution/tasks/2026-07-19-operational-readiness-closure-program.md`
- Create: `docs/04.execution/tasks/2026-07-19-compose-runtime-readiness-remediation.md`
- Create: `docs/04.execution/tasks/2026-07-19-security-supply-chain-remediation.md`
- Create: `docs/04.execution/tasks/2026-07-19-infrastructure-operations-readiness-remediation.md`
- Create: `docs/04.execution/tasks/2026-07-19-deployment-release-engineering-remediation.md`
- Modify: `docs/04.execution/tasks/README.md`

- [x] Copy the canonical Task template structure into all five files.
- [x] Set each domain Task parent to its Spec and domain Plan; set the program
      Task parent to this Plan.
- [x] Record exact allowed paths, prohibited remote/secret surfaces, runtime
      command classes, rollback/cleanup, redaction, review roles, and deferred
      destinations.
- [x] Run
      `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 758aa0d2`.
- [x] Run `bash scripts/validation/check-doc-traceability.sh` and
      `bash scripts/validation/check-doc-implementation-alignment.sh`.
- [x] Commit as `docs(sdlc): activate operational readiness tasks`.

### Task 2: Implement Compose runtime readiness

**Plan:** [Compose runtime readiness Plan](./2026-07-11-compose-runtime-readiness-remediation.md)

- [x] Execute that Plan using a fresh implementation agent.
- [x] Require the exact `readiness-verdict.json` contract above with
      `overall_status=ready` and verified owned cleanup before Task 5 may use it.
- [x] Close the fresh specification and separate quality/security reviews after
      remediation and re-review of all critical, important, and minor findings.
      Terminal re-reviews returned specification and quality/security
      `APPROVED C0/I0/M0` after the Program Plan/Task inconsistency was fixed.
- [x] Amend and record the verified implementation as
      `feat(harness): add compose runtime acceptance`; the logical commit
      containing this checklist is the branch-history identity.

### Task 3: Implement local supply-chain verification

**Plan:** [Security supply-chain Plan](./2026-07-11-security-supply-chain-remediation.md)

- [x] Execute deterministic policy, preflight, fixture-only, CI/local/repository,
      and generated-summary portions of that Plan using a fresh implementation
      agent after Task 2. The optional live advisory rehearsal was attempted
      with an authorized pinned Grype DB retrieval and truthfully rejected the
      baseline at the critical-vulnerability policy gate.
- [ ] Require distinct accepted baseline/candidate verdicts with the exact
      fields and paths above before Task 5 starts.
- [x] Require a fresh specification reviewer and a separate security/quality
      reviewer; the initial/combined `C3/I1/M1` findings and first re-review C1
      were remediated, and terminal specification and quality/security reviews
      both returned APPROVED C0/I0/M0.
- [x] Record the deterministic implementation as
      `72e584f51badfd194c0a1b6d32510a3bf3ab395c`
      (`feat(security): add local supply-chain verification`).

### Task 4: Implement PostgreSQL logical recovery rehearsal

**Plan:** [Infrastructure operations Plan](./2026-07-11-infrastructure-operations-readiness-remediation.md)

- [x] Execute that Plan using a fresh implementation agent after Task 3.
- [x] Require the exact synthetic-local `recovery-verdict.json` contract above;
      keep it a rollback-boundary input rather than a deployment gate.
- [x] Require a fresh specification reviewer and a separate operations/quality
      reviewer. Initial reviews returned specification C1/I3/M1 and
      operations/quality C0/I5/M2; the second review wave returned
      specification C0/I3/M1 and operations/quality C0/I2/M0. Both historical
      waves are remediated, including stable authenticated TCP postmaster
      identity plus running/healthy state, direct-control isolation, exact
      per-project rendering, and bounded sleeps. Terminal specification and
      operations/quality reviews both returned APPROVED C0/I0/M0 after the
      specification evidence-sync finding was remediated.
      The reviewer's direct-control regression invalidated the canonical as
      designed; exactly one approved normal rehearsal then regenerated the
      final-state handoff for project
      `hyhome-ior-20260719-229164-source/target`, fixture SHA-256
      `b8d5421bba8fb32a1be3d485660f7d0cc018405e1cf7f2564f653bf0dd725460`,
      dump SHA-256
      `090b92324621b40e87355d705483e2ac66c027ac3fed2940b588a525cdaae6f3`,
      4,484 bytes, backup 1s, restore 0s, and exact 12-key mode-0600 canonical
      SHA-256
      `c5f9e3a135d032e480c4484a5c545486f461562fc327923c9e4a3887f2883899`.
      Schema 1, scope, integrity, cleanup, and redaction passed; owned resources
      were empty, and no test, negative, direct-control, or `--check` command
      followed regeneration.
- [x] Keep the verified implementation in the logical unit
      `feat(ops): add postgres recovery rehearsal`; the initial reviewed
      identity was `db2418c2`, and the final amended identity is resolved from
      branch history after amendment rather than self-recorded in that commit.

### Task 5: Implement local promotion and rollback

**Plan:** [Deployment/release Plan](./2026-07-11-deployment-release-engineering-remediation.md)

- [x] Implement that Plan with a fresh implementation agent after Tasks 2-4;
      keep positive promotion/rollback runtime blocked while the accepted
      Spec 126 pair is absent.
- [x] Fail closed unless both supply-chain verdicts and the readiness verdict
      satisfy the coordination table; record `data_impact=none` or stop and hand
      off to Spec 125.
- [ ] Require a fresh specification reviewer and a separate release/security
      reviewer; remediate and re-review all findings.
- [x] Commit the verified implementation as
      `feat(release): add local promotion and rollback`.

### Task 6: Reconcile evidence and close the local program

**Files:**

- Modify: the five Task documents created by Task 1.
- Modify: the four domain Plans and Specs 124-127 only when their evidence
  supports the lifecycle transition.
- Modify: `docs/03.specs/README.md`, `docs/04.execution/plans/README.md`, and
  `docs/04.execution/tasks/README.md` for lifecycle/index consistency.
- Modify generated references only through their owning generators.

- [ ] Run all four focused test suites and each domain's approved local
      rehearsal; record concise evidence and cleanup outcomes.
- [ ] Run
      `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 758aa0d2`,
      traceability, alignment, repository contracts, LLM Wiki freshness, and
      audit-inventory freshness.
- [ ] When the bare Python aggregate reports `AGC-DEPENDENCY-MISSING
      path=html5lib`, rerun through
      `UV_CACHE_DIR=/tmp/uv-cache uv run --with-requirements scripts/requirements.txt bash scripts/validation/check-repo-contracts.sh`;
      record a blocked result rather than PASS if the locked rerun is unavailable.
- [ ] Obtain a whole-branch specification review and a separate
      quality/security review; remediate and re-review all findings.
- [ ] Record all pre-wrapper evidence in the five Task documents, update
      generated outputs only through their owners, and commit the clean
      pre-wrapper state as `docs(evidence): prepare operational readiness closure`.
- [ ] Confirm `git status --short` is empty before invoking the wrapper.
- [ ] From a clean linked worktree, run
      `bash scripts/validation/run-agent-precommit-all-files.sh --task docs/04.execution/tasks/2026-07-19-operational-readiness-closure-program.md --allow-prefix .github/workflows/ci-quality.yml --allow-prefix docs/00.agent-governance/memory/progress.md --allow-prefix docs/03.specs --allow-prefix docs/04.execution --allow-prefix docs/05.operations --allow-prefix docs/90.references/data --allow-prefix examples/sample-web-service --allow-prefix infra --allow-prefix scripts --allow-prefix tests`.
- [ ] Record wrapper exit status, before/after snapshots, observed path sets,
      reviewer verdicts, and exact commit ledger in the program Task. Rerun
      metadata, traceability, alignment, and `git diff --check` after this
      evidence-only update; do not run the all-files wrapper a second time.
- [ ] Commit as `docs(evidence): close operational readiness validation`.

## Verification Plan

| Gate | Exact command | Pass condition |
| --- | --- | --- |
| Metadata | `python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 758aa0d2` | Zero changed-document violations. |
| Traceability | `bash scripts/validation/check-doc-traceability.sh` | Zero failures for the active chain. |
| Alignment | `bash scripts/validation/check-doc-implementation-alignment.sh` | Zero implementation-alignment failures. |
| Repository contracts | dependency-locked command in Task 6 | Zero failures, or an explicitly recorded pre-existing environment blocker that is not mislabeled PASS. |
| Focused domain tests | exact commands in the four domain Plans | All positive and negative cases pass. |
| Runtime evidence | exact task-owned local wrappers | Owned resources only; expected verdicts; cleanup verified. |
| Review | per-domain and whole-branch independent reviews | C0/I0/M0 after remediation. |
| All-files QA | controlled wrapper command in Task 6 | Clean-before state, allowed path set, exit 0, and Task evidence recorded. |

## Risks and Rollback

- Domain failure does not roll back earlier verified domains. Revert only the
  failing logical commit and its owned transient resources.
- If cleanup identity is ambiguous, stop and preserve non-secret evidence; do
  not use broad Docker cleanup or delete shared state.
- If upstream handoff schemas drift, fail closed before runtime and reconcile
  the producer/consumer contract in the same domain commits.
- If remote/live criteria remain unimplemented, keep the affected Specs active
  or record the explicit local-only completion boundary; never infer completion.

## Approval Gates

- The user approved this local-isolated program and protected-surface changes.
- Each active Task must still bind its exact runtime command envelope before the
  command is executed.
- Any remote mutation, publication, production/shared runtime action,
  credential/OIDC use, or live data operation requires a new independent Task
  and separate explicit approval.

## Completion Criteria

- [ ] All five Task documents contain exact implementation and review evidence.
- [ ] Task activation, four domain commits, pre-wrapper evidence, and final
      wrapper evidence are logical and independently reviewable commits.
- [ ] All local positive/negative acceptance paths pass and owned cleanup is
      verified.
- [ ] Cross-domain handoffs use concise typed verdicts, not raw evidence copies.
- [ ] Whole-branch reviews and controlled all-files QA pass.
- [ ] Lifecycle/index updates match actual evidence and retain remote/live
      exclusions.

## Related Documents

- **Compose Plan**: [2026-07-11-compose-runtime-readiness-remediation.md](./2026-07-11-compose-runtime-readiness-remediation.md)
- **Supply-chain Plan**: [2026-07-11-security-supply-chain-remediation.md](./2026-07-11-security-supply-chain-remediation.md)
- **PostgreSQL Plan**: [2026-07-11-infrastructure-operations-readiness-remediation.md](./2026-07-11-infrastructure-operations-readiness-remediation.md)
- **Delivery Plan**: [2026-07-11-deployment-release-engineering-remediation.md](./2026-07-11-deployment-release-engineering-remediation.md)
- **Task contract**: [../tasks/README.md](../tasks/README.md)
- **Operations**: [../../05.operations/README.md](../../05.operations/README.md)
