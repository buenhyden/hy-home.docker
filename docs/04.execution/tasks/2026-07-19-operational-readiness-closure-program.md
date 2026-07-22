---
status: active
artifact_id: task:2026-07-19-operational-readiness-closure-program
artifact_type: task
parent_ids:
  - plan:2026-07-19-operational-readiness-closure-program
---

# Task: Operational Readiness Closure Program

## Overview

This Task is the execution and closure ledger for the local-isolated operational
readiness program. It coordinates four domain Tasks without replacing their
evidence ownership. The Task is active and evidence-ready; no Compose service,
database rehearsal, image build, signing operation, promotion, rollback,
remote action, or controlled all-files QA result is claimed at activation.

Execution is limited to the linked worktree on
`codex/stage03-04-unimplemented-closure`. The comparison base for changed
document metadata is `758aa0d2`.

## Inputs

- [Operational readiness closure Plan](../plans/2026-07-19-operational-readiness-closure-program.md)
- [PRD 025](../../01.requirements/025-operational-readiness-closure.md)
- [ARD 0028](../../02.architecture/requirements/0028-operational-readiness-closure.md)
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md)
- Specs [124](../../03.specs/124-compose-runtime-readiness-remediation/spec.md),
  [125](../../03.specs/125-infrastructure-operations-readiness-remediation/spec.md),
  [126](../../03.specs/126-security-supply-chain-remediation/spec.md), and
  [127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
- Domain Tasks linked under Related Documents
- Stage 00 task and controlled-QA contracts

## Goals and Non-goals

Goals:

- keep Task activation, four domain implementations, review remediation,
  evidence reconciliation, and final QA as independently reviewable units;
- require concise typed handoffs between the domain Tasks;
- preserve exact local runtime, cleanup, rollback, redaction, and review
  boundaries before any command is executed;
- reconcile Spec, Plan, Task, index, and generated-owner state only from actual
  implementation and validation evidence.

Non-goals:

- production/shared runtime, production data, remote backup, registry push,
  remote attestation, GitHub mutation, release publication, or deployment;
- credential, OIDC, token, secret-value, private-key, raw-log, or shell-history
  retention;
- a production-readiness, SLSA-level, organization RTO/RPO, or real Release
  claim from local evidence.

## Scope and Change Boundaries

Allowed paths are the exact paths declared by the four domain Plans, the five
Tasks in this program, directly affected Stage 03/04 indexes and lifecycle
documents, approved Stage 05 runbooks, canonical generated owners refreshed by
their generators, and the controlled-wrapper Task evidence. Ignored runtime
artifacts are confined to the four exact
`_workspace/repo-support/task-2026-07-19-*/` directories named by the Plan.

Forbidden paths and actions are the root `main` checkout, unrelated user work,
user-global provider configuration, shared or production services, live data,
remote GitHub/registry/deployment surfaces, credentials, raw authentication
material, and direct `pre-commit run --all-files`.

Compose impact: local task-scoped projects only. The program requires exact
project identities and owned cleanup; it does not authorize broad Docker
cleanup or default-profile expansion.

Security impact: local digest, SBOM, vulnerability, provenance, and signature
verification plus deterministic fixture policy. No publication, trust-level,
identity, or remote enforcement claim is permitted.

Operations impact: synthetic PostgreSQL recovery evidence and local delivery
rehearsal only. No live runbook execution or production recovery change is
authorized.

Runtime impact: four local-isolated command envelopes owned by the domain
Tasks. A domain command may run only after its Task contract is active and its
upstream typed inputs are available.

## Approval Evidence

Approval source:

- The user explicitly approved the operational-readiness design, Plans,
  protected-surface changes, local implementation, logical commits, and
  Subagent-Driven execution in this task thread.
- The approved [program Plan](../plans/2026-07-19-operational-readiness-closure-program.md)
  binds execution to the isolated worktree and four local domain lanes.

Protected surfaces:

- Local Compose projects, task-owned Docker resources, synthetic PostgreSQL
  state, pinned tool-container pulls, ephemeral local signing keys, the sample
  service, local CI/QA definitions, validators, runbooks, and Stage 03/04
  lifecycle evidence may change only within the domain Plans.
- Production/shared runtime, live data, remote state, publication, credentials,
  user-global config, push, PR, merge, and worktree deletion remain protected.

Approval boundary:

- Local authored changes, local runtime in the declared projects, read-only
  registry image retrieval, task-owned transient artifacts, focused tests,
  independent review, and logical local commits are authorized.
- Any remote mutation, publication, live target, credential/OIDC use, paid
  action, or scope expansion requires a new Task and separate explicit approval.

Rollback or recovery:

- Stop the failing lane, execute only its exact owned cleanup, and preserve
  concise non-secret failure evidence when cleanup is ambiguous.
- Revert logical commits in reverse dependency order; regenerate only outputs
  owned by a reverted change. Never use broad Docker pruning, destructive Git
  cleanup, or state deletion outside the task identity.

Redaction boundary:

- Tracked evidence may contain commands, exit classes, stable project/service
  names, image and file checksums, durations, typed verdict fields, cleanup
  status, commit identities, and review verdicts.
- Raw logs, dumps, row payloads, response bodies, vulnerability reports,
  credentials, tokens, `.env` values, private keys, authentication material,
  and shell history remain in `/tmp` or process memory and are never tracked.

## Work Breakdown

| Work unit | Responsibility | Evidence owner | State |
| --- | --- | --- | --- |
| `T-ORC-001` | Activate five Task contracts and the Task index. | This Task | Complete; documentation gates pass, runtime not run |
| `T-ORC-002` | Exact five-service Compose readiness and bounded recovery. | Compose domain Task | Complete; terminal reviews C0/I0/M0 |
| `T-ORC-003` | Baseline/candidate local supply-chain verification. | Supply-chain domain Task | Deterministic implementation complete; advisory runtime correctly rejected the baseline at the critical-vulnerability policy gate and independent reviews are pending |
| `T-ORC-004` | Synthetic PostgreSQL 17-to-18 logical recovery. | Infrastructure domain Task | Not run |
| `T-ORC-005` | Verified-digest promotion and previous-digest rollback. | Delivery domain Task | Not run |
| `T-ORC-006` | Whole-branch reviews, controlled QA, and lifecycle reconciliation. | This Task | Not run |

## Work Log

| Date | Work unit | Agent role | Result |
| --- | --- | --- | --- |
| 2026-07-19 | `T-ORC-001` activation | Documentation implementation agent | Five canonical Task records and their index routing were prepared from the approved Plans; focused metadata, template, traceability, alignment, Markdown, and diff-hygiene gates passed without domain runtime. |
| 2026-07-19 | `T-ORC-002` | Compose implementation and independent reviewers | Exact five-service startup, Vault recovery, expected timeout, typed scenario evidence, ready canonical handoff, and cleanup/redaction completed. Historical pre-routing reviews returned C0/I0/M0. The first routing reviews returned specification `C0/I3/M0` and quality `C0/I2/M0`; the second reviews returned specification `C0/I2/M0` and quality `C0/I1/M0`. After signal-cleanup and stale-evidence remediation with `35/35` focused tests, terminal specification and quality/security re-reviews each returned `APPROVED C0/I0/M0`. |
| 2026-07-19 | `T-ORC-003`–`T-ORC-006` | Assigned future implementers/reviewers | `not_run`; evidence must be appended only after each exact command and review executes. |
| 2026-07-22 | `T-ORC-003` | Fresh security implementation agent | Deterministic tool/policy/fixture, wrapper, CI/local/repository, and generated-summary work completed. An authorized bounded local pull cached exact pins; a first SBOM-subject binding defect was fixed. A separately authorized read-only retrieval using only pinned Grype seeded the ignored cache (schema `v6.1.9`, built `2026-07-21T07:05:18Z`, package SHA-256 `724e5d99c799d7e9b98ae8eb11930cf8ae427c4218b1e4db9d70e711dce63ce9`). The final offline advisory built/exported distinct subjects and rejected the baseline at class `40` under the critical-vulnerability policy (14 critical matches, no exception). Raw/redacted runtime material and DB identity remain ignored; task-owned `/tmp` keys were removed. No registry push, publication, OIDC, Scorecard request, or accepted consumer verdict occurred. Independent reviews remain pending. |
| 2026-07-22 | `T-ORC-003` combined-review remediation | Combined review `C3/I1/M1` found archive-config binding, stale-verdict, multi-match exception, cross-role, and Scorecard repository defects. Remediation derives config identity from each exact OCI archive's verified index/manifest/config relationship, invalidates stale verdict paths before any advisory failure point, publishes only a completed run-scoped pair, evaluates every Grype match, verifies the opposite role archive, and uses `github.com/buenhyden/hy-home.docker`. The offline rerun reached the same truthful class `40` baseline rejection (14 critical/no exception), with no accepted pair or `/tmp` key directory. Independent review closure remains pending. |
| 2026-07-22 | `T-ORC-003` re-review C1 remediation | Two re-reviews found that an accepted Grype result carrying a non-null exception ID could reach Task 5 as a falsely unexceptioned consumer verdict. The wrapper now preserves that transient vulnerability exception record, fails at class `40` before provenance/signing/publication, and keeps both fixed consumer verdict paths absent. The new wrapper regression passes; independent review closure remains pending. |

## Verification Evidence

Exact activation commands:

```bash
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref 758aa0d2
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
python3 -m unittest tests.validation.test_document_metadata.TemplateBodyContractTests -v
pre-commit run markdownlint-cli2 --files docs/04.execution/tasks/README.md docs/04.execution/tasks/2026-07-19-operational-readiness-closure-program.md docs/04.execution/tasks/2026-07-19-compose-runtime-readiness-remediation.md docs/04.execution/tasks/2026-07-19-security-supply-chain-remediation.md docs/04.execution/tasks/2026-07-19-infrastructure-operations-readiness-remediation.md docs/04.execution/tasks/2026-07-19-deployment-release-engineering-remediation.md
git diff --check
```

Expected evidence: zero metadata, traceability, alignment, Markdown, or diff
hygiene violations for the activated Task set.

Actual evidence: metadata selected 16 changed documents with 0 violations and
0 legacy exceptions; traceability checked 46 catalog pairs with 0 failures;
alignment checked 665 stage documents and 5,429 repository-local Markdown
links with 0 failures; all 38 template body-contract tests passed; targeted
Markdown lint passed; and `git diff --check` passed.

Verification results: Task activation gates passed. Task 2 final live Docker
runs passed: startup project `hyhome-crr-20260719-2111142-y1noqxim` was ready in
71 seconds; recovery project `hyhome-crr-20260719-2188421-vietv7qq` was ready
with recovery passed in 104 seconds; and negative project
`hyhome-crr-20260719-2281412-ho7cotsq` timed out with exit class `30` in 74
seconds. The canonical handoff SHA-256
`7b95d095764ede50585e8aa267483539c39e652e94a911bdc84fabb416ee6edf` was
preserved, and task-owned resources were empty after the runs. Fresh Task 2
re-reviews remain pending. Task 3 deterministic implementation is complete
with the documented critical-vulnerability policy rejection; Task 3 accepted consumer
verdicts, Task 3 reviews, Tasks 4–5, and whole-branch verification remain
`not_run`.

Task 3's repository-contract supply-chain section and generated-owner checks
pass. Its aggregate repository contract remains at `failures=5` for four
pre-existing lifecycle manifest-consumer mismatches and the missing `html5lib`
provider renderer; the full local QA runner stops at that same renderer. The
root implementation owner separately recorded an exact targeted
`hadolint-docker` pass for the sample-service Dockerfile.

## Controlled Agent Pre-commit Evidence

The only authorized all-files command is:

```bash
bash scripts/validation/run-agent-precommit-all-files.sh --task docs/04.execution/tasks/2026-07-19-operational-readiness-closure-program.md --allow-prefix .github/workflows/ci-quality.yml --allow-prefix docs/00.agent-governance/memory/progress.md --allow-prefix docs/03.specs --allow-prefix docs/04.execution --allow-prefix docs/05.operations --allow-prefix docs/90.references/data --allow-prefix examples/sample-web-service --allow-prefix infra --allow-prefix scripts --allow-prefix tests
```

Allowed prefixes are exactly the repeated `--allow-prefix` values above. The
command may run once only during `T-ORC-006`, from an initially clean linked
worktree after pre-wrapper evidence is committed.

Wrapper exit status: `not_run`.

Snapshot result: `not_run`.

Observation boundary: Git-visible, non-ignored repository paths only. The
wrapper does not claim visibility into ignored or out-of-repository writes.

Before, after, changed, and unexpected path sets: `not_run`.

Disposition: blocked until all four domain Tasks and whole-branch reviews pass,
the pre-wrapper evidence commit exists, and `git status --short` is empty.

## Review Evidence

Implementation review verdict: Task-activation scaffolding and Task 2 are
complete. Task 2 has final runtime evidence, routing remediation, and terminal
specification and quality/security reviews at C0/I0/M0. Task 3 deterministic
implementation is complete with the critical-vulnerability advisory rejection; combined review remediation is complete at `C3/I1/M1`, while its independent
reviews remain `not_run`. Tasks 4–5 remain `not_run`.

Task-activation specification review: the initial review returned C0/I1/M0.
The Important finding was remediated by making the delivery baseline/canary
project identity PID-scoped and fail-closed across the Plan and Task. Re-review
returned PASS C0/I0/M0.

Task-activation quality review: the initial review returned C0/I2/M0. The two
Important findings were remediated by adding the exact
`.github/workflows/ci-quality.yml` controlled-wrapper allow-prefix and the
negative rehearsal cleanup command to the closed delivery subcommand set.
Re-review returned APPROVED C0/I0/M0.

Whole-branch specification review: `not_run`; a fresh reviewer must return
C0/I0/M0 after all domain implementations and reviews complete.

Whole-branch quality/security review: `not_run`; an independent reviewer must
return C0/I0/M0 after all domain implementations and remediation complete.

Findings and disposition: all Task-activation review findings are resolved.
Task 2's historical pre-routing reviews remain `C0/I0/M0`. Its first routing
reviews returned specification `CHANGES REQUIRED C0/I3/M0` and quality
`CHANGES REQUIRED C0/I2/M0`; its second routing reviews returned specification
`CHANGES REQUIRED C0/I2/M0` and quality `CHANGES REQUIRED C0/I1/M0`. Both
terminal re-reviews returned specification and quality/security
`APPROVED C0/I0/M0` after the Program Plan/Task inconsistency was remediated.
Future domain or whole-branch findings must retain severity, owner, remediation
commit, and re-review verdict without copying raw logs.

## Commit Ledger

Commit identity: `ff988ece` for Task activation. Task 2's logical commit is
`feat(harness): add compose runtime acceptance`; its initial
pre-reconciliation identity was `83298464`, and its final amended identity is
resolved from branch history after the bounded handoff re-review.

Logical unit: `docs(sdlc): activate operational readiness tasks`.

Commit validation: activation passed before its logical commit. Task 2 final
live Docker evidence passed: startup
`hyhome-crr-20260719-2111142-y1noqxim` was ready in 71 seconds; recovery
`hyhome-crr-20260719-2188421-vietv7qq` was ready with recovery passed in 104
seconds; and negative `hyhome-crr-20260719-2281412-ho7cotsq` timed out with
exit class `30` in 74 seconds. The canonical SHA-256
`7b95d095764ede50585e8aa267483539c39e652e94a911bdc84fabb416ee6edf` was
preserved and task-owned resources were empty. Terminal Task 2 reviews pass at
C0/I0/M0. Task 3's logical commit is
`feat(security): add local supply-chain verification`; its combined-review
remediation is pending the final amendment and must be resolved from branch
history after creation. Task 3 independent reviews, Tasks 4–5, pre-wrapper,
and closure commits remain `not_run` and must be recorded after creation, never
predicted as completed evidence.

## Deferred and Blocked Items

Deferred items:

- remote/live Compose validation, production database recovery, physical
  backup/PITR/HA, registry publication, keyless/OIDC signing, remote Scorecard
  enforcement, GitHub Environment/Release, and production deployment;
- production RTO/RPO, SLSA conformance, and production-readiness claims.

Blocked items: `T-ORC-003` has exact pinned images cached but cannot supply
Task 5 because the baseline remains rejected by the critical-vulnerability
policy (14 critical matches, no exception) and no accepted distinct verdict
pair exists; its independent review closure remains pending. `T-ORC-004`–`T-ORC-006` remain blocked on
their documented sequence, upstream typed verdicts, exact local evidence, and
independent review.

Deferral destination: each remote, credential, production, publication, or
live-data expansion requires a new Stage 01-04 design chain and explicit human
approval; state recovery remains Spec 125-owned and remote delivery remains
Spec 127 follow-up scope.

## Related Documents

- [Program Plan](../plans/2026-07-19-operational-readiness-closure-program.md)
- [Compose Task](./2026-07-19-compose-runtime-readiness-remediation.md)
- [Supply-chain Task](./2026-07-19-security-supply-chain-remediation.md)
- [Infrastructure Task](./2026-07-19-infrastructure-operations-readiness-remediation.md)
- [Delivery Task](./2026-07-19-deployment-release-engineering-remediation.md)
- [Task contract](./README.md)
