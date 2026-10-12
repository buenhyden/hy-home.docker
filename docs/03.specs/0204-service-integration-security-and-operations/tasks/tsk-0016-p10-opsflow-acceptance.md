---
title: "P10 Opsflow Acceptance Task"
version: "0.1.4"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0016"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P10 Opsflow Acceptance Task

## Objective

Own criterion 21 and W63–W69: acceptance of one bounded Opsflow vertical slice,
from a manifest input through authenticated Airflow publication, DEV transaction
and outbox, reader query, n8n claim, SMTP capture and acknowledgement, followed
by failure handling and an independently bounded restore. This Task prepares the
acceptance contract and evidence ladder before any native or HOME action.

The slice remains independent of the unimplemented Wiki application. It does not
create a Wiki core, client, search resource, collection, workspace, schedule or
blog-data write. Learning applications and LAB runtime services, configuration,
secrets, data, images and execution are excluded. P08 may move typed LAB
documents only into the corresponding Stage05 family `labs/` paths.

## Inputs and Authorization

The direct P10 request authorizes an owning Task, source/test preparation,
logical commits, review and reviewed local-main delivery. The historical analysis
baseline is `860ac1c3633eac9ad416fb1abd8a61a6e617ebd8`; it is context, not a
runtime target. The initial P10 worktree branch is
`codex/p10-opsflow-acceptance` at local HEAD
`43917df47f94f0ddd7e1dbbf7bb7cc87701a56c8`. Fresh `origin/main` and the
actual remote observation are `c26c3b93f4e73034ddad4d08ba9da8eaa9fec0c7`.

Git history was checked for the maximum issued Task number 15 and no issued
Task 16 or P10 ref. The shared root's 24 foreign paths remain preserved; no
secret values were read. Recheck the exact input refs, dirty paths and relevant
owner heads before every implementation unit. Never reset, stash, clean or
stage another worker's changes.

The direct delivery lane is local `main`, without `dev` or a required PR.
The supplied prompt's future PR language does not authorize a remote action in
this lane. A later explicit remote lane must recheck its current ruleset, CI and
independent review at the actual head. No secret value, raw environment file,
credential, production client or external SMTP send is permitted in preparation.

One owner may prepare only this Task, the acceptance test
`tests/validation/test_opsflow_e2e_acceptance.py`, and
`tests/fixtures/opsflow-acceptance/{README.md,manifest.valid.json,cases.json}`.
The fixture README is Korean and describes synthetic input only. A new helper
requires a completed reuse audit and an additional exact lease; it must be pure,
value-free and unable to provision, import, schedule or mutate a runtime.
Write a RED test before the corresponding implementation and retain both
receipts. Shared registration, README/index, manifest, workflow and CI edits are
coordinator proposals until one named writer takes a bounded lease.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0016 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0016 | ready | in-progress | #w63-frozen-public-input-audit-2026-10-11 |

### W63 admission, reuse and source-receipt inventory

Inventory existing P04 publication, P05 notification, P01 issuer/recovery,
P02 catalog, P03 endpoint and P06 migration contracts before adding a test or
fixture. Record each source receipt as SOURCE, UNIT, STATIC, ISOLATED, HOME,
MIGRATION, ROTATION, RECOVERY or DELIVERY rather than promoting a synthetic
result to native acceptance. Existing P04 SQL/DAG/parser, P05 workflow/node,
P01 issuer, P02 catalog, P03 contracts, P06 migration, P07 controls and P08
moves remain owned by their current Tasks.

Current source preparation is permitted while those owners retain operational
acceptance. No global SEC01, P01 or P06 completion gate blocks a scoped,
pre-migration DEV source fixture. An exact image, service identity, endpoint,
role, backup set, operator, recovery boundary and cleanup plan are still needed
before an affected runtime lane starts.

At admission, committed SEC continuation `6f230c56`, SEC integration
`6aff7433`, SMTP `39ff7f91`, and the current P01/P03/P04/P05/P06/P07 heads are
ancestors of local `main` `43917df` and remote `main` `c26c3b93`; P08 `43917df`
is local only. Dirty SEC integration paths and the foreign Task0008 edit in the SMTP worktree
remain uncommitted and preserved. Task-reported historical tests are inputs to this inventory, not
fresh P10 tests; every P10 source, unit and runtime test remains NOT_RUN until
its own receipt is recorded.

### Dated prerequisite snapshot — 2026-10-11

These are public owner-record observations at local main `43917df47`, not fresh
native tests or automatic knowledge of other chats. GitHub observation proves
remote main `c26c3b93f` and no open PR; matching committed ancestry proves source
inclusion, not operational acceptance. P10 consumes committed public inputs only.

- SEC01: continuation branch `codex/sec01-home-continuation` has clean HEAD
  `6f230c56eb97c3cd587d636ba6492b24de13e53d`, included in both observed main
  refs. Its integration checkout is detached at
  `6aff7433c755feacf659f7654a5ad3b9e70f401d` with ten dirty foreign paths.
  Task0009 remains in-progress; the global latest/security ledger and complete
  HOME deployment/recovery are not accepted. Those dirty bytes are not P10
  inputs. A fresh provider lookup may pass the latest-version dimension when
  no newer stable release exists; it cannot substitute for scans, authentication,
  HOME or restoration evidence.
- SMTP01: integration HEAD `39ff7f91562906ae87194693a0e3895f33a8acd3`
  is included in both observed main refs. Only its foreign Task0008 file is
  dirty there. Canonical COMM-002 source wiring is integrated. Task0005 records
  an attributed assignee report of comparison, backup and duplicate unlink;
  its independent operational retirement acceptance remains DEFER/pending.
  The later coordinator-owned two-file isolated restore has an actual exit-0
  SUCCEEDED receipt dated 2026-10-11T00:13:36Z, with outcome SHA256
  `74794448811aa3632b707ec8043e67e84033510d6731cb96a3335717a0690699`.
  This is bounded historical-snapshot restoreability only, not application
  recovery, SMTP authentication/send, HOME activation, production RPO/RTO,
  offsite custody or external-consumer absence. P10 did not rerun that restore.
- CLN01: its source/helper is included in current main, while Task0007 is
  draft and source-bounded. Fresh source/runtime/job/backup-restore/external
  consumer proof, private apply, actual deletion and real recovery remain
  blocked or NOT_RUN. COMM-003 stays held for the SMTP01 executor; cross-executor lock/order
  compatibility remains unresolved and owner-gated; PG-020 remains retained as an initialization/recovery consumer.

P10 neither edits nor stages the shared root's 24 foreign paths, SEC dirty
source/evidence or SMTP Task0008. The owners must deliver current relevant
artifact/connection/backup facts before the dependent P10 runtime lane starts.

### W63 frozen public input audit — 2026-10-11

Continuation starts at local main and clean P10 HEAD
`73ebd1ea16d457b1de8ba7b99d02c42c73f48805`. The actual remote and
origin observation remains `c26c3b93f4e73034ddad4d08ba9da8eaa9fec0c7`.
The acceptance test/fixture writer owns only the four paths issued above; the
coordinator alone owns this Task and final common registration. No P04/P05
implementation or operational executor lease is transferred.

The coordinator reread the committed P04 parser/adapter, publication SQL, P05
preflight, inactive workflow and outbox contract. Reuse is sufficient for
caller-side manifest/object/publication and notification-projection assertions;
no new production helper is required. This is not a native SQL, SMTP or restore
execution. P04 remains the sole publisher/SQL owner and P05 remains the sole
notification/node owner.

| Public input | SHA256 or observed condition | Meaning |
| --- | --- | --- |
| P04 publication SQL `001_opsflow.sql` | `57a744cf33581bafd73f610b9c18c83d64c9457486a02e02398df56b444ee584` | Current source identity, not installed migration or privilege acceptance. |
| P04 SQL checks `002_checks.sql` | `0a00944569aa05b7a0eec6a555cc3357197b26257ee76a1779c7e258eb9a0b73` | Current source identity, not native PostgreSQL execution. |
| P04 parser | `ef19e0093b990c6b8400b29f234877e9d6f346a38440f3a181c37aa5cd744b60` | Reused immutable manifest/run identity API. |
| P04 adapter | `2bba454121d52d04716d55d9adb8986374b9324a7f6259ba83b6ad15de707af3` | Reused conditional object/readback and function publication API. |
| P05 outbox contract | `dd73e9ca574e677d2edfcf2e4b7ffe7d4a31f59b9d6d2545c53a07413b0c8e70` | Source hashes match P04; native binding fields remain null. |
| P05 preflight | `2ebcb7fd2174fd1631c9d4eb4489382861667d14b3eba8a29779b0ab0962ded9` | Existing fail-closed consumer validation, not credential delivery. |
| P05 inactive workflow | `4cfbfec5ecbcb286196131336c92c2afc72c5639c25af7f7e596648942c3c719` | Existing five-field claim projection; SMTP acceptance and DB ack remain non-atomic. |

The exact coordinator command was a Python subprocess invocation of
`docker image inspect --format '{{json .Id}}\n{{json .RepoDigests}}\n{{json .Config.User}}'`
for each selected public tag: `hy-home/airflow:3.3.2-keycloak`,
`hyhome/n8n:2.42.6-local` and `chrislusf/seaweedfs:4.48`.
All three exited 1 with the stable error class `IMAGE_ABSENT`; a follow-up
read-only inspection classified the failures without printing raw diagnostics.
This proves those local tags were absent at this observation, not that every
candidate digest or a running older service is absent. No image was pulled,
built, started or accepted. The orchestration script exited 0 after retaining
each child exit code; it is not an image gate PASS.

The P04 protected CA-to-driver contract explicitly rejects TLS execution with
`tls_delivery_not_ready`. Its README still requires reviewed function-only
provisioning instead of the current broad-grant provisioner. P05's native SQL
commit/hash/interface/review binding is null, transport cancellation is unbound,
and the native credential/executor/Mailpit boundary is unaccepted. These are
concrete affected-lane prerequisites, not a blanket dependency on completion of
SEC01, P01 or P06.

Next native inputs are the SEC01 accepted workload image/package receipt,
P03 actual worker UID/GID and selected endpoint/TLS/delivery/timeout boundary,
P04 accepted SQL/function privileges/object-prefix policy and real publication,
and P05 accepted installation/credential/capture boundary. Until those owners
supply the relevant exact contracts, W65 remains NOT_RUN. The complete P10
backup set and empty restore target remain UNKNOWN; W67 waits for its feature
owner. W64 may proceed now against the frozen public inputs. The read-only
inventory and hashes are preserved in ignored local audit material; the Task is
the authoritative progress record.

### W63 baseline regression and authored-row correction

At unchanged public source input `73ebd1ea`, the coordinator ran:

```sh
python3 -m unittest tests.lib.ops.test_opsflow_manifest \
  tests.lib.ops.test_opsflow_adapters tests.lib.ops.test_opsflow_provision_contract \
  tests.validation.test_opsflow_airflow_contract \
  tests.lib.ops.test_n8n_outbox_workflow \
  tests.validation.test_n8n_outbox_contract \
  tests.validation.test_n8n_outbox_rehearsal -q
```

The existing seven modules passed 68 tests in 0.387 seconds, exit 0. This is a
fresh baseline synthetic regression receipt, not W64's new test, native
publication, SMTP capture or a new coverage measurement. The W63 independent
read-only review recomputed all seven public hashes and accepted the source
claims with no Critical or Important finding.

The first authored Task row combined source PASS and image FAIL in a free-text
Result cell. The actual metadata gate rejected the registered result-domain
violation, exit 1, with 146 findings including package-fallback archive cascades;
lifecycle exited 3. Full links passed, exit 0, with the existing archive capture
warning. The correction separates source audit PASS from image inspection FAIL
using the existing Result and Acceptance enums. No validator, archive or
unrelated document was changed. The next lifecycle check exited 1 with two invalid-event findings because the
new evidence anchor used a manually guessed double hyphen. The existing
`links._headings` API returned the single-hyphen anchor; that Task reference was
corrected. Corrected final checks remain a separate receipt.

### W64 synthetic acceptance preparation

Prepare one value-free manifest and fault cases that model the accepted path:
manifest validation, immutable object identity, DEV transaction/outbox state,
reader visibility, notifier claim, capture acknowledgement, retry/dead state
and independent recovery reconciliation. Tests reject duplicate or conflicting
inputs, unsafe paths, invalid source/date, bounded-size violations, negative
roles, secret-path aliases, plan collisions and premature deletion.

Fixtures must contain no operational credential, actual recipient, real object
data, connection string or operational identifier. Synthetic IDs, hashes and
bounded synthetic bytes may model the existing public contracts. They prove only caller-side acceptance contracts.
They do not provision PostgreSQL roles, a bucket, an Airflow DAG, an n8n import,
an SMTP account or an OpenBao identity.

### W64 caller seam RED/GREEN and registration — 2026-10-12

The initial assigned writer reported no source writes or executed tests after
its read tools returned no output. The coordinator suspended that four-file
lease, confirmed the files were absent, and became their sole writer. This is
not an external SEC01/SMTP01/CLN01 restart or an operational executor transfer.

The six new tests compose existing P04 `ingest`, `S3Store` and `PgPublisher`
with the existing adapter-test SDK/driver doubles, then reuse P05
`validate_claim`, `evaluate_outcome` and `pending_prerequisites`. There is no
new publisher, SQL/outbox state machine, notifier or restore helper. The test
supplies a synthetic caller claim; it does not generate that claim through SQL
or authenticate an actual lease. P05 outcome evaluation is its existing
synthetic oracle, not a native SMTP/DB operation.

The witnessed initial RED used:

```sh
python3 -m unittest tests.validation.test_opsflow_e2e_acceptance -v
```

It exited 1: five missing-fixture errors and one assertion for the absent
mandatory CI module. This is RED for preparation assets/registration, not a
reproduced production defect. After the three named fixtures were authored, the
five seam tests passed. The first full run still exited 1 because the new test
omitted the existing routing API's `changed` profile argument. Correcting that
call produced six PASS, exit 0. No guard or existing implementation was weakened.

The scenarios verify conditional object creation/readback before parameterized
publication, identity propagation to the five-field notification projection,
DB-failure rollback with verified object retention and replay reuse, conflicting
object refusal without overwrite/publication, unsafe path/secret alias/partition
rejection without publication effects, and refusal to claim success after ack
loss, truthy-but-not-true ack, wrong run receipt or lost retry lease. Native
binding remains blocked even after a synthetic publication success. These do
not prove real concurrency, reader visibility, function privileges, dead
requeue, backup completeness or restoration; those remain W65–W67 work.

The coordinator added only one mandatory module to the existing repository
integrity leaf, explicit test/fixture changed-path and changed-root rules,
the fixture README's existing package profile path and parent navigation.
Existing workflow nodes, argv, routes, actions, permissions and Registry
payloads were programmatically compared with the baseline, allowing only these
specified additions. `scripts/manifest.yaml` is NO_CHANGE because no library or
executable was added. No runtime source, Compose, environment, catalog or
secret file changed.

A system-Python coverage availability probe exited 1 (`No module named
coverage`). The existing `/tmp/hy-home-p09-qa/bin/python` environment was reused;
no global install was performed. The exact combined synthetic command was:

```sh
env COVERAGE_FILE=.agent-work/p10-coverage-data \
  /tmp/hy-home-p09-qa/bin/python -m coverage run --branch \
  --include='*/workflow_lib/manifest.py,*/workflow_lib/adapters.py,*/manifest-outbox-notifier/tools/build_workflow.py,*/manifest-outbox-notifier/tools/preflight.py' \
  -m unittest tests.lib.ops.test_opsflow_manifest tests.lib.ops.test_opsflow_adapters \
  tests.lib.ops.test_opsflow_provision_contract tests.validation.test_opsflow_airflow_contract \
  tests.lib.ops.test_n8n_outbox_workflow tests.validation.test_n8n_outbox_contract \
  tests.validation.test_n8n_outbox_rehearsal tests.validation.test_opsflow_e2e_acceptance -q
```

This passed 74 tests in 3.070 seconds, exit 0. The earlier 68-test baseline is a
subset, not an additional 68 unique tests. After the process exited, the final
`coverage report --fail-under=80` exited 0: combined statement/branch coverage
99 percent for these four existing helpers only (536 statements, five missing;
192 branches, three partial). It is not repository, TypeScript node, SQL,
native runtime or deployment coverage. The published fixture fields contain
only synthetic bytes/IDs, source allowlist names and expected bounded outcomes.
The first eight-file staged gate exited 1 solely because Ruff format-check
requested formatting of the new test. Ruff was applied only to that owned file;
all other selected lint/secret checks had passed. Final staged/common-head
checks and independent source/security review are required before local-main
delivery; they are recorded separately below.

### W64 exact fixture README gate correction

The initial styled eight-path candidate reached actual validation, not merely
an explain plan. The registered run exited 2 at candidate preflight with
`additional-path-invalid` for the new fixture README; later leaves were NOT_RUN.
Actual metadata exited 2 and lifecycle exited 3 for the same configuration
error. The Registry addition alone did not admit the path through the existing
repository-surface allowlist. The initial independent content/code approval was
therefore not a final gate acceptance.

The coordinator's shared-file lease was expanded only to
`scripts/lib/document_governance/registry.py`,
`scripts/lib/document_governance/metadata/profile.py`, and the existing
`tests/lib/document_governance/test_registry.py`. This implements the current
user-authorized document registration with its regression rather than adding
an exception or another validator. It is a narrow supporting change for W64;
P08 document mappings, moves and runtime remain untouched.

The existing two operations-fixture README tests were extended to the one new
P10 README, actual metadata selection and adjacent data/nested/case-fold refusal.
Before the source correction, the focused unittest exited 1 (RED). Adding the
single exact path to the existing Registry surface and metadata managed-file
sets produced two PASS, exit 0 (GREEN). No generic `tests/fixtures/` wildcard,
fixture-data profile, parser bypass or lower validation threshold was added.
The final candidate therefore has eleven owned paths, including those three
supporting source/test paths. Existing declarations and preserved foreign
inputs must still match, and final source/security review and registered gates
must be rerun against this new input.

### W64 registered taxonomy failure and bounded continuation

The exact eleven-path registered aggregate exited 1. Candidate preflight,
full links, fifteen lifecycle CLI regressions and 148 metadata regressions had
passed; the document-governance library leaf ran 690 tests in 702.913 seconds
and failed only `ActiveStageScopeTests.test_native_provider_files_are_exact_paths_not_directory_prefixes`.
Its explicit expected managed-file set still listed the earlier fixture README
paths. Remaining seven registered leaves were NOT_RUN at that failure.

The coordinator extended its supporting lease only to the existing
`tests/lib/document_governance/test_taxonomy.py`. The expected exact set now
includes the P10 README, while adjacent JSON, nested README and a case-varied
folder remain rejected. The focused class then passed, exit 0. This changes a
registered path expectation to match the newly approved contract; it does not
remove a guard or convert the original aggregate FAIL into PASS.

The final source candidate now has twelve owned paths. All previously accepted
production helper/Registry/workflow/fixture bytes remain unchanged; only the
existing taxonomy expectation and this Task receipt changed. The final review additionally required a fresh registered candidate preflight.
The continuation below runs that preflight, the failed document-governance leaf
and the seven not-yet-run leaves, retaining only applicable unchanged-input receipts.
There is no timeout increase, gate waiver, substitute executor or mocked PASS.
A final segmented result must explicitly identify its frozen inputs and the
original aggregate exit 1; document-only receipt changes receive their own
metadata/link/lifecycle/staged review rather than repeating unrelated suites.

### W64 registered source acceptance and environment correction

The final frozen input is HEAD `73ebd1ea16d457b1de8ba7b99d02c42c73f48805`
plus twelve owned paths, staged-diff SHA256
`e8026d255bec513cc1acb725dc1af41707bf749cbd4f5e3bff4fdeda909038dc`.
The independent reviewer accepted the taxonomy change but required the registered
candidate preflight over the new twelve-path set. That finding was resolved by
actual execution, not an explain plan. Preflight exited 0 in 131.880 seconds:
metadata selected eight documents with zero violations; the tech-stack checker
retained `OPSFLOW_AIRFLOW_IMAGE` as an unresolved required input, not an image pin.

The controller used `rtk proxy python3 -`, the canonical changed/local-only
plan builders and `execute_execution_plan(root, (invocation,), dict(os.environ))`
with the default real executor. Its first plan call incorrectly supplied leaf IDs
as public roots and exited 1 before any gate executed. It was corrected to build
the canonical changed-profile plan and select its existing registered invocations.
All registered argv, timeout and isolated child-environment definitions were
preserved. No mock executor, gate waiver or timeout extension was used.

| Registered leaf | Bound execution | Actual result |
| --- | --- | --- |
| Candidate preflight | Final twelve-path frozen input | Exit 0; 131.880 seconds |
| Document traceability | Earlier eleven-path input, unchanged source links | Exit 0; 1221 documents, 11756 links, zero failures, one existing archive warning |
| Lifecycle CLI regressions | Earlier eleven-path input, unchanged lifecycle implementation | Exit 0; 15 tests, 124.802 seconds |
| Metadata CLI regressions | Earlier eleven-path input, unchanged metadata implementation | Exit 0; 148 tests, 417.944 seconds |
| Document governance library | Final twelve-path frozen input | Exit 0; 690 tests, 699.064 seconds |
| Gate contract | Final twelve-path frozen input | Exit 0; 28 tests |
| Gate runner | Final twelve-path frozen input | Exit 0; 62 tests |
| Gate adapter | Final twelve-path frozen input | Exit 0; 46 tests |
| Workflow contract | Final twelve-path frozen input | Exit 0; 39 tests |
| Control-plane regressions | Final twelve-path frozen input | Exit 0; 59 tests |
| Precommit regressions | Final twelve-path frozen input | Exit 0; registered shell contract including expected negative probes |
| Repository integrity | Same frozen input, corrected existing QA environment | Exit 0; 503 tests, 129.439 seconds |

The first real continuation still exited 1 at repository integrity: system
Python lacked `referencing`, causing 16 failures and 14 errors across 436 tests.
P09/P02/P06/P07 imports and related fail-closed subprocesses could not use the
registered jsonschema dependency. This is retained as an environment FAIL,
not discarded or relabeled as a production fix.

The existing `/tmp/hy-home-p09-qa/bin/python` was reused without installation.
Its PyYAML 6.0.3, markdown-it-py 3.0.0, html5lib 1.1 and jsonschema 4.26.0
satisfied `scripts/requirements.txt`; referencing 0.37.0 and active transitive
requirements were checked through package metadata and actual imports. The
availability probe `python -m pip check` exited 1 because this existing environment
has no pip. No pip-check PASS is claimed. Dependency metadata/import checks
exited 0 and no global or repository dependency configuration changed.

Only the failed real repository-integrity leaf was retried with
`rtk proxy /tmp/hy-home-p09-qa/bin/python -` and an invocation environment whose
PATH prepended `/tmp/hy-home-p09-qa/bin`. The canonical plan, registered leaf argv,
timeout and executor remained unchanged. All twelve frozen file hashes matched
before and after execution. Independent review accepted this scoped environment
correction with no Critical or Important finding.

This is segmented registered source acceptance, not a monolithic aggregate PASS,
remote CI, native test, deployment or criterion-21 completion. The original
aggregate exit 1 and first continuation exit 1 remain preserved. Previously
accepted production/Registry/workflow/fixture bytes were unchanged; final
result-only Task additions require their own metadata, links, lifecycle, staged
checks and independent review before commit. Local delivery is recorded below
only after its actual commit and fast-forward result.

### W63 selected running metadata — 2026-10-12

The coordinator ran `docker ps --filter label=com.docker.compose.service=<service>`
for `airflow-worker`, `n8n` and `n8n-worker`, then inspected only Config.Image,
Image and Config.User for the one running match per service. Listing and
inspection all exited 0. No exec, environment, raw log or credential read occurred.
Airflow declared `hy-home/airflow:3.3.1-keycloak`, local image ID
`sha256:0388863fe9964d7f2d0d8bacc26dcae0ad5888eadd275c10086a7683bfe46c56`,
configured user `1000:0`. Both n8n services declared `hyhome/n8n:2.41.6-local`,
local image ID
`sha256:1de3d197f8b6bad00af0b6945a2ede5ec321c93ab5344bf09b9919311650d492`,
configured user `node`. This is configured image/user metadata only, not process
UID/GID, supplementary groups, installed-package, authenticated functional or
security-readiness acceptance. No image was deployed. The selected newer local
tag absence above and older running-image observations are separate facts.

### W64 source commit and local-main receipt — 2026-10-12

The coordinator committed the eleven reviewed source/fixture/registration paths
as `545272d3c3cdeb5cddee886b7cc12765f43d13fd`,
`test(opsflow): Add synthetic P10 acceptance seams`. The ordinary commit exited 0
without a verification bypass. Its immediately preceding eleven-path staged
check and whitespace check exited 0; all eleven non-Task hashes still matched
the frozen input. The owning Task changes remained unstaged for a separate
result-only document commit.

Before delivery, `git rev-parse HEAD main origin/main` returned source HEAD
`545272d3c3cdeb5cddee886b7cc12765f43d13fd`, local main
`73ebd1ea16d457b1de8ba7b99d02c42c73f48805` and origin/main
`c26c3b93f4e73034ddad4d08ba9da8eaa9fec0c7`. The target worktree's
branch was main and its porcelain status was empty. Actual `git ls-remote origin
refs/heads/main` independently returned the same c26 remote SHA, exit 0.
`git merge --ff-only 545272d3c3cdeb5cddee886b7cc12765f43d13fd` then exited 0
in the clean local-main integration worktree. Source delivery is LOCAL_MAIN;
remote push, PR and remote CI were not executed in this lane.

After the actual gate results were recorded, metadata selected the three changed
governed documents with zero violations, exit 0; lifecycle reported zero
violations, exit 0. Task-only link checking through the existing graph/mode APIs
checked six links with zero findings, exit 0. The twelve-path staged check and
diff check exited 0, and final independent source/security/specification review
accepted with no Critical or Important finding. These result-only additions
receive another minimal document check and review; unchanged implementation
suites are not repeated.

The first bare `cz check` attempts resolved an unrelated Node command, whose
wrapper returned 0 while reporting an invalid git option. They are not message
validation PASS; no commit occurred and HEAD was reconfirmed unchanged.
The existing QA environment's Python Commitizen 4.15.1 matches the registered pin.
Explicit `python -m commitizen check --message-length-limit 75` then validated
both logical messages, exit 0. No hook, tool pin or global configuration changed.

The shared root remains at `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`
with 24 foreign paths; its tracked diff SHA256 remains
`17c15ccb91ff4f13f7a203a0e8aeb525f89e51e102c701da6a45539e18040f74`.
The old P05 index still has 28 staged paths with cached binary-diff SHA256
`44db414ba98c88746df1dadcd3c4c69f519bf634cbe39b7f406cdcb0f130f33d`.
These observations do not establish byte equality of every untracked file.
No foreign file was staged, reset, stashed, cleaned, committed or removed.

SOURCE, UNIT and STATIC have scoped acceptance; DELIVERY has this actual
local-main source receipt. ISOLATED native, HOME, MIGRATION, ROTATION and complete
opsflow RECOVERY remain NOT_RUN. W65–W69 and criterion 21 stay open. Source-only
rollback is a reviewed revert of the logical commit; no runtime rollback was
performed or required. The worker branch and ignored evidence remain retained
because the owning operational Task is still in-progress and its new commits
are not included in actual remote main.

This is an intentional incomplete operational handoff after source delivery.
A manual Stop exception may apply only to its exact invocation to preserve
foreign root changes; it is not a delivery-check waiver, a persistent hook edit
or a claim that the desktop parent's environment inherits the exception.

### W65 isolated vertical slice

After W64 and the selected exact contracts are reviewed, run one isolated
vertical slice in dependency order: P04 native publication first, then P05
native notifier consumption. The selected Airflow image/DAG import, worker
execution, PostgreSQL schema/function privileges, concurrent replay and object
read/validation must use unique synthetic resources. The n8n import, claim,
SMTP capture, acknowledgement and error path must consume the frozen P04
contract rather than recreate it.

An isolated lane requires its exact image digest/version, Compose projection,
DEV role/schema, object prefix/policy, network boundary, credential delivery
reference, resource budget, cleanup and rollback plan. It does not wait for an
unrelated global SEC/P01/P06 completion claim, but it does stop if its selected
owner contract or resource review is missing. Optional native skips remain
NOT_RUN, never PASS.

### W66 selected HOME acceptance

HOME starts only after a named host, selected services, image digest, operator,
approved rollout boundary, backups, resource budget and reversal path are
recorded in the owning Tasks. Verify running image and in-service version,
authenticated readiness, actual worker/reader/notifier behavior and MNG/DEV
separation. Reject wrong issuer/audience, expired identity, direct-backend
access, cross-project A-to-B access and empty key material.

Do not perform a full-stack startup or broad cleanup. Credential rotation
retains its selected feature owner and exact operational boundary. The final
report consumes relevant ROOT stable-version/security evidence under the resumed
instruction; unrelated global completion is not a
start gate for one admitted isolated consumer. This Task cannot select a HOME
target by inference.

### W67 failure, backup and empty-target restore

Inject faults only into an isolated or named approved scope: object timeout or
wrong credential, validation failure, object-stored/database-unavailable,
replay/backfill, deadlock retry, lost acknowledgement, expired lease and
notifier dead/requeue. Verify actual backup-set completeness for opsflow
database/roles/extension metadata, retained objects, outbox, n8n metadata and
encryption key, OpenBao snapshot and independently held custody material.

Have the owning recovery executor restore one exact snapshot identifier into a
named empty target under its reviewed runtime lease; P10 observes and verifies
the resulting acceptance. P10 may execute a restore only after an exact lease
is transferred. It owns synthetic acceptance fault/reconciliation tests and
collects feature receipts without creating a second restore executor. Reconcile the
reader view/latest pointer, idempotency, outbox lease and capture acceptance
before declaring recovery. P01 and P06 operational migration, authentication,
rotation and recovery lanes remain gated by their owners; this Task does not
invent snapshot custody, a backup set or an image digest.

The complete P10 backup-set, snapshot selection and new empty-target inputs are
currently UNKNOWN. The narrower two-file SMTP snapshot/restore receipt above
is an existing input; it cannot establish the full opsflow recovery set.
Investigate them through the named owner records and read-only inventory before
asking for a new operational action; their absence leaves this runtime lane
NOT_RUN and does not stop W63/W64 source preparation.

### W68 P08 path handoff and dry run

After P08 final path delivery, bind each affected operation document to its
exact old/new path, source and target hash, artifact ID, anchors, README coverage
and generated-owner evidence. Run only the reviewed relative working-directory
dry run or selected command environment. Distinguish a typed LAB document move
from LAB runtime work. If P08 has no final hash handoff, retain this lane as
NOT_RUN.

### W69 final owner report and delivery

At the actual final head, report every owner criterion and the separate SOURCE,
UNIT, STATIC, ISOLATED, HOME, MIGRATION, ROTATION, RECOVERY and DELIVERY result.
Run affected syntax/schema/Registry/link/secret-leak checks, selected unit and
native acceptance, staged gates and independent review. Record exact commands,
input SHA, exit status, failures/corrections, rollback proof and local-main
receipt. Tests do not establish deployment, deletion, migration or recovery
without their actual evidence.

### W69 completed-source worktree cleanup — 2026-10-12

The user's current instruction prioritizes integration and removal of completed
worktrees and development branches. At main
`fc3a03e5f2a22750118b929d1f099bf5a32bed33`, twelve clean source branches
already had every commit in main; no content merge was needed. Normal
`git worktree remove` and `git branch -d` removed their twelve worktrees and
local branches: P01 recovery, P02 catalog, both P03 branches, P04 pipeline,
three accepted P05 branches, P07 optimization, P08 layout, P10 preparation and
workflow source integration. The clean, merged, detached P01 catalog-document
QA worktree was also removed. Total: thirteen worktrees and twelve local
branches. Their disposable scripts, test invocations, logs and caches were
removed with the worktrees; permanent regressions remain tracked in main.

Before removal, the coordinator rechecked exact HEAD/branch, empty index and
worktree status, and ancestry. Sixty-nine selected public handoff records were
copied byte-for-byte into the ignored private directory
`.agent-work/accepted-worktree-handoffs/20261012/`. Four unknown-content P02
preview documents were preserved separately as opaque private copies, without
interpretation or published hashes. They were not imported into Git. The
preservation index SHA-256 is
`41ab4fea415625fcf08537cedf8b14e775b1c7371344de2b52fbd3038d72a4e3`.
The two cleanup result receipts in that directory retain exact removed paths,
branch names and input SHAs. No forced worktree removal, reset, stash, clean,
force push, service change, credential change or data deletion was used.

Fresh remote verification confirmed P01 recovery's exact head was an ancestor
of remote main before deleting only that remote development ref. An initial
P01 trust ancestry check failed, but the coordinator incorrectly continued its
local and remote ref deletion. The original ref
`bb63f27ed62ccf860aa8af2b8e5603dce481b12e` was restored locally and remotely,
including its tracking relationship; remote equality was rechecked. No commit
was lost. P01 trust remains excluded until its squash/reconciliation history is
independently verified. Subsequent cleanup executes deletion only after every
prerequisite succeeds in the same guarded sequence.

The shared root's twenty-four foreign paths, old P05's twenty-eight staged
paths, dirty SEC01/SMTP01 worktrees, dirty nested QA, and active operator or
source-review workspaces remain preserved. Clean source delivery does not close
operational Tasks. W65–W68, full SEC01/HOME, actual SMTP provider delivery,
OpenBao authentication/recovery and the remaining owning runtime criteria stay
open. This cleanup is not native E2E, migration, rotation or recovery evidence.

### Current user-accepted SMTP/CLN boundary — 2026-10-12

At clean root main `2773a20c1c24ce1b70f64b36fe8f6f5108f49542`, the user confirmed
acceptance of the delivered SMTP01/CLN01 changes and excluded actual LAB GoTrue
SMTP connection configuration from their Spec/Plan/Task scope. Missing LAB
connection/activation/send readiness is not a remaining acceptance condition.
P10 must not start GoTrue or repair LAB SMTP to obtain its Opsflow receipt.
P04/P05 native publication/notifier acceptance keeps its independent scope.

A genuine future sender/recipient test uses the mailbox designated in the
current user instruction. The personal address is not published in Git,
fixtures, workflow exports or this ledger. This selection does not dispatch a
message and user acceptance does not create a native/provider/restore result.
The prior source/isolated receipts remain attributed to their actual inputs.
No runtime, secret, account, message or data changed in this clarification.

### Current completion reconciliation and draft cleanup — 2026-10-12

At main `69b070b759e9ca235d5aa9ee31c2ab311df4dffc`, user-accepted SMTP01/CLN01
scope and completed P09 preparation remain accepted. P01 HOME/recovery, P02
private issuance/delivery, P03 native identity/TLS/consumer use, P04 DEV/S3
publication, P05 native notifier, P06 actual pilot/recovery, P07 representative
workload/rollout, P08 W59–W62 moves and P10 W65–W68 remain open under their
owning Tasks. They are not complete merely because source was merged.

The latest user resume instruction restores stable-version updates and their
associated official-documentation/compatibility investigation; it supersedes
the intervening warning-only modernization restriction. UNKNOWN stays unknown,
and no-newer stable lookup requires no version bump. P10 consumes its selected
artifact's version/security evidence and exact native/recovery contract;
unrelated global SEC completion is not an isolated-lane start prerequisite.
The current ROOT source census excludes relocated LAB Supabase/GoTrue.

The original checkout was confirmed clean on main before this increment, rather than detached a03.
Its prior twenty-four paths were privately archived and reconciled against
accepted main: one exact state, twenty-two corrected/superseded public drafts,
and one disposable coverage artifact. Obsolete generic retirement prototypes
and colliding Task drafts were rejected, not falsely described as byte-merges.
Four changed public bind-source files match main; Kafka YAML semantics were
unchanged, Grafana's version metadata changed, and Tempo preserves vParquet4.
No reload/restart/recreate or private env/password change was performed;
host-source equality does not prove running-container application.

The already merged SMTP proof branch/worktree was removed normally after
preserving its public handoff; forty-nine one-off coverage/cache paths were
removed, while permanent regressions and source commit 5fd5397 remain in main.
Two independent read-only audits then found no missing meaningful source in
twelve older dirty/staged QA/integration worktrees. Their 131 public draft paths
were verified against private ZIP rollback copies and scoped reconciliation;
normal `git worktree remove` removed those twelve plus the clean P06 parent.
Normal `git branch -d` removed P05 notifier, P06 migration and P08 path-contract
branches. No force/reset/stash/clean, private data or runtime deletion occurred.
The non-ancestor c940c2ac P06 admission document was superseded in intent, not
claimed merged as a commit; its history was retained in a verified private Git
bundle. A first bare-SHA bundle command exited 128 before source cleanup; the
QA HEAD-ref bundle succeeded and was verified before removal.

The canonical ignored receipts are `.agent-work/root-main-transition-20261012/`,
`.agent-work/completed-worktree-handoffs-20261012/` and
`.agent-work/reconciled-draft-cleanup-20261012/`. Raw drafts, opaque previews,
logs and rollback artifacts are not Git or execution authorities. Pending
source/runtime acceptance stays in the owning Tasks; removed development
worktrees are not required to keep those criteria open.

### Dependency Matrix

| Owner | Required handoff before dependent runtime | P10 preparation boundary |
| --- | --- | --- |
| SEC01 / TSK-0009 | Selected image tag/digest/USER/Entrypoint/Cmd, package and security receipt | Whole-image completion stays open; one accepted artifact may admit its bounded lane. |
| SMTP01 / TSK-0005 | Canonical COMM-002 and selected capture/cutover/retirement receipt | COMM-003 execution remains with SMTP01; no private value comparison in preparation. |
| CLN01 / TSK-0007 | Fresh five-axis consumer proof and recovery-aware disposition | No duplicate deletion executor or release of PG-020/COMM-003 holds. |
| P04 / TSK-0012 | Reviewed publication/outbox schema, exact Airflow image and DEV/S3 resource contract | May model the interface; P04 owns publication acceptance; its proof precedes the notifier lane. |
| P05 / TSK-0013 | Frozen P04 version/hash, exact n8n image/node and SMTP capture contract | May model claim/ack faults; native notifier follows P04 publication. |
| P01 / TSK-0006 | Named issuer/recovery target and custody/restore evidence | No issuer or snapshot operation is performed here. |
| P02 / TSK-0010 | Reviewed catalog IDs, classifications and secret-reference contract | No catalog row, identity or destination is invented. |
| P03 / TSK-0011 | Selected endpoint, UID/mode, TLS and network facts | No public endpoint or network is changed. |
| P06 / TSK-0014 | Accepted consumer wave and recovery/rotation evidence | Pre-migration DEV preparation can proceed; copier and deletion remain owner-gated. |
| P07 / SPEC-0218 | Selected capacity/least-privilege baseline where relevant | No resource or permission change is accepted by a fixture. |
| P08 / TSK-0015 | Final path/hash and README coverage handoff | W68 waits; no document move is inferred. |

### Cleanup correction: unfinished scanner execution source

The later SEC01 reuse audit found that two ignored v2 scanner execution sources
in the removed SEC01 worktree were not included in the retained draft archive.
The claim of reconciled tracked drafts does not establish preservation of all
unfinished operational tooling. This is an actual cleanup error, not a completed
scanner task. The preserved preparation receipt and 8/8/2 manifests remain input
evidence; native execution is blocked pending exact-source recovery or fresh
review. TSK-0009 records the missing hashes and current memory observation.
No scan PASS, deployment or complete SEC01 acceptance is inferred.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Task admission | 21 | W63 | Verify Task identity, current refs, ownership and preservation boundary | Local 43917df; remote/origin c26c3b93 | PASS | Inputs and Authorization | accepted |
| Source receipt inventory | 21 | W63 | Reread public owner inputs and hash P04/P05 contracts | 73ebd1ea; source hashes above | PASS | W63 frozen public input audit | accepted |
| Selected local image tags | 21 | W63 | Read-only image metadata inspection | Three public tags; each child exit 1 / IMAGE_ABSENT | FAIL | W63 frozen public input audit | pending |
| Synthetic acceptance preparation | 21 | W64 | New caller seam, CI registration and segmented real registered gates | 73ebd1ea plus twelve owned paths; frozen hash above | PASS | W64 registered source acceptance and environment correction | accepted |
| Isolated vertical slice | 21 | W65 | P04 publication then P05 notifier against reviewed exact contracts | Named isolated resources and owner handoffs | NOT_RUN | W65 isolated vertical slice | pending |
| Selected HOME acceptance | 21 | W66 | Selected host rollout and authenticated service evidence | Named host, resources, backups and rollback | NOT_RUN | W66 selected HOME acceptance | pending |
| Fault, backup and restore | 21 | W67 | Fault receipt, complete set and exact empty-target restore | Named fault scope and snapshot custody | NOT_RUN | W67 failure, backup and empty-target restore | pending |
| P08 path handoff | 21 | W68 | Hash-bound path/README handoff and command-directory dry run | P08 final receipt | NOT_RUN | W68 P08 path handoff and dry run | pending |
| Final owner report | 21 | W69 | Exact-head checks, review and local-main delivery evidence | Final candidate and owner receipts | NOT_RUN | W69 final owner report and delivery | pending |

## Review and Completion

This in-progress Task records admission and the source-input audit. Synthetic
tests now have source-layer receipts; final combined-head delivery is separate. It has no P10 native
runtime, data, secret, migration, deletion, rotation, restore or HOME result. An independent reviewer must inspect
each exact source or operational change without editing it. The Task remains
incomplete until W63–W69 have their actual evidence, while missing runtime facts
leave only their dependent lane NOT_RUN.

Use small logical commits by owning acceptance surface. Preserve existing worker
commits and use one writer for every shared file. Roll back source/test work by
reverting the reviewed logical commit; roll back a runtime lane only through its
pre-recorded target-specific recovery plan. Do not treat this Task issuance or a
synthetic test as a production readiness or restoration receipt.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [P04 Task](tsk-0012-p04-airflow-manifest-pipeline.md)
- [P05 Task](tsk-0013-p05-n8n-outbox-notifier.md)
- [P06 Task](tsk-0014-p06-openbao-consumer-migration.md)
- [P08 Task](tsk-0015-p08-operations-document-layout.md)
