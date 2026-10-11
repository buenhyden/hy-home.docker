---
title: "P03 Service Integration and Four-location Port Contracts Task"
version: "0.2.1"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-11"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0011"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P03 Service Integration and Four-location Port Contracts Task

## Objective

Own criterion 17/W33: reconcile current service integration, environment,
identity and four-location port contracts without duplicating the current
inventory or reopening completed Tasks. Begin with independent source and
synthetic proof; defer only consumer-specific final mappings and runtime lanes
whose exact prerequisites remain unavailable.

## Inputs and Authorization

The user's complete P03 execution prompt and current request authorize this
prerequisite assessment, ownership assignment and independent worker handoff.
Its historical input is `860ac1c3633eac9ad416fb1abd8a61a6e617ebd8` (PR410).
Actual clean local main at assessment is
`6da5e3bf380d5002e0e28181136fde8c016e49ce`; `git ls-remote` returned remote
main `2b9f5ec82cb73ea148fb27bfbd2d35c10e328e51`, and `gh pr list` returned
no open PRs. The three local-only commits are documentation preparation;
they are not remote delivery receipts. This issuance makes no remote write.

The current full P03 prompt selects an owning-Spec PR after implementation,
latest-head CI and independent review. SEC01/SMTP01/CLN01 retain their earlier
local-main/no-PR integration instruction. Dev is not used. Preserve logical
commits and reconcile the local preparation prefix with a fresh remote base
before a P03 PR; do not implicitly push main or include unrelated runtime work.
User authorization is not requested repeatedly for already-authorized source
and review. Exact operational targets, effects and recovery still precede
private/runtime actions.

Read bootstrap/provider and current SPEC-0204/0212 before writing. Reuse
TSK-0002's completed generic registration schema, TSK-0005's integrated SMTP
contracts, TSK-0006/0007/0009/0010 and existing service owners. Preserve
PR409/410 OpenBao TLS, wrapped reauthentication, readiness, audit and snapshot
source. Preserve delivered DEV/MNG, Influx retirement, RedisInsight/exporter,
k6/OTLP, common-controls and Stage05 source. Completed Tasks are historical,
not empty implementation slots. TSK-0005 remains SMTP/history ownership.

### Worker Branch and Exact Ownership

Use one P03 writer on `codex/p03-service-integration-contracts` in
`/home/hyunyoun/data/hy-home.docker/.worktrees/p03-service-integration-contracts`,
from the commit issuing this Task after local-main integration. Before writing,
record actual branch, HEAD, clean status and file digests. This issuance starts
no second worker chat. Do not alter another writer's uncommitted files.

After a reuse check, the initial exclusive file set is:

- This Task, including execution evidence and logical commit ledger.
- `scripts/lib/ops/port_inventory.py` and
  `scripts/operations/port-inventory.py`: one importable projector and narrow CLI.
- `infra/09-platform-ops/service-integration/port-contract.schema.json` and
  `infra/09-platform-ops/service-integration/README.md`: closed value-free
  contract and Korean navigation. Do not create a second service registry.
- `tests/lib/ops/test_port_inventory.py` and
  `tests/validation/test_port_contract.py`.
- Synthetic files under `tests/fixtures/port-contract/`, with a Korean README
  for that folder and any new child folder. Existing parent README changes
  remain integration proposals.

The canonical service inventory remains m0021's bounded
`current-service-inventory` table with the existing
`operations_catalog.render_service_inventory`/`validate_service_inventory`.
Derive current root membership from its dynamic include closure; the existing
latest-gate root parser is a reuse input, not a second hardcoded inventory.
The source inventory and a selected rendered configuration have different
semantics. No fixed service count, manually copied rows or new top-level
PORT_CONTRACT file is permitted. Operational meaning goes into existing
Traefik subject0013, onboarding0008 and the corresponding service owners,
through coordinator-reviewed proposals.

Root/leaf Compose, public/real environment, common optimizations, gateway,
Keycloak clients, Alloy, backup, secret catalog/support metadata, m0021 and its
renderer, Registry, Spec/Plan, `scripts/manifest.yaml`, workflow contract,
shared validators and README indexes are read-only to this worker. Submit exact
base blob IDs, changed hunks, consumer/test map and rollback in ignored
`.agent-work/integration-proposal/README.md`. The coordinator is the single
final writer. A necessary service-specific fix requires an exact named file
lease and reconciliation before source edits; an all-infra ownership claim is
not a lease. Review both writers' changes rather than overwriting a file.

P01 alone owns OpenBao helpers/configuration, subject0085 and its README; P02
owns catalog/schema/tools/tests and proposes documentation to P01. SEC01 owns
image/version/security acceptance and its projections. SMTP01 owns canonical
SMTP, its generator/adapter and sole proposed COMM-003 executor. CLN01 owns
five-axis consumer/deletion eligibility. P03 does not take these writers' files.

### Parallel Scope and Waiting Conditions

Proceed now with public declaration/consumer-edge auditing, the new closed
port contract, synthetic fixtures, parser/projection tests and common-file
proposals. Record each item as NO_CHANGE, IMPLEMENT, VERIFY_RUNTIME, DELETE,
BLOCKED_FACTS or OUT_OF_SCOPE. DELETE is a proposed disposition until its
owning consumer and recovery facts are established. Keep declared/running/
healthy/used/recovered observations distinct, with SHA and freshness.

The four locations are listener IP/port, internal DNS/port, published host
IP/port and Traefik backend network/port. Keep IPv6, UDP, ranges, aliases and
multiple backends lossless; distinguish absent, unknown and intentionally
unpublished. `ports` and `expose` do not prove actual listening. A host-port
change must preserve internal consumers; a listener change needs coordinated
health/exporter/provisioning/gateway/consumer evidence. The attached reference
parser covers only partial declarations; its short syntax is unparsed and it
has no complete listener, alias, range, authentication or recovery proof.
Compare and adapt it rather than copying `reference/tools` into production.

Render only explicitly named root-plus-override inputs using synthetic public
environment in the initial slice. Prevent ambient dotenv/private inheritance;
extract a closed metadata allowlist before output. Never persist or print raw
render, environment values, arbitrary labels/commands, authentication, logs or
secret payloads. Test synthetic leakage markers. Future real-host observation
requires its exact input hashes, output filter and independent review here.

Final secret/ACL/reload mappings await P02's frozen catalog and P01's final
OpenBao auth/recovery contract. COMM-002 stays canonical and COMM-003 stays a
value-free alias; no independent SMTP value is created. Image-dependent source
verdicts follow SEC01's exact contract; HOME activation requires that artifact's
security acceptance. CLN01 decides legacy SERVICE_POSTGRES_* eligibility after
source/runtime/job/backup/external consumers, never profile inactivity alone.
P03 supplies connection contracts to P04/P05; it cannot claim their future
native Airflow/n8n workers exist. P06 actual migration awaits P01/P02/P03 and
consumer proof. Missing one runtime target does not stop unrelated source work.

No learning-app investigation/planning, LAB runtime change, actual Wiki app/
DB/collection/credential/model/workspace, production client, Wiki schedule or
blog-data write occurs. P09 stays preparation-only and P08 owns later Stage05
moves, including LAB document paths. No full up/down, prune, broad chown,
credential rotation, live resource creation or private retirement occurs in
this initial worker slice.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0011 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0011 | ready | in-progress | #p03-initial-implementation-slice |

### P03 Initial Implementation Slice

Implementation began on 2026-10-11 in the assigned clean worktree at
`74feff9429d302233d2475b31beed3dbf2ac07c9`. Branch is
`codex/p03-service-integration-contracts`. Fresh remote main readback is
`6da5e3bf380d5002e0e28181136fde8c016e49ce`, newer than the issuance
assessment; no remote write or shared-file reconciliation was performed.

The existing W33 Plan remains coordinator-owned. Its initial slice maps
criterion 17 to the owned port schema, pure declaration projector, public-source
closure CLI, synthetic fixtures and dedicated unit/contract tests. Reuse
`latest_version_gate.expected_from_root` and the existing bounded operations
catalog reader; do not duplicate root traversal or inventory rows. Order:
record RED; implement lossless four-location projection; add explicit synthetic
root-plus-override config isolation; check leakage and DEV/MNG metamorphic
cases; independently review; commit logically; propose common registration.
Service-specific native/identity/recovery increments remain pending their named
consumer and coordinator file leases.

Available tools: Python/unittest, existing PyYAML/jsonschema and Docker Compose
for configuration only; coverage/style tool paths are checked before use.
Sandbox command bootstrap currently fails with bwrap loopback permission error;
authorized scoped commands use the escalation route, with no private reads.
Numeric token/time/concurrency budgets are UNKNOWN. Synthetic subprocess
timeout will be bounded; deployment/rotation/deletion remains NOT_RUN. Rollback
is a logical revert of this owned source slice only.

### Assessment and Next Executable Units

At input `6da5e3bf3`, P01 worktree was clean at the same SHA. P02 had seven
uncommitted paths: its Task, catalog/schema, CLI/library and dedicated tests;
its subject0085/OpenBao README edits were absent from the current diff, and its
Task records proposal-only ownership. SEC and SMTP retained separate foreign
worktree changes. These are local observations, not GitHub commits. Preserve
all those files; do not reset, stash, clean or stage them.

Read-only HOME inspection found OpenBao server/Agent running and healthy on
image ID `sha256:11fd73a2102cda9c55d5d881a8c3210303146a7ec1e8ac76f526e175c6d24641`
(the existing 2.6.2 image), while source selects 2.7.1. Health is not proof of
current image rollout/auth/recovery. SEC01's full latest/security gate and HOME
remain unfinished. SMTP's bounded two-file encrypted-backup restore is existing
evidence, not whole-service delivery/recovery or CLN deletion acceptance.

1. Inventory/reuse: trace root includes and current owners; audit public
   declarations and existing connection schemas without changing them.
2. RED/GREEN: port schema/library/CLI and synthetic fixtures. Cover short/long,
   IPv6/UDP/ranges, aliases/multiple backends, absent/unknown listeners,
   fail-closed malformed inputs and no arbitrary-value output. Test DEV/MNG
   one-side mutations for independent rendering; cover host-only changes.
3. Service contract proposals: inspect each declared root service's effective
   configuration, env keys, secret references, mounts/UID/mode, health,
   consumers/jobs and recovery edges. Cover gateway/browser/machine identity;
   MNG/DEV role and object/search ACL separation; existing Kafka/CDC/dbt/Avro;
   Airflow/n8n workers; telemetry temporality/identity/cardinality; existing AI/
   crawler constraints; platform socket access; SMTP outcomes; quality,
   analytics and Storybook/docs-MCP. Reuse each owner rather than reimplementing.
4. Confirmed defect lease: only after coordinator review, add exact service
   files and RED/GREEN cases here. Structured DSNs or correct encoding must
   handle synthetic @/:#?%, spaces, quotes and Unicode. Include empty/nested/
   symlink/autocreate/UID readability and bounded retry/failure cases.
5. Native/runtime increment: after exact target/consumer/image/resource/
   recovery and operational-writer assignment, prove positive native SDK,
   scanner or executor auth plus expired/wrong issuer/audience/project and
   direct-backend denial. Generic 401, PID/socket declarations or synthetic
   passes cannot close MLflow SDK, Sonar scanner or Terrakube executor gaps.
   Preserve Pact native auth; do not create arbitrary Keycloak clients.
6. Delivery: freeze own commits/proposals, coordinator integrates shared hunks
   once, rerun affected registered gates and independent code/security/docs
    review at final head, then the P03 owning-Spec PR with current-head CI.

### Initial Source Verification and Integration Boundary

Two initial RED commands exited 1 for the missing new library and missing
`render_synthetic` interface. The first whole source/fixture suite had 25 tests
and exited 1 on public Traefik interpolated aliases. Two targeted alias/network
regressions then exited 1 before correction. GREEN preserves unresolved alias
positions while omitting expressions, and separates logical network keys from
unknown project-prefixed names. A fresh 27-test command exited 0 (3.095s).

`coverage --source=scripts/lib/ops/port_inventory.py` was an incorrect module
selector: tests passed but the coverage report exited 1 with no data. Corrected
`--source=scripts.lib.ops.port_inventory` executed 27 tests, exit 0, and reported
273 statements, 4 missed, 99-percent coverage, exit 0. This is source/synthetic
proof, not daemon/native auth/HOME evidence. Subsequent bounded-reader negative
cases and review fixes require a new final input receipt.

The synthetic renderer executes only selected bytes via Docker Compose config.
The root and DEV override were rendered with a fresh closed child environment,
explicit public env file and invocation-owned temporary paths. The MNG
projection remains equal under a DEV-only publication addition; neither images
nor resources are started. Source root membership matches the reused dynamic
closure; declarations do not imply listeners or runtime health.

Common integration is NOT_APPLIED. The ignored proposal directory is
`.agent-work/integration-proposal/`, with `base-blobs.json`,
`common-registration.patch` and `README.md`. Base is
`74feff9429d302233d2475b31beed3dbf2ac07c9`; initial patch SHA256 is
`b0697a2b45786c39dc5f4ef9dbe2944d546fd670aa78ff212ae1660b288b1d97`.
`git apply --check` exited 0 without target changes. Targets are current script
manifest, workflow contract, Platform Operations navigation and the newly needed
fixture family README (absent at base). The coordinator must also regenerate
scripts navigation through its existing owner and validate current Registry
routing. No shared Compose/env/gateway/Keycloak/Alloy/backup/catalog/inventory/
Registry file was edited. P03 owns the two dedicated test modules; registration
belongs to their existing LOCAL repository-integrity gate, never a new CI stack.

| Item | Disposition | Evidence boundary and next owner |
| --- | --- | --- |
| Existing inventory and root closure | NO_CHANGE | Reused source authority; no second registry |
| Four-location parser/schema/CLI | IMPLEMENT | Owned new source and synthetic fixtures |
| Listener/runtime/machine authentication | VERIFY_RUNTIME | Unknown/NOT_RUN; exact selected target and owning consumer required |
| Final secret/ACL/reload mapping | BLOCKED_FACTS | P01/P02 frozen contract and catalog required |
| Image security/HOME activation | BLOCKED_FACTS | SEC01 exact artifact acceptance required |
| Legacy SERVICE_POSTGRES_* retirement | BLOCKED_FACTS | CLN01 consumer/recovery eligibility; P03 deletes nothing |
| Wiki implementation/learning apps/LAB runtime | OUT_OF_SCOPE | No resources, data or service changes |

Independent code/security review of the exact owned source has been requested.
The canonical changed local plan was inspected with `--explain`; final aggregate
and PR remain NOT_RUN until common registration/prefix reconciliation. Focused
standalone unit results cannot stand in for the registered final gate.

### Worker Input and Current Results

The complete P03 prompt supplied on 2026-10-11 was read and reconciled with this
Task's exclusive paths. The reference parser's unparsed short strings and raw
label map were replaced by the existing owned implementation; no duplicate
`reference/tools` tree or service inventory was created. This initial unit does
not close the whole service/environment/identity criterion.

Implementation input HEAD remains `74feff9429d302233d2475b31beed3dbf2ac07c9`.
Fresh fetched origin/main is `4e26a5a8022a7307c7461af60337442912955df1`.
That suffix contains the P04 Spec/Plan/Task preparation only, with no change to
this unit's runtime/source inputs or proposed common base blobs. The previously
local issuance prefix is now remote; common registration is still NOT_APPLIED.

The initial unit's twelve source/schema/test/fixture/README files at commit
`93ad5da2538f99cc978745a458587e2fde71550c` have recorded aggregate SHA256
`3b00068da8690d57113113f6a8db6c95b5e239541fb52e40cb44e8ceb338b241`.
The exact per-file manifest is preserved in ignored `.agent-work/p03-port-input.json`.
The reused root closure input manifest SHA256 is
`c2515b005e14a6242e88bf684da9db97f1355798f11dff31a90bb9e8acb0c614`.
The Task itself is excluded from this aggregate to avoid a self-referential hash.

Independent review found and RED cases reproduced concatenated interpolation,
missing-versus-unresolved binding/network loss, path traversal admission,
duplicate service/source evidence, contradictory state/range/allocation,
malformed optional descriptions/aliases, missing h2c support, endpoint product
amplification, unbounded pipe capture, pre-read override amplification and
quadratic object-array uniqueness. Corrections are confined to the owned unit.
All diagnostics remain fixed and raw values/configuration are not returned.

The first worker metadata check failed because draft-to-in-progress lacked a
registered event chain. The Lifecycle Events table now records draft-to-ready
from the user's authorization and ready-to-in-progress from actual execution;
the subsequent check selected two governed documents and reported zero violations.
The first local-staged controller returned 2 because its Markdown hook removed
one extra blank line in this Task. The controller restored its input; after a
second identical failure, that exact whitespace correction was explicitly
applied and restaged rather than relying on hook mutation.
The final evidence expansion initially put prose and the grouped audit table
inside the registered Evidence section before its canonical table. Metadata
returned 1 with the contiguous-evidence defect and cascading package/archive
inference diagnostics. Those worker paragraphs were moved into Work Log; no
archive or common contract was changed to suppress the failure.
The first link command omitted its required mode and returned 2. The first
`--mode all` run returned 1 for three forbidden cross-stage links from owned
READMEs; those links now use the registered docs entrypoint. Fresh all-links
returned 0 with zero failures and one existing archive-capture warning.

Executed commands for the current unit are:

```sh
/tmp/hy-home-p09-qa/bin/coverage run \
  --data-file=/tmp/p03-final-port.coverage \
  --source=scripts.lib.ops.port_inventory -m unittest \
  tests.lib.ops.test_port_inventory tests.validation.test_port_contract -q
/tmp/hy-home-p09-qa/bin/coverage report \
  --data-file=/tmp/p03-final-port.coverage --include='*/port_inventory.py' --fail-under=80
python3 scripts/validation/check-document-links.py --mode all
python3 scripts/validation/check-script-manifest.py
```

The final artifact aggregate above executed 42 tests, 8.385s, exit 0, with
384 statements, 10 missed, 97-percent helper coverage, report exit 0. Docker
Compose config used synthetic bytes only; no daemon workload/native auth test
was performed. The reviewer-created local coverage artifact was preserved at
an invocation-owned `/tmp` path rather than committed or deleted.
Independent final security review returned ACCEPT with no open finding; its
fresh 42-test run exited 0 (3.545s) against the same frozen source hashes. This
verdict excludes evolving Task prose and all native/HOME acceptance.
Independent final code/proposal review returned APPROVE for specification and
quality on the same twelve-file aggregate, with no open Critical/Important
finding. Its latest attempted rerun was NOT_RUN due to sandbox bootstrap;
the unchanged artifact was matched to its earlier independent PASS. Common
patch applicability is approved; integration and runtime delivery are not.
The local-staged controller subsequently completed with exit 0 after the
explicit whitespace fix; its style, syntax and hardcoded-secret leaves passed.
That controller is not the unregistered final changed gate or remote CI.

The existing five-module baseline command below was rerun at this worker input:
84 tests, 8.110s, exit 0. This is fresh source regression evidence, not a fresh
native/HOME/recovery receipt. Manifest check exited 1 for exactly the two new
script records absent from coordinator-owned registration. The canonical final
changed gate remains NOT_RUN pending that integration; no bypass is introduced.

### Public Consumer Audit and Next Integration

This is a grouped audit of existing owners, not a replacement service inventory.
Read-only source inspection covered the following contracts. Existing historical
guide/native outcomes are not reused as new P03 PASS.

| Contract group | Current source and owner evidence | Disposition and remaining boundary |
| --- | --- | --- |
| Gateway/browser identity | Traefik/keycloak/oauth2-proxy source; guides 0013/0014/0015/0079 | NO_CHANGE for existing controls; direct-backend and current issuer/audience proof VERIFY_RUNTIME |
| DEV/MNG | dev-db/mng-db leaf and baseline provisioning tests; guide 0028 | NO_CHANGE for separation; named consumer/readiness/port consumption VERIFY_RUNTIME |
| Kafka/CDC | Kafka leaf, guide 0036 and baseline feature provisioning tests | BLOCKED_FACTS for named CDC/Avro/offset/worker acceptance; P04/P05/P06 own targets |
| Observability | Existing observability/Prometheus source, guide 0079 and runtime compatibility tests | NO_CHANGE for source paths; current freshness/telemetry/identity VERIFY_RUNTIME |
| Workflow | Airflow/n8n source and owning follow-up Tasks | BLOCKED_FACTS for actual workers and DEV/object/mail auth; P04/P05 own native execution |
| MLflow | MLflow leaf; guide/policy 0088 | IMPLEMENT proposed: direct SDK path lacks MLflow user/experiment authorization; actual SDK auth NOT_RUN |
| Ollama/WebUI | Existing AI leaves and guide 0079 | NO_CHANGE for owned source; current user/GPU/cancellation VERIFY_RUNTIME, no model pull |
| Terrakube | Terrakube leaf and guides 0069/0079 | IMPLEMENT proposed: cookie ForwardAuth blocks CLI/API-token/executor; native audience/RBAC NOT_RUN |
| Mail | Stalwart/Mailpit leaves and SMTP Task 0005 | NO_CHANGE for source owners; SMTP01 retains accepted/failed/unknown delivery acceptance |
| SonarQube | SonarQube leaf; guide/policy 0066 | IMPLEMENT proposed: scanner token cannot pass browser ForwardAuth; native scanner/auth NOT_RUN |
| Analytics | Existing optional role declarations and guide 0094 | BLOCKED_FACTS for named read-only query, writer and checkpoint/recovery consumer |
| Experience | Storybook leaf and existing docs-MCP owners | NO_CHANGE for source ownership; current client auth/build/tool call VERIFY_RUNTIME |

Named file leases are needed for the MLflow, SonarQube and Terrakube leaves,
their corresponding service auth/configuration and dedicated native-test files,
plus any shared gateway/identity changes. They are proposals only; the coordinator
still owns common Compose/env/gateway/Keycloak/Alloy/backup/catalog/Registry.
No generic 401, native-auth assumption or arbitrary new client substitutes for
actual consumer proof. P01/P02 catalog/auth mapping and SEC01 image acceptance
remain required before private/HOME action. Exact native command/credential
transport for those new auth increments is UNKNOWN until the named target and
implementation lease are reconciled; it is not represented as an executable
that already exists.

Next coordinator source commands are `git apply --check` on the preserved
common-registration patch, source integration against its exact base blobs,
`python3 scripts/validation/check-script-manifest.py`, the registered changed
local gate and independent final-head review. The owned source CLI and synthetic
command are documented in the new service-integration README. Rollback for this
initial unit is a logical revert of its owned commit; it does not restore any
deployed state. No HOME/data/secret deletion/rotation/restore was performed.

### Supported Interpolation Clarification

The coordinator's 2026-10-11 handoff verification confirmed the initial unit's
artifact/public-root input hashes and public CLI/diff checks. It did not rerun
the worker's 42 dedicated tests, 84 regressions or 97-percent coverage; those
remain the dated worker receipts above. This documentation correction starts
from clean worker HEAD `93ad5da2538f99cc978745a458587e2fde71550c`;
observed local main is `f7543e0697e2473cbbbeb254792e7a1d5b4b8423`, remote
main is `4e26a5a8022a7307c7461af60337442912955df1`.

Unknown interpolation preservation applies to supported IP/port/network-name/
alias address fields. Unresolved `protocol`, publication `mode` and Traefik
backend `scheme` are rejected, not retained as unknown. The current root lacks
those interpolated enum declarations; the initial source acceptance therefore
does not assert generic lossless handling of all Compose expressions. README
wording is narrowed to this existing behavior. No helper, schema, test, fixture,
image or runtime behavior is changed and no previous PASS is relabeled as a
fresh test result. The initial twelve-file aggregate above remains historical;
new document hashes must accompany this correction to the coordinator.
Three freshly executed offline probes against the unchanged helper rejected
synthetic unresolved protocol/mode/backend-scheme inputs with fixed errors,
exit 0. These probes confirm the documentation limit; they are not a rerun of
the broad frozen suites or any native/HOME test. Document metadata/link/style
checks and independent correspondence review are scoped to this increment.

The coordinator reproduced P02/P03 registration conflicts in both patch orders
on `scripts/manifest.yaml` and `.github/workflow-contract.yml`. It owns P03
registration first and P02's subsequent rebase, preserving both entries and
routing. This worker does not apply either patch. Final integrated-head gates,
review, P03 PR/CI/merge and actual native authentication/HOME/migration/rotation/
recovery remain pending. Criterion 17 is open. Rollback for this increment is
only the reviewed documentation commit revert; no operational rollback occurs.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Git baseline | 1, 17 | W33 | status/log/worktrees, ls-remote and open PR list | Local 6da5e3bf3; remote 2b9f5ec82 | PASS | Assessment above; exit 0, baseline only | pending |
| Existing source contracts | 1, 4, 8, 17 | W33 | Inventory, wiring, compatibility, version and SMTP unit modules | Clean 6da5e3bf3 | PASS | Exact command below; 84 tests, 8.084s, exit 0, existing source only | pending |
| P03 implementation | 17 | W33 | New schema/parser/fixtures and RED/GREEN | Final artifact aggregate above | PASS | Source/synthetic slice only; whole criterion remains open | pending |
| Initial private/runtime lanes | 4, 6, 17 | W33 | ISOLATED/HOME/MIGRATION/ROTATION/RECOVERY | No exact selected action | NOT_RUN | Owning follow-up needed; no operational acceptance | pending |
| Delivery | 8, 17 | W33 | Latest-head CI/review/PR/merge | No P03 PR | NOT_RUN | Future PR; no remote delivery claim | pending |

The first issuance metadata check exited 1 on Result-cell detail text; the
second exited 1 on Acceptance-cell detail text. Both columns use registered
closed domains. Result now contains PASS/NOT_RUN and Acceptance remains pending;
command details and scope limits are in Location and prose. These defects also
caused package-inference diagnostics for unchanged archive documents. Only this
new Task was corrected; unrelated historical files were not changed.

The coordinator's actual baseline command was:

```sh
/tmp/hy-home-p09-qa/bin/python -m unittest \
  tests.lib.document_governance.test_operations_catalog.ServiceInventoryTests \
  tests.validation.test_service_wiring_contracts \
  tests.validation.test_service_runtime_compatibility \
  tests.validation.test_sec01_version_contract \
  tests.lib.ops.test_smtp_contract -q
```

Worker verification selects the new unit/contract modules plus affected existing
modules, metadata/link checks, manifest/workflow registration and the actual
changed/staged gate. Record commands, input HEAD/blob hashes, exits, failures
and corrections, coverage and skipped opt-in native classes. Initial source
work targets at least 80-percent meaningful coverage. Required registration is
integrated by the coordinator before the final changed/staged gate; a proposal
alone is not registered QA. Maintain SOURCE / UNIT / STATIC / ISOLATED / HOME /
MIGRATION / ROTATION / RECOVERY / DELIVERY separately.

## Review and Completion

Task issuance began in draft; the lifecycle chain now records ready and actual
in-progress execution. This initial source slice does not complete P03.
Close only against all criterion17 service/port/environment/identity acceptance,
with consumer-specific failures/unknowns accurately recorded and any remaining
criteria disposition following the canonical lifecycle. Source-only delivery
may be reported without a runtime PASS; do not mark the full Task completed
merely because public fixtures pass.

Use logical test/source/docs commits, one owning-Spec P03 PR after prerequisite
prefix reconciliation, required latest-head CI and independent review. On head
change, rerun affected checks/review. Shared integration rollback is a reviewed
logical revert; deployed state needs its own compatible recovery, not source
revert alone. No automatic cleanup of dirty worktrees. Retire branches/worktrees
only after delivery and preservation of ignored evidence.

Hand P01/P02 final endpoint/secret reference differences, SEC01 image-dependent
consumer/support evidence, CLN01 exact retained/unknown/delete-candidate edges,
P04/P05 worker network/auth/DEV/object/mail boundaries, P06 delivery/ACL/reload
contracts, P07 actual workload/resource facts, P08 final documentation paths and
P10 acceptance/negative/recovery cases. Each handoff binds final SHA, schema
version, proposal base blobs, executed versus NOT_RUN lanes and next exact
command. Unsupported budgets are unknown; do not invent token/time/retry grants.

## Related Documents

- [Specification](../spec.md)
- [Plan](../plan.md)
- [Current request reconciliation](../../0212-request-baseline-and-reconciliation/spec.md)
- [OpenBao continuation](tsk-0006-openbao-trust-bootstrap-and-recovery.md)
- [CLN01 consumer assessment](tsk-0007-cln01-material-retirement.md)
- [SEC01 stable/security integration](tsk-0009-sec01-stable-security-integration.md)
- [P02 catalog](tsk-0010-p02-secret-catalog-and-views.md)
- [Traefik guide](../../../05.operations/guides/0013-traefik.md)
- [Service onboarding](../../../05.operations/guides/0008-new-service-onboarding.md)
