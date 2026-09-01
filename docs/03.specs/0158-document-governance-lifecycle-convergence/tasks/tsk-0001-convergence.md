---
title: Converge Document Governance by Lifecycle
type: specs/task
layer: specification
status: active
owner: "@buenhyden"
artifact_id: SPEC-0158-TSK-0001
parent_ids: [SPEC-0158, SPEC-0158-PLAN-0001]
created: 2026-09-01
updated: 2026-09-01
---

# Converge Document Governance by Lifecycle

## Objective

Classify the approved target corpus, repair current owners, remove obsolete
authority, simplify validation, and close the packet with observed evidence.

## Inputs

- SPEC-0158 and SPEC-0158-PLAN-0001.
- Completed SPEC-0157 evidence.
- Current Stage 00, Stage 99, manifest, workflow, and Git recovery authorities.

## Work Log

### 2026-09-01 execution baseline

- Branch: `codex/0158-document-governance-lifecycle-convergence`.
- Baseline and recovery commit: `6317553e`, used only as a regular-blob
  recovery address. It is not an expected branch tip, checksum, lineage Gate,
  or byte-equality oracle.
- The approved eight stage roots contain 592 tracked Markdown files.
- `git ls-tree -r 6317553e` proves all 592 are regular `100644` blobs.
- Ordered keep selectors cover 366 files; the explicit table covers 226 paths.
  Their sum is 592 with zero overlap or omission. Mutation remains blocked
  until the consumer handoffs and two independent review corrections below are
  resolved and re-reviewed.
- No byte-identical Markdown duplicates were found in the measured target set.
- The existing implementation-alignment command and provider contract baseline
  passed, but manual semantic scans found retired path and authority claims that
  structural validation does not currently reject. Those paths are explicit
  rewrites below.

| Stage | Measured Markdown | Keep selector | Explicit disposition |
| :--- | ---: | ---: | ---: |
| `docs/00.agent-governance` | 76 | 66 | 10 |
| `docs/01.requirements` | 26 | 25 | 1 |
| `docs/02.architecture` | 54 | 47 | 7 |
| `docs/03.specs` | 70 | 7 | 63 |
| `docs/05.operations` | 208 | 204 | 4 |
| `docs/90.references` | 89 | 0 | 89 |
| `docs/98.archive` | 47 | 0 | 47 |
| `docs/99.templates` | 22 | 17 | 5 |
| **Total** | **592** | **366** | **226** |

### Atomic latest-research protection

The following complete current-baseline set is one Task-local
`PROTECT_LATEST` unit. All 21 paths are protected before consumer review.
All 21 paths require a non-lossy path, metadata, owner, link, or persistent
declaration review because even otherwise stable leaves can consume owners or
indexes being retired. No protected path may be
deleted, archived, tombstoned, checksum-pinned, or reduced in body, sources, or
claims.

- `docs/90.references/research/0002-agentic-engineering-research-pack/README.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0001-agent-instructions-vibe-coding.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0002-agent-model-selection.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0003-ai-agent-catalogs.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0005-docker-compose-infrastructure.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0006-document-metadata-lifecycle.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0007-documentation-architecture.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0008-harness-engineering.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0009-llm-wiki-system.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0010-loop-engineering.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0011-memory-hierarchy.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0012-provider-implementation-comparison.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0013-provider-model-landscape.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0014-quality-ci-formatting.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0015-scope-application-matrix.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0016-sdlc-document-roles.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0017-security-governance.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0018-spec-driven-sdlc.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0019-verification-validation.md`
- `docs/90.references/research/0002-agentic-engineering-research-pack/m0020-workspace-baseline.md`

| Commit | Classified purpose | Control effect |
| :--- | :--- | :--- |
| `95142c3a` | draft promotion and activation | illustrative only; not restore baseline |
| `07b94403` | substantive restore-and-merge across all 21 files | illustrative content provenance |
| `3bf50f94` | claim-bearing corrections in two leaves | illustrative content provenance |
| `65e8dfde` | last new substantive leaf additions | illustrative content provenance |
| `6663f02c` | three link-only corrections | mechanical; never selects protected content |

The durable protection oracle must move to the package README before this Task
body is retired. It will declare the safe tracked package set dynamically,
without a pinned count, hashes, expected SHAs, or byte equality.

### Current implementation truth inventory

| Implementation subject | Observed current fact | Classification | Canonical Stage 01/02 owner | Mismatch or gap | Disposition | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Gateway routing | `infra/01-gateway/**`; `docs/05.operations/catalog/01-gateway/**` implement Traefik/Nginx hybrid routing | requirement + structure + decision | REQ-0001; AD-0001; ADR-0001 | none in selected surfaces | keep owners | `git ls-files 'infra/01-gateway/**' 'docs/05.operations/catalog/01-gateway/**'`; clause review |
| Authentication | `infra/02-auth/**`; `docs/05.operations/catalog/02-auth/**` implement Keycloak and OAuth2 Proxy | requirement + structure + decision | REQ-0002; AD-0002; ADR-0002 | none in selected surfaces | keep owners | exact selector + clause review |
| Secrets management | `infra/03-security/**`; `secrets/README.md`; `docs/05.operations/catalog/03-security/**` implement Vault/file-secret boundaries | requirement + structure + decision | REQ-0003; AD-0003; ADR-0003 | none in selected surfaces | keep owners | exact selector + secret-value exclusion review |
| Operational data platforms | `infra/04-data/{cache-and-kv,lake-and-object,nosql,operational,relational,specialized}/**`; matching Stage 05 subjects implement current data services | requirement + structure + decision | REQ-0004; AD-0004; ADR-0004 | SPEC-0004 uses generic phase prose | rewrite Spec; keep owners | exact selector + service/owner comparison |
| Analytics data platforms | `infra/04-data/analytics/**`; Stage 05 subjects `0017`--`0020` implement analytics engines | requirement + structure + decision | REQ-0005; AD-0012; ADR-0015 | none in selected surfaces | keep owners | exact selector + engine comparison |
| Messaging | `infra/05-messaging/**`; `docs/05.operations/catalog/05-messaging/**` implement Kafka and RabbitMQ | requirement + structure + decision | REQ-0006; AD-0005; ADR-0005 | SPEC-0006 uses generic phase prose | rewrite Spec; keep owners | exact selector + broker comparison |
| Observability | `infra/06-observability/**`; `docs/05.operations/catalog/06-observability/**` implement LGTM, Alloy, Alertmanager, and retention procedures | requirement + structure + decision | REQ-0007; AD-0006; ADR-0006 | SPEC-0007 uses generic phase prose; policy `0048` names Stage 04 | rewrite both consumers; keep owners | exact selector + component/procedure comparison |
| Workflow orchestration | `infra/07-workflow/**`; Stage 05 subjects `0050`, `0051`, `0053` implement Airflow/n8n | requirement + structure + decision | REQ-0008; AD-0007; ADR-0007 | SPEC-0008 publishes a retired route | rewrite Spec; keep owners | exact selector + orchestrator comparison |
| Local AI | `infra/08-ai/**`; Stage 05 subjects `0055`, `0056`, `0059` implement Ollama/GPU/RAG behavior | requirement + structure + decision | REQ-0009; AD-0008; ADR-0008 | SPEC-0009 publishes a retired route | rewrite Spec; keep owners | exact selector + AI service comparison |
| Tooling | `infra/09-tooling/**`; `docs/05.operations/catalog/09-tooling/**` implement registry, test, IaC, and quality tools | requirement + structure + decision | REQ-0010; AD-0009; ADR-0009 | none in selected surfaces | keep owners | exact selector + tooling comparison |
| Communication | `infra/10-communication/**`; `docs/05.operations/catalog/10-communication/**` implement mail services | requirement + structure + decision | REQ-0011; AD-0010; ADR-0010 | none in selected surfaces | keep owners | exact selector + mail comparison |
| Laboratory | `infra/11-laboratory/**`; `docs/05.operations/catalog/11-laboratory/**` implement dashboard/admin/notebook tools | requirement + structure + decision | REQ-0012; AD-0011; ADR-0011 | none in selected surfaces | keep owners | exact selector + laboratory comparison |
| Open WebUI | `infra/08-ai/open-webui/**`; Stage 05 subject `0057-open-webui/**` implement the Open WebUI boundary | requirement + structure + decision | REQ-0013; AD-0013; ADR-0016 | none in selected surfaces | keep owners | exact selector + Open WebUI comparison |
| Authentication hardening | `infra/02-auth/**`; Stage 05 auth policies/runbooks implement fail-closed and health controls | requirement + structure + decision | REQ-0014; AD-0014; ADR-0017 | none in selected surfaces | keep owners | selected Compose keys + auth policy clauses |
| Security hardening | `infra/03-security/**`; Stage 05 Vault policy/runbook implement hardening and expansion constraints | requirement + structure + decision | REQ-0015; AD-0018; ADR-0018 | AD-0018 uses generic phase prose | rewrite AD; keep requirement/decision | selected Compose keys + security clauses |
| Data hardening | `infra/04-data/**`; Stage 05 subjects `0021`, `0030`, `0032`, `0035` implement backup, hardening, restore, and exhaustion controls | requirement + structure + decision | REQ-0016; AD-0019; ADR-0019 | AD-0019 uses generic phase prose | rewrite AD; keep requirement/decision | exact subject selector + data controls |
| Messaging hardening | `infra/05-messaging/**`; Stage 05 subject `0037-optimization-hardening/**` implements broker hardening | requirement + structure + decision | REQ-0017; AD-0020; ADR-0020 | none in selected surfaces | keep owners | exact selector + hardening clauses |
| Observability hardening | `infra/06-observability/**`; Stage 05 subjects `0044` and `0048` implement telemetry hardening/retention | requirement + structure + decision | REQ-0018; AD-0021; ADR-0021 | policy `0048` names Stage 04 | rewrite policy; keep owners | exact selector + telemetry clauses |
| Workflow hardening | `infra/07-workflow/**`; Stage 05 subjects `0051` and `0054` implement DAG and workflow hardening | requirement + structure + decision | REQ-0019; AD-0022; ADR-0022 | none in selected surfaces | keep owners | exact selector + workflow clauses |
| AI hardening | `infra/08-ai/**`; Stage 05 subjects `0055`, `0058`, `0059` implement AI recovery/hardening/RAG controls | requirement + structure + decision | REQ-0020; AD-0023; ADR-0023 | none in selected surfaces | keep owners | exact selector + AI hardening clauses |
| Tooling hardening | `infra/09-tooling/**`; Stage 05 subjects `0060`--`0069` implement IaC, performance, registry, and quality controls | requirement + structure + decision | REQ-0021; AD-0024; ADR-0024 | none in selected surfaces | keep owners | exact selector + tooling hardening clauses |
| Laboratory hardening | `infra/11-laboratory/**`; Stage 05 subject `0074-optimization-hardening/**` implements laboratory constraints | requirement + structure + decision | REQ-0022; AD-0025; ADR-0025 | none in selected surfaces | keep owners | exact selector + laboratory clauses |
| Shared infrastructure network | `docker-compose.yml`; `infra/**/docker-compose*.yml`; Stage 05 subject `0077-ip-address-management/**` implement `infra_net` | requirement + structure + decision | REQ-0023; AD-0026; ADR-0026 | none in selected surfaces | keep owners | `git ls-files 'infra/**/docker-compose*.yml'`; `infra_net` comparison |
| Agent/provider runtime projection | `docs/00.agent-governance/**`; `.agents/**`; `.claude/**`; `.codex/**`; provider renderer and hook scripts implement policy-to-native translation | requirement + structure + decision | REQ-0024; AD-0027; ADR-0029 | Registry restates neutral workflow; ADR-0027 contains retired HADS/Stage 04 prose | Tasks 3/5 separate sources and rewrite the superseded record | exact tracked selectors + provider drift/contract checks |
| Document and validation authority | `docs/99.templates/registry.json`; `scripts/manifest.yaml`; `.github/workflow-contract.yml`; document-governance libraries implement profile, validator, and CI routing | requirement + structure + decision | REQ-0024 clauses; AD-0027 boundaries; ADR-0029 | Migration and duplicate inventories still act as inputs | Tasks 4/6/7 derive from current owners | exact files + Registry/manifest/workflow relation review |
| Operational readiness | `examples/sample-web-service/**`; `docs/05.operations/catalog/**`; `scripts/validation/run-compose-core-readiness.sh`; `scripts/validation/compose-core-readiness.lib.sh`; `scripts/lib/ops/rehearse-postgres-logical-upgrade.sh`; `scripts/security/verify-sample-service-supply-chain.sh`; `scripts/validation/check-supply-chain-policy.py`; `scripts/operations/rehearse-sample-service-delivery.sh`; and their focused tests implement typed procedures plus local-isolated readiness, recovery, supply-chain, promotion, and rollback behavior | requirement + structure + decision | REQ-0025; AD-0028; ADR-0028 | two Stage 98 links and one Stage 04 reference | Tasks 4/5 rewrite current procedures; keep implemented owners | exact tracked selectors + `test_compose_core_readiness`, `test_postgres_logical_upgrade_rehearsal`, `test_supply_chain_policy`, and `test_sample_service_delivery_rehearsal` |

The bidirectional review uses the exact selectors above, not the
`--mode alignment` link predicate as a semantic oracle. In the owner-to-
implementation direction, all 25 Requirement leaves, all 25 Architecture
Description leaves, and all 25 active ADR leaves occur in at least one row;
ADR-0027 is deliberately excluded from the active-ADR set and receives an
explicit superseded-record rewrite. In the implementation-to-owner direction,
every selected current subject maps each required behavior to one Requirement,
each structure to one Architecture Description, and each adopted decision to
one active ADR. One owner file may contain several related clauses, but no
individual fact is assigned to two current files. The exact mismatches above
are mutation prerequisites, so the review does not claim that the existing
alignment script proves semantic completeness.

### Ordered keep cohorts

| Order | Selector | Disposition | Covered count | Exceptions | Evidence |
| :--- | :--- | :--- | ---: | :--- | :--- |
| 1 | `docs/00.agent-governance/**/*.md` minus explicit table | keep | 66 | 10 rewrite paths | typed Stage 00 profiles and current consumer map |
| 2 | `docs/01.requirements/**/*.md` minus explicit table | keep | 25 | REQ-0024 | active Requirement profiles and implementation owner map |
| 3 | `docs/02.architecture/**/*.md` minus explicit table | keep | 47 | 7 current/superseded-owner rewrites | Architecture/ADR profiles and implementation owner map |
| 4 | exact set `docs/03.specs/{0001-gateway,0002-auth,0005-data-analytics,0010-tooling,0011-communication,0012-laboratory}/spec.md` | keep | 6 | none | current capability profile and implementation review |
| 5 | exact path `docs/03.specs/0156-compose-enablement-model-convergence/spec.md` with `profile_id=spec` and `status=draft` | keep | 1 | explicitly future, not implemented-current authority | legal draft lifecycle and separate future scope |
| 6 | `docs/05.operations/**/*.md` minus explicit table | keep | 204 | 4 current-procedure rewrites | Operations catalog membership and no byte-identical duplicates |
| 7 | `docs/99.templates/**/*.md` minus explicit table | keep | 17 | 5 template/index dispositions | Registry template consumers |

`PROTECT_LATEST` has priority over these cohorts, but all of its measured paths
are explicit `rewrite-non-lossy` rows rather than silent `keep` members.

### Stage 90 consumer and replacement handoff ledger

For each non-protected package, the baseline consumer command is
`git grep -l -F '<package-directory-name>' 6317553e --`. The retained inbound
set below excludes only the package itself, other retiring non-protected Stage
90 package paths, Stage 98 paths, explicit rows whose disposition contains
`delete`, and this transient Task. It does **not** exclude protected research,
current documents scheduled for rewrite, scripts, tests, structural indexes,
or provider projections.
This makes the filter executable and prevents a rewrite dependency from being
mistaken for a retiring consumer.

`S90-NONE` is the exact 28-package no-retained-consumer set:

- Audit packages `0001`--`0018` and `0034`--`0038`;
- Data packages `0062`, `0063`, `0070`, `0075`, and `0077`.

Their observed inbounds are confined to the excluded retiring cohort. The
user-authorized retention boundary permits these historical snapshots to be
discarded without copying their bodies. Their replacement is
therefore `none`; Git regular-blob recovery remains available until the Task 6
deletion commit is accepted. The other 36 packages have the exact handoffs
below, so the two sets cover all 64 non-protected package roots.

| Handoff | Package | Retained inbound consumers at `6317553e` | Required handoff and canonical replacement |
| :--- | :--- | :--- | :--- |
| `S90-A0019` | `audits/0019-readme` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/audit_criterion_contract.py`; `scripts/validation/check-agentic-audit-semantic-freshness.py`; `scripts/validation/generate-audit-implementation-matrix.sh`; `tests/validation/test_agentic_audit_semantic_freshness.py` | Remove audit-package catalogs from these consumers; current document rules derive from Stage 99 Registry and Stage 00 policy. No audit output replacement. |
| `S90-A0020` | `audits/0020-agent-instructions-catalog-vibe-models` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/audit_criterion_contract.py` | Remove audit-package catalog coupling; Stage 00 role/skill/provider sources replace current meaning. |
| `S90-A0021` | `audits/0021-automation-candidates` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/operations/generate-compose-profile-service-coverage.sh`; `scripts/operations/generate-tech-stack-version-provenance.sh`; `scripts/validation/agentic-audit-semantic-contract.json`; `scripts/validation/audit_criterion_contract.py`; `scripts/validation/generate-audit-implementation-matrix.sh`; `scripts/validation/generate-security-automation-readiness.sh`; `tests/validation/test_security_automation_readiness.py` | Remove historical candidate IDs from consumers; manifest-owned current commands and their focused tests remain the replacement. |
| `S90-A0022` | `audits/0022-compose-infrastructure-operations-readiness` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/audit_criterion_contract.py` | Remove audit-package catalog coupling; current Compose, Stage 01/02, and Stage 05 owners replace current meaning. |
| `S90-A0023` | `audits/0023-frontmatter-semantic-inventory` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/lib/document_governance/metadata/reference.py`; `scripts/validation/audit_criterion_contract.py` | Derive profiles and references from the Stage 99 Registry/current tree; delete historical inventory bindings. |
| `S90-A0024` | `audits/0024-frontmatter-template-readme-implementation` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/agentic-audit-semantic-contract.json`; `scripts/validation/audit_criterion_contract.py` | Derive contracts from Stage 99 templates/Registry; delete audit-specific criterion rows. |
| `S90-A0025` | `audits/0025-harness-engineering-implementation` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/audit_criterion_contract.py` | Stage 00 policies and current provider tests replace the historical implementation snapshot. |
| `S90-A0026` | `audits/0026-implementation-overview` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/agentic-audit-semantic-contract.json`; `scripts/validation/audit_criterion_contract.py`; `scripts/validation/check-agentic-audit-semantic-freshness.py`; `scripts/validation/generate-audit-implementation-matrix.sh`; `scripts/validation/report-audit-pack-coverage.sh`; `tests/validation/test_audit_criterion_contract.py` | Retire audit-only generators/reports and derive surviving checks from Stage 00, Stage 99, manifest, and current tree. |
| `S90-A0027` | `audits/0027-loop-engineering-implementation` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/audit_criterion_contract.py` | Stage 00 workflow policy replaces the historical loop snapshot; remove audit IDs. |
| `S90-A0028` | `audits/0028-provider-harness-loop-implementation` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/audit_criterion_contract.py` | Stage 00 workflow policy plus provider-native checks replace the historical snapshot. |
| `S90-A0029` | `audits/0029-sdlc-document-contracts-implementation` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/audit_criterion_contract.py` | Stage 99 Registry and Stage 00 SDLC policy replace the historical snapshot. |
| `S90-A0030` | `audits/0030-sdlc-quality-formatting-implementation` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/agentic-audit-semantic-contract.json`; `scripts/validation/audit_criterion_contract.py` | Current Stage 00 quality policy and Stage 99 profiles replace the audit criteria. |
| `S90-A0031` | `audits/0031-security-framework-maturity` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/audit_criterion_contract.py`; `scripts/validation/generate-audit-implementation-matrix.sh`; `scripts/validation/generate-security-automation-readiness.sh`; `tests/lib/document_governance/test_references.py`; `tests/validation/test_security_automation_readiness.py` | Current security policy, security validators, and fixture tests remain; remove audit maturity/path assertions and generated audit output. |
| `S90-A0032` | `audits/0032-workspace-rules-environment-implementation` | `scripts/lib/document_governance/metadata/profile.py`; `scripts/validation/audit_criterion_contract.py` | Stage 00 environment/policy sources replace the snapshot; remove audit IDs. |
| `S90-A0033` | `audits/0033-readme` | `scripts/validation/check-agentic-audit-semantic-freshness.py`; `tests/validation/test_agentic_audit_semantic_freshness.py` | Retire the audit-pack freshness route and its test; no replacement artifact. |
| `S90-D0059` | `data/0059-compose-profile-service-coverage` | `docs/03.specs/0156-compose-enablement-model-convergence/spec.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0005-docker-compose-infrastructure.md`; `scripts/manifest.yaml`; `scripts/operations/generate-compose-profile-service-coverage.sh`; `scripts/operations/generate-tech-stack-version-provenance.sh`; `tests/validation/test_script_manifest.py` | Update both documents and manifest consumers; derive coverage from `docker-compose.yml` and `infra/**/docker-compose*.yml`, emitting check/stdout evidence rather than a tracked Stage 90 snapshot. |
| `S90-D0060` | `data/0060-image-version-interpretation` | `scripts/operations/generate-compose-profile-service-coverage.sh`; `scripts/operations/generate-tech-stack-version-provenance.sh` | Inline only required parsing rules in the generators; Compose/config files remain the factual source. No data document replacement. |
| `S90-D0061` | `data/0061-tech-stack-version-provenance` | `docs/90.references/research/0002-agentic-engineering-research-pack/m0005-docker-compose-infrastructure.md`; `scripts/manifest.yaml`; `scripts/operations/generate-tech-stack-version-provenance.sh`; `scripts/validation/generate-audit-implementation-matrix.sh`; `scripts/validation/generate-security-automation-readiness.sh`; `tests/validation/test_script_manifest.py` | Correct the protected link and remove generated-output dependencies; current Compose/config sources plus check/stdout generator behavior replace the snapshot. |
| `S90-D0064` | `data/0064-agent-output-eval-fixtures` | `.agents/skills/provider-model-evaluation/SKILL.md`; `.claude/skills/provider-model-evaluation/SKILL.md`; `docs/00.agent-governance/skills/provider-model-evaluation.md`; `scripts/validation/agent_output_eval.py`; `scripts/validation/generate-audit-implementation-matrix.sh`; `tests/validation/test_agent_output_eval_fixtures.py` | Make `scripts/validation/agent_output_eval.py` plus `tests/fixtures/agent-output-eval/**` the sole typed fixture/regression source; regenerate provider skills and remove Markdown-catalog parity/count tests. |
| `S90-D0065` | `data/0065-audit-implementation-matrix` | `docs/01.requirements/0025-operational-readiness-closure.md`; `docs/02.architecture/decisions/0028-local-isolated-readiness-evidence.md`; `scripts/manifest.yaml`; `scripts/validation/generate-audit-implementation-matrix.sh`; `tests/lib/document_governance/test_registry.py`; `tests/validation/test_agentic_audit_semantic_freshness.py`; `tests/validation/test_script_manifest.py` | Move durable readiness meaning to REQ-0025/ADR-0028 and current Task evidence; retire the generated matrix route, manifest row, and output-specific tests. |
| `S90-D0066` | `data/0066-foundation-summary` | `docs/03.specs/0155-validation-surface-reduction/spec.md`; `scripts/lib/document_governance/operations_catalog.py` | Rewrite SPEC-0155 and derive Operations shape from Stage 99 Registry/current Stage 05 tree; remove the frozen foundation path. |
| `S90-D0067` | `data/0067-foundation` | `docs/03.specs/0155-validation-surface-reduction/spec.md`; `scripts/lib/document_governance/operations_catalog.py` | Same current Registry/tree derivation as `S90-D0066`; no retained data output. |
| `S90-D0068` | `data/0068-target-surface-convergence-summary` | `docs/03.specs/0155-validation-surface-reduction/spec.md`; `scripts/lib/document_governance/operations_catalog.py`; `tests/lib/document_governance/test_taxonomy.py`; `tests/lib/target_surface/test_target_surface_contracts.py` | Rewrite SPEC-0155; derive taxonomy/target relations from Stage 99 Registry and current tree, removing snapshot-path assertions. |
| `S90-D0069` | `data/0069-target-surface-convergence` | `docs/03.specs/0155-validation-surface-reduction/spec.md`; `scripts/lib/document_governance/lifecycle/promoted.py`; `scripts/lib/document_governance/operations_catalog.py`; `scripts/lib/target_surface/target_surface_contract.py`; `tests/lib/target_surface/test_target_surface_contracts.py` | Replace frozen target data with Stage 99 Registry/current-tree relations and rewrite SPEC-0155; no data output. |
| `S90-D0071` | `data/0071-github-actions-control-plane-observation` | `.github/INDEX.md`; `.github/rulesets/main-protection.md`; `docs/00.agent-governance/policies/github-governance.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md` | Move current ownership wording to Stage 00 GitHub policy, `.github/workflow-contract.yml`, and `.github` indexes; correct the protected citation without reducing research. |
| `S90-D0072` | `data/0072-provider-hook-parity-matrix` | `scripts/manifest.yaml`; `scripts/validation/agent_output_eval.py`; `scripts/validation/report-provider-hook-parity.sh`; `tests/lib/document_governance/test_references.py`; `tests/validation/test_provider_hook_parity.py` | Provider Registry plus check-only parity output replace the tracked matrix; remove output path/freshness coupling from manifest, evaluator, reference tests, and parity tests. |
| `S90-D0073` | `data/0073-target-surface-delta-manifest` | `docs/03.specs/0155-validation-surface-reduction/spec.md`; `tests/lib/target_surface/test_target_surface_contracts.py` | Rewrite SPEC-0155 and make target-surface tests derive current Registry/tree relations. No retained manifest output. |
| `S90-D0074` | `data/0074-target-surface-delta-summary` | `docs/03.specs/0155-validation-surface-reduction/spec.md` | Remove the superseded output reference from SPEC-0155; current Task records the accepted outcome. |
| `S90-D0076` | `data/0076-llm-wiki-stage-category-coverage` | `docs/90.references/research/0002-agentic-engineering-research-pack/m0009-llm-wiki-system.md`; `scripts/knowledge/generate-llm-wiki.py`; `scripts/lib/document_governance/metadata/profile.py`; `scripts/lib/document_governance/operations_catalog.py`; `scripts/manifest.yaml`; `scripts/validation/generate-audit-implementation-matrix.sh`; `tests/validation/test_generate_llm_wiki.py` | Correct protected research non-lossily; make `llms.txt` the sole tracked LLM output and remove category-count/output coupling from code, manifest, and tests. |
| `S90-D0078` | `data/0078-security-automation-readiness` | `docs/90.references/research/0002-agentic-engineering-research-pack/m0017-security-governance.md`; `scripts/lib/document_governance/operations_catalog.py`; `scripts/manifest.yaml`; `scripts/validation/generate-audit-implementation-matrix.sh`; `scripts/validation/generate-security-automation-readiness.sh`; `tests/validation/test_script_manifest.py`; `tests/validation/test_security_automation_readiness.py` | Correct protected research non-lossily; retain current security predicates/tests but remove the tracked readiness output, its manifest route, and audit-output generator coupling. |
| `S90-D0079` | `data/0079-supply-chain-sample-service` | `scripts/lib/document_governance/operations_catalog.py`; `scripts/manifest.yaml`; `scripts/security/generate-supply-chain-sample-service-summary.sh`; `tests/validation/test_script_manifest.py` | Retain `infra/supply-chain.*.json`, `scripts/validation/check-supply-chain-policy.py`, and `tests/fixtures/supply-chain/**` as the oracle; remove only the duplicate Markdown summary generator/output route. |
| `S90-D0082` | `data/0082-llm-wiki-index` | `README.md`; `docs/03.specs/0096-llm-wiki-agent-first-completion/spec.md`; `docs/05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/guide.md`; `docs/05.operations/catalog/00-workspace/0007-llm-wiki-maintenance/policy.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/README.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0009-llm-wiki-system.md`; `docs/README.md`; `llms.txt`; `scripts/README.md`; `scripts/knowledge/generate-llm-wiki.py`; `scripts/lib/document_governance/metadata/profile.py`; `scripts/lib/document_governance/operations_catalog.py`; `scripts/manifest.yaml`; `scripts/validation/agent_output_eval.py`; `scripts/validation/check-script-manifest.py`; `tests/validation/test_generate_llm_wiki.py`; `tests/validation/test_reference_stage_repo_contract.py`; `tests/validation/test_script_manifest.py` | Rewrite every named document consumer and protected research non-lossily; generate only `llms.txt` and derive navigation from root/stage READMEs. Remove tracked index output and all path/count freshness assertions. |
| `S90-D0083` | `data/0083-repository-map` | `README.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0009-llm-wiki-system.md`; `docs/README.md`; `llms.txt`; `scripts/knowledge/generate-llm-wiki.py`; `scripts/lib/document_governance/references.py`; `tests/lib/document_governance/test_references.py` | Move curated entrypoint meaning into `llms.txt` and existing root/stage READMEs; correct protected research and remove repository-map retention/path assertions. |
| `S90-R0080` | `research/0080-roadmap-v1` | `docs/90.references/research/README.md` | Remove the retiring roadmap from the structural research index; protected RES-0002 remains the sole package entry. No replacement artifact. |
| `S90-R0081` | `research/0081-roadmap` | `docs/90.references/research/README.md` | Remove the retiring roadmap from the structural research index; protected RES-0002 remains the sole package entry. No replacement artifact. |
| `S90-R0084` | `research/0084-github-actions-platform` | `docs/90.references/research/README.md`; `scripts/lib/document_governance/lifecycle/promoted.py`; `tests/lib/document_governance/test_links.py`; `tests/lib/document_governance/test_references.py` | Remove the retiring package from the structural research index, move any current provider fact to Stage 00 GitHub policy and `.github/workflow-contract.yml`, and remove research-path lifecycle/link/reference assertions. |

The explicit table references these handoff IDs. An ID is a deletion
precondition, not permission to retain the package. Task 6 must make each
listed inbound stop naming the package and must land the stated replacement
before deleting that package.

### Stage 03 and Stage 98 deletion handoff ledgers

The same retained-inbound filter is applied to deleting Spec Packages and
Migrations: search the exact package/Migration slug at `6317553e`, exclude the
package itself, other rows whose disposition contains `delete`, non-protected
Stage 90, Stage 98, and this Task, but retain every current rewrite, source,
test, index, and protected-research consumer. Every deleting Stage 03 row
references one of these package-level handoffs.

| Handoff | Deleting package | Retained inbound consumers at `6317553e` | Required handoff and canonical replacement |
| :--- | :--- | :--- | :--- |
| `S03-0102` | `0102-workspace-document-contract-audit-pack` | `docs/03.specs/README.md` | Remove the package from the index; Stage 00 documentation protocol and `docs/99.templates/registry.json` own the current contract. |
| `S03-0103` | `0103-document-restructure-audit-contract-archive` | `docs/03.specs/README.md` | Remove the package from the index; Stage 99 Registry and Git recovery replace the restructure/archive ledger. |
| `S03-0105` | `0105-agentic-engineering-implementation-audit-pack` | `docs/03.specs/README.md` | Remove the package from the index; the current implementation-owner map and protected RES-0002 replace any still-current meaning. |
| `S03-0123` | `0123-agentic-engineering-audit-remediation` | `docs/03.specs/README.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0016-sdlc-document-roles.md`; `scripts/lib/document_governance/spec_packages.py` | Remove package-specific routing/count logic; protected RES-0002 and current Stage 00 owners replace accepted outcomes. |
| `S03-0131` | `0131-document-corpus-lifecycle-migration-foundation` | `docs/03.specs/README.md` | Remove the package from the index; Stage 99 Registry/current lifecycle library own the surviving contract. |
| `S03-0132` | `0132-agent-governance-harness-convergence` | `docs/03.specs/README.md` | Remove the package from the index; REQ-0024, AD-0027, ADR-0029, and Stage 00 own the outcome. |
| `S03-0133` | `0133-target-surface-contract-convergence` | `docs/03.specs/README.md`; `scripts/lib/document_governance/lifecycle/contract.py`; `scripts/lib/document_governance/metadata/profile.py` | Remove historical package bindings; derive the current contract from Stage 99 Registry and current libraries. |
| `S03-0134` | `0134-agent-governance-canonical-convergence` | `.agents/skills/provider-model-evaluation/SKILL.md`; `.claude/skills/provider-model-evaluation/SKILL.md`; `docs/00.agent-governance/skills/provider-model-evaluation.md`; `docs/03.specs/README.md`; `scripts/lib/document_governance/spec_packages.py` | Move accepted behavior to the Stage 00 skill/provider sources, regenerate projections, remove package-specific routing, and delete the index entry. |
| `S03-0135` | `0135-target-surface-delta-convergence` | `.github/INDEX.md`; `docs/03.specs/README.md`; `scripts/lib/document_governance/spec_packages.py` | Rewrite the GitHub/index consumers; Stage 99 Registry, current target-surface code, and `.github/workflow-contract.yml` own current meaning. |
| `S03-0136` | `0136-sdlc-taxonomy-convergence` | `docs/03.specs/README.md`; `scripts/README.md`; `scripts/lib/document_governance/metadata/profile.py`; `scripts/lib/document_governance/operations_catalog.py`; `scripts/lib/document_governance/spec_packages.py`; `scripts/manifest.yaml`; `tests/lib/document_governance/test_operations_taxonomy.py`; `tests/lib/document_governance/test_requirements.py`; `tests/lib/document_governance/test_taxonomy.py`; `tests/validation/test_script_manifest.py`; `tests/validation/test_workspace_governance_migration.py` | Remove package/history pins from all named consumers; `docs/README.md`, stage indexes, Stage 99 Registry, manifest, and current-tree predicates own the taxonomy. |
| `S03-0137` | `0137-agentic-research-pack-rebuild` | `docs/03.specs/0155-validation-surface-reduction/spec.md`; `docs/03.specs/README.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/README.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0002-agent-model-selection.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0005-docker-compose-infrastructure.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0008-harness-engineering.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0010-loop-engineering.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0012-provider-implementation-comparison.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0015-scope-application-matrix.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0017-security-governance.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0019-verification-validation.md`; `docs/90.references/research/0002-agentic-engineering-research-pack/m0020-workspace-baseline.md`; `scripts/lib/document_governance/metadata/profile.py` | Rewrite SPEC-0155 and metadata routing; protected RES-0002 README declaration owns retained research membership. |
| `S03-0152` | `0152-deleted-reference-leaf-disposition` | `docs/03.specs/README.md`; `scripts/lib/document_governance/spec_packages.py` | Remove package-specific routing/indexing; current reference library/tests and this Task own the accepted deletion rule until closure. |
| `S03-0154` | terminal execution bodies in `0154-governance-consistency-convergence` | `docs/03.specs/0155-validation-surface-reduction/spec.md`; `docs/03.specs/0157-script-surface-ownership-convergence/spec.md`; `docs/03.specs/README.md`; `scripts/validation/agent_output_eval.py` | Write durable outcomes to `docs/03.specs/0154-governance-consistency-convergence/spec.md`; every named consumer may reference only that Spec, not its Plan/Tasks. |
| `S03-0155` | terminal execution bodies in `0155-validation-surface-reduction` | `docs/03.specs/0157-script-surface-ownership-convergence/spec.md`; `docs/03.specs/README.md` | Write durable outcomes to `docs/03.specs/0155-validation-surface-reduction/spec.md`; remove Plan/Task links. |
| `S03-0157` | terminal execution bodies in `0157-script-surface-ownership-convergence` | `docs/03.specs/0158-document-governance-lifecycle-convergence/spec.md`; `docs/03.specs/README.md`; `scripts/README.md` | Keep only `docs/03.specs/0157-script-surface-ownership-convergence/spec.md` as the completed outcome and rewrite named consumers. |
| `S03-0158` | terminal Plan/Task in `0158-document-governance-lifecycle-convergence` | `docs/03.specs/README.md` | Complete `docs/03.specs/0158-document-governance-lifecycle-convergence/spec.md`, prove Git recovery, then make the index point only to that Spec. |

Migration handoffs use exact retained code/document consumers. References from
other deleting execution bodies are still removed in the same wave but are not
retention reasons.

| Handoff | Migration | Retained inbound consumers at `6317553e` | Required handoff and canonical replacement |
| :--- | :--- | :--- | :--- |
| `S98-M0001` | `0001-sdlc-taxonomy-convergence.md` | `scripts/lib/document_governance/lifecycle/promoted.py`; `scripts/lib/document_governance/metadata/lifecycle.py`; `tests/lib/document_governance/test_archive.py`; `tests/lib/document_governance/test_taxonomy.py`; `tests/validation/test_script_manifest.py` | Remove Migration membership/promotion coupling; Stage 99 Registry, current lifecycle predicates, and Git recovery replace it. |
| `S98-M0002` | `0002-operations-catalog-convergence.md` | `scripts/lib/document_governance/metadata/lifecycle.py`; `scripts/lib/document_governance/operations_catalog.py`; `scripts/manifest.yaml`; `scripts/validation/check-script-manifest.py`; `tests/validation/test_script_manifest.py` | Derive Operations membership from Stage 99 Registry/current Stage 05 tree; remove Migration and manifest/output coupling. |
| `S98-M0003` | `0003-workspace-governance-simplification.md` | `docs/02.architecture/decisions/0029-workspace-governance-authority.md`; `docs/05.operations/catalog/00-workspace/0003-env-key-comparison/guide.md`; `docs/05.operations/catalog/00-workspace/0010-sensitive-env-vars-comparison/guide.md`; `docs/99.templates/README.md`; `scripts/lib/document_governance/archive.py`; `scripts/lib/document_governance/identity_history.py`; `scripts/lib/document_governance/lifecycle/public.py`; `scripts/lib/document_governance/metadata/heading.py`; `scripts/lib/document_governance/metadata/lifecycle.py`; `scripts/lib/document_governance/metadata/profile.py`; `scripts/lib/document_governance/metadata/reference.py`; `scripts/lib/document_governance/operations_catalog.py`; `scripts/lib/document_governance/references.py`; `scripts/lib/document_governance/spec_packages.py`; `scripts/manifest.yaml`; `scripts/security/generate-supply-chain-sample-service-summary.sh`; `scripts/validation/check-script-manifest.py`; `scripts/validation/generate-audit-implementation-matrix.sh`; `scripts/validation/generate-security-automation-readiness.sh`; `tests/lib/document_governance/test_archive.py`; `tests/lib/document_governance/test_metadata_validator.py`; `tests/lib/document_governance/test_references.py`; `tests/validation/test_script_manifest.py`; `tests/validation/test_security_automation_readiness.py`; `tests/validation/test_workspace_governance_migration.py` | Rewrite named current docs and remove historical-target coupling from every named source/test; Stage 00, Stage 99, manifest, current Task evidence, current-tree predicates, and Git recovery replace the Migration. |

The Stage 99 Migration template has one retained consumer:
`docs/99.templates/registry.json`; Data 0082 is already governed by
`S90-D0082`. Task 6 removes the Registry route/profile and then deletes
`docs/99.templates/templates/archive/migration.template.md`; no replacement
template is created.

### Explicit non-keep dispositions

The table records every non-`keep` Markdown path. “Migrate” means move its
current consumer or unique needed meaning first; it never means copying the
body. Recovery values are regular-blob addresses at the Task baseline.

| Path | Owner | Current consumers | Finding | Disposition | Replacement | Recovery | Reviewer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `docs/00.agent-governance/policies/approval-boundaries.md` | Stage 00 policy | bootstrap, roles, providers, validators | Neutral workflow or approval semantics overlap Provider Registry/runtime | rewrite | same Stage 00 policy owner | `6317553e:docs/00.agent-governance/policies/approval-boundaries.md` | `rules-engineer` + `code-reviewer` |
| `docs/00.agent-governance/policies/bootstrap.md` | Stage 00 policy | bootstrap, roles, providers, validators | Neutral workflow or approval semantics overlap Provider Registry/runtime | rewrite | same Stage 00 policy owner | `6317553e:docs/00.agent-governance/policies/bootstrap.md` | `rules-engineer` + `code-reviewer` |
| `docs/00.agent-governance/policies/documentation-protocol.md` | Stage 00 policy | authors, roles, document validators | Treats Stage 98 as an active historical lookup/authoring route | rewrite | Stage 99 current document contract plus Git recovery policy | `6317553e:docs/00.agent-governance/policies/documentation-protocol.md` | `rules-engineer` + `code-reviewer` |
| `docs/00.agent-governance/policies/environment-constraints.md` | Stage 00 policy | bootstrap, roles, providers, validators | Neutral workflow or approval semantics overlap Provider Registry/runtime | rewrite | same Stage 00 policy owner | `6317553e:docs/00.agent-governance/policies/environment-constraints.md` | `rules-engineer` + `code-reviewer` |
| `docs/00.agent-governance/policies/github-governance.md` | Stage 00 policy | bootstrap, roles, providers, validators | Neutral workflow or approval semantics overlap Provider Registry/runtime | rewrite | same Stage 00 policy owner | `6317553e:docs/00.agent-governance/policies/github-governance.md` | `rules-engineer` + `code-reviewer` |
| `docs/00.agent-governance/policies/hooks/hookify.warn-hook-parity-edit.md` | Stage 00 hook policy | hook parity procedure | References `.codex/README.md`, which has no native runtime role and is scheduled for deletion after document handoff | rewrite | Provider Registry plus native hook configs | `6317553e:docs/00.agent-governance/policies/hooks/hookify.warn-hook-parity-edit.md` | `rules-engineer` + `code-reviewer` |
| `docs/00.agent-governance/policies/hooks/hookify.warn-parallel-doc-file.md` | Stage 00 hook policy | documentation workflow | Publishes retired Plan/Task route | rewrite | Stage 03 co-located Task route | `6317553e:docs/00.agent-governance/policies/hooks/hookify.warn-parallel-doc-file.md` | `rules-engineer` + `code-reviewer` |
| `docs/00.agent-governance/policies/provider-capability-matrix.md` | Stage 00 policy | bootstrap, roles, providers, validators | Neutral workflow or approval semantics overlap Provider Registry/runtime | rewrite | same Stage 00 policy owner | `6317553e:docs/00.agent-governance/policies/provider-capability-matrix.md` | `rules-engineer` + `code-reviewer` |
| `docs/00.agent-governance/policies/workflows.md` | Stage 00 policy | bootstrap, roles, providers, validators | Neutral workflow or approval semantics overlap Provider Registry/runtime | rewrite | same Stage 00 policy owner | `6317553e:docs/00.agent-governance/policies/workflows.md` | `rules-engineer` + `code-reviewer` |
| `docs/00.agent-governance/providers/README.md` | Stage 00 provider index | provider adapters and renderer | Provider/runtime and document-path namespaces need separation | rewrite | same canonical provider index | `6317553e:docs/00.agent-governance/providers/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/01.requirements/0024-agent-governance-standardization.md` | REQ-0024 | agent-governance architecture and Specs | Stale Stage 04, HADS, and phase terminology | rewrite | REQ-0024 current governance obligations | `6317553e:docs/01.requirements/0024-agent-governance-standardization.md` | `rules-engineer` + `code-reviewer` |
| `docs/02.architecture/decisions/0028-local-isolated-readiness-evidence.md` | Stage 02 current architecture | requirements, Specs, implementation | Retired path or lifecycle wording is presented as current | rewrite | same Stage 02 Architecture/ADR owner | `6317553e:docs/02.architecture/decisions/0028-local-isolated-readiness-evidence.md` | `rules-engineer` + `code-reviewer` |
| `docs/02.architecture/decisions/0029-workspace-governance-authority.md` | ADR-0029 | Stage 00, Stage 99, validators | Treats Migration 0003 and a Stage 98 file as current authority | rewrite | ADR-0029 current owner boundaries | `6317553e:docs/02.architecture/decisions/0029-workspace-governance-authority.md` | `rules-engineer` + `code-reviewer` |
| `docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md` | superseded ADR-0027 | ADR-0029 reciprocal supersession and architecture tests | Superseded body publishes HADS, Phase, and Stage 04 routes that are not current | rewrite | minimal superseded decision record pointing to ADR-0029; no current procedure | `6317553e:docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md` | `rules-engineer` + `code-reviewer` |
| `docs/02.architecture/descriptions/0018-security-optimization-hardening-architecture.md` | AD-0018 | REQ-0015, ADR-0018, security implementation | Generic Phase 1--3 roadmap is not a registered lifecycle | rewrite | same implemented-current architecture with future items explicitly labeled | `6317553e:docs/02.architecture/descriptions/0018-security-optimization-hardening-architecture.md` | `rules-engineer` + `code-reviewer` |
| `docs/02.architecture/descriptions/0019-data-optimization-hardening-architecture.md` | AD-0019 | REQ-0016, ADR-0019, data implementation | Generic Phase 1--3 roadmap is not a registered lifecycle | rewrite | same implemented-current architecture with future items explicitly labeled | `6317553e:docs/02.architecture/descriptions/0019-data-optimization-hardening-architecture.md` | `rules-engineer` + `code-reviewer` |
| `docs/02.architecture/descriptions/0027-agent-governance-canonical-adapter.md` | Stage 02 current architecture | requirements, Specs, implementation | Retired path or lifecycle wording is presented as current | rewrite | same Stage 02 Architecture/ADR owner | `6317553e:docs/02.architecture/descriptions/0027-agent-governance-canonical-adapter.md` | `rules-engineer` + `code-reviewer` |
| `docs/02.architecture/descriptions/0028-operational-readiness-closure.md` | Stage 02 current architecture | requirements, Specs, implementation | Retired path or lifecycle wording is presented as current | rewrite | same Stage 02 Architecture/ADR owner | `6317553e:docs/02.architecture/descriptions/0028-operational-readiness-closure.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0003-security/spec.md` | current capability Spec | security implementation and Operations | Generic phase roadmap mixes implemented and future obligations | rewrite | same capability Spec with explicit current/future distinction | `6317553e:docs/03.specs/0003-security/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0004-data/spec.md` | current capability Spec | data implementation and Operations | Generic phase roadmap mixes implemented and future obligations | rewrite | same capability Spec with explicit current/future distinction | `6317553e:docs/03.specs/0004-data/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0006-messaging/spec.md` | current capability Spec | messaging implementation and Operations | Generic phase roadmap mixes implemented and future obligations | rewrite | same capability Spec with explicit current/future distinction | `6317553e:docs/03.specs/0006-messaging/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0007-observability/spec.md` | current capability Spec | observability implementation and Operations | Generic phase roadmap mixes implemented and future obligations | rewrite | same capability Spec with explicit current/future distinction | `6317553e:docs/03.specs/0007-observability/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0008-workflow/spec.md` | current capability Spec | implementation and Operations | Retired route appears in current capability contract | rewrite | same capability Spec | `6317553e:docs/03.specs/0008-workflow/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0009-ai/spec.md` | current capability Spec | implementation and Operations | Retired route appears in current capability contract | rewrite | same capability Spec | `6317553e:docs/03.specs/0009-ai/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0093-docs-taxonomy-agent-first-migration/spec.md` | predecessor change Spec | current implementation and stage index | Completed change packet remains active | rewrite | terminal Spec with outcomes in current owners | `6317553e:docs/03.specs/0093-docs-taxonomy-agent-first-migration/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0094-harness-agent-first-engineering/spec.md` | predecessor change Spec | current implementation and stage index | Completed change packet remains active | rewrite | terminal Spec with outcomes in current owners | `6317553e:docs/03.specs/0094-harness-agent-first-engineering/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0095-infra-secrets-docs-refresh/spec.md` | predecessor change Spec | current implementation and stage index | Completed change packet remains active | rewrite | terminal Spec with outcomes in current owners | `6317553e:docs/03.specs/0095-infra-secrets-docs-refresh/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0096-llm-wiki-agent-first-completion/spec.md` | predecessor change Spec | current implementation and stage index | Completed change packet remains active | rewrite | terminal Spec with outcomes in current owners | `6317553e:docs/03.specs/0096-llm-wiki-agent-first-completion/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0097-home-docker-revalidation-deferred-follow-up/spec.md` | predecessor change Spec | current implementation and stage index | Completed change packet remains active | rewrite | terminal Spec with outcomes in current owners | `6317553e:docs/03.specs/0097-home-docker-revalidation-deferred-follow-up/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0098-standardize-infra-net/spec.md` | predecessor change Spec | current implementation and stage index | Completed change packet remains active | rewrite | terminal Spec with outcomes in current owners | `6317553e:docs/03.specs/0098-standardize-infra-net/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0102-workspace-document-contract-audit-pack/spec.md` | predecessor Spec | `S03-0102` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0102` canonical handoff | `6317553e:docs/03.specs/0102-workspace-document-contract-audit-pack/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0102-workspace-document-contract-audit-pack/tasks/tsk-0001-governance-conformance-audit.md` | predecessor execution body | `S03-0102` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0102` canonical handoff | `6317553e:docs/03.specs/0102-workspace-document-contract-audit-pack/tasks/tsk-0001-governance-conformance-audit.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0103-document-restructure-audit-contract-archive/spec.md` | predecessor Spec | `S03-0103` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0103` canonical handoff | `6317553e:docs/03.specs/0103-document-restructure-audit-contract-archive/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0105-agentic-engineering-implementation-audit-pack/spec.md` | predecessor Spec | `S03-0105` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0105` canonical handoff | `6317553e:docs/03.specs/0105-agentic-engineering-implementation-audit-pack/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0123-agentic-engineering-audit-remediation/spec.md` | predecessor Spec | `S03-0123` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0123` canonical handoff | `6317553e:docs/03.specs/0123-agentic-engineering-audit-remediation/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0123-agentic-engineering-audit-remediation/tasks/tsk-0001-research-pack-extension.md` | predecessor execution body | `S03-0123` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0123` canonical handoff | `6317553e:docs/03.specs/0123-agentic-engineering-audit-remediation/tasks/tsk-0001-research-pack-extension.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0131-document-corpus-lifecycle-migration-foundation/spec.md` | predecessor Spec | `S03-0131` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0131` canonical handoff | `6317553e:docs/03.specs/0131-document-corpus-lifecycle-migration-foundation/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0132-agent-governance-harness-convergence/spec.md` | predecessor Spec | `S03-0132` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0132` canonical handoff | `6317553e:docs/03.specs/0132-agent-governance-harness-convergence/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0133-target-surface-contract-convergence/spec.md` | predecessor Spec | `S03-0133` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0133` canonical handoff | `6317553e:docs/03.specs/0133-target-surface-contract-convergence/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0134-agent-governance-canonical-convergence/plan.md` | predecessor execution body | `S03-0134` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0134` canonical handoff | `6317553e:docs/03.specs/0134-agent-governance-canonical-convergence/plan.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0134-agent-governance-canonical-convergence/spec.md` | predecessor Spec | `S03-0134` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0134` canonical handoff | `6317553e:docs/03.specs/0134-agent-governance-canonical-convergence/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0134-agent-governance-canonical-convergence/tasks/tsk-0001-canonical-convergence.md` | predecessor execution body | `S03-0134` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0134` canonical handoff | `6317553e:docs/03.specs/0134-agent-governance-canonical-convergence/tasks/tsk-0001-canonical-convergence.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0135-target-surface-delta-convergence/plan.md` | predecessor execution body | `S03-0135` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0135` canonical handoff | `6317553e:docs/03.specs/0135-target-surface-delta-convergence/plan.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0135-target-surface-delta-convergence/spec.md` | predecessor Spec | `S03-0135` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0135` canonical handoff | `6317553e:docs/03.specs/0135-target-surface-delta-convergence/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0135-target-surface-delta-convergence/tasks/tsk-0001-delta-convergence.md` | predecessor execution body | `S03-0135` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0135` canonical handoff | `6317553e:docs/03.specs/0135-target-surface-delta-convergence/tasks/tsk-0001-delta-convergence.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0136-sdlc-taxonomy-convergence/plan.md` | predecessor execution body | `S03-0136` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0136` canonical handoff | `6317553e:docs/03.specs/0136-sdlc-taxonomy-convergence/plan.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0136-sdlc-taxonomy-convergence/spec.md` | predecessor Spec | `S03-0136` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0136` canonical handoff | `6317553e:docs/03.specs/0136-sdlc-taxonomy-convergence/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0136-sdlc-taxonomy-convergence/tasks/tsk-0001-taxonomy-convergence.md` | predecessor execution body | `S03-0136` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0136` canonical handoff | `6317553e:docs/03.specs/0136-sdlc-taxonomy-convergence/tasks/tsk-0001-taxonomy-convergence.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0137-agentic-research-pack-rebuild/plan.md` | predecessor execution body | `S03-0137` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0137` canonical handoff | `6317553e:docs/03.specs/0137-agentic-research-pack-rebuild/plan.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0137-agentic-research-pack-rebuild/spec.md` | predecessor Spec | `S03-0137` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0137` canonical handoff | `6317553e:docs/03.specs/0137-agentic-research-pack-rebuild/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0002-source-refresh.md` | predecessor execution body | `S03-0137` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0137` canonical handoff | `6317553e:docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0002-source-refresh.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0003-deepening.md` | predecessor execution body | `S03-0137` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0137` canonical handoff | `6317553e:docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0003-deepening.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md` | predecessor execution body | `S03-0137` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0137` canonical handoff | `6317553e:docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0152-deleted-reference-leaf-disposition/plan.md` | predecessor execution body | `S03-0152` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0152` canonical handoff | `6317553e:docs/03.specs/0152-deleted-reference-leaf-disposition/plan.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0152-deleted-reference-leaf-disposition/spec.md` | predecessor Spec | `S03-0152` retained-inbound set | Audit/migration/convergence packet duplicates current owner | consolidate-then-delete | `S03-0152` canonical handoff | `6317553e:docs/03.specs/0152-deleted-reference-leaf-disposition/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0152-deleted-reference-leaf-disposition/tasks/tsk-0001-reference-disposition.md` | predecessor execution body | `S03-0152` retained-inbound set | Active/draft/cancelled execution ledger overlaps SPEC-0158 | consolidate-then-delete | `S03-0152` canonical handoff | `6317553e:docs/03.specs/0152-deleted-reference-leaf-disposition/tasks/tsk-0001-reference-disposition.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0154-governance-consistency-convergence/plan.md` | completed Spec execution | `S03-0154` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0154` canonical handoff | `6317553e:docs/03.specs/0154-governance-consistency-convergence/plan.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0154-governance-consistency-convergence/spec.md` | completed capability Spec | current validators and stage index | Current outcome still cites retired history or route | rewrite | same completed Spec without archive dependency | `6317553e:docs/03.specs/0154-governance-consistency-convergence/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0001-stage-00-canonical-repair.md` | completed Spec execution | `S03-0154` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0154` canonical handoff | `6317553e:docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0001-stage-00-canonical-repair.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0002-role-skill-canonicalization.md` | completed Spec execution | `S03-0154` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0154` canonical handoff | `6317553e:docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0002-role-skill-canonicalization.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0003-lifecycle-completion.md` | completed Spec execution | `S03-0154` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0154` canonical handoff | `6317553e:docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0003-lifecycle-completion.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0004-retired-taxonomy-removal.md` | completed Spec execution | `S03-0154` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0154` canonical handoff | `6317553e:docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0004-retired-taxonomy-removal.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0005-gate-scope-correction.md` | completed Spec execution | `S03-0154` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0154` canonical handoff | `6317553e:docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0005-gate-scope-correction.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0006-blocking-gate-reconciliation.md` | completed Spec execution | `S03-0154` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0154` canonical handoff | `6317553e:docs/03.specs/0154-governance-consistency-convergence/tasks/tsk-0006-blocking-gate-reconciliation.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0155-validation-surface-reduction/plan.md` | completed Spec execution | `S03-0155` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0155` canonical handoff | `6317553e:docs/03.specs/0155-validation-surface-reduction/plan.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0155-validation-surface-reduction/spec.md` | completed capability Spec | current validators and stage index | Current outcome still cites retired history or route | rewrite | same completed Spec without archive dependency | `6317553e:docs/03.specs/0155-validation-surface-reduction/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0001-full-gate-restoration.md` | completed Spec execution | `S03-0155` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0155` canonical handoff | `6317553e:docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0001-full-gate-restoration.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0002-blocking-mode-closure.md` | completed Spec execution | `S03-0155` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0155` canonical handoff | `6317553e:docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0002-blocking-mode-closure.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0003-spec-0137-disposition.md` | completed Spec execution | `S03-0155` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0155` canonical handoff | `6317553e:docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0003-spec-0137-disposition.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0004-resurrected-contract-removal.md` | completed Spec execution | `S03-0155` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0155` canonical handoff | `6317553e:docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0004-resurrected-contract-removal.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0005-gate4-and-retiring-pack-removal.md` | completed Spec execution | `S03-0155` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0155` canonical handoff | `6317553e:docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0005-gate4-and-retiring-pack-removal.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0006-stage-04-literal-closure.md` | completed Spec execution | `S03-0155` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0155` canonical handoff | `6317553e:docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0006-stage-04-literal-closure.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0007-generated-evidence-verification.md` | completed Spec execution | `S03-0155` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0155` canonical handoff | `6317553e:docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0007-generated-evidence-verification.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0008-gate-sweep-and-merge-preparation.md` | completed Spec execution | `S03-0155` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0155` canonical handoff | `6317553e:docs/03.specs/0155-validation-surface-reduction/tasks/tsk-0008-gate-sweep-and-merge-preparation.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0157-script-surface-ownership-convergence/plan.md` | completed Spec execution | `S03-0157` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0157` canonical handoff | `6317553e:docs/03.specs/0157-script-surface-ownership-convergence/plan.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0157-script-surface-ownership-convergence/spec.md` | completed capability Spec | current validators and stage index | Current outcome still cites retired history or route | rewrite | same completed Spec without archive dependency | `6317553e:docs/03.specs/0157-script-surface-ownership-convergence/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0157-script-surface-ownership-convergence/tasks/tsk-0001-convergence.md` | completed Spec execution | `S03-0157` retained-inbound set | Terminal Plan/Task duplicates durable outcome | delete-after-writeback | `S03-0157` canonical handoff | `6317553e:docs/03.specs/0157-script-surface-ownership-convergence/tasks/tsk-0001-convergence.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0158-document-governance-lifecycle-convergence/plan.md` | SPEC-0158 execution | `S03-0158` retained-inbound set | Transient execution body | delete-after-completion | `S03-0158` canonical handoff | `6317553e:docs/03.specs/0158-document-governance-lifecycle-convergence/plan.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0158-document-governance-lifecycle-convergence/spec.md` | SPEC-0158 | current Plan and Task | Transitional archive-file names must not survive terminal state | rewrite | completed SPEC-0158 outcome | `6317553e:docs/03.specs/0158-document-governance-lifecycle-convergence/spec.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/0158-document-governance-lifecycle-convergence/tasks/tsk-0001-convergence.md` | SPEC-0158 execution | `S03-0158` retained-inbound set | Transient execution body | delete-after-completion | `S03-0158` canonical handoff | `6317553e:docs/03.specs/0158-document-governance-lifecycle-convergence/tasks/tsk-0001-convergence.md` | `rules-engineer` + `code-reviewer` |
| `docs/03.specs/README.md` | Stage 03 index | all Spec Packages | Links archive as current destination and describes completed bodies as retained | rewrite | Stage 03 current-package index | `6317553e:docs/03.specs/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/05.operations/catalog/00-workspace/0003-env-key-comparison/guide.md` | Stage 05 Operations subject | operators and Operations validator | Current procedure links Stage 98 or retired Stage 04 evidence | rewrite | same Guide/Policy with current Task/owner route | `6317553e:docs/05.operations/catalog/00-workspace/0003-env-key-comparison/guide.md` | `rules-engineer` + `code-reviewer` |
| `docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/guide.md` | Stage 05 Operations subject | operators and Operations validator | Current procedure consumes `.codex/README.md`, which has no native runtime role and is scheduled for deletion | rewrite | same Guide pointing to `.codex/agents/*.toml`, `.codex/hooks.json`, and the Stage 00 provider index/registry | `6317553e:docs/05.operations/catalog/00-workspace/0004-harness-agent-first-engineering/guide.md` | `rules-engineer` + `code-reviewer` |
| `docs/05.operations/catalog/00-workspace/0010-sensitive-env-vars-comparison/guide.md` | Stage 05 Operations subject | operators and Operations validator | Current procedure links Stage 98 or retired Stage 04 evidence | rewrite | same Guide/Policy with current Task/owner route | `6317553e:docs/05.operations/catalog/00-workspace/0010-sensitive-env-vars-comparison/guide.md` | `rules-engineer` + `code-reviewer` |
| `docs/05.operations/catalog/06-observability/0048-telemetry-retention/policy.md` | Stage 05 Operations subject | operators and Operations validator | Current procedure links Stage 98 or retired Stage 04 evidence | rewrite | same Guide/Policy with current Task/owner route | `6317553e:docs/05.operations/catalog/06-observability/0048-telemetry-retention/policy.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/README.md` | Stage 90 structural index | reference navigation | Index must match protected-only final package set | rewrite | protected RES-0002 package | `6317553e:docs/90.references/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0001-readme/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0001-readme/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0002-automation-coverage-map/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0002-automation-coverage-map/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0003-ci-qa-parser-graphify-decision/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0003-ci-qa-parser-graphify-decision/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0004-contract-governance-map/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0004-contract-governance-map/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0005-frontmatter-inventory/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0005-frontmatter-inventory/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0006-frontmatter-routing-profile/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0006-frontmatter-routing-profile/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0007-gap-register/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0007-gap-register/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0008-historical-evidence-preservation/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0008-historical-evidence-preservation/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0009-readme-profile-inventory/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0009-readme-profile-inventory/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0010-section-profile-inventory/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0010-section-profile-inventory/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0011-template-application-gaps/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0011-template-application-gaps/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0012-readme/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0012-readme/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0013-ci-qa-formatting-contract/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0013-ci-qa-formatting-contract/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0014-frontmatter-profile-inventory/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0014-frontmatter-profile-inventory/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0015-operations-bucket-restructure/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0015-operations-bucket-restructure/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0016-restructure-gap-register/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0016-restructure-gap-register/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0017-sdlc-spec-archive-candidates/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0017-sdlc-spec-archive-candidates/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0018-template-contract-drift/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0018-template-contract-drift/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0019-readme/README.md` | Stage 90 non-normative evidence | `S90-A0019` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0019` canonical handoff | `6317553e:docs/90.references/audits/0019-readme/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0020-agent-instructions-catalog-vibe-models/README.md` | Stage 90 non-normative evidence | `S90-A0020` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0020` canonical handoff | `6317553e:docs/90.references/audits/0020-agent-instructions-catalog-vibe-models/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0021-automation-candidates/README.md` | Stage 90 non-normative evidence | `S90-A0021` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0021` canonical handoff | `6317553e:docs/90.references/audits/0021-automation-candidates/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0022-compose-infrastructure-operations-readiness/README.md` | Stage 90 non-normative evidence | `S90-A0022` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0022` canonical handoff | `6317553e:docs/90.references/audits/0022-compose-infrastructure-operations-readiness/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0023-frontmatter-semantic-inventory/README.md` | Stage 90 non-normative evidence | `S90-A0023` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0023` canonical handoff | `6317553e:docs/90.references/audits/0023-frontmatter-semantic-inventory/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0024-frontmatter-template-readme-implementation/README.md` | Stage 90 non-normative evidence | `S90-A0024` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0024` canonical handoff | `6317553e:docs/90.references/audits/0024-frontmatter-template-readme-implementation/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0025-harness-engineering-implementation/README.md` | Stage 90 non-normative evidence | `S90-A0025` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0025` canonical handoff | `6317553e:docs/90.references/audits/0025-harness-engineering-implementation/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0026-implementation-overview/README.md` | Stage 90 non-normative evidence | `S90-A0026` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0026` canonical handoff | `6317553e:docs/90.references/audits/0026-implementation-overview/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0027-loop-engineering-implementation/README.md` | Stage 90 non-normative evidence | `S90-A0027` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0027` canonical handoff | `6317553e:docs/90.references/audits/0027-loop-engineering-implementation/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0028-provider-harness-loop-implementation/README.md` | Stage 90 non-normative evidence | `S90-A0028` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0028` canonical handoff | `6317553e:docs/90.references/audits/0028-provider-harness-loop-implementation/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0029-sdlc-document-contracts-implementation/README.md` | Stage 90 non-normative evidence | `S90-A0029` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0029` canonical handoff | `6317553e:docs/90.references/audits/0029-sdlc-document-contracts-implementation/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0030-sdlc-quality-formatting-implementation/README.md` | Stage 90 non-normative evidence | `S90-A0030` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0030` canonical handoff | `6317553e:docs/90.references/audits/0030-sdlc-quality-formatting-implementation/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0031-security-framework-maturity/README.md` | Stage 90 non-normative evidence | `S90-A0031` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0031` canonical handoff | `6317553e:docs/90.references/audits/0031-security-framework-maturity/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0032-workspace-rules-environment-implementation/README.md` | Stage 90 non-normative evidence | `S90-A0032` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0032` canonical handoff | `6317553e:docs/90.references/audits/0032-workspace-rules-environment-implementation/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0033-readme/README.md` | Stage 90 non-normative evidence | `S90-A0033` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-A0033` canonical handoff | `6317553e:docs/90.references/audits/0033-readme/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0034-agent-catalog-audit/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0034-agent-catalog-audit/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0035-automation-candidates/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0035-automation-candidates/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0036-harness-loop-audit/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0036-harness-loop-audit/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0037-implementation-overview/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0037-implementation-overview/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/0038-sdlc-qa-security-audit/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/audits/0038-sdlc-qa-security-audit/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/audits/README.md` | Stage 90 structural index | reference navigation | Category becomes empty after mandatory convergence | delete-after-migration | Stage 90 root index | `6317553e:docs/90.references/audits/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0059-compose-profile-service-coverage/README.md` | Stage 90 non-normative evidence | `S90-D0059` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0059` canonical handoff | `6317553e:docs/90.references/data/0059-compose-profile-service-coverage/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0060-image-version-interpretation/README.md` | Stage 90 non-normative evidence | `S90-D0060` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0060` canonical handoff | `6317553e:docs/90.references/data/0060-image-version-interpretation/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0061-tech-stack-version-provenance/README.md` | Stage 90 non-normative evidence | `S90-D0061` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0061` canonical handoff | `6317553e:docs/90.references/data/0061-tech-stack-version-provenance/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0062-stable-reference-terms/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/data/0062-stable-reference-terms/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0063-agent-governance-retirement-ledger/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/data/0063-agent-governance-retirement-ledger/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0064-agent-output-eval-fixtures/README.md` | Stage 90 non-normative evidence | `S90-D0064` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0064` canonical handoff | `6317553e:docs/90.references/data/0064-agent-output-eval-fixtures/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0065-audit-implementation-matrix/README.md` | Stage 90 non-normative evidence | `S90-D0065` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0065` canonical handoff | `6317553e:docs/90.references/data/0065-audit-implementation-matrix/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0066-foundation-summary/README.md` | Stage 90 non-normative evidence | `S90-D0066` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0066` canonical handoff | `6317553e:docs/90.references/data/0066-foundation-summary/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0067-foundation/README.md` | Stage 90 non-normative evidence | `S90-D0067` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0067` canonical handoff | `6317553e:docs/90.references/data/0067-foundation/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0068-target-surface-convergence-summary/README.md` | Stage 90 non-normative evidence | `S90-D0068` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0068` canonical handoff | `6317553e:docs/90.references/data/0068-target-surface-convergence-summary/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0069-target-surface-convergence/README.md` | Stage 90 non-normative evidence | `S90-D0069` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0069` canonical handoff | `6317553e:docs/90.references/data/0069-target-surface-convergence/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0070-gap-to-stage-routing/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/data/0070-gap-to-stage-routing/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0071-github-actions-control-plane-observation/README.md` | Stage 90 non-normative evidence | `S90-D0071` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0071` canonical handoff | `6317553e:docs/90.references/data/0071-github-actions-control-plane-observation/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0072-provider-hook-parity-matrix/README.md` | Stage 90 non-normative evidence | `S90-D0072` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0072` canonical handoff | `6317553e:docs/90.references/data/0072-provider-hook-parity-matrix/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0073-target-surface-delta-manifest/README.md` | Stage 90 non-normative evidence | `S90-D0073` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0073` canonical handoff | `6317553e:docs/90.references/data/0073-target-surface-delta-manifest/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0074-target-surface-delta-summary/README.md` | Stage 90 non-normative evidence | `S90-D0074` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0074` canonical handoff | `6317553e:docs/90.references/data/0074-target-surface-delta-summary/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0075-profile/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/data/0075-profile/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md` | Stage 90 non-normative evidence | `S90-D0076` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0076` canonical handoff | `6317553e:docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0077-docker-compose-to-k3s-migration/README.md` | Stage 90 non-normative evidence | `S90-NONE` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-NONE`; no replacement artifact | `6317553e:docs/90.references/data/0077-docker-compose-to-k3s-migration/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0078-security-automation-readiness/README.md` | Stage 90 non-normative evidence | `S90-D0078` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0078` canonical handoff | `6317553e:docs/90.references/data/0078-security-automation-readiness/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0079-supply-chain-sample-service/README.md` | Stage 90 non-normative evidence | `S90-D0079` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0079` canonical handoff | `6317553e:docs/90.references/data/0079-supply-chain-sample-service/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0082-llm-wiki-index/README.md` | Stage 90 non-normative evidence | `S90-D0082` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0082` canonical handoff | `6317553e:docs/90.references/data/0082-llm-wiki-index/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/0083-repository-map/README.md` | Stage 90 non-normative evidence | `S90-D0083` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-D0083` canonical handoff | `6317553e:docs/90.references/data/0083-repository-map/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/data/README.md` | Stage 90 structural index | reference navigation | Category becomes empty after mandatory convergence | delete-after-migration | Stage 90 root index | `6317553e:docs/90.references/data/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/README.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0001-agent-instructions-vibe-coding.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Must be checked against retiring governance/evidence routes | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0001-agent-instructions-vibe-coding.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0002-agent-model-selection.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Presents retired Stage 04 as a current evidence owner | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0002-agent-model-selection.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0003-ai-agent-catalogs.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Presents retired Stage 04 as a current evidence owner | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0003-ai-agent-catalogs.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0004-automation-pipeline-workflow.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0005-docker-compose-infrastructure.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0005-docker-compose-infrastructure.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0006-document-metadata-lifecycle.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0006-document-metadata-lifecycle.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0007-documentation-architecture.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0007-documentation-architecture.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0008-harness-engineering.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0008-harness-engineering.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0009-llm-wiki-system.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Presents retired Stage 04 and non-protected Stage 90 outputs as current owners | rewrite-non-lossy | same protected path; preserve body, sources, claims; route current navigation to `llms.txt` | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0009-llm-wiki-system.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0010-loop-engineering.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Presents retired Stage 04 as a current evidence owner | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0010-loop-engineering.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0011-memory-hierarchy.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0011-memory-hierarchy.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0012-provider-implementation-comparison.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0012-provider-implementation-comparison.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0013-provider-model-landscape.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Must be checked against retiring provider/evidence routes | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0013-provider-model-landscape.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0014-quality-ci-formatting.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0014-quality-ci-formatting.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0015-scope-application-matrix.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0015-scope-application-matrix.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0016-sdlc-document-roles.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0016-sdlc-document-roles.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0017-security-governance.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Must be checked against retiring governance/evidence routes | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0017-security-governance.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0018-spec-driven-sdlc.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0018-spec-driven-sdlc.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0019-verification-validation.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0019-verification-validation.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0002-agentic-engineering-research-pack/m0020-workspace-baseline.md` | RES-0002 `PROTECT_LATEST` | user retention decision and research readers | Stale path/link metadata inside protected evidence | rewrite-non-lossy | same protected path; preserve body, sources, claims | `6317553e:docs/90.references/research/0002-agentic-engineering-research-pack/m0020-workspace-baseline.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0080-roadmap-v1/README.md` | Stage 90 non-normative evidence | `S90-R0080` retained-inbound set | Not user-protected; structural index consumer must move | migrate-then-delete | `S90-R0080` canonical handoff | `6317553e:docs/90.references/research/0080-roadmap-v1/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0081-roadmap/README.md` | Stage 90 non-normative evidence | `S90-R0081` retained-inbound set | Not user-protected; structural index consumer must move | migrate-then-delete | `S90-R0081` canonical handoff | `6317553e:docs/90.references/research/0081-roadmap/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/0084-github-actions-platform/README.md` | Stage 90 non-normative evidence | `S90-R0084` retained-inbound set | Not user-protected; current meaning/consumers must move | migrate-then-delete | `S90-R0084` canonical handoff | `6317553e:docs/90.references/research/0084-github-actions-platform/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/90.references/research/README.md` | Stage 90 structural index | reference navigation | Index must match protected-only final package set | rewrite | protected RES-0002 package | `6317553e:docs/90.references/research/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/README.md` | Stage 98 structural index | recovery readers | Current archive tree and validation contract are excessive | rewrite | minimal one-way recovery index | `6317553e:docs/98.archive/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md` | temporary Migration history | `S98-M0001` retained-inbound set | Historical file still acts as current membership/authority | migrate-then-delete | `S98-M0001` canonical handoff | `6317553e:docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/migrations/0002-operations-catalog-convergence.md` | temporary Migration history | `S98-M0002` retained-inbound set | Historical file still acts as current membership/authority | migrate-then-delete | `S98-M0002` canonical handoff | `6317553e:docs/98.archive/migrations/0002-operations-catalog-convergence.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/migrations/0003-workspace-governance-simplification.md` | temporary Migration history | `S98-M0003` retained-inbound set | Historical file still acts as current membership/authority | migrate-then-delete | `S98-M0003` canonical handoff | `6317553e:docs/98.archive/migrations/0003-workspace-governance-simplification.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0099-template-system-numbered-sdlc-paths.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0099-template-system-numbered-sdlc-paths.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0100-template-system-contract-standardization.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0100-template-system-contract-standardization.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0101-template-system-reorganization.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0101-template-system-reorganization.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0104-agentic-research-pack-refresh.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0104-agentic-research-pack-refresh.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0106-workspace-support-surface-contract.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0106-workspace-support-surface-contract.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0107-provider-semantic-parity-validator.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0107-provider-semantic-parity-validator.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0108-compose-profile-service-coverage-snapshot.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0108-compose-profile-service-coverage-snapshot.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0109-gap-routing-recommendation.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0109-gap-routing-recommendation.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0110-agent-output-eval-fixtures.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0110-agent-output-eval-fixtures.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0111-qa-gate-recommendation-ci-summary.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0111-qa-gate-recommendation-ci-summary.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0112-audit-pack-coverage-report.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0112-audit-pack-coverage-report.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0113-llm-wiki-stage-category-coverage.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0113-llm-wiki-stage-category-coverage.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0114-tech-stack-version-provenance.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0114-tech-stack-version-provenance.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0115-provider-hook-parity-matrix.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0115-provider-hook-parity-matrix.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0116-agent-output-eval-runner.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0116-agent-output-eval-runner.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0117-security-automation-readiness-snapshot.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0117-security-automation-readiness-snapshot.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0118-audit-implementation-matrix-snapshot.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0118-audit-implementation-matrix-snapshot.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0119-sdlc-document-contract-corpus-normalization.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0119-sdlc-document-contract-corpus-normalization.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0120-agent-output-eval-ci-gate.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0120-agent-output-eval-ci-gate.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0121-dependency-vulnerability-audit-gate.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0121-dependency-vulnerability-audit-gate.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0122-agentic-research-pack-consolidation.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0122-agentic-research-pack-consolidation.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0124-compose-runtime-readiness-remediation.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0124-compose-runtime-readiness-remediation.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0125-infrastructure-operations-readiness-remediation.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0125-infrastructure-operations-readiness-remediation.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0126-security-supply-chain-remediation.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0126-security-supply-chain-remediation.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0127-deployment-release-engineering-remediation.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0127-deployment-release-engineering-remediation.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0128-agentic-audit-harness-consolidation.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0128-agentic-audit-harness-consolidation.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0129-document-contract-canonicalization.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0129-document-contract-canonicalization.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0130-template-contract-system-canonicalization.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0130-template-contract-system-canonicalization.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0154-workspace-audit-2026-05.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0154-workspace-audit-2026-05.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0155-workspace-doc-consistency-2026-05.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0155-workspace-doc-consistency-2026-05.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0156-workspace-consistency-2026-05b.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0156-workspace-consistency-2026-05b.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/03.specs/0157-workspace-governance-simplification.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/03.specs/0157-workspace-governance-simplification.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/05.operations/0086-01-setup.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/05.operations/0086-01-setup.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/05.operations/0087-ksql-streaming.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/05.operations/0087-ksql-streaming.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/05.operations/0088-01-airflow-dag-dev.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/05.operations/0088-01-airflow-dag-dev.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/05.operations/0089-airbyte.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/05.operations/0089-airbyte.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/05.operations/0090-01-llm-inference.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/05.operations/0090-01-llm-inference.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/05.operations/0091-local-llm-setup.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/05.operations/0091-local-llm-setup.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/05.operations/0092-01-iac-automation.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/05.operations/0092-01-iac-automation.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/05.operations/0093-airbyte.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/05.operations/0093-airbyte.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/05.operations/0094-airbyte.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/05.operations/0094-airbyte.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/05.operations/0095-windows-network-ip.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/05.operations/0095-windows-network-ip.md` | `rules-engineer` + `code-reviewer` |
| `docs/98.archive/tombstones/90.references/0158-agentic-research-pack-refresh.md` | Stage 98 Tombstone | zero live recovery-navigation consumers measured | No current preservation or navigation need | delete | Git regular-blob recovery only | `6317553e:docs/98.archive/tombstones/90.references/0158-agentic-research-pack-refresh.md` | `rules-engineer` + `code-reviewer` |
| `docs/99.templates/README.md` | Stage 99 template authority | authors, Registry, validators | Migration-backed current authoring language | rewrite | same current Stage 99 owner | `6317553e:docs/99.templates/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/99.templates/templates/README.md` | Stage 99 template authority | authors, Registry, validators | Migration-backed current authoring language | rewrite | same current Stage 99 owner | `6317553e:docs/99.templates/templates/README.md` | `rules-engineer` + `code-reviewer` |
| `docs/99.templates/templates/archive/migration.template.md` | Stage 99 template authority | `docs/99.templates/registry.json`; retiring `S90-D0082` consumer | Temporary Migration authoring surface has no final consumer | delete-after-consumer-handoff | remove Registry `archive/migration` route/profile; no replacement template | `6317553e:docs/99.templates/templates/archive/migration.template.md` | `rules-engineer` + `code-reviewer` |
| `docs/99.templates/templates/archive/tombstone.template.md` | Stage 99 template authority | minimal retained Tombstone authoring | Template depends on Migration/archive link | rewrite | minimal one-way Tombstone shape | `6317553e:docs/99.templates/templates/archive/tombstone.template.md` | `rules-engineer` + `code-reviewer` |
| `docs/99.templates/templates/common/README.md` | Stage 99 template authority | authors, Registry, validators | Migration-backed current authoring language | rewrite | same current Stage 99 owner | `6317553e:docs/99.templates/templates/common/README.md` | `rules-engineer` + `code-reviewer` |

### Provider-runtime surfaces outside the Markdown target count

| Surface | Measured count | Disposition | Authority |
| :--- | ---: | :--- | :--- |
| `.agents/README.md`, `.agents/agents/*.md`, `.agents/skills/*/SKILL.md` | 38 | regenerate | Stage 00 sources plus Provider Registry |
| `.claude/CLAUDE.md`, `.claude/agents/*.md`, `.claude/skills/*/SKILL.md` | 38 | regenerate | Stage 00 sources plus Provider Registry |
| `.codex/agents/*.toml` | 14 | regenerate | Stage 00 role sources plus Provider Registry |
| `.agents/rules/workspace.md`, `.agents/workflows/documentation.md`, `.codex/README.md` | 3 | delete after exact consumer migration below | no retained native runtime consumer |
| Claude hooks/settings/output style and `.codex/hooks.json` | 10 | keep and validate as native mechanics | Provider Registry plus native runtime config |
| ignored root-checkout `.claude/RESUME.md`, `.claude/settings.local.json` | 2 | exclude from tracked authority and do not mutate without proven local ownership | user/provider-local state |

The two `.agents` leaves are consumed by renderer static routes only after the
retiring Stage 90 evidence is excluded. `.codex/README.md` is consumed by the
renderer, the Stage 00 hook-parity policy, the current Stage 05 harness guide
that is explicitly scheduled for rewrite, the protected provider comparison
research, and SPEC-0094/SPEC-0154 outcome documents; those exact current
consumers must be rewritten before deletion.
The current SPEC-0158 Plan may continue to name the deletion target as execution
scope until its own terminal retirement. Provider freshness was `drift=0`; the
defect is semantic authority duplication rather than generated-file drift.

### Auxiliary current surfaces outside the 592-path target

These paths are not added to the stage-total arithmetic, but they are mandatory
consumer handoffs because a target disposition changes their navigation.

| Path or exact set | Current dependency | Disposition | Replacement | Recovery |
| :--- | :--- | :--- | :--- | :--- |
| `docs/README.md` | Stage 98 Migrations/README and Data 0082/0083 links | rewrite before Stage 90/98 deletion | same current docs index, routing only to active stages, protected RES-0002, Stage 99, and Git recovery policy | `6317553e:docs/README.md` |
| `README.md`, `scripts/README.md`, `llms.txt`, SPEC-0096, and Stage 05 LLM Wiki guide/policy | Data 0082/0083 navigation/output | rewrite under `S90-D0082`/`S90-D0083` | `llms.txt` plus existing root/stage READMEs; no replacement Stage 90 output | each path at `6317553e` |
| `.github/INDEX.md`, `.github/rulesets/main-protection.md` | Data 0071 observation | rewrite under `S90-D0071` | Stage 00 GitHub policy and `.github/workflow-contract.yml` | each path at `6317553e` |
| retained code, tests, manifests, and provider projections named in the Stage 90 ledger | non-protected package path or generated-output coupling | migrate under the exact handoff ID | current Registry, manifest, runtime source, fixture, or check-only output named in that row | each tracked path at `6317553e` |

## Verification Evidence

- `git ls-files <eight roots> | rg '\\.md$' | sort -u`:
  592 tracked Markdown files with per-stage counts recorded above.
- `git ls-files docs/90.references/research/0002-agentic-engineering-research-pack/**`:
  21 protected current-baseline paths.
- `git ls-tree -r 6317553e -- <eight roots>`:
  592 Markdown regular blobs, zero non-regular entries.
- Coverage program: 366 keep plus 226 explicit equals 592; 226 unique explicit
  paths and recovery addresses; zero overlap or missing paths.
- `git cat-file --batch-check` over all 226 recorded recovery addresses:
  226 `blob`, zero missing or non-blob objects.
- Baseline `git grep` set comparison against each ledger row: Stage 90 exact
  retained consumers `36/36`, `S90-NONE` zero-consumer sets `28/28`, Stage 03
  package handoffs `16/16`, and Stage 98 Migration handoffs `3/3`; zero missing
  or extra consumer paths and zero unused handoff IDs.
- `python3 scripts/validation/check-document-links.py --mode alignment`: exit 0.
- `bash scripts/operations/sync-provider-surfaces.sh --check`:
  `providers=2 drift=0`.
- `python3 scripts/validation/check-agent-governance-contract.py --mode repository --section all`:
  failures 0.
- Byte-identical target Markdown scan: zero duplicate groups.
- The Plan's exact archive-file scan returns 35 current-stage files; every one
  is explicit. `docs/README.md`, outside the eight-root total, is separately
  recorded as a mandatory auxiliary rewrite.
- The Plan's exact retired-route/token scan returns 106 files; every affected
  target path is either explicit or a reviewed current-prohibition/example
  use. Generic Phase prose found outside that regex is separately explicit.
- All 64 non-protected Stage 90 package roots have `migrate-then-delete`
  dispositions. The two retained structural indexes (`90.references/README.md`
  and `research/README.md`) are not package roots and are explicit rewrites;
  empty `audits/` and `data/` category indexes are explicit deletions.
- Independent coverage and exact-diff review must be GREEN before this baseline
  is committed.

### 2026-09-01 Task 3 observed evidence

- The provider-registry ownership regression was RED while provider-neutral
  workflow and harness fields remained in the Registry, then GREEN after Stage
  00 became their sole owner. Read-only review-role permissions stayed GREEN.
- Renderer regressions were RED then GREEN for malformed generated markers,
  oversized or stale Codex projections, FIFO nonblocking behavior, symlink and
  replacement races, private quarantine handoff, and pending-cleanup failure.
  Stale generated paths are never automatically unlinked: `--write` preserves
  them in quarantine and returns nonzero until exact manual cleanup, while
  `--check` also remains nonzero.
- Structured-surface regressions parse every generated shared and Claude YAML
  frontmatter document and every Codex TOML role. Arbitrary colon-containing
  identities and model controls are quoted safely, and a Codex null-effort
  mutation is rejected.
- Agent-output evaluation regressions were RED then GREEN for direct
  prohibitions, passive and modal forms, conditional carve-outs, same-sentence
  reversals, and 5,000 repeated clauses. Seven hazard/direct-negation pairs
  prove symmetric handling, including `will/was inferred` versus
  `will/was not inferred`.
- The five changed unit modules ran 116 tests in aggregate with final result
  `OK`. Intentional negative fixture logs are expected assertions, not test
  failures.
- Provider freshness reported `providers=2 drift=0`; the repository
  agent-governance contract reported `failures=0`; script manifest, fixture and
  regression catalogs, hook parity, and both generated LLM Wiki outputs passed.
- Document alignment and traceability each inspected 569 documents and 4,870
  links with zero failures and zero current-to-archive links. Changed metadata
  against the explicit local `main` base selected 25 documents with zero
  violations. Shell syntax, Python compilation, and `git diff --check` passed.
- The protected RES-0002 research pack changed by one line replacement in the
  provider comparison only; no quarantine, temporary projection, archive,
  redirect, or Tombstone artifact was added.

### 2026-09-01 Task 4 observed evidence

- Stage 99 Registry is the sole current profile, path, lifecycle, identity,
  and template-role authority. Operations profiles no longer delegate current
  membership to a Migration, and the Operations validator no longer consumes
  archive rows, recovery commits, frozen inventories, or branch-tip witnesses.
- Current Operations membership is derived from the bounded tracked tree under
  `docs/05.operations/catalog/`. Required indexes and role leaves must be
  tracked regular files without symlink components; malformed Registry input,
  excessive JSON depth, final or parent symlinks, and FIFO replacement races
  fail closed with findings rather than tracebacks or blocking reads.
- Every live copy template has exactly one Registry role. The unused Migration
  authoring template and role were removed, `common/readme` was registered for
  its real consumers, and subject README authoring was removed because current
  Operations subjects are containers whose managed leaves are guides,
  policies, and runbooks.
- Registry, Operations catalog, and Operations taxonomy ran 96 tests with final
  result `OK`. The broader Python review ran 201 core tests, 21 metadata
  heading/lifecycle/reference tests, and 39 archive/taxonomy tests with final
  result `OK`; the metadata suite run recorded here ran 82 tests with result
  `OK`.
- Metadata contracts reported `violations=0`; changed metadata against explicit
  `main` selected 46 paths with zero violations; Operations complete reported
  `PASS`; document links inspected 568 documents and 4,866 links with zero
  failures and zero current-to-archive links; script manifest and both generated
  LLM Wiki outputs passed.
- Scoped Ruff and `git diff --check 360ef5d6` passed. The protected RES-0002
  research pack has zero diff from the Task 3 commit. Changes to Data 0076 and
  Data 0082 are generated path removal only; both non-protected outputs remain
  scheduled for Task 6 deletion.

## Review Evidence

The first read-only reviews both returned `FAIL` and did not grant approval:

- `rules-engineer`: missing actionable Stage 90 consumers/replacements,
  omitted `docs/README.md`, non-executable Stage 03 keep selection, insufficient
  implementation ownership proof, and an unrecorded `.codex/README.md`
  consumer.
- `code-reviewer`: seven protected paths were incorrectly treated as
  unchanged, Stage 90 placeholders were non-actionable, the Stage 03 selector
  was not executable, implementation completeness was overclaimed, and the
  recorded scan counts did not reproduce.

Corrections now make all 21 protected paths explicit non-lossy rewrites, add
exact Stage 90/03/98 deletion handoff ledgers and auxiliary consumers, split
Stage 03 by exact path/status predicates, replace the broad implementation
inventory with exact subject selectors and owner sets, and record the observed
35/106 scan counts. Subsequent read-only review cycles additionally exposed
protected-research consumers in two Stage 03 handoffs, the Stage 05 harness
guide rewrite, retained Stage 90 structural-index consumers, the sample-service
implementation boundary, and the Compose readiness runner. Each finding was
corrected and the complete current diff was re-reviewed.

The final read-only verdicts are GREEN and do not grant approval:

- `rules-engineer`: `GOVERNANCE VERDICT: PASS`; no Critical, Important, or
  Minor findings. Independently reproduced 592-path coverage, 226 blob recovery
  addresses, all 21 protected paths, Stage 90 `36 + 28`, Stage 03 `16/16`,
  Stage 98 `3/3`, implementation-owner coverage, provider contracts, and scan
  counts.
- `code-reviewer`: `EXACT-DIFF VERDICT: PASS`; no Critical, Important, or Minor
  findings. Confirmed one-file scope, arithmetic, handoff equality, recovery,
  protected dispositions, readiness implementation selection, recorded
  validators, and diff hygiene.

### Task 3 independent review

- `rules-engineer`: no Critical, High, or Medium findings; `SPEC`, `QUALITY`,
  and `EXACT-DIFF` verdicts all PASS. It confirmed the Stage 00/Registry
  authority boundary, derived identities, simplified lifecycle controls, and
  inferred-approval grammar.
- `code-reviewer`: no Critical, High, or Medium findings; `SPEC`, `QUALITY`, and
  `EXACT-DIFF` verdicts all PASS. It confirmed exactly 74 regenerated role and
  skill projections, three consumerless deletions, one protected-research line
  replacement, no automatic quarantine deletion, and no transient artifacts.
- `python-reviewer`: no Critical, High, or Medium findings; `SPEC`, `QUALITY`,
  and `EXACT-DIFF` verdicts all PASS. It independently reran the 116 tests,
  compilation and available linting, provider freshness, contracts, manifest,
  parity, and diff hygiene. These review verdicts are evidence and do not
  substitute for user approval.

### Task 4 independent review

- `rules-engineer`: final governance verdict PASS. Its only Low finding was a
  stale fixed-count PASS message; the message was reduced to the derived
  predicate result and revalidated. It confirmed Registry authority, exact
  template registration, current-tree Operations membership, and zero
  protected-research diff.
- `code-reviewer`: no remaining Critical, High, Medium, or Low findings;
  `SPEC`, `QUALITY`, and `EXACT-DIFF` verdicts all PASS. It confirmed archive
  independence, manifest consumer evidence, deleted-template cleanup, Stage 05
  terminology, validators, and diff hygiene.
- `python-reviewer`: final PASS with no High, Medium, or Low findings after
  iterative corrections for tracked membership, non-regular indexes, Registry
  adapter ownership, malformed shapes, allocation bounds, depth limits,
  parent/final symlinks, and FIFO races. It independently ran 201 core tests
  plus focused metadata and archive/taxonomy suites. These review verdicts are
  evidence and do not substitute for user approval.

## Commit Ledger

| Logical change | Commit | Verification |
| :--- | :--- | :--- |
| Activate SPEC-0158 and create its one current Task | `6317553e` | metadata contracts 0, changed metadata 0, links 0, diff hygiene |
| Record lifecycle disposition and consumer handoffs | `f5420ebe` | exact 592-path coverage, recovery blobs, independent governance and exact-diff review |
| Separate neutral governance from provider projections | `360ef5d6` | 116 changed tests, provider drift 0, agent contract 0, links 0, independent three-seat review |
| Make current contracts independent of archive ledgers | `ff82f135` | archive independence, manifest consumer evidence, links 0 |
| Consolidate current governance owners | `e368a092` | Registry authority, exact template registration, protected-research diff 0 |
| Derive Spec Package deletion approval from the current tree | `dcaf9bf1` | RED witnessed then GREEN; `test_spec_packages` 20 OK; Stage 98 authority coupling removed; fixed counts `49`/`46` removed |
| Consolidate duplicate current owners | `d87e3ae4` | `test_requirements` 20 OK, `test_architecture` 14 OK |
| Normalize active execution lifecycles | `61d408ce` | 44 members removed with zero retained parent declarations; metadata contracts 0, check-active 0 |
| Consolidate current procedures | `60608e95` | provider drift 0, links 0 |
| Anchor validation ownership to current authorities | `c2080c6c` | script manifest PASS, `test_script_manifest` OK |
| Correct stale evidence references | `25a38723` | links `failures=0`, generated LLM Wiki fresh, protected pack body unchanged |

## Rulings

1. Lifecycle, owner, consumer, and recovery precede directory location.
2. `PROTECT_LATEST` applies atomically to all 21 current-baseline RES-0002
   paths and survives zero consumers.
3. `llms.txt` becomes the sole tracked LLM entrypoint; generated Stage 90
   index and coverage outputs do not move to another evidence package.
4. All non-protected Stage 90 packages migrate unique current meaning and
   consumers, then delete. Category indexes are structural, not packages.
5. Superseded 2026-09-01 by the Stage 00 document retention and retirement
   policy. Tombstones are not measured by live recovery-navigation consumers
   and are not deleted: one Tombstone per retired package is the tracked
   pointer that keeps deleted content findable, and
   `validate_spec_package_lifecycle` now rejects an unrecorded retirement.
   The temporary Migration documents remain scheduled for deletion once their
   consumers move to current owners.
6. Current stages never link to a Stage 98 file. One-way recovery may point
   from a retained archive record to a current owner. Stage 98 retains one
   Tombstone for every retired package under the Stage 00 policy.
7. Generated provider projections cannot define policy. Neutral workflow,
   evidence, retry, and stop rules belong to Stage 00; the Provider Registry
   retains only runtime translation facts.
8. Fixed role, skill, generated-root, fixture, corpus, or branch-tip counts are
   not acceptance controls. Set equality is derived from current authorities.
9. Historical words such as `legacy` are not deletion selectors when they
   describe a current prohibition or a superseded ADR. Published retired paths,
   duplicated authority, and obsolete active procedures are explicit rewrites
   or deletions.
10. Ignored provider-local files are observed but not promoted to evidence or
    deleted without exact ownership proof.

### 2026-09-01 Task 5 observed evidence

- `PYTHONPATH=. python3 -m unittest <every tests/**/test_*.py module>`:
  `Ran 1094 tests ... OK (skipped=11)`.
- `python3 scripts/validation/run-ci-gate.py --profile full`: exit 0 with zero
  `FAIL` lines on the committed tip.
- `python3 scripts/validation/check-document-metadata.py --mode check-active`:
  `selected=401 violations=0`.
- `python3 scripts/validation/check-document-metadata.py --mode check-contracts`:
  `violations=0`.
- `python3 scripts/validation/check-document-links.py --mode all`:
  `documents=527 links=4451 failures=0`.
- Deletion measurement before mutation: twelve packages were removed in whole
  and three retained their Spec while dropping only `completed` execution
  bodies. No retained Stage 03 document declares a removed member as a parent.

### Task 6 inputs observed during Task 5

- About thirty unlinked plain-text references to the retired `0102` and `0103`
  execution bodies remain inside non-protected Stage 90 audit packages. They
  break no registered check and their containing packages are deleted by
  Task 6, so they were left for that deletion rather than edited twice.
- `identity_history`, `metadata/heading`, `metadata/profile`,
  `lifecycle/promoted`, and `check-agentic-audit-semantic-freshness` still read
  the Stage 98 Migration authority. `spec_packages` no longer does.

## Deferred Items

Runtime, deployment, remote, secret, credential, infrastructure, and
user-global provider state remain out of scope. Stage 90/98 deletion and
terminal Plan/Task retirement occur only in their planned later Tasks after
consumer handoff and focused verification.
