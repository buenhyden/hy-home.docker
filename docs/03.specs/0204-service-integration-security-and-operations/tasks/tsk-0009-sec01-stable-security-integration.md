---
title: "SEC01 Stable Security Integration Task"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0009"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-10"
---

# SEC01 Stable Security Integration Task

## Objective

Integrate the SEC01 stable/security source ledger and bounded repairs without
treating candidate images, source receipts or isolated recovery rehearsal as
production rollout. This Task owns criterion 15 and W31. It does not replace
CLN01 criterion 12/W24, P09 criterion 13/W25, or SMTP01's criterion 14/W26–W30
reservation.

## Inputs and Authorization

The direct 2026-10-10 request and coordinator authorization issue this Task on
base main `e93e0c8223191bf26aea7578a231b2dbf016fc7c`. SEC01's six-commit source
branch ended at `55a0d4719635f325f1d4ea477dcf50a5ff5ddbf6`; PR #416 was merged
at the base revision, but latest candidate-quality CI run `38052766613` failed.
CodeQL and GitGuardian passed; main-security was skipped. This Task therefore
starts in progress with latest/security acceptance blocked, not complete.

The received ledger is `infra/09-platform-ops/security-updates/integration-handoff.json`.
It is evidence input, not permission to apply proposed common-file patches. The
coordinator serially integrates the shared validator, service inventory, script
manifest and navigation after current-main review. SEC01 does not deploy an
image, read a secret, change LAB runtime, or create a learning application.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0009 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0009 | ready | in-progress | #sec01-received-handoff |
| SPEC-0204 | blocked | in-progress | #sec01-received-handoff |
| SPEC-0204-PLAN-0001 | blocked | in-progress | #sec01-received-handoff |

### SEC01 Received Handoff

The branch reported source/unit/static/isolated receipts for OpenBao issuance
(36 tests, 92-percent helper coverage), workflow bundle (8 tests), supply-chain
gates (71 tests), version contracts and isolated OpenBao rehearsal (2 tests,
177.078 seconds). These receipts are attributed to the handoff's recorded
inputs, not latest-main or production acceptance. The historical common
validator suite was 20 PASS/2 FAIL, the script manifest had two missing records,
both stable/security evidence gates exited 2 as `BLOCKED_EVIDENCE`, and the
changed local gate failed six shared assertions. Those failures remain the
repair boundary until coordinator-owned current-main checks prove otherwise.

On current `e93e0c8223191bf26aea7578a231b2dbf016fc7c` plus the coordinator
integration input, both gate CLIs again exited 2. The latest gate reported
`ready=false`, no missing or unexpected services, `deployed=false` and
`externalfacts=false`; the security gate reported `ledger_complete=false`,
`coverage_checked=true`, 124 observed `blocked-evidence` entries and no missing
or unexpected services. Both bind root input manifest SHA-256
`3a2e7451e6211b43b9d8f9c9760fed0fcf5cdac381e45e1b2323628b60756f66`.
The observed 124 is a receipt, not an inventory constant. An earlier root
aggregate failed four manifest assertions while interpreting authority; retain
that historical failure rather than presenting all aggregate QA as PASS.

PR #416 candidate-quality failed on service-inventory Airflow Env drift. Its
proposal may be reviewed against current main, but apply-check or in-memory
rehearsal is not a shared-suite PASS. The GoTrue v2.197.0 image contract is
read-only input for SMTP01; SEC01 neither converts SMTP secrets nor implements
a native `_FILE` adapter.

### Coordinator Common Repair Receipt

The coordinator used a dedicated `codex/sec01-integration` worktree on
`e93e0c8223191bf26aea7578a231b2dbf016fc7c`; other sessions' worktrees and dirty
root files were untouched. The validator proposal was reviewed and applied to
its two target tests. The existing inventory renderer supplied only the seven
current Airflow Env-cell changes; dated historical inventory stayed unchanged.
The two existing supply-chain libraries were registered under their durable
security-updates README authority, without changing their bytes or weakening
manifest validators. Initial Task-authority/README-consumer registration failed
four assertions; corrected durable ownership and direct consumers passed.

Before repair, the runtime/wiring command ran 30 tests with four failures,
exit 1. After repair, the same suite passed 30 tests; ServiceInventoryTests
passed 15; script-manifest regressions passed 48. The coordinator replay of
all four modules ran 93 tests, exit 0 (18.000 seconds). Manifest/generated
checker and operations-catalog checker also exited 0. Runtime validator hash
is `48ccd21370d2b6557a7dccbe0d9a4ac02143786d21aef955f1a89272fb3e1950`;
wiring validator is `9b61ab1b64399f62d28e261a3da10bf71f55bc69860cca57cba345ca63873870`;
inventory is `8535b63b85068a185cc59646e932e47c67689cbd72563adaa811756c62502951`.

The received SEC regressions were absent from the hosted candidate leafs.
A new routing regression first failed seven assertions, exit 1. The coordinator
registered offline issuance/trust, candidate expiry, version and workflow bundle
selectors in the required Compose leaf and update-gate negatives in the
supply-chain fixture leaf. Native selectors remain separately opt-in; selecting
only offline classes cannot imply native PASS. A first root-rule attempt used
non-optional roots and failed schema checks; those invalid root rules were
removed, preserving the existing operations aggregate owners. Routing plus
workflow-contract regressions then passed 39 tests, exit 0, and
`check-github-workflow-contract.py` exited 0. A guessed nonexistent checker
filename exited 2 before the correct registered checker was used; this is a
command-selection error, not a product regression.

Fresh public-source CLI evaluation used `update-ledger.json` for both
`latest_version_gate` and `security_update_gate`. Both exited 2: latest
`ready=false`, security `ledger_complete=false`, no missing/unexpected source
services, `deployed=false` and `verified_external_facts=false`. Source input
manifest SHA is `3a2e7451e6211b43b9d8f9c9760fed0fcf5cdac381e45e1b2323628b60756f66`.
The observed 124 rows are a result, never a service-count constant. Field/coverage
checks do not verify supplier releases, scans, live compatibility or recovery.
Criterion 15 remains pending; a source repair merge cannot close SEC01.

### Candidate Image Grammar Repair

PR #418 head `3f6aa5e8d4b09d8d270166a19587884ee0612445` failed
candidate-quality run `38056697221` at Tier01 with `invalid compose service
image contract`. The existing parser accepted either tag or digest and rejected
valid `tag@sha256` references. The one-line grammar repair makes the constrained
tag and exact lowercase SHA-256 digest independently optional while preserving
full matching, 255-character bounds and safe YAML parsing. Two new regression
assertions failed before repair; the repaired full version-contract module
passed 49 tests. The actual `01-gateway` hardening check, shell syntax, Ruff
and diff checks passed. Independent code and security reviews found no P1/P2.

Frozen hardening hash is
`068a87dc1cb2c6afb937602f4497c3c467a91d588684aa1be081b925058f702c`;
test hash is `ff6629f6e8a80987c74da9572107c3054c95965f5ae4721ba44c4a64f77cc76b`.
These are offline/source checks. Hosted CI at the new committed head remains
required; run `38056697221` remains a FAIL receipt, not accepted delivery. No
image deployment or HOME verification occurred.

### Delivered Common Repair and Module Registration Follow-up

GitHub confirmed PR #418 merged by the repository owner at
`80c31405df7983dc4b7d8ad8823f73323247d264` on 2026-10-10 14:17:16 UTC.
Its head `d0d15c0662139cb34bbeb7ad1a65e2dc52b719d9` passed hosted
candidate-quality run `38058055919`, CodeQL and GitGuardian. This records
external delivery of the bounded common repair, not SEC01 global completion.

A separate full-profile ownership replay ran seven tests with one FAIL: the
new required class selectors appeared as classes rather than reachable modules.
The coordinator replaces those selectors with their complete containing modules,
each once, and allows skips only for `CandidateNative` and
`WorkflowCandidateRehearsalTests`. Existing expiry and workflow-source tests
remain required; native flags remain explicit opt-ins. The ownership validator
is unchanged. Tests-only RED failed five assertions; the corrected ownership
suite passed seven tests and workflow/routing passed 40 in that initial freeze.
Those receipts were superseded when independent code review reproduced duplicate
native skip receipts: the candidate module exposed an imported foreign TestCase.
The canonical adapter rejected them with `ci-gate-adapter-tests-skipped`, exit 2
(outer regression exit 1; 13 tests, six skips).

The candidate now imports the rehearsal module rather than exposing its TestCase;
two existing references preserve native behavior. The bounded 60-second canonical
adapter regression passed after this correction. Replacement workflow/routing
passed 41 tests; offline modules passed 12 with five expected native skips,
without duplicate receipts. The routing module passed five tests again after
the timeout was added. These are source/unit results, not native verification.
The intermediate duplicate class/module registration failed ownership and was
removed, rather than weakening the invariant. Hosted CI on the follow-up head
remains required. No HOME, deployment or private resource action occurred.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SEC01 source and isolated receipts | 15 | W31 | Received six-commit source, focused tests and isolated rehearsal | Recorded branch/input hashes in integration handoff | PASS | security-updates handoff | pending |
| Common validator and manifest state | 15 | W31 | Current shared suite and manifest registration | 20 PASS/2 FAIL; two records missing | FAIL | integration handoff | pending |
| Latest/security evidence gates | 15 | W31 | Current root-bound stable and security gate commands | Both `BLOCKED_EVIDENCE`, exit 2; latest `ready=false`, security `ledger_complete=false`; manifest SHA recorded above | DEFER | SEC01 received handoff | pending |
| PR #416 candidate CI | 15 | W31 | candidate-quality, CodeQL, GitGuardian and main-security | Run `38052766613`; candidate-quality failed | FAIL | PR #416 handoff | pending |
| Coordinator shared repair | 15 | W31 | Runtime/wiring, inventory, manifest and candidate regression registration | e93e0c822 plus reviewed integration; 93 and 39 tests exit 0 | PASS | #coordinator-common-repair-receipt | pending |
| HOME, migration, rotation and recovery | 15 | W31 | No operational action authorized | No exact target/custody/recovery boundary | NOT_RUN | Future exact Task | not-required |

## Review and Completion

Before delivery, integrate only reviewed common changes through their assigned
single writer; regenerate the version projection after preceding SMTP/CLN work;
run the registered changed gate, current common validator/inventory/manifest
checks, both latest/security gates and latest-head CI. Require independent
security and code review at that head. Preserve failed and blocked receipts.
Source rollback is a logical revert of owning commits; HOME rollback requires a
separately approved pre-upgrade backup and recovery proof.

`SOURCE`, `UNIT`, `STATIC` and `ISOLATED` remain distinct from `HOME`,
`MIGRATION`, `ROTATION`, `RECOVERY` and `DELIVERY`. The latter lanes are not
accepted by this Task's received evidence.

## Related Documents

- [SPEC-0204](../spec.md)
- [SPEC-0204 Plan](../plan.md)
- [Security updates ledger](../../../../infra/09-platform-ops/security-updates/README.md)
- [Platform Operations](../../../../infra/09-platform-ops/README.md)
