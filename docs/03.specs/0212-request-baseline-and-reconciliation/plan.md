---
title: "Request Baseline and Reconciliation Plan"
version: "1.53.0"
type: "sdlc/plan"
status: "approved"
owner: "@buenhyden"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0212-PLAN-0001"
parent_ids:
- "SPEC-0212"
created: "2026-10-07"
---

# Request Baseline and Reconciliation Plan

## Overview

The current 11–30 request preserves completed P00 Tasks. SEC01 delivers first,
SMTP01 owns the source transition second, and CLN01 deletes the old file third.

R10 adds W16–W23 in TSK-0007 from the 2026-10-15 source baseline. Existing
W1–W15 and completed bodies retain their earlier scope and evidence. The direct user request authorizes this bounded local contract and Plan;
that authority is not inferred from historical acceptance and does not approve
a shared edition or remote action.

## Scope

W9–W15 reconcile the request baseline, owner routes, shared-file leases
and SEC01 → SMTP01 → CLN01 handoffs; W1–W8 retain their historical receipts.
R10 W16–W23 add the current authority, document, lifecycle, retention,
hook/release, memory and OpenBao source corrections in TSK-0007 without
reopening completed Tasks or assigning new downstream acceptance owners.
R13 adds W25 in TSK-0009 for one current-source follow-up. It began separately
from W24's independent infrastructure work and now preserves the published
W24/criterion 19 allocation alongside W25/criterion 20. W26 in TSK-0010
classifies the links behind the standing `historical-links-unrecorded` warning
as a read-only, documentation-only follow-up. W27 in TSK-0011 records a
read-only per-unit Stage 98 disposition dry-run; it removes nothing. W28 in
TSK-0012 applies the owner-approved history-only removal of its candidates.
W29 in TSK-0013 records the follow-up review of the remaining request areas.
W30 in TSK-0014 removes a repeated history scan from the archive check.
W31 in TSK-0015 applies the owner-approved blocked items from TSK-0013.
W32 in TSK-0016 records the owner's choices for the remaining TSK-0013 items.
W33 in TSK-0017 re-reviews the deferred and not-run items from TSK-0016.
W34 in TSK-0018 applies the owner's choices on the items TSK-0017 left open.
W35 in TSK-0019 applies the owner's choices on two gaps from a request re-read.
W36 in TSK-0020 adds a quality characteristic and measure to the NFR template line.
W37 in TSK-0021 scopes the worktree rule to branch worktrees.
W38 in TSK-0022 records a read-only runtime snapshot and a skill bundle audit.
W39 in TSK-0023 records the owner's correction of the exporter drift.
W40 in TSK-0024 corrects stale paths named in agent and provider surfaces.
W41 in TSK-0025 removes a dead CI routing prefix.
W42 in TSK-0026 records the re-run of the full request against the baseline.
W43 in TSK-0027 reads the archive policy against its code.
W44 in TSK-0028 reads the SDLC and CI/QA policy and renames the release workflow.
W45 in TSK-0029 audits the meaning of every request line.
W46 in TSK-0030 judges every pair of the 148 requirements.
W47 in TSK-0031 adds the five missing governance rules.
W48 in TSK-0032 makes governance and provider guidance English.
W49 in TSK-0033 adds a Verification section to every skill.
W50 in TSK-0034 moves the Migration 0003 proof into its own module.
W51 in TSK-0035 writes the rule text behind the partly met lines.
W52 in TSK-0036 records the investigations, decisions and currency fixes.
W53 in TSK-0037 lets the validator accept the approved terminal Task correction.
W54 in TSK-0038 accepts ADR-0050 and archives the Vault ADRs.
W55 in TSK-0039 records the open Spec reconciliation and the OpenTofu promotion.

W24 adds the independent `INFRA-P0` routing snapshot for requirements 11–32.
It freezes common boundaries before `INFRA-P1` data/secret/recovery work or any
variable implementation; it does not reopen r10 criteria 11–18.

W56–W60 implement the direct 2026-11-01 P01 request in TSK-0040. The
existing service, port, Secret and version owners remain canonical. DATA-0096
is a non-normative current observation consumed by this Task and P02–P12
handoffs; it does not replace their acceptance contracts.

W61–W65 implement the direct 2026-11-02 P02 request in TSK-0041. The
infrastructure writer integrates all `infra/` changes; tool code, contract
tests, documentation and CI registration have separate writers. P02 retains
shared MNG Valkey as the default and does not reopen the historical secret
catalog Task. Local source and isolated tests are in scope; operating services,
host changes, actual secrets, external repositories and remote CI are not.

W66–W70 implement the approved P03 plan in TSK-0042. P03 retains local-only
model use, narrows model registration, runner and tool-policy source contracts,
and reuses the completed offline Wiki preparation package. Local source and
isolated tests are in scope; HOME services, host security settings, actual
credentials, model downloads, external workspaces and remote CI are not.

W71–W76 implement the approved local P04 plan in TSK-0043. Existing Opsflow
is the only selected business path. The implementation preserves historical
CDC and Iceberg acceptance, defers a new experiment until actual inputs exist,
and does not change operating services, hosts, real credentials or remote state.
The dependencies below route available source inputs; a historical Task's
terminal status is not a hidden prerequisite for this approved local work.

W77–W80 implement the approved local P05 plan in TSK-0044. The existing
selected Opsflow notifier remains the business consumer; C19/C22 history and
P04's TEST_RESIDUAL acceptance remain unchanged. Source, synthetic/owned
isolated tests and a local logical commit are authorized; HOME services,
actual credentials, external delivery/repositories and remote integration are not.

W91–W94 implement the approved local P08 plan in TSK-0047. The Task inventories
the current public image and package source, evaluates only selected Valkey and
n8n candidates, and rechecks the tracked Storybook lock in isolation. It does
not authorize operating services, host changes, actual credentials, external
delivery, remote integration, LAB runtime or an inference from a base/sample
artifact receipt to a different artifact.

W99–W102 implement the approved local P10 plan in TSK-0049. The Task
normalizes current generation-7 documentation contracts, registers existing
local CI/QA routes and aligns governance wording to active repository changes.
It does not rewrite completed history, weaken admission, operate services,
access credentials, transmit externally or run remote CI.

W103–W107 implement the approved local P11 plan in TSK-0050. The Task adds
receipt-bound Hermes source collection and bounded durable replay/restore
guards, while recording the current five trust boundaries. It preserves rather
than re-runs SPEC-0204's historical Gateway/Attester/Export 1.0 receipts;
Windows B, live scheduling, actual credentials, routes and remote CI remain
outside the authorized local source and owned-isolation scope.

W108 records D12, the first Opsflow installation in HOME, in TSK-0051.
The [2026-11-10 owner acceptance](tasks/tsk-0051-opsflow-home-installation.md#owner-acceptance-2026-11-10)
closes all six PASS steps and criterion103. Earlier unrun/open-item text in
that terminal Task is historical; it does not reopen installation. Likewise,
[TSK-0043 final acceptance](tasks/tsk-0043-opsflow-data-path.md#criterion-acceptance)
sets criterion70 to not-required and accepts66-69/71. Terminal bodies stay
unchanged; this is the current correction route.

W111 in TSK-0053 assesses the108 master requirements and supplements and
owns scoped current-guidance corrections. SPEC-0270 separately owns the
approved memory capacity/search/backup follow-up. The concurrently issued
TSK-0052 owns the supply-chain successor criteria104/105/W109-W110.

W112 in TSK-0054 diagnoses and fixes the failing Hermes `devops` daily brief;
configuration outside the repository stays an owner decision.

W113 in TSK-0055 adds the authenticated Hermes OTLP ingest path to Alloy and
the Hermes dashboard; Hermes configuration and the token value stay owner actions.

W114 in TSK-0056 runs the v14.2 W01 governance standardization: authoring
owners, approval and adoption records, and generated-copy drift for GOV-01 to
GOV-08 and SUP-12. Template work goes to W03 and runtime wiring to W07 as
handoffs, not as this Task's changes.

W115 in TSK-0057 runs the v14.2 W02 archive and safe-removal assessment.
Removal candidates get readiness and byte-recovery proofs first; deletion
waits for the owner's approval of each batch. The SPEC-0248, 0249, 0250 and
0260 Tasks keep their own residual criteria.

W116 in TSK-0058 runs the v14.2 W03 template, metadata and relation work; W05
owns the validators. Its H2-retention decision Q-03 was superseded on
2026-11-12: the headings migrate to the common section contract.

W117 in TSK-0059 runs the v14.7 W00 intake. It records the read boundary, the
recent pull requests, the OPEN-01 to OPEN-14 reassessment and the per-file
differences from the common target contracts, corrects current guidance that
conflicts with the current requirement, and hands each remaining difference
to one receiving work unit without starting that work.

W118 in TSK-0060 runs the v14.7 W01 governance work: per-ID verdicts, the
local adoption record of each common contract and the policy corrections.

W109–W110 record the supply-chain evidence that TSK-0047 handed off for
criteria 86 and 89, in TSK-0052. The 2026-11-10 owner decision opens the Task;
lookups start only after the owner approves the network host scope there.

W81–W86 implement the approved local P06 plan in TSK-0045. Existing OpenBao
consumer acceptances and public catalog authority remain scoped to their own
receipts. Value-free synthetic tests and independently reviewed read-only
private structural comparison are authorized; private modifications, credential
issuance, rotation, deletion, service changes and remote integration are not.

W87–W90 implement the approved local P07 plan in TSK-0046. Existing SPEC-0224
datastore and SPEC-0214 quality-OTLP acceptance is reused at its recorded
scope. Local source, bounded owned isolation and the exact declared Prometheus
image pull are authorized; HOME changes, actual secrets and external alert
delivery are not. Historical P07 resource work belongs to SPEC-0218.

W95–W98 implement the approved local P09 plan in TSK-0048. The Task records
consumer-backed role dispositions, source-bound common-control and resource
evidence, accepted storage placement and protected retirement input handling.
It preserves current default and optional configurations. It does not authorize
service operation, host configuration, storage migration, actual deletion,
Secret access or remote integration.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1 | Historical local/remote and Project-Template baseline read; retained evidence only | None | TSK-0001 | Preserved Task evidence |
| W2 | 2 | Historical fifteen-item ownership; superseded for current routing | W1 | TSK-0001 | Preserved Task evidence |
| W3 | 3, 4 | Historical root/LAB inventory and profile probes; LAB excluded from current execution | W1 | TSK-0001 | Preserved Task evidence |
| W4 | 5 | Historical conflict map and ADR-0047 | W2, W3 | TSK-0001 | Preserved Task evidence |
| W5 | 6 | Historical QA/protection read and validation | W4 | TSK-0001 | Preserved Task evidence |
| W6 | 1, 2 | Historical twenty-item main/template baseline | W5 | TSK-0002 | Preserved Task evidence |
| W7 | 3 | Historical inventory comparison; no fresh LAB run | W6 | TSK-0002 | Preserved Task evidence |
| W8 | 7 | Historical open-Spec disposition | W6 | TSK-0002 | Preserved Task evidence |
| W9 | 1 | Compare local/origin/remote main, dirty state and named baseline; parse root service keys and current inventory only | None | TSK-0003 | Value-free baseline and source-set evidence |
| W10 | 2, 3, 6, 7 | Read open Spec/Plan/Task frontmatter, latest tracked source and PR state; classify residuals and exclusions | W9 | TSK-0003 | Requirement table and owning evidence paths |
| W11 | 2, 4 | Observe contract RED; update SPEC-0212 Spec/Plan and SPEC-0204 Spec/Plan current routing | W10 | TSK-0003 | Contract GREEN; current authority checker |
| W12 | 4, 5 | Record writers/order/rollback, validate final documents, independent review, logical commits and protected PR delivery | W11 | TSK-0003 | Document checks; staged checks; actual hosted observations |
| W13 | 8 | Record current routing and SEC01 → SMTP01 → CLN01 ordering | W12 | TSK-0005 | Value-free contract probe; Stage 99 checks |
| W14 | 10 | Bind current main, supplied COORD input, observed worktree/PR state and active-package inventory; retain PR #457's merged receipt as input only | None | TSK-0006 | Value-free Git/source and lifecycle audit |
| W15 | 9 | Map requirements 11–30, reconcile active routing conflicts, record writer locks/recovery boundaries, run Stage99 selectors and hand off exact current inputs | W14 | TSK-0006 | Cross-package source, Task and document audit |
| W16 | 11 | P01 source/permission/delta baseline, attachment identity and classified finding map | None | TSK-0007 | Read-only Git and canonical-owner audit |
| W17 | 12 | P02 role, language, section and link correction; coupled Stage99 target amendment design | W16 | TSK-0007 | Changed metadata/links and affected contract regressions |
| W18 | 13 | P03 distinguish existing approval, Task state, acceptance, integration and observations | W16 | TSK-0007 | Generation-6 reader and exact lifecycle/acceptance evidence |
| W19 | 14 | P04 consumer/assurance/hold assessment and authorized retention or retirement | W16 | TSK-0007 | Direct consumer trace and applicable archive integrity checks |
| W20 | 15 | P05 hook/CI call graph and reproduced push-stage or duplicate assurance correction | W16 | TSK-0007 | Focused hook/routing tests and isolated installed-stage probe |
| W21 | 16 | P06 branch/release/CHANGELOG/rollback producer audit and concrete source corrections | W16 | TSK-0007 | Current producer/config trace and scoped contracts |
| W22 | 17 | P07 shared-memory/native-off/Restic reuse and justified missing assurance design or implementation | W16 | TSK-0007 | Existing receipts plus synthetic memory/backup regressions |
| W23 | 18 | P08 OpenBao optional-skip and CA-overlay discrepancies, operations promotion and quality limits | W16 | TSK-0007 | Focused OpenBao synthetic tests and changed document checks |
| W24 | 19 | INFRA-P0 inventory scope, owner routes, QA/CI mapping, writer leases, evidence ladder, and P1–P9 handoffs for requirements 11–32 and distinct F01–F29 findings | None | TSK-0008 | Value-free source/static evidence; no native/HOME/recovery claim |
| W25 | 20 | Classify r13 P01-P08 follow-up findings; remove one reproduced link-graph duplicate, bind repository-file provenance to its declared revision, and retain one shared memory store through sanitized CLI common-directory identity | W16 | TSK-0009 | Focused link and memory regressions, changed-path CI selection, and changed document checks |
| W26 | 21 | Classify the links counted by `historical-links-unrecorded` against each record's pre-archive Git origin and record the residual set and its proven cause | W25 | TSK-0010 | Read-only Git object resolution; changed document metadata and link checks |
| W27 | 22 | Per-unit Stage 98 retention-payload dry-run: consumers, capture, hold, isolated restore, and candidate or blocked disposition; no removal | W26 | TSK-0011 | Read-only checker-library reuse and `git archive` restore; changed document metadata and link checks |
| W28 | 23 | Owner-approved history-only removal of the TSK-0011 candidates: capture rows for pre-catalog units, assessment rows, whole-payload removal | W27 | TSK-0012 | Corpus lifecycle, link alignment, and changed document checks after removal |
| W29 | 24 | Review of the remaining request areas: apply verified small corrections; defer or block the rest with owner and reason | W28 | TSK-0013 | Renderer drift, metadata contracts and changed checks, affected unit tests |
| W30 | 25 | Measure and remove the repeated history scan in the archive assessment snapshot check | W29 | TSK-0014 | Archive regressions and timed corpus check |
| W31 | 26 | Remove git-cliff configuration, add template subtopics, and repair the index-membership regression | W30 | TSK-0015 | Metadata contracts, template and gate tests, full unit suite |
| W32 | 27 | Classify repository-path absence tests, list `_workspace` writers, and keep external acceptance not run | W31 | TSK-0016 | Absence-test scan, metadata contracts, workspace contract tests |
| W33 | 28 | Replace past-removal absence checks with current-rule checks and read remote and cross-repository state without writing | W32 | TSK-0017 | Tier and routing tests, manifest negative check, read-only API and repository reads |
| W34 | 29 | Narrow merge methods, diagnose pre-existing unit failures, run static Compose validation, and hand off cross-repository gaps | W33 | TSK-0018 | Merge-method read-back, isolated-venv test run, Compose validation in a clean worktree |
| W35 | 30 | Delete the stale `main-current` tag and add the worktree location rule | W34 | TSK-0019 | Remote tag read-back, governance contract, provider render |
| W36 | 31 | Add a quality characteristic and measure to the requirement template's NFR line | W35 | TSK-0020 | Requirement parser and template tests |
| W37 | 32 | Scope the worktree location rule to branch worktrees | W36 | TSK-0021 | Governance contract, provider render |
| W38 | 33 | Read running container health and audit skill bundles | W37 | TSK-0022 | Read-only `docker ps`/`inspect`, skill inventory |
| W39 | 34 | Record the owner's recreation of `airflow-statsd-exporter` and its health | W38 | TSK-0023 | Read-only `docker inspect` and project health count |
| W40 | 35 | Correct repository paths in agent and provider surfaces that no longer exist | W39 | TSK-0024 | Path existence scan, governance contract |
| W41 | 36 | Remove routing and references to files that do not exist in active surfaces | W40 | TSK-0025 | Path existence scan, workflow-contract and gate tests |
| W42 | 37 | Re-run the request against the baseline, close TSK-0008, and record the unperformed specification audits | W41 | TSK-0026 | Baseline readback, metadata contracts |
| W43 | 38 | Read the archive policy text against its code and checks, and correct mismatches | W42 | TSK-0027 | Archive corpus check, metadata contracts, routing tests |
| W44 | 39 | Read SDLC and CI/QA policy against code and rename the release workflow | W43 | TSK-0028 | Workflow contract, gate and release tests, metadata contracts |
| W45 | 40 | Audit the meaning of each non-blank request line against the repository | W44 | TSK-0029 | Line coverage, metadata contracts, agent governance |
| W46 | 41 | Judge every pair of the 148 requirements for duplication and conflict | W45 | TSK-0030 | Pair coverage, attribute coverage, metadata contracts |
| W47 | 42 | Add the missing rules for lines L047, L171, L175, L292, and L369 | W46 | TSK-0031 | Agent governance, provider projections, routing tests, metadata contracts |
| W48 | 43 | Make governance and provider guidance English and enforce it | W47 | TSK-0032 | Language check, language and registry tests, agent governance, metadata contracts |
| W49 | 44 | Add a required Verification section to every skill | W48 | TSK-0033 | Section coverage, metadata contracts, registry and heading tests |
| W50 | 45 | Move the Migration 0003 cutover proof into its own module | W49 | TSK-0034 | Archive behavior parity, document governance suite, script manifest |
| W51 | 46 | Write the rule text behind the partly met request lines | W50 | TSK-0035 | Agent governance, language check, routing tests, metadata contracts |
| W52 | 47 | Record the investigations, owner decisions and currency fixes | W51 | TSK-0036 | Metadata contracts, links, corpus and archive, workflow contract, tests |
| W53 | 48 | Accept the one approved terminal Task `Resolves` correction | W52 | TSK-0037 | RED and GREEN tests, end-to-end check, spec package tests, lint |
| W54 | 49 | Accept ADR-0050 and archive the Vault ADRs it supersedes | W53 | TSK-0038 | Changed metadata, metadata contracts, links, corpus and archive |
| W55 | 50 | Record the open Spec reconciliation and promote the OpenTofu documents | W54 | TSK-0039 | Package pull requests, metadata contracts, changed metadata, links |
| W56 | 51 | Capture actual workspace roots, source identity and safe before/after fingerprints | None | TSK-0040 | Git/non-Git and boundary regression |
| W57 | 52 | Implement scan/compare/validate and publish independent census denominators | W56 | TSK-0040 | Unit, integration, CLI and isolated render probes |
| W58 | 53 | Reconcile historical acceptance with current evidence and explicit residuals | W56 | TSK-0040 | Current Task/criterion readback and ledger validation |
| W59 | 54 | Bind single writers and exact leaf-owner handoffs to current file fingerprints | W56 | TSK-0040 | Lease conflict and ownership validation |
| W60 | 55 | Recheck official sources and record bounded product applicability | W56 | TSK-0040 | Direct official-source consultation and independent review |
| W61 | 56 | Reconcile selected caller, DNS, listener, service-DNS, host and gateway port contracts | W56 | TSK-0041 | Focused source and isolated Compose/route contracts |
| W62 | 57 | Preserve browser, application and machine authentication boundaries and direct-backend protections | W61 | TSK-0041 | Negative route and controlled OIDC contract tests |
| W63 | 58 | Reconcile DEV/MNG environment and readiness evidence without promoting liveness to function readiness | W61 | TSK-0041 | Environment, readiness and unsupported-variable regressions |
| W64 | 59 | Retain shared MNG Valkey default and align named ACL, dedicated opt-in and safe secret delivery contracts | W61 | TSK-0041 | Synthetic-secret, ACL and persistence-contract regressions |
| W65 | 60 | Publish bounded connection evidence and exact P03–P08 handoffs, including the Grafana exception review | W61, W62, W63, W64 | TSK-0041 | Ledger validation, document contracts and independent review |
| W66 | 61 | Reconcile local-only model actors, endpoint and non-fallback boundaries | W61, W65 | TSK-0042 | Model-route policy and negative-contract tests |
| W67 | 62 | Add bounded Open Notebook model-registration planning and preserve recovery/registration distinctions | W66 | TSK-0042 | Synthetic API, persistence and conflict/rollback tests |
| W68 | 63 | Tighten external runner source isolation without changing common resource owners | W61, W64 | TSK-0042 | Runner configuration and synthetic denial tests |
| W69 | 64 | Bind automation-tool policy to approved destination and bounded requests before credential use | W66 | TSK-0042 | URL/DNS/redirect, budget and authority-negative tests |
| W70 | 65 | Reuse Wiki preparation and publish P03 evidence axes and leaf-owner handoffs | W66, W67, W68, W69 | TSK-0042 | Wiki contract/evaluation, Task, ledger and independent review |
| W71 | 66 | Reuse current DEV/MNG ownership and bind source, initialization and restore responsibilities | W56 | TSK-0043 | Ownership/provisioner regression and current-source evidence |
| W72 | 67 | Repair Airflow URI construction, bounded input quarantine, data_version and metadata-preserving isolated restore | W71 | TSK-0043 | RED/GREEN unit, integration, CLI and actual isolated Worker/restore tests; changed code coverage at least 80% |
| W73 | 68 | Reconcile current CDC/Avro consumers and preserve the platform_dev acceptance scope | W71 | TSK-0043 | Current connector/provisioner/source readback; explicit Opsflow deferral and resume contract |
| W74 | 69 | Reuse Opsflow quality blocking and reconcile optional analytics smoke versus business publication | W72 | TSK-0043 | Invalid-input/no-publication tests and source-to-consumer evidence |
| W75 | 70 | Defer a new experiment until actual dataset, time field, target, baseline and owner exist | W71 | TSK-0043 | Explicit missing-input and no-private-inference record |
| W76 | 71 | Preserve optional Iceberg platform acceptance and document workload deferral and recovery limits | W71 | TSK-0043 | Version-specific maintenance evidence, current consumer and historical receipt mapping |
| W77 | 72 | Reuse historical C19/C22 queue/schedule acceptance and reconcile current source/image scope | None | TSK-0044 | Exact-version source/consumer readback and bounded regression; current private/live state remains separate |
| W78 | 73 | Add approval-bound one-shot no-send dead retry, restored-sending quarantine and in-flight recovery barrier | W77 | TSK-0044 | RED/GREEN SQL/Node/CLI and controlled isolated normal/denial/interruption/recovery cases; preserve history and uncertainty |
| W79 | 74 | Preserve queue-mode default storage and reject binary input in the selected notifier | W77 | TSK-0044 | Exact-source/default readback and notifier binary-rejection regression; no new storage or binary consumer |
| W80 | 75 | Add opt-in authenticated Mailpit STARTTLS fixture and next-execution same-ID credential refresh proof | W78 | TSK-0044 | Controlled TLS/auth success/refusal, same-ID refresh, bounded owned rehearsal, independent review and local gates |
| W81 | 76 | Reconcile catalog, generated views and supported secret delivery contracts without duplicate identities | None | TSK-0045 | Public catalog/generator regressions and value-free source review |
| W82 | 77 | Implement bounded read-only full environment and registry structure comparison | W81 | TSK-0045 | RED/GREEN CLI, value-redaction, unsafe path and interrupted-read tests |
| W83 | 78 | Preserve scoped OpenBao trust, custody and recovery acceptance and classify current residuals | None | TSK-0045 | Source/version and historical actor/criterion evidence |
| W84 | 79 | Reconcile completed/held consumers and hand off n8n credential refresh ownership | W81 | TSK-0045 | Catalog/consumer binding review and synthetic contract regressions |
| W85 | 80 | Harden bounded SMTP public/private readers and preserve canonical alias semantics | None | TSK-0045 | FIFO/growth/rebind, equality/absence and regression tests |
| W86 | 81 | Inventory retirement readers and preserve protected recovery copies without deletion | W83–W85 | TSK-0045 | Read-only source evidence, owner/hold and P09 handoff |
| W87 | 82 | Implement source-bound producer companion selection and guarded operator start planning | None | TSK-0046 | RED/GREEN source closure, safe CLI and start-stub tests |
| W88 | 83 | Add selection-bound expected scrape, backend and freshness signals with dashboards and alert rules | W87 | TSK-0046 | Synthetic configuration, promtool rules and isolated metrics checks |
| W89 | 84 | Reuse authenticated OTLP and test pinned Alloy delivery and outage recovery | None | TSK-0046 | Existing quality regressions and owned isolated Alloy/Prometheus proof |
| W90 | 85 | Bind HOME/profile expected-state and recovery handoffs without changing operating resources | W87, W88, W89 | TSK-0046 | Selection on/off, absent inventory, owner review and scoped evidence |
| W91 | 86 | Preserve the not-required decision and hand fresh source review to successor W109/TSK-0052 | None | TSK-0047 | Historical source receipts and explicit successor ownership; fresh lookup remains separate |
| W92 | 87 | Evaluate selected Valkey 9.1.3 and owner-retargeted n8n 2.46.6 compatibility bundles without promoting a candidate to operation | W91 | TSK-0047 | Pin/consumer/source checks and bounded isolated ACL, queue, restore and runner regressions |
| W93 | 88 | Preserve Storybook 10.6.3 and verify its tracked lock in a clean isolated installation | W91 | TSK-0047 | Isolated install, lint/typecheck/build and scoped UI/MCP/OIDC regression evidence |
| W94 | 89 | Preserve the not-required decision and hand exact artifact verification to successor W110/TSK-0052 | W91, W92 | TSK-0047 | Historical receipts and explicit successor ownership; no cross-artifact inference |
| W95 | 90 | Record the fifteen current role comparisons with public-source/consumer evidence and explicit unknowns | None | TSK-0048 | DATA-0096 role rows, preserved historical decisions and no deletion inference |
| W96 | 91 | Preserve common controls while binding base/overlay provenance and measurement inputs to canonical sources | W95 | TSK-0048 | RED/GREEN synthetic overlay, exception and canonical-binding checks; runtime remains separate |
| W97 | 92 | Reuse accepted C1–C6 placement and record only measured drift as a future candidate | W95 | TSK-0048 | Read-only current-source comparison and explicit no-migration boundary |
| W98 | 93 | Reject unsafe or incomplete retirement manifests without creating an eligible deletion target | W95 | TSK-0048 | RED/GREEN manifest parser and owned-fixture rejection checks; apply remains blocked |
| W99 | 94 | Normalize current document evidence and acceptance contracts without rewriting historical archives | None | TSK-0049 | Generation-7 document contract and sequential metadata/corpus/link checks; failures remain explicit |
| W100 | 95 | Register existing P03 public validation and correct required P04/P05 selector expectations | W99 | TSK-0049 | Public plan/parity and exact selector tests in registered contexts |
| W101 | 96 | Align hook and governance wording with active repository-change scope while preserving fail-closed admission | W99 | TSK-0049 | Synthetic payload and temporary-Git-fixture regressions |
| W102 | 97 | Preserve result lifecycle and record local QA/CI residuals without upgrading them to remote acceptance | W99–W101 | TSK-0049 | EvidenceStore lifecycle and explicit NOT_RUN remote/operational outcomes |
| W103 | 98 | Bind new report items to persisted collector receipts and scheduled execution identity without granting producer-signature authority | None | TSK-0050 | RED/GREEN collector, receipt binding, source-quality and SSRF/interrupt regressions |
| W104 | 99 | Validate exact Gateway durable receipts and preserve corrupt or uncertain direct-submission records without implicit replay | W103 | TSK-0050 | Direct outbox, receipt-contract, concurrency and response-loss regressions |
| W105 | 100 | Preserve selected Export 2.0 and distinguish synthetic ACK from recorded Export 1.0 Windows ACKs | W104 | TSK-0050 | Isolated Export 2.0 manifest/fixture contract; external Windows acceptance remains NOT_RUN |
| W106 | 101 | Bind Attester retry and SQLite backup/restore to one report's stored evidence and state | W104 | TSK-0050 | Mixed-record, tamper, interruption, concurrent replay and owned backup/restore regressions |
| W107 | 102 | Publish current trust-boundary, route and external-receiver handoffs without mutating watched routes | W103–W106 | TSK-0050 | Documentation/readme/runbook checks, offline gate and explicit operational/remote residuals |
| W108 | 103 | Preserve the completed six-step Opsflow HOME installation | W72 | TSK-0051 | Six PASS steps and owner acceptance on2026-11-10; no repeat installation |
| W109 | 104 | Give every current ledger entry a fresh review and reviewed decision from official sources | None | TSK-0052 | `security_update_gate` exit 0, or each unreviewable entry recorded as a residual |
| W110 | 105 | Bind each selected artifact to its own signature, provenance and SBOM evidence | W109 | TSK-0052 | Per-artifact Cosign or publisher verification receipts; missing material recorded |
| W111 | 106 | Assess108 master requirements and supplements; align current guidance and preserve residual owners | None | TSK-0053 | Task-owned assessment, unchanged terminal bodies, metadata/links/lifecycle and independent review |
| W112 | 107 | Diagnose and restore the scheduled Hermes `devops` daily brief | None | TSK-0054 | One scheduled run submitted and its alerts resolved, or the external cause recorded |
| W113 | 108 | Collect host-run Hermes OTLP traces, logs and gateway metrics through an authenticated Alloy receiver | None | TSK-0055 | Receiver and route tests, dashboard contract, then one live trace, log and metric readback after the approved apply |
| W114 | 109 | Assess and correct the v14.2 W01 governance obligations GOV-01 to GOV-08 and SUP-12 against their canonical owners | None | TSK-0056 | Per-ID owner, approval and adoption trace; reproduced gaps fixed with regression; metadata, links, contract and renderer checks |
| W115 | 110 | Assess ARC-01 to ARC-09 (v14.2) and W02-A, W02-B, R147-08, QA-C04, WP-19, WP-20 and OPEN-ARCHIVE (v14.7), and prove readiness and byte recovery for each removal candidate before any removal | W114 | TSK-0057 | Per-ID trace; per-candidate readiness, commit:path reachability and byte comparison; blocked cases recorded; removals only on owner approval |
| W116 | 111 | Assess DOC-01 to DOC-12 and SUP-11 and change the template, metadata and relation contract only for reproduced gaps | W115 | TSK-0058 | Per-ID trace; each changed key, section or table with producer, consumer and passing and failing tests; current documents migrated, history unchanged |
| W117 | 112 | Assess the v14.7 W00 obligations and the common-contract differences, correct conflicting current guidance and hand off each remaining difference | W116 | TSK-0059 | Read denominator, PR and OPEN-01 to OPEN-14 tables, per-file handoff table with one writer each; metadata, links and lifecycle checks |
| W118 | 113 | Assess the v14.7 W01 governance obligations, record local adoption of each common contract revision and correct conflicting policy | W117 | TSK-0060 | Per-ID verdicts, adoption table with contract revision and approval source, changed policy with metadata, links, governance contract and renderer checks |

### Current v30 continuation and delivery

The direct 2026-10-26 request extends W24's previous 11–31 routing scope to
R32 without a new Task, criterion, inventory authority, or duplicate prompt
package. TSK-0008 records the current source survey, package provenance,
four-axis owner map and exact writer leases. TSK-0006/0009/0010 and other
completed records remain historical evidence. Reuse the existing v30 bundle's
five standalone prompts and its single dependencies folder; preserve missing
historical references as unavailable rather than recreating their contents.

The survey classifies the whole tracked-path set and the relevant current
Task/consumer/source scopes; it does not claim semantic review of every byte.
After the coordinator reconciles the read-only findings, exact safe source
units proceed through their own prerequisites and independent prechange
review. A missing runtime/private/owner decision does not block unrelated
reversible source fixes. TSK-0008 names the current scopes; old writer names
below are historical assignments and confer no present lease.

The Quality cancellation correction belongs to SPEC-0214's current C10/W11
continuation, preserving completed criterion 7. Service selection, network and
optional ACL changes retain SPEC-0204 P02/P03/P05 and SPEC-0218 ownership.
Root Compose and environment edits require the coordinator's explicit release
to the single service writer after review; no current parallel writer owns
those files. The coordinator integrates only reviewed exact inputs.

This execution delivers local logical commits and per-Spec PR drafts only.
Earlier prospective push/PR/remote-merge directions below are superseded for
this request until separate direct authorization. No integration target is
inferred from being on main; an unidentified local target blocks integration
alone. Runtime, credential, deletion, host and external-cluster actions retain
their exact target, approval and recovery gates. Independent review and final
verification precede local delivery; no future result is recorded as PASS.

### W25 file map and checks

The link slice owns `scripts/lib/document_governance/links.py`,
`scripts/validation/check-document-links.py`, and
`tests/lib/document_governance/test_links.py`. Its regression proves one
same-input parse reaches the graph once and retains the CLI's existing modes.
The memory slice owns `scripts/lib/ops/memory_sources.py`,
`scripts/operations/agent_memory.py`, and `tests/lib/hooks/test_agent_memory.py`;
it adds a bogus-revision rejection and makes the CLI's own/caller
common-directory identity use the sanitized Git runner, without weakening the
digest, tracked-file, or no-symlink checks. This source-only regression does not
read a memory store.
`tests/validation/test_agent_governance_ci_routing.py` verifies that a memory
helper change selects the focused agent-governance route. The W25 memory writer
also owns the one-line `.github/workflow-contract.yml` changed-path map and its
direct gate-contract tests; it maps the helper and its regressions to the
focused route without changing unrelated workflow selection.
The metadata QA slice owns
`scripts/lib/document_governance/metadata/reference.py` and
`tests/lib/document_governance/metadata/test_reference.py`. It transports the
already-computed immutable legacy-archive binding into changed-record validation;
it does not alter an archive, add a predicate or constant, or redefine the
immutable-binding rule.

W25's doc-writer exception owns only
`.agents/governance/environment-constraints.md` and
`docs/05.operations/runbooks/10-platform-and-backup/0021-backup-and-restore.md`.
After an actual required-check readback and scoped review, it also owns only
`.github/rulesets/main-protection.md` for that canonical observation. These
exceptions clarify the full-commit/current-byte source-pin contract and the
observed protection state; they do not change a policy schema, runtime
procedure, or historical record.

### Exact writer map

The historical P00 doc-writer owned this Spec, this Plan and TSK-0003 for the
first reviewable current-contract unit. The current COORD writer owns only this
Spec, this Plan and TSK-0006. TSK-0001, TSK-0002, TSK-0003 and TSK-0005 are
completed historical bodies and remain immutable. Existing operations bodies,
inventory, Registry, runtime and governance sources are read-only here.
No new Spec number is issued. Independent reviewers do not edit the patch. A delivery-receipt unit after
actual P00 merge may reconcile the frontmatter of TSK-0001/TSK-0002 from their
already accepted historical criteria, preserving both bodies byte-for-byte.
The current Task records their lifecycle edges and actual delivery separately;
this is no fresh execution or downstream native acceptance.

For downstream work, each acceptance owner assigns one implementation writer
before touching a shared path. P01 owns secret classification/prerequisites;
P02 owns metadata/path mappings; P03 owns root gateway, endpoint and port
contracts; P04 owns Airflow source/native integration; P05 owns n8n source/native
integration; P06 owns per-image consumption; P07 owns root-leaf controls and
exact exceptions. SEC01 owns P09 preparation documents, schemas, synthetic
fixtures and future acceptance contracts. It creates no external workspace,
Wiki engine, native application or production consumer. SMTP01 provides only
the canonical secret/consumer/catalog interface and reviews related P09
contracts; it does not duplicate P09 files. P10 owns a named input-to-recovery
consumer. These stage labels allocate no new Spec IDs or unnamed live targets.

Only one writer at a time may own `docker-compose.yml`, public environment
contracts, `.github/workflow-contract.yml`, `scripts/manifest.yaml`, the
Stage 99 Registry, document indexes, shared Alloy/gateway/backup configuration,
and both `infra/common-optimizations.yml` and
`infra/common-optimizations.exceptions.json`. P00 owns none of their implementation.
P07 reuses SPEC-0218 v2; no full common-file rewrite follows from this Plan.

For W24, the coordinator exclusively writes this Spec, this Plan, and
TSK-0008. The bounded matrix at `m0021-local-docker-service-consolidation.md`
is an input projection, not a second inventory authority. Later writers are:
P01/P06/P07 for data, secret, backup and root-control work; SEC01 plus each
affected leaf owner for images, Dockerfiles, OCI evidence and update records;
P03 for connection and port contracts; P04/P05/P10 for the vertical flow;
the QA/CI owner for workflow contracts, gate scripts and tests; and P08/
SPEC-0227 plus the image owner for Stage 05 and requirement-31 documents.
Root Compose, `.env.example`, catalogs/exceptions, Stage 99 Registry, Stage 05
indexes, shared scripts, and CI contracts require a named single-writer lease.
Unknown task-level token, time, and rate limits do not release that lease.

For W14–W15, the coordinator writes only this package's Spec, Plan and
TSK-0006. Existing worktrees are evidence of possible concurrent ownership, not
permission to edit their paths. The lock map is: SEC01 image/digest/build;
P01 OpenBao TLS/custody; P02 catalog; SMTP01 canonical SMTP/alias; CLN01 exact
retirement; P03 common connection/port contracts; P04 SQL/DAG; P05 workflow and
SMTP node; P06 migration; P07 measurements/root leaves; P08 Stage05 moves; P10
acceptance fixtures; SPEC01 active-contract documents. The coordinator may
propose a shared-file change, but the lease holder integrates it after the
preceding source identity and review are fixed.

### Dependency and P08 integration order

1. P00 fixes baseline, ownership and exclusions first. Applied work stays
   NO_CHANGE and genuine gaps keep their existing acceptance owner.
2. P01 classification precedes P02 mappings and P06 actual secret consumption.
   P03 endpoint/port contracts precede their P04/P05 consumers; P09 references
   these contracts only for preparation. P07 uses
   observed demand and consumer prerequisites, with no invented optimal limits.
3. P04 and P05 native runs require actual connection/secret/recovery targets.
   Wiki preparation has no external workspace, native/app or production-consumer
   assignment. A future canonical SMTP interface may later name a consumer; P10
   consumes only verified interfaces and its named recovery fixture.
4. P08 selects exact current common/domain document destinations through the
   Registry. Finish a feature writer's edits and evidence before moving those
   paths; then one P08 writer moves documents and updates all references,
   indexes and applicable checks. Re-read SHA and hand the new paths back to
   the feature owner before any further edit. Do not edit old/new paths in
   parallel. P08 may move LAB documents to typed `labs/` destinations; LAB code,
   config, secrets and runtime are not moved.
5. Each feature owner completes its Task, independent review and per-Spec PR.
   P00's inventory or merge receipt cannot complete a downstream native run.
6. W24 records its reviewed P0 route before P1 or any variable source change;
   criterion acceptance remains pending while its evidence rows stay open. P1 establishes
   non-destructive restore prerequisites before live or irreversible image,
   connection, leaf, workflow, or retirement work; it does not block unrelated
   reversible source, test, CI, or P9 documentation work. Every logical change
   maps changed files to a regression, selector/gate, rollback, and operating
   documentation owner; requirement 31 is completed in the same unit as its
   actual ROOT-image change.

### R10 ownership and integration

The coordinator assigns one writer per slice. The documentation writer owns
this Spec, Plan and TSK-0007. Hook/CI implementation, Stage 99 and governance
contracts, and OpenBao source each have a distinct writer; the controller
integrates shared files and releases their lease before another writer edits.
No worktree path alone proves a lease released. Do not rewrite earlier Tasks.

Start with the Stage 99 stale authority prose and empty REQ-0024/AD-0030
scaffolding. Align new common-guidance language at its policy owner. Reproduce
pre-push multiple-ref/deletion behavior in an isolated repository. Independently
fix the OpenBao optional-skip contract and SPEC-0243 CA-overlay source wording.
The controller sequences any table/lifecycle/memory amendment after its exact
consumer impact and compatibility are reviewable; unimplemented targets stay
pending in TSK-0007 rather than being treated as completed by this Plan.

### Current P01 implementation and ownership

The qa-engineer writes the inventory CLI/library and its tests; the doc-writer
writes this package amendment, TSK-0040 and DATA-0096; the ci-cd-engineer
writes the script manifest and existing CI selector registration. The doc-writer
holds only the DATA-0096 allocation segment of the shared Registry. Each
shared-file lease records its pre-edit fingerprint locally. Independent reviewers
read without editing. Unassigned data owners and operational accepters remain
unknown; P labels confer no account authority.

The CLI supports scan, compare and validate. Public regular source files receive
SHA-256 fingerprints; private/authentication inputs, binaries, generated files
and Git internals receive explicit exclusion treatment without content reads.
Review receipts bind reviewer, time, fingerprint and scope. Publication validates
before atomic replacement and excludes its own payload from recursive hashing.
No service starts, host edits, credential actions or remote writes occur here.

## Verification Plan

### Current P06 implementation and ownership

TSK-0045 issues per-path single-writer leases and public fingerprints before
each edit. The structural tool, SMTP readers, QA helpers, documentation and CI
registration have separate writers and independent reviewers. The real private
comparison follows synthetic leak tests and independent security review; it
never prints or records private bytes, values, value hashes, or lengths.
Metadata comparison is read-only, preserves ownership and rejects missing,
ambiguous, unbounded, replaced or linked inputs. SMTP missing historical copy
is an observation, not a deletion receipt or an equality result.

Reuse historical acceptance only at its recorded version, actor and consumer
scope. Keep source, static, synthetic/isolated, prior acceptance, direct HOME,
rotation, independent restore, remote CI and final operator acceptance as
separate evidence. The existing catalog destination state is not independent
approval for a new OpenBao copy. n8n producer and native-credential updates are
handed to their owner; no private mutation or runtime service change is implied.

### Current P05 implementation and ownership

The documentation writer issues TSK-0044 and per-path baseline fingerprints
before source edits. The SQL writer alone owns new 007/008 SQL plus its tests;
the Node writer owns OpsflowSmtp and directly required workflow exports/tests;
the QA writer owns the controlled native fixture and the bounded P12 seam
compatibility tests. CI registration and P08 source-preparation receipt correction
have separate writers. No one edits an already issued SQL001–006 or completed
Task body. P04 full Worker/restore acceptance is not a start condition.

Keep manual no-send reprocessing approval-bound and single-use. Preserve
attempts, audit provenance and unknown SMTP state; verify both live and restored
in-flight barriers before replay. Never classify absence of a captured message
as proof that SMTP did not accept it. Reject binary input in the selected
notifier and do not add a binary storage service. Use only the optional owned
Mailpit STARTTLS/auth profile for delivery tests; a controlled native same-ID
credential update must affect the next execution without replacing the ID.

Perform meaningful RED/GREEN normal, refusal, interruption and recovery tests
with at least 80% coverage of new executable code. Preflight exact cached images,
resources, trusted paths and ownership, run one owned cluster at a time and keep
bounded attempts. Record missing environment and failed stages individually.
Independent code/security/SQL/IaC/document reviews precede normal local gates,
graphify freshness, source fingerprint comparison and local logical delivery.
Operating services, real secrets, external mail, remote CI and P12 final
acceptance remain NOT_RUN unless separately authorized and observed.

### Current P04 implementation and ownership

The P04 source writer integrates DAG, adapter and SQL changes. One infrastructure
writer integrates the Airflow Compose/Dockerfile slice; QA, documentation and CI
registration have separate writers. TSK-0043 records the pre-edit fingerprint,
single writer and exact paths before modification. Independent reviewers do not
edit the reviewed files. Unknown data and operational acceptance owners remain
unassigned and confer no runtime authority.

Install the small connection URI helper as read-only image content while keeping
all package and image versions unchanged. Preserve the supported Airflow _CMD
interface and the existing shared/default and dedicated broker selections.
Password components are encoded once, literal percent/space is preserved, and
the explicit single-line UTF-8 reader contract permits at most one terminal LF.
The current MNG listener variables remain independent from DEV's internal 5432
and host-published ports. Keep SQL migrations already issued immutable; expose
data_version through a new migration and preserve P05 outbox interfaces.

Extend the existing owned Celery Worker fixture rather than introducing a new
workflow. Its Worker uses the actual helper and restricted S3 credentials;
setup/recovery use a separate identity. Prove normal, rejection, interruption,
retry/backfill, duplicate/conflict and independent-target restore semantics.
Object restore includes Content-Type, metadata, tags, size and body; a newly
issued server ETag/version is not expected to equal the original. Quarantine is
bounded and fails closed before SQL/outbox publication. Oversized/unreadable
inputs are not copied into quarantine or reported as successfully preserved.

Preflight the existing tools, exact cached images, trusted UID/temp paths and
available resources. Use no image downloads, one owned cluster at a time and
the existing execution budgets. Record timeouts by failing phase. Do not weaken
filesystem guards or relabel unrelated n8n receipt drift as a P04 pass. Run the
registered local QA/render/doc/Registry checks and independent code, security,
SQL/IaC and document review before graphify freshness, final inventory/diff
comparison and a normal local logical commit. Operating service changes,
credential rotation, HOME independent restore, remote CI and final P12
acceptance remain NOT_RUN unless separately authorized and observed.

Run a value-free source-set audit, actual frontmatter parse and read-only PR
metadata before authoring. Observe the requirement-coverage/exclusion contract
probe fail on the baseline, then pass after the active-contract edits. Its
input SHA and result are recorded in the Task; no persistent snapshot test or
new service-count constant is added for this documentation change.

On the final source run document metadata/relationship/lifecycle checks,
local document links and `git diff --check`; select through the current changed
profile with `--explain`, without substituting a local aggregate candidate
run for the hosted PR. Run the existing agent-authority checker to establish
whether SPEC-0221 already meets the request. No public full/private env render,
LAB check, container run or secret read is part of P00.

W14–W15 add no live validation. They use tracked source and public Git metadata
only. HOME, migration, rotation, deletion, native workflow execution and empty
target restoration remain NOT_RUN until their owning Task identifies the exact
resource, approved operator/window, backup set and recovery boundary. A P08
document move waits for the feature-owner path freeze and a single move writer;
the confirmed duplicate README headings and stale domain wording are source
findings, not permission to move LAB runtime assets.

W24 records only tracked, value-free source and authenticated public Git
observations. `SOURCE_APPLIED`, `STATIC_PASS`, `ISOLATED_PASS`, `NATIVE_PASS`,
`HOME_PASS`, and `RECOVERY_PASS` are ordered domains; no lower domain implies a
higher one. A local changed no-op or `full --explain` selection is not hosted
required-check coverage. Missing live targets remain `BLOCKED` or `NOT_RUN`.

After independent review, validate the Conventional Commit message and run
`scripts/validation/run-ci-precommit.sh --mode local-staged` on the exact
staged set. Read actual branch protection and PR checks. Push this request's
branch, create its PR and attach it; merge only when its current review/check
conditions are satisfied. Record hosted results separately from local results.

For r10, select the smallest checks that establish each changed guarantee.
Content-only edits use changed metadata, relationships, links and diff checks;
Registry/parser/permission/workflow changes add their directly affected
regressions. Use synthetic repositories and DBs for failure probes. Record
actual commands, revisions, result and elapsed observations once. Hosted CI,
real provider effectiveness, HOME backup/restore and remote main protection
remain separate observations. Never create credentials or change managed
settings to make a source check pass.

P01 adds meaningful Git/non-Git, symlink, duplicate declaration, ownership,
secret-boundary, stale-review, permission, cancellation and atomic-output probes.
The new executable code must achieve at least 80% coverage. Manifest/CI selection,
metadata, links and Registry checks accompany the source unit. Current direct
operation, credential rotation, independent restore, hosted CI and final operator
acceptance stay NOT_RUN unless separately observed. Compare the initial and
final public manifests and review only affected rows after a source change.

## Risks and Recovery

### Risks and Rollback

Revert only the logical W13 documentation commit through a protected PR to
restore the prior active contract; preserve historical Tasks and issued IDs.
No service, credential, data, volume or host state changes, so no runtime/data
rollback is claimed. Equal baseline, merged draft and historical runtime PASS
must not be promoted to fresh validation. A concurrent shared-writer/path
change invalidates affected inputs and requires a fresh scoped check.

Revert W24 as its isolated documentation unit through the protected PR path;
do not revert an independent owner’s implementation with it. Before a secret
rotation, data migration, retirement, or live upgrade, the owner records the
concrete target, backup identity, restore boundary, compatibility result,
operator/window, stop condition, and rollback. Missing prerequisites block
only that dependent operation.

## Related Documents

- [Master workspace reconciliation](tasks/tsk-0053-master-workspace-reconciliation.md)
- [v14.7 W00 intake](tasks/tsk-0059-w00-v14-7-intake.md)
- [v14.7 W01 governance](tasks/tsk-0060-w01-v14-7-governance.md)
- [Existing supply-chain evidence owner](tasks/tsk-0052-supply-chain-evidence.md)
- [Memory capacity and search](../0270-shared-memory-capacity-and-search/spec.md)

- [Workspace inventory Task](tasks/tsk-0040-workspace-inventory.md)
- [Opsflow data path Task](tasks/tsk-0043-opsflow-data-path.md)
- [Opsflow notifier recovery Task](tasks/tsk-0044-opsflow-notifier-recovery.md)
- [Secret structure and OpenBao contract Task](tasks/tsk-0045-secret-structure-openbao.md)
- [Exporter and observability contracts Task](tasks/tsk-0046-exporter-observability.md)
- [Image, supply-chain and Storybook compatibility Task](tasks/tsk-0047-image-supply-chain-storybook.md)
- [Role, resource and retirement input Task](tasks/tsk-0048-role-resource-retirement.md)
- [Documentation, governance, QA and CI contract Task](tasks/tsk-0049-document-governance-qa-ci.md)
- [Hermes provenance, trust and export Task](tasks/tsk-0050-hermes-provenance-trust-export.md)
- [Opsflow first HOME installation Task](tasks/tsk-0051-opsflow-home-installation.md)
- [Workspace inventory data](../../90.references/data/0096-workspace-inventory/README.md)

- [Spec](spec.md)
- [R10 reconciliation Task](tasks/tsk-0007-r10-reconciliation.md)
- [Infrastructure audit execution Task](tasks/tsk-0008-infra-audit-execution.md)
- [Historical link classification Task](tasks/tsk-0010-historical-link-classification.md)
- [SMTP01 request contract Task](tasks/tsk-0005-smtp01-request-contract.md)
- [Current coordination audit Task](tasks/tsk-0006-current-coordination-audit.md)
- [Completed P00 Task](tasks/tsk-0003-active-contract-and-exclusions.md)
- [Historical baseline Task](tasks/tsk-0001-request-baseline-and-inventory.md)
- [Historical twenty-item Task](tasks/tsk-0002-twenty-item-reconciliation.md)
- [Integration plan](../0204-service-integration-security-and-operations/plan.md)
