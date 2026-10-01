---
title: "Operations Documentation System Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0198-PLAN-0001"
parent_ids:
- "SPEC-0198"
created: "2026-10-01"
---

# Operations Documentation System Implementation Plan

## Objective

Implement approved [SPEC-0198](spec.md): audit every current service and all
225 baseline role documents, fill required/implemented-content gaps, consolidate
without losing meaning, reconcile version-specific contradictions, and connect
service operations to whole-system operation through the existing role layout.

Procedure after written-plan approval: `superpowers:subagent-driven-development`
or `superpowers:executing-plans`, according to the user's execution-method choice.
Recommended: bounded subject/tier implementers with independent review because
225 bodies and many product versions require substantial separate attention.
Shared indexes, registry and system documents have one integrating owner.
Technology: Markdown, existing Python document validators, Compose/YAML source
inspection and official product/version documentation. No new dependency.

## Dependencies

- Written Spec approved by the user on 2026-10-01, including exhaustive topic
  coverage, lossless consolidation and current-version contradiction resolution.
  Frontmatter remains draft for initial registration; do not fabricate committed
  lifecycle transitions. Implementation is authorized by the user's written Plan approval.
- Use SPEC-0197's reviewed twelve-tier layout. Before editing, inspect the
  current branch/base, its final validation receipt, concurrent work and actual
  source inventory. Do not interpret an uncommitted dependency as merged main.
- Read bootstrap/provider, doc-writer role, documentation protocol, Stage 99
  operation profiles/templates and the applicable operations skill explicitly.
  Stateful recovery instructions require the existing stateful-recovery review.
- Preserve concurrent SPEC-0182/SPEC-0193 work. RUN-0098 is currently tied to
  SPEC-0182: consume its existing procedure by link; coordinate any necessary
  edit to a concurrently changing operational owner before touching its body.
- Scope excludes runtime mutation, external publication and implementation
  repairs. A discovered security/control defect requires read-only security
  review and a separate remediation decision, not weaker policy text.

### Global constraints

Write Spec, Plan and Task prose in English. Write Stage05 Guide, Policy and
Runbook explanatory prose, and README prose, in Korean. Preserve registered
headings, identifiers, commands, paths, metadata and technical names. Preserve
actual historical quotations with source context and the required explicit
quotation marker; a dated heading alone does not exempt current instructions.
Numeric language checks supplement semantic review rather than replace it.

Keep role-first paths, issued IDs, subject slugs, unique Guide service ownership
and service-bound Guide/Policy/Runbook siblings. Non-service subjects need only
applicable roles. Link shared content and state service-specific differences.
No tier directory migration, duplicate service registry, frozen-history edit,
secret access, live probe/rehearsal or speculative recovery procedure.

### Review focus

1. A helper/provisioning service disappears inside a grouped subject: W1/W3-W6
   compare all exact Compose identities to the evidence matrix, not package count.
2. A shared link silently drops a local exception: W3-W7 compare every moved
   instruction/constraint to its final section and explicit applicability.
3. A mutable tag is treated as an exact runtime version: W1/W3-W6 record source
   pin/digest/build or explicit uncertainty and matched official evidence.
4. Policy contradicts implementation: W3-W7 distinguish editorial drift from
   implementation nonconformance; preserve the control and state the gap.
5. A syntactically valid recovery is claimed proven: W2/W3-W7 separate static,
   read-only source and runtime evidence, with expected signals and stop points.

## Execution Sequence

### File ownership and exact baseline map

All filenames below are under the existing
`docs/05.operations/{guides,policies,runbooks}/` role roots **where that file
already exists**. W1 resolves this table into exact full paths and artifact IDs;
never create absent role siblings merely because a filename is listed here.
The historical Airflow exception remains Guide 0051 / Policy 0052.

| Work unit | Existing index classification | Existing leaf filenames |
| --- | --- | --- |
| W7 | 00 Workspace | `0001-common-optimizations-template-exceptions.md`, `0002-developer-environment.md`, `0003-env-key-comparison.md`, `0004-harness-agent-first-engineering.md`, `0006-infrastructure-optimization-governance.md`, `0008-new-service-onboarding.md`, `0009-release-management.md`, `0010-sensitive-env-vars-comparison.md`, `0078-compose-profile-vocabulary.md`, `0086-dependency-version-management.md`, `0098-cold-start-and-reboot.md` |
| W3 | 01 Gateway | `0011-nginx.md`, `0012-edge-routing-stack.md`, `0013-traefik.md` |
| W3 | 02 Auth | `0014-keycloak.md`, `0015-oauth2-proxy.md`, `0079-application-auth-integration.md` |
| W3 | 03 Security | `0085-openbao.md` |
| W4 | 04 Data | `0017-influxdb.md`, `0019-opensearch.md`, `0021-backup-and-restore.md`, `0022-valkey-cluster.md`, `0024-seaweedfs.md`, `0025-cassandra.md`, `0026-couchdb.md`, `0027-mongodb.md`, `0028-management-database.md`, `0029-supabase.md`, `0030-data-optimization-hardening.md`, `0031-postgresql-cluster.md`, `0032-postgresql-logical-upgrade-restore-rehearsal.md`, `0033-neo4j.md`, `0034-qdrant.md`, `0035-storage-exhaustion.md` |
| W4 | 05 Messaging | `0036-kafka.md`, `0037-messaging-optimization-hardening.md` |
| W5 | 06 Observability | `0039-alertmanager.md`, `0040-alloy.md`, `0041-grafana.md`, `0042-lgtm-stack.md`, `0043-loki.md`, `0044-observability-optimization-hardening.md`, `0045-prometheus.md`, `0046-pushgateway.md`, `0047-pyroscope.md`, `0048-telemetry-retention.md`, `0049-tempo.md`, `0087-gatus.md` |
| W5 | 07 Workflow | `0050-airflow.md`, `0051-airflow-dag-lifecycle.md`, `0052-airflow-dag-lifecycle.md`, `0053-n8n.md`, `0054-workflow-optimization-hardening.md` |
| W5 | 08 AI | `0055-gpu-recovery.md`, `0056-ollama.md`, `0057-open-webui.md`, `0058-ai-optimization-hardening.md`, `0059-rag-workflow.md`, `0081-comfyui.md`, `0091-crawl4ai.md` |
| W6 | 09 Tooling | `0060-iac-deployment.md`, `0061-k6.md`, `0062-locust.md`, `0063-tooling-optimization-hardening.md`, `0064-performance-testing.md`, `0065-registry.md`, `0066-sonarqube.md`, `0068-terraform.md`, `0069-terrakube.md`, `0082-opentofu.md`, `0083-renovate.md`, `0092-wiremock.md`, `0093-pact-broker.md`, `0095-conftest.md` |
| W6 | 10 Communication | `0070-mail.md`, `0084-mailpit.md` |
| W6 | 11 Laboratory | `0072-dozzle.md`, `0073-open-notebook.md`, `0074-laboratory-optimization-hardening.md`, `0076-redisinsight.md`, `0080-surrealdb.md`, `0088-mlflow.md`, `0089-jupyterlab.md` |
| W4 | 12 Analytics | `0090-dbt.md`, `0094-lakehouse.md`, `0097-superset.md` |
| W7 | Infra Net | `0077-ip-address-management.md`, `0096-k8s-integration.md` |

The integrating executor owns `docs/05.operations/README.md`, the three role
`README.md` files, registry allocation and this package's Plan/Tasks. W2 creates
`guides/0099-system-operations.md` after verifying allocation is still free;
optional same-subject Policy/Runbook are justified by the audit, not pre-created.
Current observed highest role number is 0098, while the registry's operations
cursor is stale at 0088. Reconcile issued IDs and advance monotonically before
allocating; never reuse 0088. If concurrent allocation occupies 0099, allocate
the next free number and record the resolved path in W1 before W2 starts.

Existing implementation files under `infra/`, scripts, Compose and current
architecture are read-only evidence. Changes to validators are exceptional,
bounded by a reproduced structural gap, and owned by the integrating executor.
No worker edits another wave's files or reverts another worker's changes.

### W1: Baseline, exhaustive evidence ledger and source versions

Owner: integrating executor. Creates
`tasks/tsk-0001-baseline-and-integration.md`; later waves create their numbered
Tasks listed below. Consumes current source plus the approved Spec; produces
an exact document/service manifest and shared evidence format.

- [x] Capture base SHA, all role artifact IDs/full paths/statuses and each
  Guide's `implementation_services`; reconcile the 225/87/153 dated baseline.
- [x] Assign every current role leaf to exactly one of W3-W7; identify common
  owner files needed by W2 without giving parallel writers ownership of them.
- [x] Inventory source version evidence from Compose, inherited declarations,
  Dockerfiles and declared package pins. Separate immutable pins, mutable tags
  and unverified runtime versions. Reuse the existing image projection as a
  discovery aid, not as a replacement for Dockerfile/build evidence.
- [x] Define evidence rows in the owning Task: artifact/service identity,
  required topic, implementation location, declared version certainty,
  official URL/release/section, finding, old section, final owner/section,
  applicability/exception, action, check and reviewer result. Do not introduce
  a parallel JSON service registry or automated semantic score.
- [x] Run `python3 scripts/validation/check-operations-catalog.py`; expected
  PASS. Preserve initial failures with their source before correcting them.
- [x] Establish the existing-test baseline and commit boundaries without
  claiming future results. Do not mark any body reviewed from its filename.

### W2: Shared content owners and system operating entrypoint

Owner: integrating documentation writer. Evidence goes in
`tasks/tsk-0002-system-operations.md`. Consumes W1 manifest and existing AD-0031,
RUN-0098, POL-0006/POL-0078 and subjects 0021/0077/0086.

- [x] Map shared operating topics to existing content owners. Identify exact
  missing system explanation/decision flow before authoring new material.
- [x] Author the allocated `system-operations` Guide: reader purpose, system
  and tier responsibilities, actual request/auth/data paths, shared dependencies,
  profile/readiness distinctions and links to common policies/procedures.
- [x] Add a same-subject cross-service diagnostic Runbook only for a demonstrated
  gap: symptom -> safe observation -> decision -> existing service procedure.
  No copied service recovery sequence or invented isolation environment.
- [x] Retain existing common Policies unless a concrete missing cross-service
  control warrants a same-subject Policy. Record the addition or omission reason.
- [x] Update existing navigation with system/tier/service routes and cross-cutting
  categories. Explain service-bound required triplets versus optional roles
  for other subjects; keep each leaf's index membership exactly once.
- [x] Check coverage manually for startup/reboot, authentication, backup/recovery,
  upgrades, capacity and cross-service diagnosis. Missing implemented capability
  must have an explicit limit and remediation owner instead of an empty section.
- [x] Run catalog, metadata and link checks. Independent review verifies dependency
  and readiness claims against source; static PASS is not runtime recovery PASS.

### Common procedure for W3-W7

Each wave owns the exact manifest paths assigned by W1, plus its Task. Read all
bodies, including tables/examples/notes/related links; sampling is insufficient.
Use the Spec's required topic groups for every service identity. Shared evidence
may cover an explicit set of named identities only after differences are checked.

- [x] Read each role triplet/available subject documents and all corresponding
  implementation/README/build/script sources; identify missing applicable topics.
  For Compose-built services, resolve the selected Dockerfile/context/args/target
  and inspect FROM, package installation, COPY sources and ENTRYPOINT/CMD; record
  effective overrides and uncertainty rather than relying on the image label.
- [x] Research version-dependent claims in official product documentation and
  release notes matched to declared versions. Record URL/release and uncertainty;
  do not use latest upstream behavior as evidence for an older source pin.
- [x] Record all current instructions/constraints and findings before editing.
  Separate missing/incomplete content, duplicate ownership, contradictory claims,
  implementation nonconformance, non-applicable topics and unsupported capability.
- [x] Fill missing supported content and relocate role-mixed material in place.
  Preserve source-to-final section mappings, local exceptions and meaningful
  warnings. Guides explain, Policies constrain, Runbooks execute and recover.
- [x] Reconcile conflicts with source/version evidence. Preserve required controls
  when implementation is deficient; document the limitation and separate remedy.
  Do not claim an implementation defect was fixed by editing Markdown.
- [x] Check each Runbook's target, prerequisites, command effects, expected result,
  failure/stop branches, validation, recovery and accountable escalation boundary.
  Inspect syntax/source safely; run no live command merely to prove a document.
- [x] Reconcile every matrix cell and original section. Run existing catalog and
  link checks, then obtain independent semantic review of the complete owned
  batch. No unresolved material documentary contradiction may be marked complete.
- [x] Prepare a coherent documentation commit for the batch; commit only under
  applicable delivery authorization. Preserve the exact review/check receipts.

### W3: Gateway, identity and security

Execution receipt: W3 source/content work complete and independently approved;
the minor receipt-count clarification is recorded in Task0003 (final10286 links).

Files: W3 rows above. Task: `tasks/tsk-0003-gateway-auth-security.md`.
Consume W2 common owners; produce complete service-specific applicability and
lossless role separation for these subjects. Apply every common step above.

Pilot findings to verify against the execution base: duplicated Nginx/Traefik
Guide recovery steps and Runbook recovery sections; mandatory controls under
Disallowed; Traefik chain policy versus membership; Nginx HTTP health redirect;
mutable Nginx tag; authentication dependencies and placeholder `/app` behavior;
Traefik401/403 handling and activation/bind inputs. These are source findings,
not live observations. Independent security review owns any security inference;
route implementation fixes outside this documentation plan.

Independent read-only security review confirmed two source-level limitations:
Traefik's declared limiter is absent from the chain consumed by routers
(Important implementation nonconformance); Nginx's placeholder `return` finishes
before auth/access handlers (Minor for the current placeholder-only route).
The backend proxy is commented out; do not claim protected backend exposure.
Official evidence: [Traefik v3.7 Chain](https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/http/middlewares/chain/),
[RateLimit](https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/http/middlewares/ratelimit/),
[Nginx request phases](https://nginx.org/en/docs/dev/development_guide.html) and
[return](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html#return).
No live exposure or deployed version was observed; both implementation fixes
remain outside this Plan's documentation execution authority.

### W4: Data, messaging and analytics

Files: W4 rows above. Task: `tasks/tsk-0004-data-messaging-analytics.md`.
Apply every common step. Preserve lakehouse subject ownership across storage
initialization and engines; cover every helper/provisioning identity explicitly.
Check persisted versus derived state, feature grants, shared PostgreSQL/Valkey,
SeaweedFS catalog/bucket policy, authentication, backup/restore and destructive
maintenance boundaries. Use stateful-recovery review before authoring executable
recovery steps. Never infer HA from multiple containers on one host.

W4 execution receipt, 2026-10-01: all59 leaves and87 service identities, including13 built identities/eight Dockerfiles, reviewed. Independent fix1 re-review: Spec PASS, quality ACCEPT; three Important and three Minor findings addressed, no new findings. Focused metadata/catalog/links/diff PASS; runtime NOT_RUN. Final integrated gate remains W8.

### W5: Observability, workflow and AI

Files: W5 rows above. Task: `tasks/tsk-0005-observability-workflow-ai.md`.
Apply every common step. Coordinate current SPEC-0193 document ownership;
check telemetry ingestion versus storage/retention, usable alert evidence,
workflow state and side effects, model/GPU capacity, authentication and provider
access. Keep the existing Airflow Guide/Policy ID exception. No trace/log output
containing private data is needed for this source/document audit.

W5 receipt, 2026-10-01:60 leaves,34 identities,306 topic cells and12 built identities audited. Independent final Spec/quality PASS; final61-file packet confirmed. Runtime NOT_RUN; documented implementation gaps and W8 integration remain open.

### W6: Tooling, communication and laboratory

Files: W6 rows above. Task: `tasks/tsk-0006-tooling-communication-laboratory.md`.
Apply every common step. Distinguish persistent UI services from one-shot jobs,
load generators and optional experiments; explain publication/authentication,
mail/data durability, dependency and cleanup effects. Do not claim experiments
are physically isolated merely because they use a separate profile or tier.

W6 receipt, 2026-10-01:67 leaves,24 identities,216 topic cells and8 built identities accepted by independent final Spec/quality review after three bounded corrections. Original683 heading mappings and four historical payloads preserved. Focused checks PASS; runtime NOT_RUN.

### W7: Workspace, cross-cutting subjects and whole-system reconciliation

Files: W7 rows above and final shared-owner amendments agreed with W2.
Task: `tasks/tsk-0007-cross-cutting-reconciliation.md`.
Apply every common step to non-service subjects using their actual applicable
roles. Reconcile existing requirements, policy exceptions, release/profile and
version rules, networks, backup, reboot and cross-repository dependencies.
Preserve factual incident records and dated rehearsal evidence. Check the final
system Guide links to the resulting canonical owners and has no obsolete service
boundary. Coordinate any RUN-0098 body change with its current SPEC-0182 owner.

W7 receipt, 2026-10-01:21 common leaves accepted by independent fix-round1 review; four findings closed,71 profile memberships and RUN-0098 history preserved. Parent reconciles adjacent metadata/revocation wording before the frozen W8 gate.

### W8: Integrated verification and completion receipts

Owner: integrating executor plus fresh independent reviewer. Evidence lives in
W1 Task, referencing all wave Tasks; no second status ledger.

- [x] Compare final artifact/service sets to W1: all baseline members accounted
  for, issued IDs stable, new allocations explained, no duplicate owner/index row.
- [x] Check all topic cells and old-to-final section mappings. Document each
  non-applicable item and implementation limitation; no unexplained omission.
- [x] Run the verification commands below on the final source state and repair
  only scoped defects. Existing structural checks do not replace semantic review.
- [x] Have an author-independent reviewer inspect all wave receipts and changed
  owners, verify version-sensitive corrections and trace common links end to end.
- [x] Map Spec criteria 1-7 to actual outcomes and document locations in the Task;
  mark runtime/recovery/hosted CI NOT_RUN unless separately executed and authorized.
- [x] Finish only after source criteria pass and no material documentary conflict
  remains. Runtime implementation gaps remain explicitly unremediated; remote
  publication, merge and historical disposition require their own authorization.

## Risk and Rollback

Keep immutable historical facts and preserve every meaningful active constraint.
The main risks are silently dropped exceptions, wrong-version instructions,
duplicated ownership and unsupported recovery confidence. Evidence mappings and
independent review address these directly. Restore a rejected document batch
with its inbound links together; never reset unrelated files or runtime state.

If common-owner changes overlap, the integrating owner resolves them before a
wave continues. Security findings go to independent security review, and any
configuration repair returns to approved implementation scope. A source audit
must not expand into reading credentials or running service/recovery commands.

## Verification

| Check | Required result | Spec criteria |
| --- | --- | --- |
| W1 manifest vs final documents, service identities and topic matrix | Exact coverage; each exception justified | 1, 4, 5, 7 |
| Old-section to final-owner mapping and official version evidence | No lost substance or unsupported conflict resolution | 4, 5 |
| `python3 scripts/validation/check-operations-catalog.py` | PASS, unique service bindings and current required siblings | 2, 4, 6 |
| `python3 scripts/validation/check-document-metadata.py --mode check-contracts` | violations=0 | 2, 6 |
| `python3 scripts/validation/check-document-links.py --mode all` | failures=0; pre-existing history warnings disclosed | 2, 3, 6 |
| `python3 -m unittest tests.lib.document_governance.test_operations_catalog tests.lib.document_governance.test_operations_taxonomy` | PASS | 2, 4, 6 |
| `python3 scripts/validation/run-ci-gate.py --profile changed` | Registered selected checks PASS | 6 |
| Independent semantic/security review where applicable | No unresolved material documentary discrepancy | 3, 4, 5, 6, 7 |

Do not write tests that merely mirror edited prose. If a reproduced structural
checker gap needs code, add its smallest RED/GREEN regression to the existing
operations module/test owner and measure at least 80% changed executable lines.
No new checker or runtime test is planned absent such a gap. Source verification,
live procedure validation and recovery rehearsal remain separate evidence types.

Execution complete, 2026-10-01: all source/document work units and independent reviews accepted; final `python3 scripts/validation/run-ci-gate.py --profile changed` exit0. The reviewable packet is staged but uncommitted. Live deployment/recovery, installed-unit refresh and remote publication remain outside this completion. Detailed outcomes, earlier failed attempts and remaining implementation limits are preserved in the canonical Tasks.

## Rulings

- Written Spec approval: user, 2026-10-01. Plan approved by the user on 2026-10-01; tier-scoped subagent implementation
  with independent review selected.
- Canonical Stage03 Plan/Tasks override generic skill output/progress paths.
- This is one integrated documentation contract; tier waves have disjoint file
  ownership but share common owners and one final service join.
- Mandatory service siblings remain. Common-content reuse is explicit linking
  and local applicability, not deletion of required documents.
- Pilot Gateway findings inform the worklist; they do not prove other subjects
  were reviewed. All 225 current bodies and every current service/topic are audited.
- Do not change source pins, relax controls, alter running services or invent
  recovery evidence to turn a documentation discrepancy into a false PASS.
