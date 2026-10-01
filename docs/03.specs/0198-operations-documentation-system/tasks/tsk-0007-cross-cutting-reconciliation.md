---
title: "W7 Cross-Cutting Operations Reconciliation"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0198-TSK-0007"
parent_ids:
- "SPEC-0198"
- "SPEC-0198-PLAN-0001"
created: "2026-10-01"
---

# W7 Cross-Cutting Operations Reconciliation

## Objective

Reconcile the exact21 cross-cutting role leaves (8 Guides,7 Policies,6 Runbooks), preserve meaningful instructions and approved controls, and correct audited source contradictions. This Task records authoring, focused static evidence and independent acceptance; the parent-owned final integrated gate passed; Task0001 records the result.

## Inputs

- [Spec](../spec.md), [Plan](../plan.md), [W1](tsk-0001-baseline-and-integration.md), [W2 common owners](tsk-0002-system-operations.md).
- Read bootstrap/provider, documentation protocol, environment constraints, doc-writer role, repository ownership map, all three registered operations templates and the Task template. Applied the local ops-runbook-agent skill; read stateful recovery review boundaries without issuing a recovery acceptance verdict.
- Read complete before/current bodies of all21 leaves, referenced public source and common owners. Prepared audit findings A01–A33, supplied shared findings S01–S21 and independent gateway/security review informed these changes. Reused official-source evidence; no new broad research or inferred deployment observation.
- Base Git revision: `c26bc8026254dffd7d51fc45b4081a1f80f855f2`. Parent owns the approved SPEC-0197 package moves, final09-platform-ops naming, shared indexes and package README integration. No runtime or activation change follows from the tier move.

## Work Log

### Scope and boundaries

Only the21 role leaves below and this new Task were edited by W7. Stage05 explanatory prose is Korean; this Task is English. Required headings, commands, IDs and technical names retain their form. Dated quotations use the exact historical marker and source context. No service triplet or capability was invented for cross-cutting subjects.

W6's67 leaves, shared indexes, GDE-0099 and other Tasks remain parent/other-author owned. Before RUN-0098 body write, main HEAD matched the base above, main RUN-0098/SPEC-0182 scope was clean, worktree SPEC-0182 was clean, and RUN-0098 bytes matched the handoff snapshot containing only the parent's approved Restic prefix change. The complete2026-09-30 Verification Record table payload was asserted byte-identical before writing. This is historical evidence, not a new rehearsal.

No private `.env`/secret values, runtime, builds, pulls, provider calls, cluster operations, host configuration, staging, commits or full gate were performed. Source/CLI inspection does not establish native-hook execution, service availability, credential rotation, restore success or deployment behavior.

### Exact leaf dispositions and source-to-final preservation

All entries are revisions of existing bodies. Instructions not specifically moved or corrected retain their role owner. Invalid success claims are replaced by bounded failure/stop instructions, never by weaker controls.

| Artifact and exact leaf | Source-to-final disposition and preservation |
| --- | --- |
| `GDE-0002` `docs/05.operations/guides/0002-developer-environment.md` | Purpose/audience, Bash/WSL, local permissions and protected inputs -> Usage / Local tools and configuration / Certificates and Common Checks; certificate mutation -> RUN-0013. Generic self-description replaced by concrete scope. Compose include compatibility is bounded, not an installed-version claim. |
| `GDE-0003` `docs/05.operations/guides/0003-env-key-comparison.md` | Original exact-set checks, indirect consumers, protected backup/prune and Value preservation retained in Usage; dry-run versus private-reading metadata comparison and exit0/1/2 clarified. No new same-number Runbook created. |
| `GDE-0004` `docs/05.operations/guides/0004-harness-agent-first-engineering.md` | Usage authority/navigation retained; ordered audit/CI mismatch execution -> RUN-0004 Checklist and CI quality-gate version alignment. Source/native evidence limits retained. Dated PR169/CI follow-up retained as exact historical quotations. |
| `GDE-0008` `docs/05.operations/guides/0008-new-service-onboarding.md` | Original onboarding seed, approval, pin, secret and Spec Package controls retained; seed integration gaps and required service Guide binding added in Usage. Runtime delivery/recovery -> service Runbook; release readiness -> RUN-0009. |
| `GDE-0010` `docs/05.operations/guides/0010-sensitive-env-vars-comparison.md` | All metadata/ID/Value/indirect-consumer and secret-file controls retained in Usage. Public-only dry-run versus private-reading metadata check clarified; exact-shape control remains unchanged. |
| `GDE-0077` `docs/05.operations/guides/0077-ip-address-management.md` | Original purpose, flow, IPAM example and pitfalls -> Usage / network scope / Common Checks. Numbered source-change/check sequence -> RUN-0077 Procedure. Root/external/leaf-owned networks and actual membership distinguish isolation from tier labels. |
| `GDE-0086` `docs/05.operations/guides/0086-dependency-version-management.md` | Original image/build/update explanation and pitfalls retained in Usage. Build authority extended to installed/copied requirements and entrypoint; current Guide bindings own service classification; Stage90 research remains provenance. |
| `GDE-0096` `docs/05.operations/guides/0096-k8s-integration.md` | Original contract/handoff/pitfalls retained. Tempo3200 query/API separated from Alloy4317/4318 ingestion; exact ESO and bootstrap permissions, configurable defaults, Basic route selection and source rotation block explained. |
| `POL-0001` `docs/05.operations/policies/0001-common-optimizations-template-exceptions.md` | Original exception/control/review requirements retained; current JSON remains sole exception owner. Dated subset is exact historical quotation. Accountable owner and check-coverage limits clarified without waiving requirements. |
| `POL-0004` `docs/05.operations/policies/0004-harness-agent-first-engineering.md` | All governance/source/native/hook safety/verification controls retained. Stale fixed counts and permanent domain exclusions removed; canonical registry and approved affected scope own selection. Procedures remain RUN-0004. |
| `POL-0006` `docs/05.operations/policies/0006-infrastructure-optimization-governance.md` | All score weights, roadmap status, backlog service items and minimum controls retained. Old census explicitly historical; catalog moved under final tier headings while preserving proposal text and priority. Executable mount apply -> RUN-0086; coverage remains mandatory. ADR-0042 manual unseal remains current. |
| `POL-0077` `docs/05.operations/policies/0077-ip-address-management.md` | Original no-duplicate/static reason/dynamic-pool/no-bridging controls retained. Root scope and incomplete static-IP enforcement clarified; implementation limitation does not weaken policy. |
| `POL-0078` `docs/05.operations/policies/0078-compose-profile-vocabulary.md` | Profile/HOME machine table schemas and memberships preserved. Historical eight-profile observation marked exact quotation; selector effects, optional dependencies and conditional port collisions clarified. Tier move does not activate services. |
| `POL-0086` `docs/05.operations/policies/0086-dependency-version-management.md` | Original update/major approval/digest/architecture/timestamp/uncertainty controls retained. Added narrow Renovate infra requirements owner separate from manually reviewed CI/test/hook pins. |
| `POL-0096` `docs/05.operations/policies/0096-k8s-integration.md` | Original LAN exceptions, no k3d membership, roles, TTL, transfer and three-way rotation controls retained. Wildcard shorthand replaced by five exact paths; operator/root distinction and success/fail/indeterminate verification clarified. |
| `RUN-0004` `docs/05.operations/runbooks/0004-harness-agent-first-engineering.md` | Original procedure/evidence/recovery preserved; receives Guide CI alignment sequence. Preflight effects precede gate; each tracked shell checked independently; Graphify absent guard and source/native limits retained. |
| `RUN-0009` `docs/05.operations/runbooks/0009-release-management.md` | Original manual release procedure and complete sample-delivery v2/v3/v4 identity/cleanup contract retained. Explanatory prose translated; committed base/candidate diff added, obsolete freshness removed, static versus runtime/remote approval clarified. |
| `RUN-0077` `docs/05.operations/runbooks/0077-ip-address-management.md` | Original change/check/recovery intent -> exact target preconditions, source changes, sanitized validation and scoped status inspection. No full inspect disclosure or blind network disconnect/delete. Source rollback remains distinct from runtime apply. |
| `RUN-0086` `docs/05.operations/runbooks/0086-dependency-version-management.md` | Original updater/version/backup/escalation obligations retained. Explicit --write added. Static configuration validation owns temporary/private input effects. Runtime configuration apply absorbs recreate/hash steps and rejects DIFF/UNREADABLE/query failure/empty coverage. |
| `RUN-0096` `docs/05.operations/runbooks/0096-k8s-integration.md` | Seven triggers and eight phases retained; cluster rebuild includes5.5 and fresh ESO auth; root ceremony -> canonical RUN-0085; explicit response classifications replace failure-as-denial/revocation. Grafana creation/token/custody and optional app handoffs preserved. Ineffective Prometheus rotation is BLOCKED before mutation. Cleanup preserves server revocation and snapshot custody. |
| `RUN-0098` `docs/05.operations/runbooks/0098-cold-start-and-reboot.md` | Current reboot procedure corrected after protected-owner precheck: persistent/job restart distinction, container-side PG expansion, manual unseal, full renderer verification, existing kubeconfig and explicit owner mutation branches. Parent Restic prefix retained; dated2026-09-30 table payload byte-identical; SPEC-0182 untouched. |

### Finding resolution

| Findings | Resolution owner / final disposition |
| --- | --- |
| A01–A04,A09–A10 | GDE-0002/0003/0008/0010: environment, certificate and metadata effects; onboarding seed adaptation; no private-read authorization inferred |
| A05–A08 | 0004 triplet: authority versus procedure, CI alignment, actual shell coverage, Graphify guard and source/native distinction |
| A11–A14,A22 | 0077 triplet: actual root/leaf/external scope, mandatory static controls despite incomplete validator, source-only edits versus runtime membership |
| A15–A17,A20 | 0096 triplet: configurable host contracts, Tempo API versus Alloy ingest, Basic/SSO distinction and exact least privilege |
| A18–A19 | POL-0001/0006: current exception registry, historical census and roadmap, preserved controls and backlog |
| A21 | RUN-0009: committed candidate range, Korean prose and exact delivery evidence contract |
| A23–A32 | RUN-0096: CA rebuild5.5, canonical root ceremony, root/bootstrap verification, protected workdir/custody, guarded Grafana token issuance, source-blocked Prometheus rotation and consumer-specific evidence |
| A33,S13–S20 | RUN-0098 current corrections under parent handoff; protected historical payload retained |
| S01–S03 | 0086 triplet: explicit writer mode, build/dependency owner and narrow updater scope |
| S04–S07 | POL-0006 and RUN-0086: source scope versus backlog; complete mount coverage, helper effects and result classifications |
| S08–S12 | POL-0078: exact profile/HOME tables, selection/dependency/port and readiness limits |
| S21 | RUN-0086 static input/effect owner linked from cross-cutting checks |

### Nine-topic applicability matrix

Cross-cutting subjects do not claim service image/runtime identities. The following ten subject groups cover all21 leaves across the nine required operating topics; service-specific mechanisms are linked to their existing owners.

| Subject set | Purpose / classification | Entrypoint / versions / readiness | Access / credentials | Configuration / persistence | Signals / resources | Rules / owner | Lifecycle execution | Diagnosis / stop | Backup / restore / cleanup |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0002 developer environment | GDE0002 local workspace; HOME state not implicitly selected | root/README/provider; compatible Compose and Bash; no installed version claim | canonical permission owners; mkcert host trust | public env and protected local files; no copied private files | tooling/check outcomes, no runtime SLA | governance + POL0006/0078/0086; @buenhyden | bounded setup Guide; cert RUN0013, runtime subject Runbooks | unavailable tools/unknown target stop; preserve local state | preserve existing env/certs; cert/secret subject handoff, no DB restore for workspace docs |
| 0003/0010 metadata | public/private schema comparison, all supported consumers | gen-secrets source contract; no service image | public-only vs privately reading check distinguished | stable IDs, exact key/metadata sets, Value preservation | exit0/1/2, value-free output; no health/resource metric applicable | existing metadata/secret ownership and explicit prune approval | existing bounded sync/how-to; generation/rotation separate | duplicates/ambiguous input/concurrent edits stop | protected0700/0600 backups, scoped restore, no secret-file deletion |
| 0004 harness | current governance and source/native boundary | current adapters/registry/CI; Graphify validity | tracked scoped tools, no global config edits | canonical source vs generated projection; fixture-only evaluation | gate outcomes, no live-native result inference | POL0004 links canonical authority | RUN0004 validation/authorized renderer path | failed/blocked/skipped counts distinct, scoped remediation | Git hunk recovery; no state restore for stateless checks; guarded projection regeneration |
| 0001/0006 shared hardening | every tracked included service, source vs backlog | template/exception JSON, no count-as-scope | retain security and exposure/secret rules | single-file config mount and mandatory apply verification | limits/health controls, static coverage limits | Policies own requirements, exceptions, owner and review | RUN0086 plus service owners, no duplicated deployment | DIFF/UNREADABLE/coverage stop and escalation | POL0021 plus service recovery; no blanket downgrade/rebuild |
| 0008/0009 onboarding/release | seed adaptation and manual candidate readiness | sample Dockerfile/Compose, current gates, actual tag workflow | no raw config, explicit publication/runtime boundaries | Guide bindings, templates, manifests and exact source pins | static vs healthy/function/hosted distinctions | POL0001/0006/0078/0086 and governance | RUN0009 release readiness; service Runbooks execute delivery | candidate commit range, failures stop, no universal rollback | changed-state backup/N/A, exact sample identity cleanup, per-service recovery |
| 0077 networks | peer flow not tier/isolation shorthand | root/leaf declarations, include compatibility | inspect only approved target; no full private inspect | subnets/dynamic/static reason and external-network scope | model checks not connectivity proof | POL0077 mandatory controls, implementation limits explicit | RUN0077 source change/validation; runtime separate | DNS/address/membership hypotheses and observed context | scoped Git config rollback; no network/volume deletion or generic reset |
| 0078 profiles | classification/selection not isolation | exact table/root source, jobs/readiness distinction | approval boundaries through source/service Policy | selection effects including init and shared state | rendered closure not application health | POL0078 owns exact selectors/HOME/companion | existing service/reboot Runbooks; no profile autoactivation | unsupported/unsafe combo stop | applicable subject backup/cleanup; selector has no own persistent storage |
| 0086 versions/config | update authority and drift | Compose/build/copied pins, update manager and mutable uncertainty | no remote job/runtime approval by sync | derived registry and config mount source | static check + mandatory postapply coverage | POL0086/POL0006 constraints | RUN0086 static writes vs approved runtime apply separated | unknown owner/version path/hash coverage stop | source+projection rollback; no data downgrade; compatible service restore |
| 0096 integration | existing selected cross-repo consumer contracts | Docker-side pins; k3d/ESO/Kiali deployed versions not observed | exact allowlists, SSO/BasicAuth/Viewer/bootstrap roles | host endpoints, CA, protected KV/tokens and config | per-consumer status; ports/query presence not whole-cluster health | POL0096; @buenhyden and named cluster owner | corrected RUN0096 branches; cross-repo mutations delegated | TLS/network/auth/readiness separated; failed revocation unknown | protected snapshot/offline custody, scoped credential rollback/revoke; RUN0085 restore only |
| 0098 reboot | preserved-state owner-run reboot, not disaster bootstrap | restart daemon vs one-shot, source-specific readiness | manual unseal, OIDC and SecretID constraints | existing Raft/Agent/data state preserved | expected selected daemon set plus canonical renderer tests | POL0006/0078/0021 and ADR0042 | RUN0098 parent handoff received; current body revised | S13–S20/A33, no broad up/restart or implicit restore | pre-reboot backups, failed-backup stop, no secret/role_id deletion; dated rehearsal retained |

### Heading preservation map

This heading inventory records the complete original-to-final section surface, supplementing the semantic dispositions above. Common template filler is represented by the concrete owner sections; role moves are explicitly identified above. A changed heading does not waive its original substantive obligations.

| Exact leaf | Before sections | Final sections |
| --- | --- | --- |
| `docs/05.operations/guides/0002-developer-environment.md` | Usage; Overview; Developer Environment Setup Usage; 1. Context & Objective; 2. Recommended Permissions (Claude Code); 3. Tool Configuration; 4. Operational Procedures; 5. Maintenance & Safety; Usage Type; Target Audience; Purpose; Prerequisites; Step-by-step Instructions; Common Pitfalls; Common Checks; Runbook Handoff; Traceability; Related Documents | Usage; Local tools and configuration; Environment and certificates; Common Checks; Runbook Handoff; Traceability; Related Documents |
| `docs/05.operations/guides/0003-env-key-comparison.md` | Usage; Common Checks; Runbook Handoff; Traceability; Related Documents | Usage; Common Checks; Runbook Handoff; Traceability; Related Documents |
| `docs/05.operations/guides/0004-harness-agent-first-engineering.md` | Overview; Usage; CI quality-gate version alignment; Audience and Prerequisites; Usage Type; Target Audience; Purpose; Prerequisites; Evaluation Maintenance; Troubleshooting; Common Checks; Runbook Handoff; Traceability; Related Documents | Overview; Usage; CI quality-gate version alignment; Audience and Prerequisites; Usage Type; Target Audience; Purpose; Prerequisites; Evaluation Maintenance; Troubleshooting; Common Checks; Runbook Handoff; Traceability; Related Documents |
| `docs/05.operations/guides/0008-new-service-onboarding.md` | Usage; Overview; Usage Type; Target Audience; Purpose; Prerequisites; Step-by-step Instructions; Common Pitfalls; Common Checks; Runbook Handoff; Traceability; Related Documents | Usage; Overview; Usage Type; Target Audience; Purpose; Prerequisites; Step-by-step Instructions; Common Pitfalls; Common Checks; Runbook Handoff; Traceability; Related Documents |
| `docs/05.operations/guides/0010-sensitive-env-vars-comparison.md` | Usage; Common Checks; Runbook Handoff; Traceability; Related Documents | Usage; Common Checks; Runbook Handoff; Traceability; Related Documents |
| `docs/05.operations/guides/0077-ip-address-management.md` | Usage; Overview; Usage Type; Target Audience; Purpose; Prerequisites; Step-by-step Instructions; Common Pitfalls; Common Checks; Runbook Handoff; Traceability; Related Documents | Usage; Flow and membership; Common pitfalls; Common Checks; Runbook Handoff; Traceability; Related Documents |
| `docs/05.operations/guides/0086-dependency-version-management.md` | Usage; Common Checks; Runbook Handoff; Traceability; Related Documents | Usage; Common Checks; Runbook Handoff; Traceability; Related Documents |
| `docs/05.operations/guides/0096-k8s-integration.md` | Usage; Purpose; Contract; What hy-home.k8s needs from this side; Common Pitfalls; Common Checks; Runbook Handoff; Traceability; Related Documents | Usage; Purpose; Contract; What hy-home.k8s needs from this side; Common Pitfalls; Routine Usage; Common Checks; Runbook Handoff; Traceability; Related Documents |
| `docs/05.operations/policies/0001-common-optimizations-template-exceptions.md` | Overview; Policy Scope; Controls; AI Agent Policy; Exceptions; Verification; Review Cadence; Traceability; Related Documents | Overview; Policy Scope; Controls; AI Agent Policy; Exceptions; Verification; Review Cadence; Traceability; Related Documents |
| `docs/05.operations/policies/0004-harness-agent-first-engineering.md` | Overview; Policy Scope; Controls; Exceptions; Verification; Review Cadence; Traceability; Related Documents | Overview; Policy Scope; Controls; Exceptions; Verification; Review Cadence; Traceability; Related Documents |
| `docs/05.operations/policies/0006-infrastructure-optimization-governance.md` | Overview; Policy Scope; Controls; Source and lifecycle boundary; AI Agent Policy; Roadmap Status and Priority Boundary; Priority Model; Roadmap Disposition; Tier-by-Tier Optimization & Expansion Catalog; 01-gateway; 02-auth; 03-security; 04-data; 05-messaging; 06-observability; 07-workflow; 08-ai; 09-platform-ops; 10-communication; 11-laboratory; Exceptions; Verification; Review Cadence; Traceability; Related Documents | Overview; Policy Scope; Controls; Source and lifecycle boundary; AI Agent Policy; Roadmap Status and Priority Boundary; Priority Model; Roadmap Disposition; Tier-by-Tier Optimization & Expansion Catalog; 01-gateway; 02-auth; 03-security; 04-data; 05-messaging; 06-observability; 07-workflow; 08-ai; 09-platform-ops; 10-communication; 11-quality; Exceptions; Verification; Review Cadence; Traceability; Related Documents |
| `docs/05.operations/policies/0077-ip-address-management.md` | Overview; Policy Scope; Controls; Exceptions; Verification; Review Cadence; Traceability; Related Documents | Overview; Policy Scope; Controls; Exceptions; Verification; Review Cadence; Traceability; Related Documents |
| `docs/05.operations/policies/0078-compose-profile-vocabulary.md` | Overview; Policy Scope; Definitions; Controls; HOME activation; Companion, exclusion and side effects; Exceptions; Verification; Review Cadence; Traceability; Related Documents | Overview; Policy Scope; Definitions; Controls; HOME activation; Companion, exclusion and side effects; Exceptions; Verification; Review Cadence; Traceability; Related Documents |
| `docs/05.operations/policies/0086-dependency-version-management.md` | Overview; Policy Scope; Controls; Exceptions; Verification; Review Cadence; Traceability; Related Documents | Overview; Policy Scope; Controls; Exceptions; Verification; Review Cadence; Traceability; Related Documents |
| `docs/05.operations/policies/0096-k8s-integration.md` | Overview; Policy Scope; Controls; Exceptions; Verification; Review Cadence; Traceability; Related Documents | Overview; Policy Scope; Controls; Exceptions; Verification; Review Cadence; Traceability; Related Documents |
| `docs/05.operations/runbooks/0004-harness-agent-first-engineering.md` | Overview; When to Use; Procedure; Checklist; Procedure; Model-free Evaluation Maintenance; Verification Steps; Observability and Evidence Sources; Safe Rollback or Recovery Procedure; Related Operational Documents; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents | Overview; When to Use; Procedure; Checklist; Procedure; CI quality-gate version alignment; Model-free Evaluation Maintenance; Verification Steps; Observability and Evidence Sources; Safe Rollback or Recovery Procedure; Related Operational Documents; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents |
| `docs/05.operations/runbooks/0009-release-management.md` | Overview; Purpose; When to Use; Procedure; Checklist; Steps; Verification Steps; Observability and Evidence Sources; Safe Rollback or Recovery Procedure; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents | Overview; Purpose; When to Use; Procedure; Checklist; Steps; Verification Steps; Observability and Evidence Sources; Safe Rollback or Recovery Procedure; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents |
| `docs/05.operations/runbooks/0077-ip-address-management.md` | Overview; Purpose; When to Use; Procedure; Checklist; Steps; Verification Steps; Evidence; Safe Rollback or Recovery Procedure; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents | When to Use; Procedure; 1. Confirm declaration and target; 2. Change and validate the scoped source; 3. Observe an approved running target; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents |
| `docs/05.operations/runbooks/0086-dependency-version-management.md` | When to Use; Procedure; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents | When to Use; Procedure; Source and updater changes; Static configuration validation; Runtime configuration apply; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents |
| `docs/05.operations/runbooks/0096-k8s-integration.md` | When to Use; Procedure; Phase 1. Prepare the repository; Phase 2. Secrets and environment; Phase 3. Gateway and Prometheus; Phase 4. Host endpoints; Phase 5. OpenBao Kubernetes auth; Phase 6. Hand off to hy-home.k8s; Phase 7. Verify from both sides; Phase 8. Clean up and record; Rotating the Prometheus API credential; Reissuing the Kiali Grafana token; Setting or replacing the Slack notifications token; Troubleshooting; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents | When to Use; Procedure; Shared prerequisites and result handling; Phase 1. Prepare the repository; Phase 2. Secrets and environment; Phase 3. Gateway and Prometheus; Phase 4. Host endpoints; Phase 5. OpenBao Kubernetes auth; Phase 6. Hand off to hy-home.k8s; Phase 7. Verify from both sides; Phase 8. Clean up and record; Rotating the Prometheus API credential; Reissuing the Kiali Grafana token; Setting or replacing the Slack notifications token; Troubleshooting; Evidence; Rollback or Recovery; Escalation; Traceability; Related Documents |
| `docs/05.operations/runbooks/0098-cold-start-and-reboot.md` | English glosses; exact original headings in handoff snapshot: When to Use (L17); Procedure (L32); 0. Preconditions (before reboot, owner-run) (L37); 1. Docker and Compose containers (after reboot) (L50); 2. Data and authentication foundations: mng-pg, mng-valkey, Traefik, Keycloak (L76); 3. OpenBao sealed start and Agent start (L91); 4. Owner unseal (interactive, hidden input) (L110); 5. Owner OIDC login (L125); 6. SecretID issuance and Agent delivery (owner-run, within10 minutes) (L132); 7. hy-home.k8s(k3d) containers (L148); Timing summary (L178); Evidence (L188); Rollback or Recovery (L194); Escalation (L209); Verification Record (L215); Traceability (L230); Related Documents (L240) | English glosses; exact current headings in Stage05: When to Use (L17); Procedure (L32); 0. Preconditions (before reboot, owner-run) (L38); 1. Docker and Compose containers (after reboot) (L51); 2. Data and authentication foundations: mng-pg, mng-valkey, Traefik, Keycloak (L85); 3. OpenBao sealed start and Agent start (L101); 4. Owner unseal (interactive, hidden input) (L120); 5. Owner OIDC login (L135); 6. SecretID issuance and Agent delivery (owner-run, within10 minutes) (L142); 7. hy-home.k8s(k3d) containers (L160); Timing summary (L199); Evidence (L209); Rollback or Recovery (L215); Escalation (L230); Verification Record (L236); Traceability (L256); Related Documents (L266) |

## Verification Evidence

Focused checks below were executed against the authored files. Exact changed-path metadata must include this untracked Task as well as all21 leaves. Parent will run integrated checks once all author snapshots are final; W7 does not run the broad changed/full gate.

| Check | Scope | Result |
| --- | --- | --- |
| Metadata | Exact22 paths including this untracked Task | PASS: selected=22, violations=0, legacy_exceptions=0, transition_overrides=0 |
| Whitespace / diff | Exact21 tracked leaves plus Task scope | PASS: git diff --check exit0 |
| Local links / anchors | Exact22 current files | PASS: 0 missing local paths or anchors |
| Historical payload | RUN-0098 dated2026-09-30 table | PASS: byte-identical; SHA256 `ecf504b22f07d46b27ef11438e8aa923a9d4d59c5013e86059852e21d6014c1f` |
| Protected concurrent owner | Main RUN-0098/SPEC-0182 and worktree SPEC-0182 immediately before edit | PASS: no concurrent delta; parent Restic line retained |
| Runtime / recovery / credentials | All subjects | NOT_RUN; outside this task |
| Round1 metadata / links / language | Exact4 files, including untracked Task | PASS: metadata selected=4, violations=0, legacy_exceptions=0, transition_overrides=0; links/anchors0; Task Hangul0; changed Stage05 prose Korean |
| Round1 unchanged scope | Other18 leaves;71 canonical profile memberships; RUN-0098 history | PASS: all18 hashes unchanged; all71 profile/category/service joins unchanged; historical payload retains the SHA256 above |

## Review Evidence

Independent security preparation was supplied before writing. The independent reviewer `/root/operations_receipt_review` inspected all21 original/final bodies and the frozen22-file packet, confirmed substantive preservation,71 profile memberships and the RUN-0098 historical payload, and requested the four bounded corrections below. Parent authorized fix round1 in exactly three role leaves and this Task. Author checks do not substitute for independent targeted acceptance; parent owns integration and whole-package acceptance.

### Independent review fix round1

Before editing, all22 hashes matched the reviewed manifest (`c42cc81f5f55d31de6de88a3be9adfb027aff02cc8a08d3ebdd6f2e8d44aa964`). The four authorized files were snapshotted separately. No other finding or ownership boundary was reopened.

| Finding | Bounded correction | Author disposition |
| --- | --- | --- |
| F1 / A32 residue | RUN-0096 Phase2.2 and troubleshooting now list supported rejection alternatives, stop before writes, preserve inputs/Value, require value-free exact-cause diagnosis and separately approved narrow correction. Generic example-row replacement is removed; default unknown-row preservation and separate prune approval remain. | Accepted by independent fix-round1 review |
| F2 | RUN-0096 troubleshooting distinguishes000 transport/TLS/DNS failure from401 HTTP authentication response. Alternative credential/route/usersFile causes require evidence; only proven stale inode plus exact project/service approval reaches Phase3.1 recreation. A failure alone grants no recreation or rotation authority. | Accepted by independent fix-round1 review |
| F3 | POL-0078 api-mock side-effect cell distinguishes host loopback publication from unauthenticated project-default-network peer access. Profile name, category and service membership remain unchanged. | Accepted by independent fix-round1 review |
| F4 | POL-0006 new-service control requires implementation_services for service-bound Guides and permits omission only for non-service/common subjects; the existing exact path/service join remains the sole catalog binding. | Accepted by independent fix-round1 review |

Round1 focused verification passed and is recorded with the actual results in Verification Evidence. The metadata check selected exactly four paths; the subsequent Task-only update records these results without changing its metadata, headings or authority. The unchanged18 other leaves, canonical71 profile memberships and RUN-0098 history remain protected. No runtime, source, indexes, staging or broad gate are part of this correction.

### Independent fix-round1 acceptance

On 2026-10-01, `/root/operations_receipt_review` accepted the frozen22-file packet: all four findings closed, all21 original/final bodies preserved,71 profile memberships unchanged, and the RUN-0098 historical payload unchanged. The reviewer verified every hash against manifest SHA-256 `9640d9a9ee271c13c8ffc5485efecf69e6d12cdd4541b90c74fb096c67559cf8`. Spec compliance and documentation quality passed. This subsequent Task-only receipt does not alter the accepted21 leaves. Whole-package acceptance was subsequently completed by the final integrated gate in Task0001.

### Parent adjacent-owner correction acceptance

Independent review reopened one source nuance missed in the initial F1 acceptance: readable safe regular files with mode different from0600 produce drift/check1, not rejection. Parent corrected the secrets README and both RUN-0096 descriptions, then corrected RUN-0085 unsupported lookup-accessor syntax and false generic-error revocation success. The same independent reviewer accepted all three exact deltas on 2026-10-01, with protected responses, pre-revoke lookup, successful revoke, authorized caller/unsealed positive controls and authoritative same-accessor invalidation required. Generic403/transport/CLI/sealed/parse failure remains INDETERMINATE. This supersedes only the RUN-0096 body hash in the prior packet: final SHA-256 `d7454bd36787520670fabb22a48557858d810958fffb2b3a1e0bdc468f04643d`. No live command ran.

### Acceptance Checklist

| Item | Status | Evidence |
| --- | --- | --- |
| Exact21 leaf authoring and role ownership | Complete; independently accepted | Disposition and section maps above |
| All A01–A33/S01–S21 findings dispositioned | Complete; independently accepted | Resolution table; blocked source defects below |
| Korean Stage05 / English Task | Author pass complete | Technical names, headings and exact historical payload excluded from translation |
| Controls and meaningful prior instructions preserved | Author pass complete | Before/final maps; explicit procedure handoffs |
| Focused static checks | Complete | Verification table; broader integration remains parent-owned |
| No runtime or protected concurrent work mutation | Complete | Scope and pre-write assertions |
| Independent acceptance | Accepted | Independent fix-round1 review below |

## Commit Ledger

No staging or commit was performed by W7. Parent owns integration commit boundaries and any later approval.

## Rulings

- Parent authorized W7 implementation after read-only preparation and confirmed disjoint W6/W7 ownership; shared indexes remain parent-owned.
- Final09-platform-ops naming and additional SPEC-0197 moves are accepted source paths, without profile activation or state changes.
- Parent explicitly handed off RUN-0098 current-procedure fixes after checking concurrent SPEC-0182 ownership. Historical rehearsal payload is frozen; SPEC-0182 itself is untouched.
- Source bugs cannot lower policy. Prometheus generator rotation remains BLOCKED before consumer/KV mutation because existing non-placeholder registry values can be restored unchanged.
- Root/bootstrap denial and revocation require verified server responses and same-token positive controls; transport, sealed and parse errors remain indeterminate. Local file removal is not server revocation.

## Deferred Items

- Parent README/index integration, wave independent review and the final integrated gate are accepted; Task0001 records whole-package completion.
- Separately approved implementation or scoped mechanism for fresh Prometheus OBS-013/INFRA-007/OpenBao rotation. No such capability was added here.
- Parent coordination closed: AD-0026 source-network wording was reconciled; independent adjacent-owner review accepted the secrets README/RUN-0096 mode-only drift distinction and RUN-0085 accessor CLI/revocation controls. No source or runtime mutation occurred.
- All live readiness, native hook, cluster consumer, token issuance/revocation and recovery evidence remain unverified in this documentation-only task. Grafana response/version compatibility must be checked in the authorized execution environment before mutation; source-declared tags do not prove installed API behavior.
