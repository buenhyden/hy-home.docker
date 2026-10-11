---
title: "P02 Secret Catalog and Value-Free Views Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-11"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0010"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P02 Secret Catalog and Value-Free Views Task

## Objective

Own criterion 16 and W32: one value-free catalog, per-ID classification,
generated views and regeneration guards, reusing existing parsers and issued
identities. This Task authorizes a parallel source preparation slice; it does
not implement P06's real credential migration or claim production consumption.

## Inputs and Authorization

The current user requests a P02 prerequisite/conflict assessment and a concrete
worker handoff. The supplied P02 prompt is compared with clean local main
`2b9f5ec82cb73ea148fb27bfbd2d35c10e328e51`, rather than its historical
`860ac1c3` baseline. Remote main observed during assessment is
`a31a38ca29ee8e0683a29e61bf41347bfddc3d62`; a subsequent `ls-remote` and fetch
confirmed remote main at `2b9f5ec82cb73ea148fb27bfbd2d35c10e328e51`.
ROOT did not push main in this assessment. These verified Git facts are separate
from session reports and operational acceptance. The earlier integration's
local-main/no-PR instruction is retained for SEC01/SMTP01/CLN01. The newly
supplied P02 execution prompt selects an owning-Spec PR after implementation
and latest-head CI/review; issuance itself makes no remote write. Dev is unused.

Read bootstrap/provider, SPEC-0204/0212, TSK-0005/0006/0007/0009, current root
declarations, public environment example, secret support matrix, generator,
public sensitive-reference example, and subject-0085 guide/policy/runbook.
Reconcile the complete reference code and tests with existing tools before
selecting canonical paths; never create a duplicate authority. Reference
heuristics are draft hints, not evidence of actual consumers or deletion safety.

### Worker Branch and Ownership

Create `codex/p02-secret-catalog` and
`/home/hyunyoun/data/hy-home.docker/.worktrees/p02-secret-catalog` from the
commit that issues this Task after it reaches local main. Record that exact
commit, worktree HEAD and clean status before writing. One existing or separately
assigned P02 worker owns the implementation; Task issuance starts no second
implementation session and does not touch foreign dirty worktrees.

The worker owns this Task and these source destinations, subject to a prior
NO_CHANGE/reuse check:

- `infra/03-security/openbao/secret-catalog.json` and
  `infra/03-security/openbao/secret-catalog.schema.json` as the single catalog
  and closed production metadata contract, not a second service inventory.
- `scripts/lib/ops/secret_catalog.py` for parsing, classification and view
  generation, plus `scripts/operations/secret-catalog.py` as its narrow CLI.
  Reuse SMTP01 and existing metadata parsing rather than copying them.
- `tests/lib/ops/test_secret_catalog.py` and
  `tests/validation/test_secret_catalog_contract.py`, with synthetic fixtures
  in `tests/fixtures/secret-catalog/` and its Korean README if needed.
- Existing `docs/05.operations/{guides,policies,runbooks}/0085-openbao.md` for
  the single secret-management owner, and the catalog paragraph in
  `infra/03-security/openbao/README.md`.

The worker prepares an ignored `.agent-work/integration-proposal/README.md` with exact
base blob IDs and patches for `scripts/operations/gen-secrets.sh`,
`secrets/SENSITIVE_ENV_VARS.md.example`, `infra/secret-file-support.json`,
`scripts/lib/ops/README.md`, test/fixture indexes and required manifest/workflow
regression registration. The integration coordinator is their sole final
writer. Any necessary public environment/schema amendment is also a proposal
for its P03/coordinator owner; it never sources or rewrites real dotenv state.
Root Compose, real/public environment, gateway, Alloy, backup, Registry,
Spec/Plan and other Tasks are read-only to the worker. A new shared need must be
added to the proposal before implementation and reviewed against current head.

### Parallel and Waiting Boundaries

Proceed now with public-source inventory, value-free catalog/schema, aliases,
classification, provisional destination plans, generated staging views,
regeneration guards, synthetic tests and subject-0085 documentation. Preserve
COMM-002 at `secrets/communication/smtp/smtp_password.txt`; COMM-003 is an
alias/tombstone without another source/value/KV entry. Never renumber IDs.

The current public scanner consumes a ten-column source table and the SMTP
two-column alias table. The reference eight-column view is not a compatible
drop-in replacement. Preserve those consumers or submit a coherent parser,
generator and regression proposal with the SMTP01 owner; never change the
generated view alone. Image support is referenced from the existing support
matrix, not duplicated into a second mutable version authority.

Classify kv_static, stable_crypto, bootstrap_external, public configuration,
derived/runtime copies, UNUSED_DELETE and LAB exclusion separately. Preserve
encryption history and independent recovery custody. Keep unknown consumers
BLOCKED_FACTS and CLN01's positive rollback/init consumers retained. No profile
or lack of recent traffic proves absence. Published metadata must distinguish
declared, observed, imported, delivered, consumed, rotated, recovered and retired.

Wait for SEC01/P01's final image, auth, Agent and recovery contracts before
asserting final ACL/delivery/restart mappings or successful consumption. P06
owns selected real KV copy, credential delivery and migration acceptance.
CLN01 owns generic deletion eligibility; SMTP01 is the sole COMM-003 executor.
Reference migration code may be adapted and tested with mocks only in this
slice. It must not access production KV, tokens, secret payloads or source files.

No private sensitive table overwrite, credential read/copy/rotation/deletion,
HOME restart, LAB runtime, learning-app planning, actual Wiki or external
workspace creation occurs. Later private metadata inspection must first name
the exact host/path, output filter and recovery boundary in this Task and pass
independent review; only names, paths, modes and consumer metadata may leave it.

## Work Log

Task issuance has a measured RED probe on input `2b9f5ec82`: no Task 0010,
criterion 16 or W32 existed. This documentation-only unit supplies those
contracts; the matching availability probe passed after issuance. The first
metadata check failed on prose in W32's dependency cell and a non-draft initial
Task status. Correcting only those fields produced selected=3, violations=0,
exit 0; the resulting Task remains draft. Independent review and document
links confirmed the issuance boundaries and existing link targets. The worker
implementation, full per-ID acceptance and all runtime
lanes remain unexecuted at issuance. Do not mark this Task completed merely
because it is issued.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Issuance baseline | 16, 8 | W32 | Task/criterion/work-unit availability probe | 2b9f5ec82 | FAIL | Coordinator private issuance RED receipt; no values | pending |
| Issuance source contract | 16, 8 | W32 | Availability GREEN and selected metadata after dependency/status correction | 2b9f5ec82 plus three issuance documents | PASS | Coordinator GREEN and metadata retry receipts; exit 0 | pending |
| P02 source implementation | 16 | W32 | Complete catalog, schema, aliases and generated views | Worker issuance commit pending | NOT_RUN | This Task and worker handoff | pending |
| Private migration and consumption | 16 | W32 | Selected P06 runtime contract and actual receipt | Final P01/SEC01 contract pending | NOT_RUN | P06 owner | pending |

## Review and Completion

Before each unit, record actual input SHA and a meaningful RED/GREEN test.
Cover malformed IDs/fields/paths, sensitive-field rejection, canonical and
alias uniqueness/cycles, SMTP one-source behavior, migrated/retired reissuance
refusal, crypto/recovery retention, staging-only output and private/env
noninterference. Do not equate schema fields or mock KV equality with actual
security, migration or recovery evidence. Scan free text and outputs for secret
leaks and independently review the generator/custody boundaries.

Run focused unit and contract tests, Ruff, schema/view drift and existing secret
metadata/support/SMTP/retirement regressions affected by the proposal. Run
metadata/links/lifecycle for changed documents, exact changed/staged registered
checks, and independent security/code/document review at the final head.
Preserve logical catalog/schema, tooling/guards, and documentation commits.
The coordinator integrates common proposals once and reruns affected checks.
Preserve those logical commits in one SPEC-0204 P02 PR, compare its diff against
fresh remote main, require actual latest-head CI and independent review, and
merge without admin bypass. Then fast-forward local main and remove only the
merged clean worker branch/worktree after preserving its evidence. If the
current remote baseline changes, rebase/reconcile and rerun affected gates
before delivery. Never include unrelated preceding integration or SEC01 HOME
units in the P02 PR; dev is unused.

Hand P01/P03/P06/P08/P10 the catalog SHA/schema version, ID/alias mapping,
planned path/ACL/delivery/reload/recovery graph, blocked consumers, exact test
receipts and final local main SHA. Report SOURCE/UNIT/STATIC/ISOLATED/HOME/
MIGRATION/ROTATION/RECOVERY/DELIVERY separately, with real commands and exits.

## Related Documents

- [SPEC-0204](../spec.md)
- [SPEC-0204 Plan](../plan.md)
- [SMTP01 contract](tsk-0005-cross-tier-contracts-second-round.md)
- [OpenBao trust and recovery](tsk-0006-openbao-trust-bootstrap-and-recovery.md)
- [CLN01 retirement](tsk-0007-cln01-material-retirement.md)
- [SEC01 continuation](tsk-0009-sec01-stable-security-integration.md)
- [OpenBao guide](../../../05.operations/guides/0085-openbao.md)
- [OpenBao policy](../../../05.operations/policies/0085-openbao.md)
- [OpenBao runbook](../../../05.operations/runbooks/0085-openbao.md)
