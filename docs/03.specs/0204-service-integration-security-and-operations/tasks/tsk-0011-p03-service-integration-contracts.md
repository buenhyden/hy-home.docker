---
title: "P03 Service Integration and Four-location Port Contracts Task"
version: "0.2.13"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-26"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0011"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-11"
---

# P03 Service Integration and Four-location Port Contracts Task

## Overview

### Objective

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

### v30 exporter selection and optional Ollama source — 2026-10-26

현 직접 요청·`SPEC-0212-TSK-0008`의 coordinator lease와 독립 IaC 사전 검토로
기준 `136b7cac4483d4af8aaa73ca6dc3f9a0da521e10`, branch
`codex/v30-infra-source-completion`의 criterion 17 source 잔여만 수정한다.
P02·P05·SPEC-0224의 실제 credential·workflow·관측 인수는 이 Task가 대신하지 않는다.

같은 단일 infra writer가 MNG/DEV `docker-compose.yml`, Kafka `docker-compose.yml`의
기존 Exporter·monitor provisioner profile을 Producer와 맞춘다. 새 서비스·이미지·
monitor 계정을 만들지 않으며 역방향 depends_on도 추가하지 않는다. POL-0078 기존
profile 표와 companion 표가 직접 Target의 정확한 목록을 소유한다. 암묵 dependency로
Producer만 기동할 때도 companion 합집합이 필요하며 임의 Docker CLI를 차단하는 도구는 아니다.
oauth2-proxy-valkey-exporter는 현재 이미 obs_net에 있으므로 NO_CHANGE다.

새 `infra/07-workflow/n8n/docker-compose.ollama-local.yml`은 기존 typed root-base
계약으로 Worker와 Ollama만 새 internal bridge에 추가한다. 기본 root include·profile·
Main/Runner·기존 AI/edge network는 유지한다. 따라서 다른 기존 AI/edge peer를 차단했다고
주장하지 않는다. Cloud 호출·키 발급·private Credential 저장·custom node는 추가하지 않는다.
POL-0078, n8n/MNG README, GDE-0053·RUN-0053과 기존
`tests/validation/test_service_wiring_contracts.py`가 source/선택/경계를 설명·검사한다.
U1의 shared ROOT/env·Catalog·entrypoint는 P02 Task0010의 동일 writer 단위다.

source RED는 core/local·CDC·analytics feature의 Exporter/provisioner 결손과 optional
overlay 부재를 재현했다. GREEN 34건(33 PASS/Native 1 SKIP), 별도 RuntimeCompatibility
28 PASS, Ruff와 diff check PASS는 Task0010과 같은 실행 범위다. direct-target 검사는
POL-0078 실제 표와 Compose depends_on closure를 대조하여 bare mng-pg/ollama 등과
mng-pg-init·kafka-connect의 암묵 Producer에서 companion 누락을 검출하고 정식 목록을
수용한다. 공개 render는 `.env.example`과 격리된 CLI 환경만 사용하고 실제 dotenv·Secret을
읽지 않았다. infra-validate의 별도 graph/Compose BLOCKED는 그대로 보존한다.

실제 Worker→Ollama Credential·목록·생성·embedding·거부·복구, Prometheus scrape와
redis_up/pg_up·Grafana query·HOME rollout은 NOT_RUN이다. `OLLAMA_NO_CLOUD=1`은 유지하며
Cloud 승인 없이는 BLOCKED_CLOUD_APPROVAL이다. Source rollback은 이 변경 unit만 revert하고,
운영 적용 후에는 승인된 drain·원래 exact service/network 재생성·독립 backup/복구가 필요하다.
최종 source 검토·staged gate·commit·criterion 17의 owner acceptance는 pending이다.

최종 통합 source 회귀는 준비된 Python에서 기존 네 모듈의 source class를 선택하여
58 PASS, 19.493초, exit 0이었다. 실제 명령은 Task0010의 후속 source 영수증을 따른다.
operations catalog의 최초 exit 1은 6개 Profile·2개 n8n Env의 기존 inventory projection
drift였다. 추가 exact lease로 RES-0002-m0021의 기존
`operations_catalog.render_service_inventory`를 사용해 bounded table과 metadata만
갱신했다. 역사적 문장·consumer·backup·처분은 보존했고 새 inventory는 만들지 않았다.
동일 `check-operations-catalog.py` 재검증은 PASS, exit 0이다. infra-validate helper의
absolute path 차단은 기존 Terrakube/Dozzle Docker socket, Alloy Docker 경로와 host
Exporter의 `/`·`/proc`·`/sys` 같은 의도된 host bind에 해당한다. 신규 private 입력 부재가
원인이라는 증거는 없으며, 이 경계를 완화하거나 host 경로를 복제하지 않았다.
추가 inventory·결과 영수증과 Native cleanup 문구 수정까지 독립 검토 READY이며
actionable finding은 없다. criterion 17 전체·실제 관측·Node/HOME 인수는 pending이다.

### 현재 증거 범위 조정 — 2026-10-22

공개 추적 소스 대조에서 네 위치 port projector와 CLI는 구현되어 있으며,
listener와 running/healthy/used/recovered는 관측 없이 unknown을 유지한다.
2026-10-20–21 gateway/Hermes 후속 결과는 해당 대상의 보고이며 criterion 17
전체의 identity, TLS, consumer 및 recovery 수락을 대신하지 않는다.

아래 frozen Evidence의 supply/integrity PASS가 metadata/document-library
timeout 행을 `Resolves`로 가리키더라도 서로 다른 check의 성공이 그 실패를
해소한 것으로 해석하지 않는다. 과거 FAIL과 aggregate NOT_RUN은 당시 입력의
결과로 보존하며, 현재 입력의 해당 등록 gate 결과는 별도로 기록한다. 이번
조정은 새 실행이나 criterion 수락 없이 현재 증거 해석만 명시한다.

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

### Registration Proposal After P02 Integration

The subsequent coordinator handoff supersedes the earlier proposed P03-first
registration order: P02 source is now in observed local and remote main
`08b009a9ce0f288926f2edc4eebcbc5fb475d1e5`. Its source history preserves
P01 main `6d1d6960e59c316fad2c6d168d853989da565faa`. Worker HEAD before
this increment is `c1bc25f1a09e9e5fb17dfbbc10d80fe07544af5e`, clean.
The shared checkout remains a separate dirty historical checkout and is not
an input for current main files. No worker history or prior proposal is replaced.

The regenerated public proposal is preserved in ignored
`.agent-work/integration-proposal-08b009/`. Its four paths are
`scripts/manifest.yaml`, `.github/workflow-contract.yml`, the Platform
Operations README and the fixture-family README. Exact base blobs and proposed
file hashes are in `base-blobs.json`; patch SHA256 is
`1bad369d8f0e0ecc86270634ea2e8880d5185f772a90ad20aeec0518bbb635df`.
The old patch remains historical comparison input. Common-owner application is
NOT_APPLIED. Only the isolated public scratch worktree
`/tmp/hy-home-p03-registration-08b009` contains the candidate common changes.

The initial manifest probe passed because untracked P03 files were outside its
Git-index enumeration. After the twelve owned public artifacts were staged in
the scratch index, RED exited 1 with exactly the two missing P03 script records.
After proposal registration, manifest and workflow validators exited 0.
Machine comparison retained all 91 prior manifest records, including P02's
library/I/O/CLI records, RUN-0085 authority and subprocess-test consumer. Removing
only the two P03 modules and appended routing from the candidate reconstructs
the complete baseline workflow: existing tests, routing, actions and permissions
are unchanged. Current-main `git apply --check` exited 0 without target writes.

Fresh candidate inputs are main SHA above plus sixteen public overlay hashes
in `candidate-input.json`, aggregate SHA256
`1b28f01127af4a0db04f4da51ea81a2a388e83e6b95761c32eaebb79802fb8cd`.
`/tmp/hy-home-p09-qa/bin/python -m unittest tests.lib.ops.test_port_inventory
tests.validation.test_port_contract tests.lib.ops.test_secret_catalog
tests.validation.test_secret_catalog_contract tests.validation.test_script_manifest -q`
ran 130 tests in 24.438 seconds, exit 0. This is fresh combined synthetic/source
evidence, not inherited 42/84-test or coverage evidence. No new coverage result
is asserted. `run-ci-precommit.sh --mode local-staged` on that candidate exited 0.
`run-ci-gate.py --profile changed --local-only --explain` exited 0 and selected the
existing repository-integrity leaf; explain mode executes no aggregate gate.

The coordinator remains the sole writer of actual common files and owns final
integrated-head gates/review/delivery. P01's four operations documents and its
stale P02 proposal are untouched. P02 schema 1.0.0, issued catalog metadata and
COMM-003-to-COMM-002 alias grant no consumer identity, credential, runtime ACL,
delivery or recovery acceptance. Actual consumer authentication, HOME, migration,
rotation, deletion and recovery remain NOT_RUN. Criterion 17 stays open.
Rollback for this increment is a reviewed Task documentation revert and rejection
of the unapplied proposal; scratch source checks imply no deployed rollback.

### Coordinator Common Integration — 2026-10-11

The coordinator independently observed clean local main and actual remote main
`08b009a9ce0f288926f2edc4eebcbc5fb475d1e5`. P02 is already integrated at
that input; it is preserved before P03, not rebased after it. The foreign shared
checkout remains detached and unchanged. Its status and tracked working/index
diff hashes match the earlier P02 preservation receipt; this does not assert
that every ignored or untracked byte was separately hashed.

The dedicated coordinator branch is `codex/p03-common-integration` in
`.worktrees/p03-common-integration`. Source merge
`4cadd4d7ea2cb1d45a18b75f76723c1fb5982d96` preserves the worker's
`93ad5da2538f99cc978745a458587e2fde71550c` and
`c1bc25f1a09e9e5fb17dfbbc10d80fe07544af5e` logical commits. Common commit
`c3fce85d2f66f24bac0908d78a3b174bce00e828` registers the two scripts and
two test modules, identical six-prefix suite/root routing, Platform Operations
navigation, the fixture-family README and three existing test/library indexes.
It preserves all 91 preceding manifest records and P02's test arguments/routes.
The later worker Task commit `c74c04bf6fc6ba2a853b000f638a9ac9d59e3ab7`
is also preserved by merge `3a79b0ae1`; its reported 130 candidate tests remain
worker evidence, not a coordinator rerun.

The old four-path patch failed actual current-base `git apply --check`, exit 1,
on Manifest/workflow. The coordinator applied only the two matching README
hunks and reconciled Manifest/workflow on current P02 bytes. The regenerated
08b proposal's four resulting file hashes exactly match this common commit;
the three extra indexes are additive navigation. There is no script README
generator route, so the earlier regeneration suggestion is superseded by the
actual index edits. No Registry, Spec/Plan, catalog, Compose, dotenv, gateway,
Alloy, backup or deployed service was edited.

Fresh coordinator source checks used the unchanged helper/schema/test/fixture
bytes plus the seven common staged files at `4cadd4d7e`. The command
`python -m unittest tests.lib.ops.test_port_inventory tests.validation.test_port_contract -q`
ran 42 tests in 3.679 seconds, exit 0. The worker's 84-test regression receipt
and 97-percent coverage remain historical, NOT_RERUN for this integration.
Script Manifest `--check-generated` and workflow-contract validators exited 0;
workflow totals were five workflows, seven jobs and eight actions. The five
explicit common README metadata paths selected one governed document, zero
violations, exit 0; this is not a claim of five governed metadata selections.

The coordinator built the canonical changed LOCAL plan for the exact 20 paths,
validated public execution parity, and executed these 12 affected registered
leaves through `ci_gate_runner.execute_execution_plan`, retaining each existing
argv, environment admission and timeout, with no custom executor:

```text
leaf.repo-document-metadata
leaf.local-candidate-preflight
leaf.docs-traceability
leaf.local-document-corpus-lifecycle
leaf.local-diff-hygiene
leaf.local-script-manifest
leaf.ci-gate-contract-regressions
leaf.ci-gate-runner-regressions
leaf.workflow-contract-regressions
leaf.repo-contracts-control-plane-regressions
leaf.workflow-contract
leaf.repository-integrity-regressions
```

All 12 exited 0. The repository-integrity leaf ran its complete registered
arguments, including both P02 and P03 modules: 407 tests, 92.623 seconds, exit 0.
Active metadata selected 492 documents with zero violations. Full link checking
found 1,198 documents/11,619 links, zero failures and one existing historical
capture-source warning. Lifecycle and candidate metadata/version checks passed.
The full 33-leaf plan was compiled, not executed as a new full aggregate.
Its canonical six-field SHA256 is
`bdcabe18407b9b3e5797a9429f5dfbca84e86550ac84ecca2b2b7a4c14624b6d`;
the selected 12-leaf SHA256 is
`b9c292d9da8f63c11368d4489ef5e8ce83b145a47b306acb09b7a28bd625e15a`.
Public input hashes, exact invocations, exits and log digests are preserved in
the coordinator's ignored `p03-gate-input.json` and `p03-affected-gates.json`.
Unchanged P02 gate-source receipts are retained rather than relabeled as fresh.

Independent coordinator code and security reviewers accepted the exact source
and seven common-file hashes, with no open Critical/Important or P1/P2 finding.
Each source/common/Task merge used the registered local-staged controller
immediately before commit, exit 0, plus Conventional Commit validation. The
final result-document increment requires its own metadata/style checks and
review; it changes no executable input or registered routing.

SOURCE, UNIT and affected STATIC evidence above support this local source
integration only. Synthetic Compose `config` does not start a daemon workload.
ISOLATED native authentication, HOME, MIGRATION, ROTATION and RECOVERY remain
NOT_RUN. P03 push, PR, hosted CI and remote merge remain NOT_RUN; later observed
remote publication must be checked separately. Criterion 17 stays open.

P01's integrated source v2 journal/issuance compatibility does not close HOME
or snapshot/empty-restore acceptance. P02's catalog metadata is not issuance or
runtime ACL. P04/P05 may continue provisional source consumers against this
port schema 1.0.0, but worker UID/GID, final DEV/S3 endpoints/TLS/CA, function-only
grants, enforced object policy and native producer/notifier proof remain open.
P06 public wave/receipt shape is not pilot/copy/delete/recovery authorization.
MLflow/SonarQube/Terrakube increments still need their named implementation
leases and exact native inputs. Next public reproduction commands are the
dedicated unittest above and `python3 scripts/operations/port-inventory.py`;
the full future delivery route is
`python3 scripts/validation/run-ci-gate.py --profile changed`, which was not
executed as a new full aggregate here. Rollback is a reviewed logical source
revert; no operational rollback was performed or implied.

### Root Acceptance Continuation — 2026-10-13

Current root and `origin/main`: `62556dc63b66c828c27e9c33017d26cdf70b8542`; the assigned worktree was clean before this Task-only change. The 377-path diff from `23e37362b72e98028a4675f282819c0346ae59dc` is context, not copied PASS. No current-image warning evidence was collected; image/scanner changes are NO_CHANGE and `SECURITY_WARNING_CONFIRMED` is not asserted.

| Surface | Disposition | Owner / boundary |
| --- | --- | --- |
| This Task; existing P03 source | SOURCE_APPLIED / NO_CHANGE | P03; no tool/schema/test rewrite |
| P03 validator augmentation; P05 capture overlay and its narrow policy correction | CONFIRMED_GAP / pending validation | QA owns the two validator/test paths; infra owns the three overlay/README/n8n-test paths; this Task and POL-0078 record scope only. Root Compose, catalog, registry, workflow and CI remain read-only. |
| Compose, dotenv, gateway, OpenBao, backup, catalog, Registry/workflow | NO_CHANGE / read-only | Coordinator; P01/P02/SEC/SMTP/P04/P05/P06 |
| LAB, private dotenv, host realpath/inode, data/secrets | OUT_OF_SCOPE / NOT_RUN | No private/LAB read or mutation |
| Native auth, peer denial, readiness, OTLP, restore/delivery | CONSUMER_DEPENDENT / RUNTIME_UNVERIFIED | Exact owner/target/recovery needed |

The first root-form validator was too broad: independent IAC/code review
reproduced admission of privileged and host-bind fields. A separate review also
reproduced incorrect root absence in version tracking because its caller passed
only an `infra`/`labs` subset. QA is correcting these as RED/GREEN with the
root network-only contract and bounded authoritative root tracking (root stays
outside image discovery). This Task now owns the policy correction as the eighth
owned path; the corrected validation, source/security review, and final gate
remain pending. Earlier review/format results and hashes are not final
acceptance.

#### 111-service four-location supplement

This dated supplement is a compact projection, not a second inventory. It binds the 111 current `m0021` rows, one unique `(Compose path, Service)`, to `project_root`/`expected_from_root`: 44 hashed root-plus-leaf inputs and 43 included leaves. `m0021` remains authority for tier/name/image or build/profile, declared dependency/reverse edge, network/mount/UID/read-only/capability, value-free secret support metadata, metrics, backup and ownership.

Legend: `U` unknown; `D` declared; `A` absent; `N` unpublished; `B` Traefik disabled. Endpoint syntax is `network/name:port/protocol`, `host-IP published->target/protocol`, and `kind/name@network:port/scheme`; `?` is an unresolved public-source field. Listener is `U` for every row. The table is source-only and every native/runtime/recovery result is `NOT_RUN`; `DNS=U` is not a live DNS failure and host publication is not a listener. `_FILE` support remains image-parser dependent.

| Service | Listener | Internal DNS declaration | Host publication declaration | Traefik backend declaration | Native state |
| --- | --- | --- | --- | --- | --- |
| `airflow-apiserver` | U | D; airflow_net/airflow-apiserver:?/tcp, edge_net/airflow-apiserver:?/tcp, mng_data_net/airflow-apiserver:?/tcp | N | U; http/airflow@?:?/? | NOT_RUN |
| `airflow-dag-processor` | U | D; airflow_net/airflow-dag-processor:?/tcp, mng_data_net/airflow-dag-processor:?/tcp | N | U | NOT_RUN |
| `airflow-init` | U | D; airflow_net/airflow-init:?/tcp, mng_data_net/airflow-init:?/tcp | N | U | NOT_RUN |
| `airflow-scheduler` | U | D; airflow_net/airflow-scheduler:?/tcp, mng_data_net/airflow-scheduler:?/tcp | N | U | NOT_RUN |
| `airflow-statsd-exporter` | U | D; airflow_net/airflow-statsd-exporter:?/tcp, obs_net/airflow-statsd-exporter:?/tcp | N | U | NOT_RUN |
| `airflow-triggerer` | U | D; airflow_net/airflow-triggerer:?/tcp, mng_data_net/airflow-triggerer:?/tcp | N | U | NOT_RUN |
| `airflow-valkey` | U | D; airflow_net/airflow-valkey:?/tcp | N | U | NOT_RUN |
| `airflow-valkey-exporter` | U | D; airflow_net/airflow-valkey-exporter:?/tcp, obs_net/airflow-valkey-exporter:?/tcp | N | U | NOT_RUN |
| `airflow-worker` | U | D; airflow_net/airflow-worker:?/tcp, mng_data_net/airflow-worker:?/tcp | N | U | NOT_RUN |
| `alertmanager` | U | D; edge_net/alertmanager:?/tcp, obs_net/alertmanager:?/tcp | N | U; http/alertmanager@?:?/? | NOT_RUN |
| `alloy` | U | D; edge_net/alloy:?/tcp, obs_net/alloy:?/tcp, quality_otlp_net/alloy:?/tcp | D; ? ?->?/tcp | U; http/alloy@?:?/? | NOT_RUN |
| `backup-sqlite-export` | U | A | N | U | NOT_RUN |
| `cadvisor` | U | D; edge_net/cadvisor:?/tcp, obs_net/cadvisor:?/tcp | N | U; http/cadvisor@?:?/? | NOT_RUN |
| `comfyui` | U | D; edge_net/comfyui:?/tcp | D; 127.0.0.1 ?->?/tcp | U; http/comfyui@?:?/? | NOT_RUN |
| `conftest` | U | A | N | U | NOT_RUN |
| `crawl4ai` | U | D; crawl4ai_egress_net/crawl4ai:11235/tcp, crawl4ai_net/crawl4ai:11235/tcp | N | B | NOT_RUN |
| `crawl4ai-egress` | U | D; crawl4ai_egress_net/crawl4ai-egress:?/tcp, crawl4ai_outbound_net/crawl4ai-egress:?/tcp | N | B | NOT_RUN |
| `dbt` | U | D; dev_data_net/dbt:?/tcp | N | U | NOT_RUN |
| `dbt-db-provision` | U | D; dev_data_net/dbt-db-provision:?/tcp | N | B | NOT_RUN |
| `dcgm-exporter` | U | D; obs_net/dcgm-exporter:?/tcp | N | U | NOT_RUN |
| `debezium-db-provision` | U | D; dev_data_net/debezium-db-provision:?/tcp | N | B | NOT_RUN |
| `dev-perf-provision` | U | D; dev_data_net/dev-perf-provision:?/tcp | N | B | NOT_RUN |
| `dev-pg` | U | D; dev_data_net/dev-pg:5432/tcp | D; 127.0.0.1 ?->5432/tcp | B | NOT_RUN |
| `dev-pg-exporter` | U | D; dev_data_net/dev-pg-exporter:9187/tcp, obs_net/dev-pg-exporter:9187/tcp | N | B | NOT_RUN |
| `dev-pg-monitor-provision` | U | D; dev_data_net/dev-pg-monitor-provision:?/tcp | N | B | NOT_RUN |
| `dev-platform-provision` | U | D; dev_data_net/dev-platform-provision:?/tcp | N | B | NOT_RUN |
| `dev-valkey` | U | D; dev_data_net/dev-valkey:6379/tcp | N | B | NOT_RUN |
| `dev-valkey-exporter` | U | D; dev_data_net/dev-valkey-exporter:9121/tcp, obs_net/dev-valkey-exporter:9121/tcp | N | B | NOT_RUN |
| `dozzle` | U | D; edge_net/dozzle:?/tcp | N | U; http/dozzle@?:?/? | NOT_RUN |
| `flink-jobmanager` | U | D; kafka_net/flink-jobmanager:8081/tcp, object_net/flink-jobmanager:8081/tcp | D; 127.0.0.1 ?->8081/tcp | U | NOT_RUN |
| `flink-taskmanager` | U | D; kafka_net/flink-taskmanager:?/tcp, object_net/flink-taskmanager:?/tcp | N | U | NOT_RUN |
| `flower` | U | D; airflow_net/flower:?/tcp, edge_net/flower:?/tcp, mng_data_net/flower:?/tcp, obs_net/flower:?/tcp | N | U; http/flower@?:?/? | NOT_RUN |
| `gatus` | U | D; edge_net/gatus:?/tcp, mng_data_net/gatus:?/tcp, obs_net/gatus:?/tcp | N | U; http/gatus@?:?/? | NOT_RUN |
| `grafana` | U | D; edge_net/grafana:?/tcp, mng_data_net/grafana:?/tcp, obs_net/grafana:?/tcp | N | U; http/grafana-svc@?:?/? | NOT_RUN |
| `grafana-db-provision` | U | D; mng_data_net/grafana-db-provision:?/tcp | N | B | NOT_RUN |
| `great-expectations` | U | D; object_net/great-expectations:?/tcp | N | U | NOT_RUN |
| `jupyterlab` | U | D; ai_net/jupyterlab:?/tcp, edge_net/jupyterlab:?/tcp | N | U; http/jupyter@?:?/? | NOT_RUN |
| `k6` | U | D; obs_net/k6:?/tcp | N | U | NOT_RUN |
| `kafbat-ui` | U | D; edge_net/kafbat-ui:?/tcp, kafka_net/kafbat-ui:?/tcp | N | U; http/kafka-ui@?:?/? | NOT_RUN |
| `kafka-1` | U | D; kafka_net/kafka-1:?/tcp, obs_net/kafka-1:?/tcp | D; 127.0.0.1 ?->?/tcp | U | NOT_RUN |
| `kafka-connect` | U | D; dev_data_net/kafka-connect:?/tcp, edge_net/kafka-connect:?/tcp, kafka_net/kafka-connect:?/tcp, obs_net/kafka-connect:?/tcp | N | U; http/kafka-connect@?:?/? | NOT_RUN |
| `kafka-exporter` | U | D; kafka_net/kafka-exporter:?/tcp, obs_net/kafka-exporter:?/tcp | N | U | NOT_RUN |
| `kafka-init` | U | D; kafka_net/kafka-init:?/tcp | N | U | NOT_RUN |
| `kafka-rest-proxy` | U | D; edge_net/kafka-rest-proxy:?/tcp, kafka_net/kafka-rest-proxy:?/tcp | N | U; http/kafka-rest@?:?/? | NOT_RUN |
| `keycloak` | U | D; edge_net/keycloak:?/tcp, mng_data_net/keycloak:?/tcp, obs_net/keycloak:?/tcp | N | U; http/keycloak@?:?/? | NOT_RUN |
| `loki` | U | D; edge_net/loki:?/tcp, object_net/loki:?/tcp, obs_net/loki:?/tcp | D; ? ?->?/tcp | U; http/loki@?:?/? | NOT_RUN |
| `mailpit` | U | D; edge_net/mailpit:?/tcp, mail_net/mailpit:?/tcp | D; 127.0.0.1 ?->?/tcp | U; http/mailpit-ui@?:?/? | NOT_RUN |
| `mlflow` | U | D; ai_net/mlflow:?/tcp, edge_net/mlflow:?/tcp, mng_data_net/mlflow:?/tcp, object_net/mlflow:?/tcp | N | U; http/mlflow@?:?/? | NOT_RUN |
| `mlflow-db-provision` | U | D; mng_data_net/mlflow-db-provision:?/tcp | N | B | NOT_RUN |
| `mng-pg` | U | D; mng_data_net/mng-pg:?/tcp | D; 127.0.0.1 ?->?/tcp | U | NOT_RUN |
| `mng-pg-exporter` | U | D; mng_data_net/mng-pg-exporter:?/tcp, obs_net/mng-pg-exporter:?/tcp | N | B | NOT_RUN |
| `mng-pg-init` | U | D; mng_data_net/mng-pg-init:?/tcp | N | B | NOT_RUN |
| `mng-pg-monitor-provision` | U | D; mng_data_net/mng-pg-monitor-provision:?/tcp | N | B | NOT_RUN |
| `mng-valkey` | U | D; mng_data_net/mng-valkey:?/tcp | D; ? ?->?/tcp | B | NOT_RUN |
| `mng-valkey-exporter` | U | D; mng_data_net/mng-valkey-exporter:?/tcp, obs_net/mng-valkey-exporter:?/tcp | N | B | NOT_RUN |
| `n8n` | U | D; edge_net/n8n:?/tcp, mng_data_net/n8n:?/tcp, n8n_net/n8n:?/tcp, obs_net/n8n:?/tcp | N | U; http/n8n@?:?/? | NOT_RUN |
| `n8n-task-runner` | U | D; n8n_net/n8n-task-runner:?/tcp | N | U | NOT_RUN |
| `n8n-task-runner-worker` | U | D; n8n_net/n8n-task-runner-worker:?/tcp | N | U | NOT_RUN |
| `n8n-valkey` | U | D; n8n_net/n8n-valkey:?/tcp | N | U | NOT_RUN |
| `n8n-valkey-exporter` | U | D; n8n_net/n8n-valkey-exporter:?/tcp, obs_net/n8n-valkey-exporter:?/tcp | N | U | NOT_RUN |
| `n8n-worker` | U | D; mng_data_net/n8n-worker:?/tcp, n8n_net/n8n-worker:?/tcp | N | U | NOT_RUN |
| `neo4j` | U | D; edge_net/neo4j:?/tcp | N | U; http/neo4j@?:?/? | NOT_RUN |
| `nginx` | U | D; edge_net/nginx:?/tcp, object_net/nginx:?/tcp | D; ? ?->?/tcp | U | NOT_RUN |
| `node-exporter` | U | A | N | U | NOT_RUN |
| `oauth2-proxy` | U | D; edge_net/oauth2-proxy:?/tcp, mng_data_net/oauth2-proxy:?/tcp, obs_net/oauth2-proxy:?/tcp | N | D; http/oauth2-proxy-svc@edge_net:?/? | NOT_RUN |
| `oauth2-proxy-valkey` | U | D; mng_data_net/oauth2-proxy-valkey:?/tcp | N | B | NOT_RUN |
| `oauth2-proxy-valkey-exporter` | U | D; mng_data_net/oauth2-proxy-valkey-exporter:?/tcp, obs_net/oauth2-proxy-valkey-exporter:?/tcp | N | B | NOT_RUN |
| `ollama` | U | D; ai_net/ollama:?/tcp, edge_net/ollama:?/tcp | D; 127.0.0.1 ?->?/tcp | U; http/ollama@?:?/? | NOT_RUN |
| `ollama-exporter` | U | D; ai_net/ollama-exporter:?/tcp, obs_net/ollama-exporter:?/tcp | N | U | NOT_RUN |
| `open-webui` | U | D; ai_net/open-webui:?/tcp, edge_net/open-webui:?/tcp | N | U; http/open-webui@?:?/? | NOT_RUN |
| `open_notebook` | U | D; ai_net/open_notebook:5055/tcp, ai_net/open_notebook:?/tcp, edge_net/open_notebook:5055/tcp, edge_net/open_notebook:?/tcp | D; 127.0.0.1 ?->5055/tcp | U; http/open-notebook@?:?/? | NOT_RUN |
| `openbao` | U | D; edge_net/openbao:?/tcp, obs_net/openbao:?/tcp, secrets_net/openbao:?/tcp | N | U; http/openbao@?:?/https | NOT_RUN |
| `openbao-agent` | U | D; secrets_net/openbao-agent:?/tcp | N | U | NOT_RUN |
| `opensearch` | U | D; edge_net/opensearch:?/tcp, obs_net/opensearch:?/tcp | N | U; http/opensearch@?:9200/https | NOT_RUN |
| `opensearch-dashboards` | U | D; edge_net/opensearch-dashboards:?/tcp | N | U; http/opensearch-dashboards@?:?/https | NOT_RUN |
| `opentofu` | U | U; default/opentofu:?/tcp | N | U | NOT_RUN |
| `pact-broker` | U | D; mng_data_net/pact-broker:9292/tcp | D; 127.0.0.1 ?->9292/tcp | U | NOT_RUN |
| `pact-broker-db-provision` | U | D; mng_data_net/pact-broker-db-provision:?/tcp | N | B | NOT_RUN |
| `prometheus` | U | D; edge_net/prometheus:?/tcp, obs_net/prometheus:?/tcp, seaweedfs_metrics_net/prometheus:?/tcp | N | U; http/prometheus@?:?/? | NOT_RUN |
| `pushgateway` | U | D; edge_net/pushgateway:?/tcp, obs_net/pushgateway:?/tcp | N | U; http/pushgateway@?:?/? | NOT_RUN |
| `pyroscope` | U | D; edge_net/pyroscope:?/tcp, obs_net/pyroscope:?/tcp | D; 127.0.0.1 ?->?/tcp | U; http/pyroscope@?:?/? | NOT_RUN |
| `qdrant` | U | D; ai_net/qdrant:?/tcp, edge_net/qdrant:?/tcp, obs_net/qdrant:?/tcp | N | U; http/qdrant@?:?/? | NOT_RUN |
| `redisinsight` | U | D; dev_data_net/redisinsight:?/tcp, mng_data_net/redisinsight:?/tcp, redisinsight_ingress_net/redisinsight:?/tcp | N | D; http/redisinsight-svc@redisinsight_ingress_net:?/? | NOT_RUN |
| `registry` | U | D; obs_net/registry:5000/tcp | D; 127.0.0.1 ?->5000/tcp | U | NOT_RUN |
| `renovate` | U | U; default/renovate:?/tcp | N | U | NOT_RUN |
| `restic` | U | A | N | U | NOT_RUN |
| `restic-offsite` | U | D; restic_offsite_net/restic-offsite:?/tcp | N | U | NOT_RUN |
| `schema-registry` | U | D; edge_net/schema-registry:?/tcp, kafka_net/schema-registry:?/tcp, obs_net/schema-registry:?/tcp | N | U; http/schema-registry@?:?/? | NOT_RUN |
| `seaweedfs-buckets` | U | D; object_net/seaweedfs-buckets:?/tcp | N | U | NOT_RUN |
| `seaweedfs-filer` | U | D; seaweed_internal/seaweedfs-filer:9326/tcp, seaweed_internal/seaweedfs-filer:?/tcp, seaweedfs_metrics_net/seaweedfs-filer:9326/tcp, seaweedfs_metrics_net/seaweedfs-filer:?/tcp | N | U | NOT_RUN |
| `seaweedfs-master` | U | D; seaweed_internal/seaweedfs-master:9324/tcp, seaweed_internal/seaweedfs-master:?/tcp, seaweedfs_metrics_net/seaweedfs-master:9324/tcp, seaweedfs_metrics_net/seaweedfs-master:?/tcp | N | U | NOT_RUN |
| `seaweedfs-s3` | U | D; edge_net/seaweedfs-s3:?/tcp, object_net/seaweedfs-s3:?/tcp, seaweed_internal/seaweedfs-s3:?/tcp | N | U; http/s3@?:?/? | NOT_RUN |
| `seaweedfs-table-bucket` | U | D; object_net/seaweedfs-table-bucket:?/tcp | N | U | NOT_RUN |
| `seaweedfs-volume` | U | D; seaweed_internal/seaweedfs-volume:9325/tcp, seaweed_internal/seaweedfs-volume:?/tcp, seaweedfs_metrics_net/seaweedfs-volume:9325/tcp, seaweedfs_metrics_net/seaweedfs-volume:?/tcp | N | U | NOT_RUN |
| `sonarqube` | U | D; edge_net/sonarqube:?/tcp, mng_data_net/sonarqube:?/tcp | N | U; http/sonarqube@?:?/? | NOT_RUN |
| `spark` | U | D; object_net/spark:?/tcp | N | U | NOT_RUN |
| `stalwart` | U | D; edge_net/stalwart:?/tcp, mail_net/stalwart:?/tcp | N | U; http/stalwart-ui@?:8080/? | NOT_RUN |
| `stalwart-config` | U | D; mail_net/stalwart-config:?/tcp | N | B | NOT_RUN |
| `storybook` | U | D; experience_ingress_net/storybook:8080/tcp | N | D; http/storybook@experience_ingress_net:8080/? | NOT_RUN |
| `storybook-mcp` | U | D; edge_net/storybook-mcp:7613/tcp | N | D; http/storybook-mcp@edge_net:7613/? | NOT_RUN |
| `superset` | U | D; edge_net/superset:?/tcp, mng_data_net/superset:?/tcp, object_net/superset:?/tcp | N | U; http/superset@?:8088/? | NOT_RUN |
| `superset-db-provision` | U | D; mng_data_net/superset-db-provision:?/tcp | N | B | NOT_RUN |
| `superset-init` | U | D; mng_data_net/superset-init:?/tcp | N | B | NOT_RUN |
| `surrealdb` | U | D; ai_net/surrealdb:8000/tcp | N | U | NOT_RUN |
| `tempo` | U | D; edge_net/tempo:?/tcp, object_net/tempo:?/tcp, obs_net/tempo:?/tcp | D; ? ?->?/tcp | U; http/tempo@?:?/? | NOT_RUN |
| `terrakube-api` | U | D; edge_net/terrakube-api:?/tcp, mng_data_net/terrakube-api:?/tcp, object_net/terrakube-api:?/tcp, terrakube_net/terrakube-api:?/tcp | N | U; http/terrakube-api@?:8080/? | NOT_RUN |
| `terrakube-executor` | U | D; edge_net/terrakube-executor:?/tcp, mng_data_net/terrakube-executor:?/tcp, object_net/terrakube-executor:?/tcp, terrakube_net/terrakube-executor:?/tcp | N | U; http/terrakube-executor@?:?/? | NOT_RUN |
| `terrakube-ui` | U | D; edge_net/terrakube-ui:?/tcp, terrakube_net/terrakube-ui:?/tcp | N | U; http/terrakube-ui@?:?/? | NOT_RUN |
| `traefik` | U | U; edge_net/?:?/tcp, edge_net/?:?/tcp, edge_net/traefik:?/tcp, experience_ingress_net/traefik:?/tcp, obs_net/traefik:?/tcp, redisinsight_ingress_net/traefik:?/tcp | D; ? ?->?/tcp | U | NOT_RUN |
| `trino` | U | D; object_net/trino:8080/tcp | D; 127.0.0.1 ?->8080/tcp | U | NOT_RUN |
| `wiremock` | U | U; default/wiremock:8080/tcp | D; 127.0.0.1 ?->8080/tcp | B | NOT_RUN |

Source identity grouping is limited to declared evidence: browser SSO is represented by `keycloak`, `oauth2-proxy`, and inventory rows with source router middleware; app JWT by the inventory `authentication_env_keys` (including Airflow source declarations); webhook HMAC and machine-token consumers have no confirmed P03 binding. Native user targets, issuer/audience/expiry and direct-backend denials are unknown.

Source audit: Host `D/N` 19/92; DNS `D/U/A` 103/4/4; Traefik `D/B/U` 4/25/82; 38 backend endpoints have an unknown selector/network. These are source limits, not native acceptance. Membership differences were empty; no membership edit is required.

#### Fresh source receipts and handoff

Catalog/version projection/port CLI checks and 42 P03 tests exited 0 (42, 4.770s). A cross-owner source/synthetic suite exited 0 (55, 5.340s), covering declared DEV/MNG and P04/P05 contracts. The root negative source suite exited 0 (27, 23.015s), covering synthetic collisions, named bind nesting/empty declarations, root network/auth and Alloy. It does not prove peer denial, issuer/audience expiry, OTLP query/freshness or host realpath/inode. Default Compose static validation exited 0 with public example/dummy secrets (66 selections, 316 services); no daemon started.

P04/P05/P06 receive this SHA and schema 1.0.0 only. `opsflow_dev`, S3 prefix, Airflow worker, Node API and mail endpoint require consumer, identity, image/security, network and recovery receipts. Rollback is a logical revert of this Task evidence only.

#### Consumer audit addendum — 2026-10-13

The value-free source audit at `62556dc63b66c828c27e9c33017d26cdf70b8542`
found that `opsflow.json` declares `password_secrets: null`; current
`dev-platform-provision` invokes only `platform.json`, and no current service
applies `opsflow.json` or SQL 001/002. This is a confirmed source gap, not a
license to infer a credential, role, bucket, or grant. P04 and the coordinator
own a named one-shot and the four login-secret references after P02 freezes its
catalog; MNG remains untouched.

`opsflow_dev` must be handed off as a declared schema with five function-only role
contracts and canonical source SQL. An operational one-shot may provision roles,
database, and reviewed `001_opsflow.sql` only. `002_checks.sql` remains an
isolated disposable-DB check: it must never become an operational DEV provision
hook because its rollback does not undo sequence advance. Native DEV checks need
separate bounded queries and denials.

The source declares no `opsflow-dev` bucket and its S3 identities configuration
has no identity/prefix ACL; action-only rendering cannot establish prefix
enforcement. P04/storage must select vendor-supported policy before native
cross-prefix denial; this lane is `NOT_RUN`. Airflow's overlay has readonly
worker/run/opsflow mounts, but source lacks delivered `pg.json`/`s3.json`/CA
mode-and-UID facts and pool creation. P04/P02/P06 own that delivery boundary.

P05's SQL source-reference hashes match the approved P04 reviewed SQL, while
its native binding is deliberately null: source compatibility is `NO_CHANGE`,
not native binding. Its Node SDK source locks OpsflowSmtp transport to Mailpit
port 1025 with empty auth/no TLS; private worker API credential IDs remain
unbound. The P03 worktree has a separate infra-implementer change for a
dedicated internal capture network between worker and Mailpit; it does not
modify the root/base n8n or Mailpit leaves here. Await its RED/GREEN receipt
before any source-resolved claim.

MLflow, SonarQube, and Terrakube native-auth proposals remain optional without a
runtime consumer target. P06 has no exact restore artifact, target, or custody
contract. All endpoints are only declared or unknown; no actual endpoint,
machine identity, native auth, migration, delivery, or recovery result is
claimed. The frozen QA receipt `b80a4…` reports 43 PASS tests in 10.190s and is
source-only; no fake RED or final-gate PASS is recorded. Actor/budget remains
UNKNOWN.

#### Current source receipt — 2026-10-13

The P03 checkout fast-forwarded to
`6de86f9dc36b087cb3a56f0ac7b346c56b58b291`, the then-current remote main.
Its P02 private-staging/SMTP documentation changes do not overlap this unit;
the P03 core source hashes remain unchanged. The reviewed document patch
`237a426…` applies three narrow corrections: GDE-0029's 13-service project
fact, a Supabase-only document-path method with unchanged assertions, and an
explicit root Grafana LAB exclusion. Independent source and rules review
approved that patch with no finding.

The public entrypoints had tracked Git mode `100755` and actual mode `775`; the
owned files were corrected to `755` only. This is a repository-mode correction,
not a runtime chmod or a service change. The focused source suite at `6de86…`
exited 0 with 145 PASS tests in 17.866 seconds: 43 P03 port inventory/contract,
53 Compose profile vocabulary, 10 n8n outbox, the latest P02 secret-catalog
coverage, three mode/root-quality checks, and one registered document method
against a tracked YAML fixture. It is a document-only wrapper and performs no
LAB render. Statement-line coverage remains 152/163 (93.25 percent), limited
to the new executable lines; it is neither module nor branch coverage.

The compiled gate evidence at historical input `62556…` is retained without
relabelling it as current-head acceptance. Candidate preflight, sync, links and
lifecycle passed; links observed 1,272 documents/11,440 links with zero
failures and one existing archive-capture warning. The six-module metadata leaf
timed out (exit 124 after 600 seconds) with no adapter output; the document
library leaf timed out (exit 124 after 900.153 seconds) likewise. Their causes
are not verified. Supply passed 265 tests (117.877 seconds; controller 118.304)
and integrity passed 558 (170.406 seconds; controller 171.011). The old Compose
leaf failed 3/errors 1/skips 71 (137.803 seconds) from two checkout modes and
two document contracts now covered by the focused receipt; the whole leaf was
not rerun because it would render excluded LAB inputs. These facts leave the
full aggregate `NOT_RUN`, not partially PASS. Conftest is `NOT_RUN`: there is
no owned isolated daemon and the runner strips `DOCKER_HOST`.

Four core source/security/contract/IAC reviews are APPROVE. Criterion 17/W33
remains open: source declarations and focused tests do not establish a listener,
network peer denial, SSO/JWT/HMAC/machine-token acceptance, runtime identity,
HOME, migration, rotation or recovery. At this pre-documentation-commit
checkpoint, only the third documentation commit, final-head affected rerun,
final-head hosted CI and merge remain pending. P04/P05/P06 receive only the
source SHA/schema/declaration handoff already stated above; no endpoint,
credential, consumer or restore authority is issued.

Rollback is a reviewed logical revert of the owned source/document increment;
it does not restore runtime state, data, secret material or rotation. The next
owner action is to record and push the documentation commit to Draft PR 432,
rerun final-head affected gates, and capture hosted CI/merge evidence. The live
PR metadata owns later delivery facts; this checkpoint does not complete P03.

Two logical commits are now recorded: test
`98fdf07b83855d67cff5c426f2453cb7d264beaa` and source
`a1323bd2ebe4a1b17e153df51f8d11cec75f7885`. Each was a normal Git commit
after canonical local-staged and pinned Commitizen 4.15.1 PASS, with no hook
bypass. The non-forced upstream push created owning
[Draft PR 432](https://github.com/buenhyden/hy-home.docker/pull/432); its live
metadata is the authoritative hosted receipt location. Candidate run
`38288943924` began on `a132…`; any successful checks there are superseded by
the next documentation head and are not final-head CI, delivery or merge PASS.
The third documentation commit, current-head affected rerun, hosted CI and
merge remain pending.

Rollback for these two commits is a logical revert of their test/source SHAs;
the pending documentation commit needs its own logical revert. Neither action
rolls back live services, data, secrets, rotations, HOME, migration or recovery.

### Gateway rate-limit conformance — 2026-10-20

The v22 prompt (§7.1) asked for per-route rate limiting. POL-0013 required
`req-rate-limit` in `gateway-standard-chain`, but the chain carried only retry
and circuit-breaker; 41 of 43 routers had no limiter (the two Storybook routers
named it directly). The owner approved raising `burst` from 50 to 200.

Read-only basis on the running gateway (Traefik 3.7.14): over 24 h the access
log held 36,693 requests and no 429. The peak per source and router was
Open WebUI at 123 req/s (175 in two seconds, one page load) and
`prometheus-api` at 33 req/s. 23,107 of the requests in 6 h came from
`10.250.1.128`, the `edge_net` gateway: host and k3d clients pass docker-proxy
and share that address, so they share one bucket per router. In the v3.7.14
source (`pkg/middlewares/ratelimiter/rate_limiter.go`) the maximum delay at
100/s is 5 ms, so a request beyond the bucket gets 429 at once, and buckets are
per router and source.

Change: the chain is now `req-rate-limit`, `req-retry`, `req-circuit-breaker`;
`req-rate-limit` is `average: 100`, `period: 1s`, `burst: 200`, keyed on the
TCP peer; the unused `api-rate-limit` is removed. A new contract test parses
the chain, the values and every router; it failed on the old chain (RED) and
passes now. The hardening check also requires the chain member.

Isolated rehearsal with the pinned image and this middleware file (one
container, 256 MiB, 0.5 CPU, label `hy.rehearsal=ratelimit`, removed with its
network afterwards): 150 parallel requests all 200; 400 parallel requests 222
200 and 178 429 in 0.237 s (200 + 23.7 refill); 100 requests with varied
`X-Forwarded-For` right after, 11 200 and 89 429, so the header does not split
the bucket; 20 requests from another container right after, all 200; 150
requests after 2.2 s, all 200.

This Task's Evidence table is a frozen pre-generation-7 table, so these
results stay here: source and RED/GREEN PASS, ISOLATED rehearsal PASS, HOME
NOT_RUN. HOME application follows merge, when the file provider reloads the
dynamic directory. Remaining: the HOME check per router (Open WebUI and Grafana page
loads without 429, one over-limit probe returning 429 and recovering); the
two Storybook routers name the limiter twice, which is redundant but harmless;
`grafana-static` has no middleware and stays outside the limiter, as recorded
in the auth integration guide.

HOME check after PR #520 merged (`main` `dda746b31`, HOME checkout
fast-forwarded at 10:09:15 +09:00). Traefik watches the bound `dynamic/`
directory and reloaded without a restart. During the reload it logged 33
`middleware ... does not exist` errors in the same second, while the files
were being replaced, and none afterwards; `gateway-standard-chain` then held
`req-rate-limit`. Results from the host through `192.168.0.13:443`:

| Probe | Result |
| --- | --- |
| `chat` (Open WebUI), 150 parallel requests | 150 × 200 |
| `mailpit-ui`, 400 parallel requests | 349 × 302 (SSO redirect), 51 × 429 |
| `mailpit-ui` 2.5 s later, 150 requests | 150 × 302 |
| `chat` afterwards, 20 requests | 20 × 200 |

More requests passed than in the isolated rehearsal (222 of 400) because TLS
handshakes spread the arrivals over about a second, during which the bucket
refilled. The over-limit probe used `mailpit-ui`, a low-traffic router,
because host and LAN clients share one bucket per router through
docker-proxy. HOME rate-limit status: PASS.

#### Per-route limiter and Hermes direct port — 2026-10-21

Source inventory at `main` `5b9ee9e74`, from `RouteAuthContractTests.routers()`
(Compose labels plus `traefik/dynamic/*.yml`): 48 HTTP routers, no TCP router.
Every router except one reaches `req-rate-limit` through
`gateway-standard-chain@file`; the limiter is shared, so each router and TCP peer
gets its own 100/s, burst 200 bucket.

| Limiter | Authentication | Routers |
| --- | --- | --- |
| standard chain | `sso-auth` | alertmanager, alloy, cadvisor, comfyui, flower, jupyter, kafka-connect, kafka-rest, loki, mailpit-ui, mlflow, n8n, ollama, prometheus, pushgateway, pyroscope, qdrant, redisinsight, redisinsight-static, schema-registry, sonarqube, stalwart-ui, tempo, terrakube-api, terrakube-executor, terrakube-ui |
| standard chain plus a direct `req-rate-limit` (redundant, same bucket) | `sso-auth` / OAuth bearer | storybook, storybook-mcp |
| standard chain | native OIDC | airflow, dozzle, gatus, grafana, hermes-dashboard, kafka-ui, open-webui, openbao, superset |
| standard chain | other named exception | dashboard, prometheus-api (gateway basic auth); keycloak, oauth2-proxy (identity provider); neo4j (app credentials); open-notebook (app password and IP allowlist); opensearch, opensearch-dashboards (security plugin); s3 (SigV4) |
| none | static only | grafana-static (favicon and `robots.txt`) |

`grafana-static` stays outside the limiter as recorded in the auth integration
guide; the existing contract test allows a bare chain only for `static-only`.

Hermes: the route (`hermes.yml`, tracked by PR #535) uses the standard chain
and is listed as native OIDC. The backend, however, runs as
`hermes dashboard --port 9119 --host 0.0.0.0` (host systemd unit
`hyhome-hermes-dashboard.service`, outside this repository). `ss -ltn` shows
`0.0.0.0:9119`, and a plain HTTP request to `192.168.0.13:9119` returns 302
(the application's own OIDC redirect). A LAN client can therefore reach the
dashboard without Traefik TLS and without the limiter. The application still
demands its own login, so this is a bypass of gateway controls, not of
authentication. Proposal for the owner, not applied: bind with
`--host 10.250.1.128` (the `edge_net` gateway Traefik uses) and order the unit
after Docker, then add a HOME probe that expects `192.168.0.13:9119` to refuse
the connection and `hermes.hy.home.arpa` through `192.168.0.13:443` to return
302. Source PASS; Hermes direct-port status: open finding, owner decision.

The owner changed the unit the same day (active since 15:24:49 +09:00):
`ExecStart` now binds `--host 10.250.1.128`. HOME probe afterwards: `ss -ltn`
shows only `10.250.1.128:9119`; `192.168.0.13:9119` and `127.0.0.1:9119` refuse
the connection; `10.250.1.128:9119` and `hermes.hy.home.arpa` through
`192.168.0.13:443` both return 302. The unit keeps `After=network.target` with
`Restart=always` and `RestartSec=3`, so after a reboot it retries until Docker
creates the `edge_net` bridge; `After=docker.service` would only shorten that.
Hermes direct-port status: PASS (HOME).

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Git baseline | 1, 17 | W33 | status/log/worktrees, ls-remote and open PR list | Local 6da5e3bf3; remote 2b9f5ec82 | PASS | Assessment above; exit 0, baseline only | - |
| Existing source contracts | 1, 4, 8, 17 | W33 | Inventory, wiring, compatibility, version and SMTP unit modules | Clean 6da5e3bf3 | PASS | Exact command below; 84 tests, 8.084s, exit 0, existing source only | - |
| P03 implementation | 17 | W33 | New schema/parser/fixtures and RED/GREEN | Final artifact aggregate above | PASS | Source/synthetic slice only; whole criterion remains open | - |
| Common source registration | 17 | W33 | Manifest/workflow and navigation reconciliation | 08b009a9c plus preserved P03 commits | PASS | c3fce85d2; two scripts, two modules and both routing tables; local source only | - |
| Coordinator dedicated tests | 17 | W33 | Two unchanged P03 unit/contract modules | 4cadd4d7e plus exact seven common staged files | PASS | 42 tests, 3.679s, exit 0; synthetic/config only | - |
| Coordinator affected gates | 17 | W33 | Twelve registered affected leaves | Twenty public input hashes and canonical plan digests above | PASS | Each exit 0; repository-integrity 407 tests; no new full aggregate or hosted CI | - |
| Initial private/runtime lanes | 4, 6, 17 | W33 | ISOLATED/HOME/MIGRATION/ROTATION/RECOVERY | No exact selected action | NOT_RUN | Owning follow-up needed; no operational acceptance | - |
| Delivery | 8, 17 | W33 | Latest-head CI/review/PR/merge | No P03 PR | NOT_RUN | Future PR; no remote delivery claim | - |
| Root four-location matrix | 17 | W33 | `project_root` and inventory membership audit | 62556dc63; 44 inputs, 43 leaves, 111 services | PASS | Work Log 2026-10-13; source mapping only | - |
| DEV/MNG and P04/P05 source boundary | 17 | W33 | Six-module source/synthetic unittest suite | 62556dc63 | PASS | 55 tests, 5.340s, exit 0; no daemon/private input | - |
| Root negative source contracts | 17 | W33 | Selected Compose baseline/network/auth/Alloy unittest suite | 62556dc63 | PASS | 27 tests, 23.015s, exit 0; native lanes NOT_RUN | - |
| Current focused source suite | 17 | W33 | Port/profile/n8n/catalog/mode/root-quality/document-method suite | 6de86f9d | PASS | 145 PASS, 17.866s, exit 0; tracked fixture only, no LAB render | - |
| Historical registered metadata and document leaves | 17 | W33 | Compiled local gate leaves | 62556dc63 | FAIL | Metadata exit 124/600s and document library exit 124/900.153s; no adapter output, cause unverified | - |
| Historical registered supply and integrity leaves | 17 | W33 | Compiled local gate leaves | 62556dc63 | PASS | Supply 265 PASS; integrity 558 PASS; historical input only | Historical registered metadata and document leaves |
| Full aggregate and Conftest daemon | 17 | W33 | Aggregate/local controller and isolated daemon leaf | No current complete aggregate or owned daemon | NOT_RUN | Compose whole leaf was not rerun because it would render excluded LAB inputs; no `DOCKER_HOST` daemon route | - |

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

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision |
| --- | --- | --- | --- |
| 17 | pending | - | - |

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
- [Traefik guide](../../../05.operations/guides/02-gateway-and-networking/0013-traefik.md)
- [Service onboarding](../../../05.operations/guides/10-platform-and-backup/0008-new-service-onboarding.md)
