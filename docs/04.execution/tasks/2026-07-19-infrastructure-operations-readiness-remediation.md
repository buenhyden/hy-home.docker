---
status: completed
artifact_id: task:2026-07-19-infrastructure-operations-readiness-remediation
artifact_type: task
parent_ids:
  - plan:2026-07-11-infrastructure-operations-readiness-remediation
  - spec:125-infrastructure-operations-readiness-remediation
---

# Task: Infrastructure Operations Readiness Remediation

## Overview

This completed Task records the synthetic local PostgreSQL 17-to-18 logical
backup, restore, integrity, upgrade, and negative-path rehearsal. At activation,
no database container has started, no dump or row data has been produced, and
no recovery or elapsed-time result is claimed.

The Task owns the concise
`_workspace/repo-support/task-2026-07-19-infrastructure-operations-readiness-remediation/postgres/recovery-verdict.json`
handoff. Dumps, row payloads, credentials, and raw database logs never enter
tracked evidence.

## Inputs

- [Spec 125](../../98.archive/03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- [Infrastructure operations Plan](../plans/2026-07-11-infrastructure-operations-readiness-remediation.md)
- [Program Plan](../plans/2026-07-19-operational-readiness-closure-program.md)
- Exact PostgreSQL source/target pins and deterministic SQL contract in the Plan
- Spec 124 readiness semantics as an upstream runtime boundary

## Goals and Non-goals

Goals:

- prove a deterministic custom-format logical backup and separate restore;
- compare a metadata-only integrity oracle across PostgreSQL 17.6 and 18.4;
- reject checksum mismatch, partial state, wrong target major, timeout, unsafe
  paths, and project collisions with stable failure classes;
- record observed local backup/restore timing, checksums, cleanup, and redaction;
- provide a recovery-boundary verdict without making a deployment claim.

Non-goals:

- production/shared data, live Supabase/Spilo state, or `${DEFAULT_DATA_DIR}`;
- physical backup, PITR, HA, replication, retention, encryption-at-rest, remote
  storage, or organization RTO/RPO certification;
- secret-value, raw dump, row payload, registry, cloud, or deployment action.

## Scope and Change Boundaries

Allowed authored paths:

- `scripts/validation/rehearse-postgres-logical-upgrade.sh`;
- `tests/fixtures/postgres-logical-upgrade/**`;
- `tests/validation/test_postgres_logical_upgrade_rehearsal.py`;
- the bounded PostgreSQL rehearsal runbook and its direct index;
- this Task and directly supported lifecycle/index evidence during closure.

Allowed transient paths are `/tmp/hyhome-ior-evidence.<decimal-pid>` and the
exact program handoff directory. The dump remains under `/tmp`, is represented
only by SHA-256 and byte size, and is deleted after successful evidence capture.

Forbidden paths/actions: live databases, bind mounts, external networks,
restart policies, host ports, shared or named persistent volumes, remote backup
destinations, secret values, raw database output, and unscoped cleanup.

Compose impact: one test fixture with only `source` and `target`, anonymous
volumes, no host ports, no `container_name`, no external network, and no restart
policy.

Security impact: process-local synthetic password, no secret-value evidence,
checksum-only dump identity, and fail-closed path/project validation.

Operations impact: representative logical backup/restore mechanics and a
bounded runbook only. No live recovery authority, retention control, or RTO/RPO
commitment changes.

Implementation-alignment impact: the Plan-required runbook is a non-service
procedure backed by `scripts/validation/rehearse-postgres-logical-upgrade.sh`
and `tests/fixtures/postgres-logical-upgrade/`, not a new
`infra/04-data/relational` service. The existing alignment validator therefore
adds exactly this stem to `NON_SERVICE_STEMS`; focused regression coverage
prevents broader exception drift.

Runtime impact: task-scoped local PostgreSQL containers using only the pinned
images and synthetic fixture. One deadline begins before the first Docker call;
normal/preflight work receives 360 seconds and accumulated cleanup reserves the
last 60 seconds inside the 420-second total. Cleanup removes only verified
owned projects, anonymous volumes, and the exclusive task `/tmp` directory.

## Approval Evidence

Approval source:

- The user approved protected-surface changes and the local representative
  recovery implementation in this program.
- [ADR 0028](../../02.architecture/decisions/0028-local-isolated-readiness-evidence.md),
  [Spec 125](../../98.archive/03.specs/125-infrastructure-operations-readiness-remediation/spec.md),
  and the active Plan approve the synthetic local topology.

Protected surfaces: the exact PostgreSQL test images, anonymous volumes,
synthetic SQL, `/tmp` dump/evidence, validation wrapper/tests, and bounded
runbook may change within the Plan. Live data, production volumes, remote
storage, credentials, and shared runtime remain protected.

Approval boundary: source is exactly
`postgres:17.6-alpine@sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94`;
target is exactly
`postgres:18.4-alpine@sha256:9a8afca54e7861fd90fab5fdf4c42477a6b1cb7d293595148e674e0a3181de15`.
Commands are normal execution, `--check`, or one
`--negative-case checksum-mismatch|partial-state|bad-target-major|timeout`.
Changed image, data, storage, target, or cleanup requires stop and new approval.

Rollback or recovery: the wrapper trap independently attempts every exact
project-prefix resource and its retained `/tmp` identity without broad cleanup.
Revert the single logical IOR commit to remove authored changes. On ambiguous
ownership, stop without reading or mutating the foreign path; on cleanup
failure, leave canonical absent and permit only an exact idempotent retry inside
the remaining deadline.

Redaction boundary: tracked evidence may contain image pins, fixture/dump
checksums, dump size, aggregate oracle values/digests, observed timing, stable
failure class, cleanup, redaction, commits, and reviews. It must not contain the
dump, SQL row payloads, passwords, environment values, raw queries, or logs.

## Work Breakdown

| Task ID | Description | Parent requirement | Validation / evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| `T-IOR-001` | Fixture, oracle, wrapper, verdict, and tests | `IOR-001`–`IOR-004` | Focused RED/GREEN suite and `--check` | Fresh implementation agent | Complete; current focused suite 51/51 and static checks pass |
| `T-IOR-002` | Logical backup and isolated restore | `IOR-003`, `IOR-004` | Dump, restore, oracle, timing, cleanup | Fresh implementation agent | Complete; final normal pass |
| `T-IOR-003` | 17-to-18 and corrupted/partial negative paths | `IOR-001`, `IOR-002` | Stable failures and cleanup disposition | Fresh implementation agent | Complete; classes 50/50/10/20 |
| `T-IOR-004` | Bounded runbook and independent reviews | `VAL-IOR-001`–`004` | Spec plus operations/security C0/I0/M0 | Separate reviewers | Complete for the representative-local Task boundary; final implementation re-reviews pass and post-evidence branch confirmation remains pending |

## Work Log

| Date | Work unit | Result |
| --- | --- | --- |
| 2026-07-19 | Task activation | Contract recorded; no database runtime, dump, restore, or destructive action executed. |
| 2026-07-19 | `T-IOR-001`–`T-IOR-004` | `not_run`; actual evidence is appended only after exact execution. |
| 2026-07-22 | `T-IOR-001` review-wave RED/GREEN (historical) | Initial 13-test suite failed/errored with the planned wrapper/fixtures absent. Initial-review remediation was RED 7/31, and the later initialization-server race regression was RED 1/1. The second review wave produced 13 expected assertion/subtest failures across 7 focused methods for socket-only readiness, direct test-control injection, PID/budget reporting, exact project/network render validation, generated-password/healthcheck drift, and unbounded sleeps. At that wave, direct execution derived identity only from `$$`, test controls required the explicit sourced-test boundary, and normal source/target readiness used authenticated TCP `127.0.0.1:5432` twice plus running/healthy state. Historical second-review-wave GREEN was 40/40. Shell syntax, ShellCheck, Python compile, and `--check` passed with fixture SHA-256 `b8d5421bba8fb32a1be3d485660f7d0cc018405e1cf7f2564f653bf0dd725460`. |
| 2026-07-22 | `T-IOR-002` second-review-wave normal rehearsals (historical) | Consecutive projects `hyhome-ior-20260719-4088641-source/target` and `hyhome-ior-20260719-4092001-source/target` passed detached PG18 custom backup, PG18 restore, semantic oracle comparison, accumulated cleanup, and post-cleanup publication during that review wave. Its then-current dump was 4,484 bytes, SHA-256 `7a3688e4d69f047dfb455ed646dafb28eb3bbb1c90e989a6afecdd7618cccd71`, backup 0s, restore 0s. |
| 2026-07-22 | `T-IOR-003` negatives | Checksum mismatch and partial state returned class 50; bad target major returned class 10; timeout returned class 20. Every run reported cleanup passed and left canonical absent. |
| 2026-07-22 | Implementation corrections | A sandbox Docker-socket denial created no resources. Two attached-client attempts were interrupted and exactly cleaned; the implementation moved to a bounded detached labeled PG18 client. PG18 target layout and oracle preamble/catalog differences then failed closed at classes 40/50 and were corrected without publishing canonical evidence. |
| 2026-07-22 | Initial independent reviews and remediation (historical) | Specification returned C1/I3/M1 and operations/quality returned C0/I5/M2. The deduplicated findings are remediated with exclusive UID/mode/device/inode evidence ownership, safe canonical invalidation/atomic publication, memory-only candidate state, accumulated/idempotent cleanup, one reserved 420-second deadline, full rendered-topology validation, real bad-major/timeout detectors, signal/publication-window tests, and corrected runbook/evidence wording. |
| 2026-07-22 | Second independent review wave and remediation (historical) | The amended candidate returned specification C0/I3/M1 and operations/quality C0/I2/M0. Those historical findings are remediated with mandatory TCP `127.0.0.1:5432` readiness, PID-only direct identity, pre-Docker rejection of every direct test control, exact active-budget reporting, exact per-project default-network render validation, generated-password and mandatory-healthcheck validation for both projects, topology mutations, and bounded readiness sleeps. |
| 2026-07-22 | Terminal re-review remediation and closure | Terminal re-reviews left exactly two Important items: direct test-control rejection could preserve a stale fixed-path success verdict, and the ignored implementation report remained stale. The new regression was RED in all 8 direct-control subcases. Main now installs traps, validates/prepares the canonical parent, and safely invalidates a stale regular canonical before returning class 10, while every variant still makes zero Docker calls; unsafe parents, symlinks, and directories remain fail-closed. GREEN is 41/41. Both items were remediated, and the ignored report was synchronized separately. Terminal operations/quality returned APPROVED C0/I0/M0. Specification then left one evidence-synchronization Important finding (C0/I1/M0); after the documentation synchronization and final-state canonical reconciliation, terminal specification re-review returned APPROVED C0/I0/M0. |
| 2026-07-22 | Final-state canonical reconciliation (historical, superseded) | The specification reviewer's direct-control regression invalidated the canonical as designed. Exactly one approved normal rehearsal then passed for project `hyhome-ior-20260719-229164-source/target` with fixture SHA-256 `b8d5421bba8fb32a1be3d485660f7d0cc018405e1cf7f2564f653bf0dd725460`, dump SHA-256 `090b92324621b40e87355d705483e2ac66c027ac3fed2940b588a525cdaae6f3`, 4,484 bytes, backup 1s, and restore 0s. Direct verification found an exact 12-key mode-0600 canonical SHA-256 `c5f9e3a135d032e480c4484a5c545486f461562fc327923c9e4a3887f2883899`, schema 1, `scope=synthetic-local`, passed integrity/cleanup/redaction, and empty owned containers, labeled clients, networks, volumes, dumps, and PID evidence. No test, negative, direct-control, or `--check` command followed regeneration. |
| 2026-07-22 | Program regression isolation | The affected regression suite no longer invokes the real wrapper or mutates ignored canonical evidence. Commit `4d25f91e806d84fa49b44cb3ac14384a16420d3d` copies the wrapper and fixture into each test repository. Full focused GREEN is 41/41 in 15.012 seconds, and the pre-rerun canonical remained byte-identical. |
| 2026-07-22 | Program closure ordered rerun (historical, superseded) | The ordered 0/50/50/10/20/final-normal sequence and its `712f289d…` handoff were valid for that committed state. The later offline image-identity boundary remediation and current frozen final-normal evidence below supersede its fixture, dump, project, and canonical identities. |
| 2026-07-22 | Offline PostgreSQL image-boundary RED/GREEN (historical, superseded) | RED `00a65be1` captured missing exact local image-object and no-pull boundaries. GREEN `571b2ab1` enforced source/target/client checks for that committed state. Its 45/45 result remains historical evidence. |
| 2026-07-22 | Strict ordered acceptance before independent identity hardening (historical, superseded) | The 0/50/50/10/20/0 sequence, project `hyhome-ior-20260719-2205794-source/target`, dump SHA-256 `12725faae1e0152c7b2ac2f6336547ec23f9c73dd96d1f5a4b1e817b1454f7f5`, and canonical SHA-256 `f0c07c294ade39417ed9c61b6c614b4bf86a59c14a8b4a26a84082ab39fbab76` were valid for `571b2ab1`; the current evidence below supersedes them. |
| 2026-07-22 | Independent PostgreSQL image-identity RED/GREEN (historical, superseded) | RED `da06a080` proved source, target, and helper-client manifest identities were not independently established from configuration IDs. GREEN `adbbdce2` compared the manifest and engine `.Id` observations available at that checkpoint. Docker Engine 29/containerd later established that `.Id` is the target descriptor rather than the image configuration digest, so the final-review correction below supersedes this observation model. |
| 2026-07-22 | Strict ordered acceptance before descriptor/config correction (historical, superseded) | The check/negative/final-normal sequence, project `hyhome-ior-20260719-2866314-source/target`, dump SHA-256 `e1f8f97636739cacf00a0824e21dc5b296e6198ed52715c496960710b0925534`, and canonical SHA-256 `bf7109f5fd15cf04615ed331cb63be7c7848d8656749e427c2a54a1aecd2d18a` were valid for the earlier observation model. The corrected final-review acceptance below supersedes them. |
| 2026-07-23 | Terminal whole-branch review closure | Quality/security review v3 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the then-current 26-document reconciliation diff. Specification review v5 returned `APPROVED C0/I0/M0` for the full branch range through `20022458` plus the final 26-document reconciliation diff. Earlier `CHANGES REQUIRED` iterations remain historical remediation evidence. No Task 4 command or test ran for this evidence-only closure, and the approvals do not change the active Task or Program lifecycle or authorize the controlled wrapper. |
| 2026-07-26 | Final lifecycle review remediation (historical checkpoint) | The representative synthetic PostgreSQL boundary is complete and this Task transitions to `completed`; live/shared/production recovery remains deferred to a new Stage 01-04 chain. The initial final Program specification review returned `CHANGES REQUIRED C0/I2/M0` for stale generated owners and still-active lifecycle metadata; generated-owner remediation is `78265090`, and this lifecycle logical unit closes the status/index finding. The initial final quality review returned `CHANGES REQUIRED C0/I1/M0` for the OCI digest helper; RED `9a24b0cb` and GREEN `73f4ea68` close that code boundary. At that checkpoint fresh final re-review had not approved the remediations; the later dual-ID and CI/governance row records the exact approved re-reviews. |
| 2026-07-26 | Final-review identity correction and strict acceptance | RED `163f434b` proves that engine `.Id` cannot establish the config digest. GREEN `e8934783` binds repo digest, target descriptor, and independently hashed Docker-save config body for source, target, and helper client. At that correction checkpoint the focused suite passed 49/49 and the local read-only preflight passed before runtime. The exact ordered sequence returned check `0`, checksum mismatch `50`, partial state `50`, bad target major `10`, timeout `20`, and one final normal `0`; every negative reported cleanup passed. Final project `hyhome-ior-20260719-1128131-source/target` used fixture SHA-256 `523d947400f5197ce362a11445a0c6e380a28431352679ea01ca24d106c34b57`; its 4,484-byte dump SHA-256 is `c3ebc52895bda22559f99efb72471f9928b9a097d64d0df6066be354d9a65581`, with backup 0s and restore 0s. The exact 12-key, mode-0600, 642-byte canonical SHA-256 is `dab8e587519a48059d62a46ae7f6b7b757fbad53486215df436fd0a90bd4b45a`; integrity, cleanup, and redaction passed. Every owner-scoped container, helper client, network, volume, dump, and `/tmp` inventory is zero. No Task 4 wrapper, test, check, negative, or normal command ran after that final normal. The later dual-ID row supersedes only the focused count and review disposition. |
| 2026-07-26 | Dual-ID compatibility RED/GREEN and review closure | Initial whole-branch quality review at `0828857657611e570e2a654efff4b17ff95083ca` returned `CHANGES REQUIRED C0/I1/M0` because the PostgreSQL predicate accepted `.Id` only as the target descriptor. RED `ffc1cf130e64db3d61d2de067239c7d720fa3ee5` added target-ID acceptance, config-ID acceptance, and unrelated-ID rejection; the config-ID case was the one intended PostgreSQL failure. GREEN `d186644e6243b0598e54303ee9bec5344516cb99` accepts `.Id` only when equal to the expected target or expected config while keeping RepoDigest, Descriptor/target, and independently hashed config-body checks mandatory. The focused suite passes 51/51, and the four-module total is 176/176. Exact quality re-review of `0828857657611e570e2a654efff4b17ff95083ca..d186644e6243b0598e54303ee9bec5344516cb99` returned `APPROVED C0/I0/M0`; the following exact specification re-review also returned `APPROVED C0/I0/M0`. The frozen runtime used `.Id=target`, remains valid, and was not rerun; no config-ID runtime execution or post-canonical Task 4 command is claimed. Final post-evidence whole-branch confirmation remains pending. |

## Verification Evidence

Exact command envelope:

```bash
python3 -m unittest tests.validation.test_postgres_logical_upgrade_rehearsal -v
bash scripts/validation/rehearse-postgres-logical-upgrade.sh --check
bash scripts/validation/rehearse-postgres-logical-upgrade.sh
bash scripts/validation/rehearse-postgres-logical-upgrade.sh --negative-case checksum-mismatch
bash scripts/validation/rehearse-postgres-logical-upgrade.sh --negative-case partial-state
bash scripts/validation/rehearse-postgres-logical-upgrade.sh --negative-case bad-target-major
bash scripts/validation/rehearse-postgres-logical-upgrade.sh --negative-case timeout
bash scripts/validation/rehearse-postgres-logical-upgrade.sh
bash scripts/validation/rehearse-postgres-logical-upgrade.sh
```

Expected evidence: focused positive/negative tests pass; the normal rehearsal
uses `pg_dump -Fc --no-owner --no-acl` and
`pg_restore --clean --if-exists --no-owner --no-acl`; source and target oracles
match on all integrity fields except declared server version; the verdict has
`scope=synthetic-local`, `integrity_status=passed`,
`cleanup_status=passed`, and `redaction_status=passed`.

Actual evidence: focused tests pass 51/51 after historical review-remediation
RED 7/31, readiness-race RED 1/1, and second-review RED with 13 expected
assertion/subtest failures across 7 focused methods. The terminal-review
regression was RED in all 8 direct-control subcases before the ordering fix;
the later dual-ID matrix added target-ID acceptance, config-ID acceptance, and
unrelated-ID rejection while preserving the independent config-body gate.
`--check` passes with independent local source/target/client manifest and
configuration identities, the
full rendered topology, exclusive retained evidence identity, 360-second
operation budget, 60-second cleanup reserve, and current fixture SHA-256
`523d947400f5197ce362a11445a0c6e380a28431352679ea01ca24d106c34b57`.
The strict runtime sequence returned `0/50/50/10/20/0`. The final normal project
`hyhome-ior-20260719-1128131-source/target` passed authenticated readiness,
integrity, cleanup, and publication. The retained 4,484-byte dump SHA-256 is
`c3ebc52895bda22559f99efb72471f9928b9a097d64d0df6066be354d9a65581`,
with backup 0s and restore 0s. The exact 12-key, mode-0600, 642-byte canonical
handoff SHA-256 is
`dab8e587519a48059d62a46ae7f6b7b757fbad53486215df436fd0a90bd4b45a`;
schema is 1, and scope, integrity, cleanup, and redaction are
`synthetic-local`, `passed`, `passed`, and `passed`. No owned resource remains.
Explicit-base metadata selected 22 changed documents with zero violations;
traceability passed 46 pairs; implementation alignment passed 666 documents
and 5,443 links with zero failures; template contracts passed 38/38; Compose
validation passed five core services; Markdown, LLM Wiki freshness, Bash
syntax, ShellCheck, and diff hygiene pass. Repository contracts retain the
known four lifecycle consumer mismatches, missing `html5lib` renderer, and
future Task 5 delivery-script absence; no Task 4 contract failure remains.

The prior `c5f9e3a135d032e480c4484a5c545486f461562fc327923c9e4a3887f2883899`,
`712f289dacf3bb72cf7c3956b51ec258ae63ae3b2919d70218884cb9623dc3b0`,
`f0c07c294ade39417ed9c61b6c614b4bf86a59c14a8b4a26a84082ab39fbab76`,
and `bf7109f5fd15cf04615ed331cb63be7c7848d8656749e427c2a54a1aecd2d18a`
canonical identities are historical and superseded by the current frozen
handoff above.

Verification results: implementation/runtime PASS. Historical findings were
remediated and reviewed for their exact commits. The terminal whole-branch
review pair recorded below ends at `20022458` and predates current RED
`163f434b`, GREEN `e8934783`, focused CI routing `324a5ea3`, and the corrected
runtime handoff. The later exact review sequence through `8a0bd6f4` closes the
remaining implementation findings; post-evidence confirmation remains pending.
Exit classes are `0=pass`, `2=usage`,
`10=preflight`, `20=readiness`, `30=backup`, `40=restore`,
`50=integrity/negative case`, and `60=cleanup`.

Task 6 documentation, owner regeneration, safe gates, and review history are
recorded by the Program Task. No PostgreSQL wrapper, test, check, negative, or
normal command followed the current canonical-producing normal run. The
controlled all-files wrapper passed exactly once from checkpoint
`263e046f64f249b0e771e4f0c5d77a91c967e10f`. Later code, generated-owner, and
lifecycle commits were not covered by that wrapper; they use targeted gates
and exact final re-reviews. The wrapper is not rerun because its contract is
exact-once; final post-evidence confirmation remains pending.

## Controlled Agent Pre-commit Evidence

Controlled wrapper command: not owned by this domain Task. The Program Task
owned the sole exact-once all-files invocation.

Allowed prefixes: `not_applicable` at domain activation.

Program wrapper result: `hook_result=passed hook_exit=0`;
`snapshot_result=passed`.

Observed counts were
`before_count=0 after_count=0 changed_count=0 unexpected_count=0`; all four
Git-visible non-ignored path sets were `(none)`.

Observation boundary:
`observation=git-visible-non-ignored-repository-status`.

Disposition: Program-owned wrapper **PASS** only for exact clean checkpoint
`263e046f64f249b0e771e4f0c5d77a91c967e10f`. Post-wrapper commits
`9a24b0cb`, `78265090`, `73f4ea68`, and this lifecycle logical unit are
explicitly outside its coverage and use targeted gates plus the exact review
sequence recorded below. The wrapper is not rerun under its exact-once contract, and direct
`pre-commit run --all-files` remains prohibited.

## Review Evidence

Implementation review verdict: PASS for exact Plan ownership, pins,
full rendered synthetic-only topology, bounded clients, stable failures,
post-cleanup atomic publication, accumulated cleanup, redaction, and
independent manifest/config identity checks.

Specification review verdict: CHANGES REQUIRED C1/I3/M1 on initial candidate
`db2418c2`. Operations/quality review verdict: CHANGES REQUIRED C0/I5/M2 on the
same candidate. The second review wave on the amended candidate returned
CHANGES REQUIRED C0/I3/M1 and C0/I2/M0 respectively. Both waves remain
historical, and their findings are remediated. The next terminal re-reviews left
exactly two Important items: stale canonical invalidation on direct-control
failure and ignored report synchronization. Both are remediated. The subsequent
terminal operations/quality review returned APPROVED C0/I0/M0. The terminal
specification review returned CHANGES REQUIRED C0/I1/M0 solely for current
evidence synchronization; after that finding was remediated and the canonical
was reconciled, terminal specification re-review returned APPROVED C0/I0/M0.
The reviewer's direct-control exercise invalidated the canonical as designed;
the single approved normal reconciliation regenerated and directly verified
the then-current handoff without any later canonical-mutating command. Those
reviews predate RED `da06a080` and GREEN `adbbdce2`. Terminal specification
review v5 returned `APPROVED C0/I0/M0` for the full branch range through
`20022458` plus the final 26-document reconciliation diff. Terminal
quality/security review v3 returned `APPROVED C0/I0/M0` for the full branch
range through `20022458` plus the then-current 26-document reconciliation diff.

Findings and disposition: the complete deduplicated review set is remediated.
It covered exclusive evidence ownership and retained identity; unsafe canonical
invalidation/publication; publication ordering; non-short-circuit cleanup and
retry; one end-to-end deadline with cleanup reserve; full rendered topology;
reachable bad-major/timeout/signal paths; Task 2 runbook semantics; exact
evidence/commit wording; authenticated TCP readiness; direct-control isolation;
process identity and active budgets; exact project/network rendering;
generated-password and healthcheck binding; and bounded sleeps. Every finding
was independently re-reviewed. The terminal pair additionally covered the
direct-control/canonical state-machine ordering and ignored report freshness.
The specification evidence-synchronization finding was remediated and closed by
terminal APPROVED C0/I0/M0 re-review for its exact historical range. No review
verdict from those historical iterations is promoted to the current range;
the separate v3/v5 whole-branch approvals above also stop at `20022458` and do
not cover the current independent-identity hardening. Earlier
`CHANGES REQUIRED` iterations remain historical remediation evidence. The
later initial post-closure quality review returned `CHANGES REQUIRED C0/I1/M0`;
dual-ID RED/GREEN `ffc1cf13`/`d186644e` closes it, and exact quality re-review
`08288576..d186644e` is `APPROVED C0/I0/M0`. Exact specification re-review of
`d186644e..8a0bd6f4` is also `APPROVED C0/I0/M0`. Final post-evidence
confirmation remains pending.

The initial final Program specification review after the controlled-wrapper
checkpoint returned `CHANGES REQUIRED C0/I2/M0`: generated navigation owners
were stale, and the 15 local-isolated lifecycle documents still reported
`active`. Commit `78265090` refreshed the generated owners; this lifecycle
logical unit transitions the exact 15 Specs, Plans, and Tasks and synchronizes
their indexes. The initial final quality review returned
`CHANGES REQUIRED C0/I1/M0` because OCI config-digest inspection used an
unbounded, symlink-following read. RED `9a24b0cb` and GREEN `73f4ea68` route it
through the bounded stable-private reader. That row preserves the historical
checkpoint; the later exact quality and specification re-reviews are both
`APPROVED C0/I0/M0`.

## Commit Ledger

Historical implementation identity: branch-history commit `db150a19`
(`feat(ops): add postgres recovery rehearsal`). The earlier offline boundary
used RED `00a65be1` and GREEN `571b2ab1`; historical engine-identity hardening
used RED `da06a080` followed by GREEN `adbbdce2`. Current target/config
hardening is RED `163f434b` followed by GREEN `e8934783`; focused CI routing is
`324a5ea3`. Final compatibility evidence is RED
`ffc1cf130e64db3d61d2de067239c7d720fa3ee5`, GREEN
`d186644e6243b0598e54303ee9bec5344516cb99`, and CI/governance correction
`8a0bd6f440e884fec875f442c55906c0dec48edd`. Evidence reconciliation then
found that the CI routing test was absent from the Foundation manifest's
`github-governance.md` consumers. Commit
`e46a0e5a4356b8439cefdc26ed6a5fa23fd0f2d9` adds that exact consumer only;
the Foundation summary remains byte-identical. Fresh manifest/summary checks
pass, impacted lifecycle passes 159/0 with only the expected Task-directory
warning, and promoted lifecycle passes at zero. This evidence-only
reconciliation intentionally omits its own SHA.

Logical unit: `feat(ops): add postgres recovery rehearsal`.

Commit validation: 51/51 focused tests, static gates, and the strict frozen
runtime evidence pass as recorded above. Historical terminal specification and
operations/quality reviews are APPROVED C0/I0/M0 only for their exact reviewed
commits; terminal whole-branch specification v5 and quality/security v3 are
APPROVED C0/I0/M0 only through historical endpoint `20022458`. Exact quality
re-review `08288576..d186644e` and exact specification re-review
`d186644e..8a0bd6f4` are both `APPROVED C0/I0/M0`; post-evidence
whole-branch confirmation remains pending.

Post-wrapper remediation identities are generated-owner refresh `78265090`,
OCI reader RED/GREEN `9a24b0cb`/`73f4ea68`, and this lifecycle logical unit.
They and the later dual-ID/CI-governance corrections are validated by targeted
gates and the exact final re-reviews, not by the exact-once wrapper.

## Deferred and Blocked Items

Deferred items: live data, physical backup, PITR, HA/replication, remote
storage, retention/encryption certification, production recovery, and
organization RTO/RPO.

Blocked items: Task 4 has no remaining local implementation/runtime blocker.
This Task is completed at the representative-local boundary. The implementation
re-reviews are approved; only final post-evidence whole-branch confirmation
remains pending. Delivery may reference this verdict only as a recovery boundary
and must not claim database recovery for the stateless sample service.

Deferral destination: broader, live, shared, remote, or production recovery
requires a new approved Stage 01-04 chain, explicit human approval, and
operations/security review. Stateful delivery impact routes to
[Spec 125](../../98.archive/03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
rather than expanding Spec 127.

## Related Documents

- [Spec 125](../../98.archive/03.specs/125-infrastructure-operations-readiness-remediation/spec.md)
- [Infrastructure Plan](../plans/2026-07-11-infrastructure-operations-readiness-remediation.md)
- [Program Task](./2026-07-19-operational-readiness-closure-program.md)
- [Compose Task](./2026-07-19-compose-runtime-readiness-remediation.md)
- [Delivery Task](./2026-07-19-deployment-release-engineering-remediation.md)
