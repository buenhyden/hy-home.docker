---
title: "Infrastructure Audit Execution Task"
version: "0.1.3"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-26"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0008"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-16"
---

# Infrastructure Audit Execution Task

## Overview

### Objective

Execute `INFRA-P0` only: establish a current, value-free source snapshot and
single-owner routing for infrastructure requirements 11–32 before P1 or any
variable source change. This Task owns SPEC-0212 criterion 19. It does not
reopen historical Task bodies or r10 criteria 11–18, and it does not accept
leaf implementation, native, HOME, recovery, hosted delivery, or remote
protection results.

## Inputs and Authorization

The direct user supplied an independent infrastructure-audit prompt identified
by SHA-256 `ea9ddbdd8db5ea93b2e8858c477d223e2ea877cdccd99c7c1e86a22303cc4935`.
It authorizes source, tests, documentation, logical commits, a SPEC-0212
feature branch, and delivery after gates. It excludes remote-protection
changes, secret values and credential mutation, live destructive actions,
rotation, migration, deployment, and recovery until the owning operation
records concrete prerequisites. Value-free secret metadata checks remain in
scope.

The coordinator created `feature/spec-0212-infra-audit` from clean main
`e6807a7d16d8b9e180ff58456ab64e4ee721ca69` after `git fetch origin main`.
At that baseline, open pull requests were empty and no extra worktree or
unpublished commit was observed. The earlier r10 criteria 11–18 use another
namespace and do not prove infrastructure requirements 11–18.

At approximately 2026-10-16 00:49 KST, the tracked/index frontmatter census
at this base plus this staged Task found 36 Specs (13 approved, 23 draft), 36
Plans (13 approved, 23 draft), and 65 Tasks (16 completed, 3 blocked, 11
in-progress, 34 draft, and this Task in-progress). The approved package IDs
are `0182`, `0204`, `0207`–`0212`, `0230`–`0233`, and `0242`; every other
current package Spec is draft. This is a lifecycle/source inventory, not an
acceptance-PASS claim: each draft or nonterminal record retains its own
criteria, evidence, merge, and operation disposition under its primary owner.

## Work Log

### P0 execution state

W24 source preparation is active while this newly issued Task remains `draft`
under the lifecycle contract. Its scope is source inventory, owner routing,
shared leases, evidence ladder, QA/CI mapping, and P1–P9 handoff. Final P0
source findings and independent review remain pending; they do not block
unrelated, reversible owner source/test/document work. P1 blocks only live or
irreversible operations until its named prerequisites are met.

### Current P0 source snapshot

The bounded current-service inventory projection records 43 root Compose
includes, 13 infrastructure layers, and 111 services. Its service rows are
source inventory evidence, not native runtime proof: 83 consumer cells and 81
backup cells are explicitly unverified or `NOT_RUN`. Current source inventory
also records 84 secret declarations, 19 networks, 65 profiles, 71 image
strings, 30 build consumers, and 21 distinct build objects. No P0 operation
prints secret values, rendered private environment, or authentication headers.

The direct request replaces the historical "security warning only" update
restriction. Every ROOT image proceeds through official latest-stable,
OCI-identity, compatibility, migration, rollback, and consumer assessment.
For example, the current official n8n lookup is 2.43.6, published
2026-10-15T07:26:03Z, non-prerelease; it is a P2 candidate, not an update or
runtime-success claim. A real compatibility barrier must name its mitigation,
review date, exit condition, and rollback boundary.

P0 also preserves two current implementation blockers for their existing
owners: the n8n 2.42.7 bundle and related custom-node package/lock remain a
coupled P2 source change, and the P04/P05 outbox currently omits its SQL
`lease_until` contract while uncertain post-send outcomes can be retried. P04
owns the versioned SQL/manual-reconciliation correction and P05 owns its
consumer contract; neither is accepted here.

### Requirement routes and shared leases

| Requirements | Primary owner | P0 route | Next boundary |
| --- | --- | --- | --- |
| 11 | SPEC-0218 / P07 | Consumer-backed root-leaf acceptance; P0 supplies bounded inventory | Existing leaf acceptance. |
| 12 | SPEC-0204 / P03 | Integration caller, contract, and verification route | P1 review, then named source/native Task. |
| 13 | SPEC-0204 / P02 | Compose, secret, config, and consumer route | P1 review, then named source/native Task. |
| 14 | SPEC-0204 / P03 | Endpoint, ACL, S3, OIDC, resource, health, and upgrade prerequisites | P1 review, then named source/native Task. |
| 15 | SPEC-0204 / P10 | Input-to-recovery vertical acceptance | Native/HOME/recovery remains pending. |
| 16 | SPEC-0204 / P04 | Airflow DEV database/S3/DAG | Existing source/native Task. |
| 17 | SPEC-0204 / P05 | n8n outbox/SMTP | Existing source/native Task. |
| 18 | SPEC-0218 / P07 | Resource and permission controls | Measured demand required. |
| 19 | SPEC-0218 / P07 | Common controls and exceptions | Measured demand required. |
| 20 | SPEC-0227 | Template authority; P08 supports layout paths | LAB runtime excluded. |
| 21 | SPEC-0212 / P0 | Lifecycle inventory | Package owners retain residual closure. |
| 22 | SPEC-0204 / P01 | OpenBao classification | P02/P06 support mapping and consumption. |
| 23 | SPEC-0204 / P03 | Listener, DNS, host, backend, and route ports | Existing contract owner. |
| 24 | SPEC-0212 / P0 | Active-contract and validation routing | Package owners retain residual closure. |
| 25 | SPEC-0204 / P08 | Operations-document layout and links | SPEC-0227 supports templates. |
| 26 | SPEC-0212 / P0 | Learning application exclusion | No app plan/code/data/resources. |
| 27 | SEC01 | Latest-stable and OCI/compatibility assessment | Image owner changes only after prerequisites. |
| 28 | SPEC-0204 / P09 criterion 13 / TSK-0008 | Offline Wiki preparation only | Wiki implementation and external workspace remain out of scope. |
| 29 | SMTP01 | Canonical source plus actual-consumer verification | Separate authorized retirement assessment. |
| 30 | CLN01 | Consumer, backup, external-dependency, authorization, recovery evidence | No deletion from profile-off or no-traffic observation. |
| 31 | SPEC-0204 / SEC01 (TSK-0009) | Same-unit Guide, Policy, Runbook, README, template, test, and configuration route | P08 checks structure; runs with each actual image change. Rerouted from P09 by the owner on 2026-10-21. |

### Requirement source, gate, and blocker trace

| Requirement | Current source / Task | Validator or gate | P0 state and blocker |
| --- | --- | --- | --- |
| 11 | `m0021` / SPEC-0218 P07 | Operations catalog and leaf contracts | SOURCE_APPLIED; consumer acceptance remains owner work. |
| 12 | SPEC-0204 P03 | Service-wiring and port contracts | NOT_RUN; named integration target required. |
| 13 | SPEC-0204 P02 | Secret catalog and Compose contracts | FAIL; catalog view drift is unresolved. |
| 14 | SPEC-0204 P03 | Endpoint/ACL/health contracts | NOT_RUN; target prerequisites pending. |
| 15 | SPEC-0204 P10 | Opsflow E2E acceptance | FAIL; lease/unknown-message correction pending. |
| 16 | SPEC-0204 P04 | Airflow contract/rehearsal tests | SOURCE_APPLIED; native target remains pending. |
| 17 | SPEC-0204 P05 | n8n outbox/rehearsal tests | FAIL; P04/P05 coupled lease handoff pending. |
| 18 | SPEC-0218 P07 | Root-resource contract | NOT_RUN; measured demand absent. |
| 19 | SPEC-0218 P07 | Common-control contract | NOT_RUN; measured demand absent. |
| 20 | SPEC-0227 | Metadata, catalog, and link checks | STATIC_PASS; no eligible move is leased. |
| 21 | Current Spec inventory | Metadata/lifecycle parser | SOURCE_APPLIED; package closures remain owner work. |
| 22 | SPEC-0204 P01 | OpenBao consumer-migration contract | NOT_RUN; secret/restore boundary absent. |
| 23 | SPEC-0204 P03 | `test_port_contract.py` | SOURCE_APPLIED; runtime listener proof pending. |
| 24 | SPEC-0212 P0 | Document/CI route checks | FAIL; CI routed regressions remain open. |
| 25 | SPEC-0204 P08 | Operations catalog, metadata, links | STATIC_PASS; document path freeze required. |
| 26 | SPEC-0212 P0 | Scope and changed-path review | SOURCE_APPLIED; no learning-app work admitted. |
| 27 | SEC01 | Version/security/OCI contracts | NOT_RUN; official lookup and compatibility ledger pending. |
| 28 | SPEC-0204 P09 TSK-0008 | Offline preparation contract | SOURCE_APPLIED; implementation excluded. |
| 29 | SMTP01 | SMTP contract/rehearsal | NOT_RUN; consumer verification pending. |
| 30 | CLN01 | Consumer/backup/retirement contract | NOT_RUN; consumer and recovery evidence absent. |
| 31 | SPEC-0204 SEC01 (TSK-0009) | Changed-image documentation and CI route | PARTIAL; image changes were accepted from 2026-10-20 (SPEC-0204 TSK-0009), and each PR updated its Guide, Policy or Runbook with the change. The owner moved the route from P09 (limited to Wiki preparation) to the SEC01 image owner on 2026-10-21. |

`docker-compose.yml`, `.env.example`, catalogs/exceptions, Stage 99 Registry,
Stage 05 indexes, shared scripts, and CI contracts require one named writer.
The coordinator (`/root/coordination_docs`) owns only this Spec, Plan, and Task
on `feature/spec-0212-infra-audit`. Read-only P0 contributors are
`/root/inventory_analysis`, `/root/ci_audit`, and `/root/workflow_analysis`;
they hold no write lease. No task-level token, time, or rate limit is known;
no ceiling is invented or used to release a lease.

### Evidence domains, stop, and recovery boundaries

The evidence ladder is `SOURCE_APPLIED`, `STATIC_PASS`, `ISOLATED_PASS`,
`NATIVE_PASS`, `HOME_PASS`, `RECOVERY_PASS`, `BLOCKED`, `OUT_OF_SCOPE`,
`SUPERSEDED`, and `NOT_RUN`. A lower stage never closes a higher stage. P0
stops the dependent operation when its resource, operator/window, backup
identity, restore boundary, compatibility result, or action-specific approval
is missing. Secret rotation, data migration, retirement, and live upgrades
require their owner’s rollback plan; an isolated documentation rollback does
not restore runtime data.

### v30 current input and survey — 2026-10-26

The current direct user request supersedes earlier delivery authority for this
execution: local source, tests, documents, logical commits and per-Spec review
drafts are authorized; remote writes and operational actions require their
separate exact authorization. Attachment SHA-256 is
`709ab7e2edd94adc2cb9e2c382b0b3935a8f5ce065088ce4d06473a8a7361aec`.
The existing `_workspace/hy_home_v30_local_prompts/` primary Docker prompt has
SHA-256 `a6375ee93f87fefdc14f3b108120d82adb7abbcf7769c899b91d9c7019d6b460`;
its normalized text equals the attachment, whose byte representation uses
different line endings. Initial local HEAD and read-only remote main both
equal `136b7cac4483d4af8aaa73ca6dc3f9a0da521e10`. This is the input identity,
not a claim that subsequent uncommitted source edits are that revision.

The supplied bundle is reused in place. Its INDEX and manifest enumerate 98
existing dependency members: all 96 ordinary SHA-256 entries match; the two
self/contract entries deliberately have null hashes to avoid a dependency
cycle. The primary hash matches traceability. The original matrix has 22
requirements, 68 subconditions and ten unnumbered constraints; traceability
retains 65 historical aliases. The current crosswalk contains exactly one of
each F01–F29, with no missing or duplicate F identifier. These are structural
and provenance checks, not proof of every condition's implementation.

The manifest's 18 unavailable historical references remain identified with
their original limits. The local learning-app inputs, unavailable to the
package author, are available here: the two existing files under
`_workspace/learning-app-prompts/` are 4119/4041 bytes and respectively hash to
`e585922622a049bf31b6224d581c89040296f885956303841d3a7464ee09024a` and
`32712c13aa33d47fb1656907cc6952cd6deb48d6768b02ce2b154ebff1f67cf3`.
Both match TSK-0006's recorded inputs and satisfy the bounded planning-prompt
fields; they are reused, not executed research or accepted products.
`_workspace/v22-drafts/` remains absent. No missing historical body is invented.

The current survey classifies 2325 tracked paths (including infra492,
scripts110, tests202, governance37, GitHub15 and Stage03 155) and the relevant
consumer/configuration/verification paths. Its ROOT population is 43 includes,
111 declared services and 12 standalone exporters. These populations are not
running services or a claim that all 2325 files received full semantic review.
The required current Task scope/metadata/acceptance survey covers SPEC-0204
TSK-0009–0020; SPEC-0212 TSK-0006–0010; SPEC-0211 TSK-0003; both SPEC-0218
Tasks; and the related SPEC-0227/0243/0244/0245/0246 Tasks. Domain surveys
corroborate the relevant implementation and latest Work Log evidence.

Completed SPEC-0212 TSK-0006/0009/0010, SPEC-0218 TSK-0001, SPEC-0227 and
SPEC-0243 retain their bounded acceptance and unchanged bodies. SPEC-0244 C3
and SPEC-0246 C1–4 remain accepted; SPEC-0246 C5–6, QA04, P04/P05/P10/P06,
exact B1, A1/A3/B4/D1 and current Native/HOME/recovery retain their owners.
W74 in-progress and later bounded successes supersede its old blanket block;
W75 remains blocked at its exact recovery evidence boundary. The historical
FAILs below remain unchanged and are not newly rerun or resolved by this survey.

### v30 four-axis requirement routing

In the following tables, retained prompt coverage means the current instruction
contains the condition. Source reuse refers to the cited current owner and
bounded prior evidence. Verification is the actual surveyed scope; acceptance
is never inferred from a source, document or package-test PASS. The existing
bundle requirements matrix supplies the 68 subcondition definitions and ten
unnumbered constraints; its crosswalk supplies exact source paths for each F
row. These remain inputs rather than a duplicate execution ledger.

| Requirement | Single primary owner | Prompt | Current source action | Verification boundary | Acceptance or residual |
| --- | --- | --- | --- | --- | --- |
| R11 | SPEC-0218 P07; inventory coordination here | retained | Reuse inventory; U2 selection closure applied | Profile/dependency source tests PASS | Real consumers/workload pending |
| R12 | SPEC-0204 P03 TSK-0011 | retained | U2/U3 source applied | Synthetic public config/closure PASS | Actual authenticated callers pending |
| R13 | SPEC-0204 P02 TSK-0010 | retained | U1 public mapping applied | Source tests and isolated ACL PASS | Private delivery/restore pending |
| R14 | SPEC-0204 P03 TSK-0011 | retained | U2/U3 source applied | Positive/negative source contracts PASS | Native readiness pending |
| R15 | SPEC-0204 P10 TSK-0016 | retained | Reuse vertical-flow source | Prior bounded evidence | End-to-end recovery pending |
| R16 | SPEC-0204 P04 TSK-0012 | retained | Reuse DAG/SQL/S3 and W75 source | W75 evidence boundary retained | P04/empty recovery pending |
| R17 | SPEC-0204 P05 TSK-0013 | retained | Reuse W74; U1/U3 source applied | Isolated Valkey ACL only; Node/Bull4 flow NOT_RUN | P05/HOME/SMTP separate |
| R18 | SPEC-0218 P07 TSK-0002 | retained | Reuse resource evaluator | No new workload measurement | Measured acceptance pending |
| R19 | SPEC-0218 P07 TSK-0002 | retained | Reuse completed common controls | Registered exceptions only | Unregistered controls/cadence pending |
| R20 | SPEC-0227; changed-document owner | retained | Reuse completed format contract | Changed-document checks required | Existing acceptance preserved |
| R21 | SPEC-0212 C19/W24 here | retained | Current Task/source routing | Current package/Task survey | Completed C9/C10 preserved |
| R22 | SPEC-0204 P01; P06 consumption | retained | Reuse HOME restore/Agent source | Current Native/HOME not run here | A1/A3/B1/B4/D1/P06 separate |
| R23 | SPEC-0204 P03 TSK-0011 | retained | Reuse four-location port contract | Declarations, not live listeners | Runtime denial checks pending |
| R24 | SPEC-0212 C19/W24; interface owners | retained | Reconcile exact current gaps | Owner/consumer/check routes | Leaf criteria stay with owners |
| R25 | SPEC-0204 P08 TSK-0015 | retained | Reuse existing moves/READMEs | Current path/format scope | No new move or LAB runtime |
| R26 | SPEC-0212 exclusion; external planning | retained | Reuse existing two instructions | Bodies and matching hashes read | Research/product acceptance separate |
| R27 | SPEC-0204 SEC01 TSK-0009 | retained | Reuse image ledger and owners | Exact-image security incomplete | Native/security/recovery pending |
| R28 | SPEC-0204 P09 TSK-0008 | retained | Reuse completed preparation | Bounded preparation evidence | Wiki product excluded |
| R29 | SMTP01 TSK-0005 | retained | Reuse canonical SMTP/alias | No real send or retirement | CLN01 eligibility/P06 separate |
| R30 | CLN01 TSK-0007 | retained | Reuse five-axis assessment | Private disposition not observed | Exact consumer/recovery facts required |
| R31 | SEC01 image owner; P08 structure | retained | Reuse approved routing | Each changed-image unit owns checks | No P09 reopening |
| R32 | SPEC-0246 TSK-0001 | retained | Reuse moves/GC/Ollama/W7 guards | Existing C1–4 and move evidence | C6/HDD disposition then W6/C5 |

### v30 F01–F29 execution crosswalk

The F namespace records the 2026-10-26 audit, independently of original R
identifiers and historical aliases. Multiple findings attached to U1/U2/U3
remain one implementation per defect. "Pending unit checks" is NOT_RUN for
the new input; no prior receipt or reviewer name grants new acceptance.

| Finding | Existing primary execution owner | Prompt | Current source disposition | Verification | Acceptance |
| --- | --- | --- | --- | --- | --- |
| F01 | COORD C19/W24 | retained | Reuse PR560 completion | Current Task state read | Leaf runtime separate |
| F02 | Existing v30 package author | retained | Reuse current INDEX | Manifest/hash scope checked | Document scope only |
| F03 | COORD C19/W24 | retained | Reuse supplied audit dependencies | 98 members present | No runtime claim |
| F04 | COORD C19/W24 | retained | Reuse original matrix | 22/68/10/65 structure | Semantic limits retained |
| F05 | COORD C19/W24 | retained | Preserve repository/product boundaries | Exact request read | Local scope only |
| F06 | P03; P07 inventory support | retained | U2 selection closure applied | Profile/direct-target closure tests PASS | Native pending |
| F07 | P03; individual service owners | retained | Reuse isolated ingress boundaries | Source peer classification | Live denial pending |
| F08 | P05; P03 network support | retained | U3 optional Worker/Ollama overlay applied | Synthetic merged config PASS | Actual Node/Credential/model/peer NOT_RUN |
| F09 | P05 and AI/security owner | retained | Preserve local no-cloud policy | No Cloud key/API use | BLOCKED_CLOUD_APPROVAL |
| F10 | P04 and AI owner | retained | Connections/SDK applicability review | Actual worker call NOT_RUN | Exact consumer pending |
| F11 | Existing product owners | retained | Reuse native candidate matrix | 72 candidates are possibilities | Actual configured calls pending |
| F12 | AI/RAG owner | retained | Reuse WebUI source; assess actual use | No reindex/data access | Consumer acceptance pending |
| F13 | AI/Notebook owner | retained | Reuse local Notebook/Ollama declarations | No new model/restore execution | Actual integration pending |
| F14 | AI owner; P03/SEC01 support | retained | Preserve local GPU/security limits | No hardware measurement | Workload acceptance pending |
| F15 | Observability owner; P07 support | retained | U2 Producer/exporter closure applied | Profile/provisioner/direct-target tests PASS | Prometheus/Grafana/HOME NOT_RUN |
| F16 | P03/Auth/Observability owner | retained | NO_CHANGE: oauth2 obs network already correct | Existing source assertion verified | Runtime pending |
| F17 | Observability owner; QA support | retained | Reuse jobs/dashboards | Up/internal health/query separate | Native query pending |
| F18 | Observability owner | retained | U2 expected optional-target states applied | Source profile expectation tests PASS | Actual scrape NOT_RUN |
| F19 | Messaging/Observability owner | retained | Reuse JMX/n8n native metrics | Source duplicate check | No new exporter |
| F20 | P04/P05; P07 resource support | retained | U1 optional named-user source applied | No queue or deployment change | Runtime topology decision pending |
| F21 | P02/P05; Valkey owner | retained | U1 named-user ACL applied | Isolated exact-image ACL attempt2 PASS | Bull4/AOF/HOME/P06 NOT_RUN |
| F22 | P02/P05; Valkey owner | retained | U1 root/Catalog/client mapping applied | Source parity/fail-closed tests PASS | No real credential mint/copy |
| F23 | Observability/Valkey owner | retained | Reuse monitor identity; assess dedicated ACL | Profile and permission proof separate | Native pending |
| F24 | P02; P08 support | retained | KEEP both SENSITIVE documents | Active Writer/Reader source | No private content read |
| F25 | CLN01; P02/P06 support | retained | Preserve unknown private assets | No deletion eligibility inferred | BLOCKED_FACTS |
| F26 | P02; P03/P05 consumers | retained | U1 public key contract applied | Public source checks PASS; private parity NOT_RUN | Existing values preserved |
| F27 | P02 | retained | Reuse single Catalog authority | Current public contract | Real consumption separate |
| F28 | COORD; QA/P04/P05 owners | retained | Reuse completed document Tasks | Current acceptance boundaries read | Native/HOME separate |
| F29 | P02/P05 | retained | U1 applied in existing TSK-0010 | No duplicate Task/ledger | C16/C17 remain pending |

### v30 bounded source readiness and writer leases

The accessible source survey and owner reconciliation admit the following
bounded reversible source units once their exact independent prechange review
is satisfied. This is source readiness, not global implementation completion,
criterion acceptance, a runtime GO or permission for private/remote changes.
Missing historical references and operational evidence do not block these
independent local fixes. Broader all-source semantic and operational acceptance
remains incomplete; no full-census PASS is inferred from path counts.

| Unit | Exact intended change | Primary owner and current writer | Admission and stop boundary |
| --- | --- | --- | --- |
| U1 | Optional typed shared-Valkey n8n named-user ACL, public Secret/Catalog/client/env mapping; retain baseline default account and DB0, with no existing queue migration | P02/P05/Valkey; service_survey | Independent prechange review; no credential value, live ACL apply, queue drain or topology switch |
| U2 | Producer/exporter profile pairing, required provisioners, exact direct-target dependency closures and verification of the existing oauth2 exporter observability network | P03/P07/Observability; service_survey | Exact final Compose models and negative tests; preserve Kafka JMX and n8n native metrics, never start the stack |
| U3 | Typed root network overlay joining only n8n Worker and Ollama | P05/P03; service_survey | Reviewed minimum peer set and denial contract; no broad ai/management bridge, app credential creation or Cloud fallback |
| Quality cancellation | Preserve interrupted path-guard outcome/artifacts and original exception when cleanup also fails | SPEC-0214 C10/W11; quality_survey | Separate RED/GREEN and independent review; completed criterion7 remains unchanged |

The quality survey reproduced that KeyboardInterrupt bypasses
`except Exception` in the path-guard acceptance runner, leaving `error=null`
and deleting raw attempt artifacts; a subsequent cleanup Timeout can mask the
original interruption. This is a reported current reproduction, not a new
whole-Quality failure or this coordinator's independently executed test. Its
owning continuation records the actual regression command/input/result.

Current leases supersede historical writer names above: this doc-writer owns
only this package's Spec, Plan and TSK-0008. `service_survey` owns the reviewed
U1/U2/U3 infra source chain and its exact assigned tests/documents. Root Compose
and public environment ownership is released only to that writer after the
required prechange review; no concurrent root/env writer exists. Its operating
documentation scope is POL-0078, the MNG/n8n READMEs and GDE/RUN-0053.
The infra source lease is `docker-compose.yml`, `.env.example`, the MNG/DEV,
Kafka and n8n Compose files, MNG `valkey/scripts/render-acl.sh`, MNG
`docker-compose.n8n-acl.yml`, n8n `docker-compose.ollama-local.yml`, n8n
`docker-entrypoint.sh` and `docker-entrypoint.dev.sh`, the canonical OpenBao
`secret-catalog.json` and its generated public
`secrets/SENSITIVE_ENV_VARS.md.example`. Its existing regression modules are
`test_mng_valkey_acl.py`, `test_service_runtime_compatibility.py`,
`test_service_wiring_contracts.py` and `test_secret_catalog_contract.py` under
`tests/validation/`; no completed Task is in that source lease.
`quality_survey` owns its acceptance runner, cancellation regressions and
SPEC-0214 continuation. The root supervisor remains read-only supervision;
independent reviewers do not edit implementation. Other writers' changes are
preserved. Session/task budget and time ceilings are UNKNOWN, maximum one
narrower retry; no invented limit releases a lease.

The five standalone files already present in the v30 bundle provide the
generic repository, Docker, Template-readiness and two app-planning prompts.
Reuse their bodies and dependency manifest rather than generate a second set.
Their document helper remains optional packaging QA, not a new repository CI
prerequisite. The parent executed it read-only: 281 checks PASS (140 clauses)
and 274 regressions PASS, zero skipped, 35.121 seconds. Validator SHA-256 is
`5cd29edc355bccf906e2b43714577c78744c79c598a9ca4a68ba23853b69b6cc`;
regression source SHA-256 is
`2233b4e1e9fca90084ebe3a3fe2c7a4f97cb2a3ff75c50099e1c0412439133cc`.
This is the parent-reported current document result, separate from repository
source tests, independent review, Docker config, Native/HOME and acceptance.
This Task remains draft and criterion19 pending until its current required
evidence and independent review support a registered lifecycle decision.

### v30 coordinator document checks

`rtk git diff --check` passed on the current worktree. A Python standard-library
assertion verified exactly 22 unique R rows and 29 unique F rows in this Task,
with the draft status preserved. The existing `build_document_graph`,
`check_alignment` and `check_traceability` APIs were used for scoped links.
An initial three-document graph omitted the traceability check's required
global navigation/policy inputs and returned three file-missing findings;
this was a diagnostic input error, not missing files in the repository. The
one narrower retry added only `docs/03.specs/README.md`,
`docs/05.operations/README.md` and POL-0006 to the same three owned documents:
six inputs, zero findings, exit0. No source, archive or checker was changed to
satisfy that diagnostic. Final metadata and independent review remain separate.
The changed-metadata invocation against explicit base136b7cac selected the
three owned documents and exited0 with zero violations, legacy exceptions or
transition overrides. It began on the prepared draft before the final
lease/result-only additions; the delivery owner must bind its final registered
checks and independent review to the integrated source rather than reuse that
prepared-input result as final delivery acceptance.

### v30 implemented source and bounded verification

The subsequent source/test/document changes use the existing SPEC-0204
TSK-0010 criterion16 (P02/U1) and TSK-0011 criterion17 (P03/U2/U3), both
in-progress with acceptance pending. No new infra Task or duplicate acceptance
owner was created. The reported 17-source/test manifest SHA-256 is
`96d77614cceabadaa7543fd787b71595edae3f0bed7e284865dbf51224e0ec15`;
the final isolated ACL regression module is
`85fa2a8b715c3156e48128c9766796e08fd34854ac47076b32ed2033a6174830`.
These describe their frozen inputs, not every later document or commit.

| Separate execution | Actual reported result | Limits and current owner |
| --- | --- | --- |
| U1/U2/U3 selected source suites | 34 tests:33 PASS,1 Native opt-in SKIP | No Native result is inferred from the skipped case; P02/P03 source contracts only |
| Full service runtime-compatibility unit module | 28 tests PASS | Separate invocation, not part of the34-test process |
| Valkey ACL Native attempt1 | FAIL after reaching ACL assertions: cleanup expected uppercase NoSuch while the client returned lowercase; the owned container was removed | Retain this failure; the correction changes only cleanup-case matching, not ACL authority |
| Valkey ACL Native attempt2 | 1 test PASS, exit0,20.822seconds after the narrow case correction | Exact isolated Valkey ACL proof only; no actual Bull4 n8n workflow, AOF recovery, HOME or P06 acceptance |
| U2 profile/provisioner/direct-target closures | Source dependency/selection contracts PASS; oauth2 exporter obs network already correct and NO_CHANGE | Actual Prometheus target/internal health/Grafana query/HOME NOT_RUN |
| U3 optional Worker/Ollama root overlay | Public synthetic merged Compose config PASS | Actual Native Node/Credential/model call, peer denial and HOME NOT_RUN; Cloud BLOCKED_CLOUD_APPROVAL |
| Infra helper | 11 PASS,0 FAIL,4 BLOCKED for external absolute-path static-graph inputs; separate public synthetic render PASS | This partial helper result is not an all-environment configuration PASS |
| Quality interruption correction | 31 tests PASS,0 skipped; independent code review reported no actionable findings | SPEC-0214 current C10/W11 continuation; completed criterion7 remains unchanged |
| Quality changed-line trace | Parent measured all7 changed executable lines hit (100percent changed-line coverage) | Neither branch, file, repository nor real Docker execution coverage |

Native attempt2 used context `default` and exact existing Valkey9.1.2 image
`sha256:a0dbf4c1d5708782907c10e2c72deff317518518b5288a58416981d9db95d30b`.
The isolated fixture had networknone, no published ports, read-only bounded
resources, tmpfs and temporary synthetic ACL material. It verified DB0 and
authorized namespace/channel/Lua access, other-DB/key/admin/scan/Lua denials,
wrong-password denial, identity-owned cleanup and final container absence.
The successful fixture did not retain its random container name; that identity
is unavailable and is not reconstructed. Neither attempt used real service
credentials or changed the baseline shared default account, DB0 or live queue.
The owning P02 Task preserves both runs and their exact scope.

Independent infra review reported READY for the frozen source; Quality review
reported no actionable findings. These are review observations and do not
accept existing C16/C17 or the named functional/runtime criteria. The parent
prepared `/tmp/hyhome-v30-python-el330y6x/venv/bin/python`: Python3.14.8,
SHA-256 `62e177f6f9523e24ae0591438b7556e14c58fea1219a5c449615e3ff9d2e12ed`,
all36 exact controller-lock packages, real memfd seals15, and the actual local
toolchain mismatch checker returned None. This temporary official build reuses
the recorded runtime identity without user-global or repository tool changes.
The final registered public changed gate is NOT_RUN pending execution after
the logical commits. No remote CI, PR, merge, deployment or final operational
acceptance follows from these local results.

### v30 local per-Spec PR drafts

These are local handoff drafts only; no remote PR was created or modified.
The delivery owner supplies each actual logical commit/base/integrated HEAD
after its registered gates; none is invented here.

| Owning package | Draft title and resulting behavior | Actual validation to carry | Remaining delivery or acceptance boundary |
| --- | --- | --- | --- |
| SPEC-0204 | Add optional n8n queue isolation and align exporter selection. An opted-in named-user ACL and Worker/Ollama overlay preserve baseline defaults while profile/direct-target closures select required provisioners/exporters; existing oauth2 obs wiring is reused. | Selected34tests(33PASS/1SKIP), separate28unitPASS, exact-image ACL attempt1FAIL then attempt2PASS, public synthetic config and independent READY review | Registered final changed gate NOT_RUN; real Bull4/Node/Credential/model calls, AOF/HOME/P06 and C16/C17 remain pending |
| SPEC-0214 | Preserve interrupted Quality attempt evidence. Cancellation retains failure/artifact context and cleanup no longer masks the original interruption. | 31unitPASS/0SKIP, parent7-of-7 changed-line trace, independent review without actionable findings | Final registered delivery gate NOT_RUN; no new whole-Quality or runtime acceptance |
| SPEC-0212 | Reconcile v30 source routes and local delivery. Existing C19/W24 now maps R11–R32 and F01–F29, records actual bounded results and preserves completed records. | Package281checks/274regressions, scoped links/metadata and exact22R/29F assertions with their documented input boundaries | Final integrated registered checks/independent review and logical delivery remain separate; draft C19 pending |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| main-baseline | 19 | W24 | `git fetch origin main`; source/branch/worktree/open-PR observation | `e6807a7d16d8b9e180ff58456ab64e4ee721ca69` | PASS | Task inputs and coordinator observation | required | - |
| document-baseline | 19 | W24 | Active metadata, operations catalog, and all-link checks before P0 edits | baseline `e6807a7` | PASS | Metadata 576 selected/0 violations; catalog PASS; links 1,310 documents/11,677 links/0 failures and 1 historical warning (2,870 links lack capture source) | required | - |
| current-service-inventory | 19 | W24 | Bounded source projection and `scripts/lib/ops/port_inventory.py` | baseline `e6807a7` | PASS | `docs/90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md`; generated temporary output is not durable evidence | required | - |
| secret-catalog-views | 19 | W24 | Value-free secret-catalog public validation and view check | baseline `e6807a7` | FAIL | Prepared dependency environment: metadata valid for 145 entries/1 alias; `check-views` exits 2 with `P02_VIEW_DRIFT` in ignored operator staging, not runtime evidence or a source repair | required | - |
| ci-local-context | 19 | W24 | `python3 scripts/validation/run-ci-gate.py --profile changed --requirements` without invented PR context | baseline `e6807a7` | FAIL | Exit 1: hosted prerequisites require a pull-request context; no fake CI variables used | required | - |
| remote-protection | 19 | W24 | Authenticated branch-protection/rules readback | baseline `e6807a7` | PASS | `strict=true`, empty required contexts/checks, admin enforcement and conversation resolution observed; no mutation | required | - |
| root-hardening-coverage | 19 | W24 | Existing hardening script tier coverage | baseline `e6807a7` | FAIL | Script passes its 01–12 list but omits `infra/13-experience`; owner must add P8 route and regression | required | - |
| ci-routing-regressions | 19 | W24 | Registered CI gate and SMTP routing unit suites | baseline `e6807a7` | FAIL | CI contract expected-route drift and SMTP optional-runtime count drift; QA/CI owner routes fixes before P8 acceptance | required | - |
| workflow-source-suite | 19 | W24 | Focused Airflow/n8n/P10 source suites | baseline `e6807a7` | PASS | `python3 -m unittest` focused suite: 108 tests, exit 0; no source mutation | required | - |
| workflow-isolated-denial | 19 | W24 | `env OPSFLOW_PG_REHEARSAL_IMAGE=sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873 OPSFLOW_PG_REHEARSAL_CONTEXT=default python3 -m unittest tests.validation.test_opsflow_database_rehearsal.OpsflowDatabaseNativeRehearsal -v` | baseline `e6807a7` | FAIL | 2 tests: restore/ACL PASS; cross-database denial failed; three owned containers cleaned up | required | - |
| native-home-recovery | 19 | W24 | Native service, HOME flow, and isolated restore result | No named live target in P0 | NOT_RUN | Deferred to owning P1–P10 Tasks | required | - |
| v30-current-source-routing | 19 | W24 | Required Task metadata/current acceptance and relevant domain-source survey; exact R/F owner comparison | HEAD and read-only remote main 136b7cac4483d4af8aaa73ca6dc3f9a0da521e10; current direct v30 request | PASS | #v30-current-input-and-survey--2026-10-26; #v30-four-axis-requirement-routing; #v30-f01f29-execution-crosswalk; bounded source survey only | required | - |
| v30-package-provenance | 19 | W24 | Read existing INDEX/manifest/requirements/traceability/crosswalk; Python Path/json/hashlib member, ID and text comparison | Primary a6375ee9; attachment709ab7e2; 98 members with 96 ordinary digests and 2 explicit cycle exceptions | PASS | #v30-current-input-and-survey--2026-10-26; structural provenance only | required | - |
| v30-package-document-checks | 19 | W24 | Parent read-only validate.validate invocation and regression unittest suite | Existing v30 bundle; validator5cd29edc and regression2233b4e1 full digests above | PASS | #v30-bounded-source-readiness-and-writer-leases; parent reported281 checks and274 regressions, no repository/runtime acceptance | optional | - |
| v30-scoped-link-diagnostic | 19 | W24 | Existing graph alignment/traceability APIs over the same owned documents and explicitly required global inputs | Initial selected3 graph omitted mandatory navigation/policy nodes | FAIL | #v30-coordinator-document-checks; diagnostic input limitation, no repository missing-file claim | optional | - |
| v30-scoped-link-correction | 19 | W24 | Existing graph alignment/traceability APIs over the same owned documents and explicitly required global inputs | Corrected selected6 graph; same three owned documents plus required navigation/policy nodes | PASS | #v30-coordinator-document-checks; zero findings, exit0 | optional | v30-scoped-link-diagnostic |
| v30-prepared-document-metadata | 19 | W24 | `check-document-metadata.py --mode check-changed --base-ref 136b7cac4483d4af8aaa73ca6dc3f9a0da521e10` with the three explicit owned changed paths | Prepared coordinator draft before final lease/result additions | PASS | #v30-coordinator-document-checks; selected3, violations0, no lifecycle override; final integrated checks separate | optional | - |
| v30-implemented-source-results | 19 | W24 | Read current owner-reported source, unit, isolated ACL and independent review results without promoting them to leaf acceptance | Frozen17-source/test manifest96d77614; exact ACL module85fa2a8b; P02/P03 and Quality current continuations | PASS | #v30-implemented-source-and-bounded-verification; separate invocations and retained first-attempt failure | optional | - |
| v30-final-public-changed-gate | 19 | W24 | Registered public changed gate on final logical commits with the prepared exact controller toolchain | Final committed input not yet executed by delivery owner | NOT_RUN | #v30-implemented-source-and-bounded-verification; #v30-local-per-spec-pr-drafts | optional | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 19 | pending | main-baseline, document-baseline, current-service-inventory, secret-catalog-views, ci-local-context, remote-protection, root-hardening-coverage, ci-routing-regressions, workflow-source-suite, workflow-isolated-denial, native-home-recovery | P0 routing is in progress; required failures and unrun higher evidence domains remain open. | SPEC-0212 coordinator for routing; named primary owners for execution. |

## Review and Completion

Independent review must verify that every requirement 11–32 has exactly one
primary owner, all shared-file leases are explicit, and the P0 snapshot does
not promote source/static observations into native, HOME, recovery, hosted, or
remote-protection acceptance. The coordinator then runs the document checks and
changed selector for this exact diff, records command/result/input revision,
and makes one logical documentation commit. No push, PR, merge, remote setting,
or live operation is performed by this Task record.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [R10 reconciliation Task](tsk-0007-r10-reconciliation.md)
- [Current coordination audit Task](tsk-0006-current-coordination-audit.md)
- [Bounded service inventory](../../../90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md)
- [Integration owner](../../0204-service-integration-security-and-operations/spec.md)
