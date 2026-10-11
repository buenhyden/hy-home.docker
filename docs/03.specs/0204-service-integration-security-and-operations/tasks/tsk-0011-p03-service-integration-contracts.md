---
title: "P03 Service Integration and Four-location Port Contracts Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Git baseline | 1, 17 | W33 | status/log/worktrees, ls-remote and open PR list | Local 6da5e3bf3; remote 2b9f5ec82 | PASS | Assessment above; exit 0, baseline only | pending |
| Existing source contracts | 1, 4, 8, 17 | W33 | Inventory, wiring, compatibility, version and SMTP unit modules | Clean 6da5e3bf3 | PASS | Exact command below; 84 tests, 8.084s, exit 0, existing source only | pending |
| P03 implementation | 17 | W33 | New schema/parser/fixtures and RED/GREEN | Issuance commit pending | NOT_RUN | Worker evidence pending; no code authored by issuance | pending |
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

Task issuance stays draft; the assigned worker records draft-to-in-progress
when actual implementation begins. This assessment does not complete P03.
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
