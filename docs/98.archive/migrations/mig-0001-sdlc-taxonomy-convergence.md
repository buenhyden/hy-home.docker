---
status: archived
artifact_id: mig-0001
artifact_type: archive
parent_ids: []
archived_from: docs/04.execution/plans/2026-08-07-sdlc-taxonomy-convergence.md
archived_at: 2026-08-10T00:00:00+09:00
archive_reason: evidence-preserve
archive_disposition: evidence-preserve
archived_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
archived_blob: 4cab4694b46904c24cf44ec1ae475ee474cbec3b
preservation_class: git-history
---

# SDLC Taxonomy Convergence Migration Ledger

## Overview

This is the bounded, typed disposition ledger for the approved SDLC taxonomy
convergence wave. It records the source baseline and exactly one target action
for every tracked document beneath the affected stages. It is evidence for
later migration Tasks, not a current-use destination.

## Archive Metadata

- `migration_id`: `mig-0001`
- `baseline_commit`: `232effd9a5e00907bdbe30efc6665023fb2d07f4`
- `record_order`: `legacy_path` ascending
- `scope`: `docs/01.requirements`, `docs/02.architecture`,
  `docs/03.specs`, `docs/04.execution`, `docs/05.operations`,
  `docs/90.references`, and `docs/98.archive`

## Archive Ledger

```yaml
schema_version: 1
migration_id: mig-0001
baseline_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
records:
- legacy_path: docs/01.requirements/001-gateway.md
  stable_path: docs/01.requirements/prd-001-gateway.md
  artifact_id: prd-001
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-001-gateway.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/002-auth.md
  stable_path: docs/01.requirements/prd-002-auth.md
  artifact_id: prd-002
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-002-auth.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/003-security.md
  stable_path: docs/01.requirements/prd-003-security.md
  artifact_id: prd-003
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-003-security.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/004-data.md
  stable_path: docs/01.requirements/prd-004-data.md
  artifact_id: prd-004
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-004-data.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/005-data-analytics.md
  stable_path: docs/01.requirements/prd-005-data-analytics.md
  artifact_id: prd-005
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-005-data-analytics.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/006-messaging.md
  stable_path: docs/01.requirements/prd-006-messaging.md
  artifact_id: prd-006
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-006-messaging.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/007-observability.md
  stable_path: docs/01.requirements/prd-007-observability.md
  artifact_id: prd-007
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-007-observability.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/008-workflow.md
  stable_path: docs/01.requirements/prd-008-workflow.md
  artifact_id: prd-008
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-008-workflow.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/009-ai.md
  stable_path: docs/01.requirements/prd-009-ai.md
  artifact_id: prd-009
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-009-ai.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/010-tooling.md
  stable_path: docs/01.requirements/prd-010-tooling.md
  artifact_id: prd-010
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-010-tooling.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/011-communication.md
  stable_path: docs/01.requirements/prd-011-communication.md
  artifact_id: prd-011
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-011-communication.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/012-laboratory.md
  stable_path: docs/01.requirements/prd-012-laboratory.md
  artifact_id: prd-012
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-012-laboratory.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/013-ai-open-webui.md
  stable_path: docs/01.requirements/prd-013-ai-open-webui.md
  artifact_id: prd-013
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-013-ai-open-webui.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/014-auth-optimization-hardening.md
  stable_path: docs/01.requirements/prd-014-auth-optimization-hardening.md
  artifact_id: prd-014
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-014-auth-optimization-hardening.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/015-security-optimization-hardening.md
  stable_path: docs/01.requirements/prd-015-security-optimization-hardening.md
  artifact_id: prd-015
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-015-security-optimization-hardening.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/016-data-optimization-hardening.md
  stable_path: docs/01.requirements/prd-016-data-optimization-hardening.md
  artifact_id: prd-016
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-016-data-optimization-hardening.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/017-messaging-optimization-hardening.md
  stable_path: docs/01.requirements/prd-017-messaging-optimization-hardening.md
  artifact_id: prd-017
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-017-messaging-optimization-hardening.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/018-observability-optimization-hardening.md
  stable_path: docs/01.requirements/prd-018-observability-optimization-hardening.md
  artifact_id: prd-018
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-018-observability-optimization-hardening.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/019-workflow-optimization-hardening.md
  stable_path: docs/01.requirements/prd-019-workflow-optimization-hardening.md
  artifact_id: prd-019
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-019-workflow-optimization-hardening.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/020-ai-optimization-hardening.md
  stable_path: docs/01.requirements/prd-020-ai-optimization-hardening.md
  artifact_id: prd-020
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-020-ai-optimization-hardening.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/021-tooling-optimization-hardening.md
  stable_path: docs/01.requirements/prd-021-tooling-optimization-hardening.md
  artifact_id: prd-021
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-021-tooling-optimization-hardening.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/022-laboratory-optimization-hardening.md
  stable_path: docs/01.requirements/prd-022-laboratory-optimization-hardening.md
  artifact_id: prd-022
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-022-laboratory-optimization-hardening.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/023-standardize-infra-net.md
  stable_path: docs/01.requirements/prd-023-standardize-infra-net.md
  artifact_id: prd-023
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-023-standardize-infra-net.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/024-agent-governance-standardization.md
  stable_path: docs/01.requirements/prd-024-agent-governance-standardization.md
  artifact_id: prd-024
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-024-agent-governance-standardization.md; migrate 14 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/025-operational-readiness-closure.md
  stable_path: docs/01.requirements/prd-025-operational-readiness-closure.md
  artifact_id: prd-025
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/01.requirements/prd-025-operational-readiness-closure.md; migrate 26 resolved inbound link(s) with it.
- legacy_path: docs/01.requirements/README.md
  stable_path: docs/01.requirements/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 16 resolved inbound link(s).
- legacy_path: docs/02.architecture/README.md
  stable_path: docs/02.architecture/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 10 resolved inbound link(s).
- legacy_path: docs/02.architecture/decisions/0001-traefik-nginx-hybrid.md
  stable_path: docs/02.architecture/decisions/adr-0001-traefik-nginx-hybrid.md
  artifact_id: adr-0001
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0001-traefik-nginx-hybrid.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0002-keycloak-oauth2-proxy-choice.md
  stable_path: docs/02.architecture/decisions/adr-0002-keycloak-oauth2-proxy-choice.md
  artifact_id: adr-0002
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0002-keycloak-oauth2-proxy-choice.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0003-vault-as-secrets-manager.md
  stable_path: docs/02.architecture/decisions/adr-0003-vault-as-secrets-manager.md
  artifact_id: adr-0003
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0003-vault-as-secrets-manager.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0004-postgresql-ha-patroni.md
  stable_path: docs/02.architecture/decisions/adr-0004-postgresql-ha-patroni.md
  artifact_id: adr-0004
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0004-postgresql-ha-patroni.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0005-kafka-vs-rabbitmq-selection.md
  stable_path: docs/02.architecture/decisions/adr-0005-kafka-vs-rabbitmq-selection.md
  artifact_id: adr-0005
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0005-kafka-vs-rabbitmq-selection.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0006-lgtm-stack-selection.md
  stable_path: docs/02.architecture/decisions/adr-0006-lgtm-stack-selection.md
  artifact_id: adr-0006
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0006-lgtm-stack-selection.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md
  stable_path: docs/02.architecture/decisions/adr-0007-airflow-n8n-hybrid-workflow.md
  artifact_id: adr-0007
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0007-airflow-n8n-hybrid-workflow.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0008-ollama-openwebui-local-ai.md
  stable_path: docs/02.architecture/decisions/adr-0008-ollama-openwebui-local-ai.md
  artifact_id: adr-0008
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0008-ollama-openwebui-local-ai.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0009-tooling-services.md
  stable_path: docs/02.architecture/decisions/adr-0009-tooling-services.md
  artifact_id: adr-0009
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0009-tooling-services.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0010-communication-services.md
  stable_path: docs/02.architecture/decisions/adr-0010-communication-services.md
  artifact_id: adr-0010
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0010-communication-services.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0011-laboratory-services.md
  stable_path: docs/02.architecture/decisions/adr-0011-laboratory-services.md
  artifact_id: adr-0011
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0011-laboratory-services.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0015-analytics-engine-selection.md
  stable_path: docs/02.architecture/decisions/adr-0015-analytics-engine-selection.md
  artifact_id: adr-0015
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0015-analytics-engine-selection.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0016-open-webui-implementation.md
  stable_path: docs/02.architecture/decisions/adr-0016-open-webui-implementation.md
  artifact_id: adr-0016
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0016-open-webui-implementation.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0017-auth-hardening-runtime-and-fail-closed.md
  stable_path: docs/02.architecture/decisions/adr-0017-auth-hardening-runtime-and-fail-closed.md
  artifact_id: adr-0017
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0017-auth-hardening-runtime-and-fail-closed.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0018-vault-hardening-and-ha-expansion-strategy.md
  stable_path: docs/02.architecture/decisions/adr-0018-vault-hardening-and-ha-expansion-strategy.md
  artifact_id: adr-0018
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0018-vault-hardening-and-ha-expansion-strategy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md
  stable_path: docs/02.architecture/decisions/adr-0019-04-data-hardening-and-ha-expansion-strategy.md
  artifact_id: adr-0019
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0019-04-data-hardening-and-ha-expansion-strategy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0020-messaging-hardening-and-ha-expansion-strategy.md
  stable_path: docs/02.architecture/decisions/adr-0020-messaging-hardening-and-ha-expansion-strategy.md
  artifact_id: adr-0020
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0020-messaging-hardening-and-ha-expansion-strategy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0021-observability-hardening-and-ha-expansion-strategy.md
  stable_path: docs/02.architecture/decisions/adr-0021-observability-hardening-and-ha-expansion-strategy.md
  artifact_id: adr-0021
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0021-observability-hardening-and-ha-expansion-strategy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0022-workflow-hardening-and-ha-expansion-strategy.md
  stable_path: docs/02.architecture/decisions/adr-0022-workflow-hardening-and-ha-expansion-strategy.md
  artifact_id: adr-0022
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0022-workflow-hardening-and-ha-expansion-strategy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0023-ai-hardening-and-ha-expansion-strategy.md
  stable_path: docs/02.architecture/decisions/adr-0023-ai-hardening-and-ha-expansion-strategy.md
  artifact_id: adr-0023
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0023-ai-hardening-and-ha-expansion-strategy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0024-tooling-hardening-and-ha-expansion-strategy.md
  stable_path: docs/02.architecture/decisions/adr-0024-tooling-hardening-and-ha-expansion-strategy.md
  artifact_id: adr-0024
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0024-tooling-hardening-and-ha-expansion-strategy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0025-laboratory-hardening-and-ha-expansion-strategy.md
  stable_path: docs/02.architecture/decisions/adr-0025-laboratory-hardening-and-ha-expansion-strategy.md
  artifact_id: adr-0025
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0025-laboratory-hardening-and-ha-expansion-strategy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0026-standardize-infra-net.md
  stable_path: docs/02.architecture/decisions/adr-0026-standardize-infra-net.md
  artifact_id: adr-0026
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0026-standardize-infra-net.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md
  stable_path: docs/02.architecture/decisions/adr-0027-stage-00-canonical-adapter-model.md
  artifact_id: adr-0027
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0027-stage-00-canonical-adapter-model.md; migrate 19 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/0028-local-isolated-readiness-evidence.md
  stable_path: docs/02.architecture/decisions/adr-0028-local-isolated-readiness-evidence.md
  artifact_id: adr-0028
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/decisions/adr-0028-local-isolated-readiness-evidence.md; migrate 31 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/decisions/README.md
  stable_path: docs/02.architecture/decisions/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 7 resolved inbound link(s).
- legacy_path: docs/02.architecture/requirements/0001-gateway-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0001-gateway-architecture.md
  artifact_id: ad-0001
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0001-gateway-architecture.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0002-auth-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0002-auth-architecture.md
  artifact_id: ad-0002
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0002-auth-architecture.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0003-security-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0003-security-architecture.md
  artifact_id: ad-0003
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0003-security-architecture.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0004-data-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0004-data-architecture.md
  artifact_id: ad-0004
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0004-data-architecture.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0005-messaging-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0005-messaging-architecture.md
  artifact_id: ad-0005
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0005-messaging-architecture.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0006-observability-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0006-observability-architecture.md
  artifact_id: ad-0006
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0006-observability-architecture.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0007-workflow-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0007-workflow-architecture.md
  artifact_id: ad-0007
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0007-workflow-architecture.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0008-ai-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0008-ai-architecture.md
  artifact_id: ad-0008
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0008-ai-architecture.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0009-tooling-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0009-tooling-architecture.md
  artifact_id: ad-0009
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0009-tooling-architecture.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0010-communication-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0010-communication-architecture.md
  artifact_id: ad-0010
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0010-communication-architecture.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0011-laboratory-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0011-laboratory-architecture.md
  artifact_id: ad-0011
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0011-laboratory-architecture.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0012-data-analytics-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0012-data-analytics-architecture.md
  artifact_id: ad-0012
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0012-data-analytics-architecture.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0013-open-webui-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0013-open-webui-architecture.md
  artifact_id: ad-0013
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0013-open-webui-architecture.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0014-auth-optimization-hardening-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0014-auth-optimization-hardening-architecture.md
  artifact_id: ad-0014
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0014-auth-optimization-hardening-architecture.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0018-security-optimization-hardening-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0018-security-optimization-hardening-architecture.md
  artifact_id: ad-0018
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0018-security-optimization-hardening-architecture.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0019-data-optimization-hardening-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md
  artifact_id: ad-0019
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0019-data-optimization-hardening-architecture.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0020-messaging-optimization-hardening-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0020-messaging-optimization-hardening-architecture.md
  artifact_id: ad-0020
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0020-messaging-optimization-hardening-architecture.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0021-observability-optimization-hardening-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0021-observability-optimization-hardening-architecture.md
  artifact_id: ad-0021
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0021-observability-optimization-hardening-architecture.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0022-workflow-optimization-hardening-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0022-workflow-optimization-hardening-architecture.md
  artifact_id: ad-0022
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0022-workflow-optimization-hardening-architecture.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0023-ai-optimization-hardening-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0023-ai-optimization-hardening-architecture.md
  artifact_id: ad-0023
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0023-ai-optimization-hardening-architecture.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0024-tooling-optimization-hardening-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0024-tooling-optimization-hardening-architecture.md
  artifact_id: ad-0024
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0024-tooling-optimization-hardening-architecture.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0025-laboratory-optimization-hardening-architecture.md
  stable_path: docs/02.architecture/descriptions/ad-0025-laboratory-optimization-hardening-architecture.md
  artifact_id: ad-0025
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0025-laboratory-optimization-hardening-architecture.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0026-standardize-infra-net.md
  stable_path: docs/02.architecture/descriptions/ad-0026-standardize-infra-net.md
  artifact_id: ad-0026
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0026-standardize-infra-net.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0027-agent-governance-canonical-adapter.md
  stable_path: docs/02.architecture/descriptions/ad-0027-agent-governance-canonical-adapter.md
  artifact_id: ad-0027
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0027-agent-governance-canonical-adapter.md; migrate 17 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/0028-operational-readiness-closure.md
  stable_path: docs/02.architecture/descriptions/ad-0028-operational-readiness-closure.md
  artifact_id: ad-0028
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/02.architecture/descriptions/ad-0028-operational-readiness-closure.md; migrate 27 resolved inbound link(s) with it.
- legacy_path: docs/02.architecture/requirements/README.md
  stable_path: docs/02.architecture/descriptions/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move the baseline Architecture Description index to the approved descriptions root; migrate 7 resolved inbound link(s) and leave no compatibility path.
- legacy_path: docs/03.specs/001-gateway/README.md
  stable_path: null
  artifact_id: spec-0001
  action: delete
  replacement: docs/03.specs/spec-0001-gateway/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/03.specs/spec-0001-gateway/spec.md.
- legacy_path: docs/03.specs/001-gateway/spec.md
  stable_path: docs/03.specs/spec-0001-gateway/spec.md
  artifact_id: spec-0001
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0001-gateway/spec.md; migrate 12 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/002-auth/README.md
  stable_path: null
  artifact_id: spec-0002
  action: delete
  replacement: docs/03.specs/spec-0002-auth/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/03.specs/spec-0002-auth/spec.md.
- legacy_path: docs/03.specs/002-auth/spec.md
  stable_path: docs/03.specs/spec-0002-auth/spec.md
  artifact_id: spec-0002
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0002-auth/spec.md; migrate 15 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/003-security/README.md
  stable_path: null
  artifact_id: spec-0003
  action: delete
  replacement: docs/03.specs/spec-0003-security/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0003-security/spec.md.
- legacy_path: docs/03.specs/003-security/spec.md
  stable_path: docs/03.specs/spec-0003-security/spec.md
  artifact_id: spec-0003
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0003-security/spec.md; migrate 17 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/004-data/README.md
  stable_path: null
  artifact_id: spec-0004
  action: delete
  replacement: docs/03.specs/spec-0004-data/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0004-data/spec.md.
- legacy_path: docs/03.specs/004-data/spec.md
  stable_path: docs/03.specs/spec-0004-data/spec.md
  artifact_id: spec-0004
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0004-data/spec.md; migrate 22 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/005-data-analytics/README.md
  stable_path: null
  artifact_id: spec-0005
  action: delete
  replacement: docs/03.specs/spec-0005-data-analytics/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0005-data-analytics/spec.md.
- legacy_path: docs/03.specs/005-data-analytics/spec.md
  stable_path: docs/03.specs/spec-0005-data-analytics/spec.md
  artifact_id: spec-0005
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0005-data-analytics/spec.md; migrate 18 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/006-messaging/README.md
  stable_path: null
  artifact_id: spec-0006
  action: delete
  replacement: docs/03.specs/spec-0006-messaging/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0006-messaging/spec.md.
- legacy_path: docs/03.specs/006-messaging/spec.md
  stable_path: docs/03.specs/spec-0006-messaging/spec.md
  artifact_id: spec-0006
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0006-messaging/spec.md; migrate 17 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/007-observability/README.md
  stable_path: null
  artifact_id: spec-0007
  action: delete
  replacement: docs/03.specs/spec-0007-observability/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0007-observability/spec.md.
- legacy_path: docs/03.specs/007-observability/spec.md
  stable_path: docs/03.specs/spec-0007-observability/spec.md
  artifact_id: spec-0007
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0007-observability/spec.md; migrate 16 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/008-workflow/README.md
  stable_path: null
  artifact_id: spec-0008
  action: delete
  replacement: docs/03.specs/spec-0008-workflow/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0008-workflow/spec.md.
- legacy_path: docs/03.specs/008-workflow/agent-design.md
  stable_path: docs/03.specs/spec-0008-workflow/spec.md
  artifact_id: spec-0008
  action: merge
  replacement: docs/03.specs/spec-0008-workflow/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline active source into canonical target docs/03.specs/spec-0008-workflow/spec.md; migrate 11 resolved inbound link(s) before source removal.
- legacy_path: docs/03.specs/008-workflow/spec.md
  stable_path: docs/03.specs/spec-0008-workflow/spec.md
  artifact_id: spec-0008
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0008-workflow/spec.md; migrate 21 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/009-ai/README.md
  stable_path: null
  artifact_id: spec-0009
  action: delete
  replacement: docs/03.specs/spec-0009-ai/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0009-ai/spec.md.
- legacy_path: docs/03.specs/009-ai/open-webui.md
  stable_path: docs/03.specs/spec-0009-ai/spec.md
  artifact_id: spec-0009
  action: merge
  replacement: docs/03.specs/spec-0009-ai/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline active source into canonical target docs/03.specs/spec-0009-ai/spec.md; migrate 11 resolved inbound link(s) before source removal.
- legacy_path: docs/03.specs/009-ai/spec.md
  stable_path: docs/03.specs/spec-0009-ai/spec.md
  artifact_id: spec-0009
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0009-ai/spec.md; migrate 16 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/010-tooling/README.md
  stable_path: null
  artifact_id: spec-0010
  action: delete
  replacement: docs/03.specs/spec-0010-tooling/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0010-tooling/spec.md.
- legacy_path: docs/03.specs/010-tooling/spec.md
  stable_path: docs/03.specs/spec-0010-tooling/spec.md
  artifact_id: spec-0010
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0010-tooling/spec.md; migrate 17 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/011-communication/README.md
  stable_path: null
  artifact_id: spec-0011
  action: delete
  replacement: docs/03.specs/spec-0011-communication/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0011-communication/spec.md.
- legacy_path: docs/03.specs/011-communication/spec.md
  stable_path: docs/03.specs/spec-0011-communication/spec.md
  artifact_id: spec-0011
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0011-communication/spec.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/012-laboratory/README.md
  stable_path: null
  artifact_id: spec-0012
  action: delete
  replacement: docs/03.specs/spec-0012-laboratory/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0012-laboratory/spec.md.
- legacy_path: docs/03.specs/012-laboratory/spec.md
  stable_path: docs/03.specs/spec-0012-laboratory/spec.md
  artifact_id: spec-0012
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0012-laboratory/spec.md; migrate 21 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/090-workspace-audit-2026-05/README.md
  stable_path: null
  artifact_id: spec-0090
  action: delete
  replacement: docs/03.specs/spec-0090-workspace-audit-2026-05/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0090-workspace-audit-2026-05/spec.md.
- legacy_path: docs/03.specs/090-workspace-audit-2026-05/spec.md
  stable_path: docs/03.specs/spec-0090-workspace-audit-2026-05/spec.md
  artifact_id: spec-0090
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/03.specs/spec-0090-workspace-audit-2026-05/spec.md; migrate 14 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/091-workspace-doc-consistency-2026-05/spec.md
  stable_path: docs/03.specs/spec-0091-workspace-doc-consistency-2026-05/spec.md
  artifact_id: spec-0091
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/03.specs/spec-0091-workspace-doc-consistency-2026-05/spec.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/092-workspace-consistency-2026-05b/spec.md
  stable_path: docs/03.specs/spec-0092-workspace-consistency-2026-05b/spec.md
  artifact_id: spec-0092
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/03.specs/spec-0092-workspace-consistency-2026-05b/spec.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/093-docs-taxonomy-agent-first-migration/README.md
  stable_path: null
  artifact_id: spec-0093
  action: delete
  replacement: docs/03.specs/spec-0093-docs-taxonomy-agent-first-migration/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0093-docs-taxonomy-agent-first-migration/spec.md.
- legacy_path: docs/03.specs/093-docs-taxonomy-agent-first-migration/spec.md
  stable_path: docs/03.specs/spec-0093-docs-taxonomy-agent-first-migration/spec.md
  artifact_id: spec-0093
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/03.specs/spec-0093-docs-taxonomy-agent-first-migration/spec.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/094-harness-agent-first-engineering/README.md
  stable_path: null
  artifact_id: spec-0094
  action: delete
  replacement: docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md.
- legacy_path: docs/03.specs/094-harness-agent-first-engineering/spec.md
  stable_path: docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md
  artifact_id: spec-0094
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/03.specs/spec-0094-harness-agent-first-engineering/spec.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/095-infra-secrets-docs-refresh/README.md
  stable_path: null
  artifact_id: spec-0095
  action: delete
  replacement: docs/03.specs/spec-0095-infra-secrets-docs-refresh/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0095-infra-secrets-docs-refresh/spec.md.
- legacy_path: docs/03.specs/095-infra-secrets-docs-refresh/spec.md
  stable_path: docs/03.specs/spec-0095-infra-secrets-docs-refresh/spec.md
  artifact_id: spec-0095
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/03.specs/spec-0095-infra-secrets-docs-refresh/spec.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/096-llm-wiki-agent-first-completion/README.md
  stable_path: null
  artifact_id: spec-0096
  action: delete
  replacement: docs/03.specs/spec-0096-llm-wiki-agent-first-completion/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0096-llm-wiki-agent-first-completion/spec.md.
- legacy_path: docs/03.specs/096-llm-wiki-agent-first-completion/spec.md
  stable_path: docs/03.specs/spec-0096-llm-wiki-agent-first-completion/spec.md
  artifact_id: spec-0096
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/03.specs/spec-0096-llm-wiki-agent-first-completion/spec.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/097-home-docker-revalidation-deferred-follow-up/README.md
  stable_path: null
  artifact_id: spec-0097
  action: delete
  replacement: docs/03.specs/spec-0097-home-docker-revalidation-deferred-follow-up/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0097-home-docker-revalidation-deferred-follow-up/spec.md.
- legacy_path: docs/03.specs/097-home-docker-revalidation-deferred-follow-up/spec.md
  stable_path: docs/03.specs/spec-0097-home-docker-revalidation-deferred-follow-up/spec.md
  artifact_id: spec-0097
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/03.specs/spec-0097-home-docker-revalidation-deferred-follow-up/spec.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/098-standardize-infra-net/README.md
  stable_path: null
  artifact_id: spec-0098
  action: delete
  replacement: docs/03.specs/spec-0098-standardize-infra-net/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0098-standardize-infra-net/spec.md.
- legacy_path: docs/03.specs/098-standardize-infra-net/spec.md
  stable_path: docs/03.specs/spec-0098-standardize-infra-net/spec.md
  artifact_id: spec-0098
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/03.specs/spec-0098-standardize-infra-net/spec.md; migrate 15 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/102-workspace-document-contract-audit-pack/README.md
  stable_path: null
  artifact_id: spec-0102
  action: delete
  replacement: docs/03.specs/spec-0102-workspace-document-contract-audit-pack/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline active index after its typed owner is established; redirect 1 resolved inbound link(s) to docs/03.specs/spec-0102-workspace-document-contract-audit-pack/spec.md.
- legacy_path: docs/03.specs/102-workspace-document-contract-audit-pack/spec.md
  stable_path: docs/03.specs/spec-0102-workspace-document-contract-audit-pack/spec.md
  artifact_id: spec-0102
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0102-workspace-document-contract-audit-pack/spec.md; migrate 12 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/103-document-restructure-audit-contract-archive/README.md
  stable_path: null
  artifact_id: spec-0103
  action: delete
  replacement: docs/03.specs/spec-0103-document-restructure-audit-contract-archive/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline active index after its typed owner is established; redirect 3 resolved inbound link(s) to docs/03.specs/spec-0103-document-restructure-audit-contract-archive/spec.md.
- legacy_path: docs/03.specs/103-document-restructure-audit-contract-archive/spec.md
  stable_path: docs/03.specs/spec-0103-document-restructure-audit-contract-archive/spec.md
  artifact_id: spec-0103
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0103-document-restructure-audit-contract-archive/spec.md; migrate 16 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/105-agentic-engineering-implementation-audit-pack/README.md
  stable_path: null
  artifact_id: spec-0105
  action: delete
  replacement: docs/03.specs/spec-0105-agentic-engineering-implementation-audit-pack/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline completed index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/03.specs/spec-0105-agentic-engineering-implementation-audit-pack/spec.md.
- legacy_path: docs/03.specs/105-agentic-engineering-implementation-audit-pack/spec.md
  stable_path: docs/03.specs/spec-0105-agentic-engineering-implementation-audit-pack/spec.md
  artifact_id: spec-0105
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/03.specs/spec-0105-agentic-engineering-implementation-audit-pack/spec.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/134-agent-governance-canonical-convergence/spec.md
  stable_path: docs/03.specs/spec-0134-agent-governance-canonical-convergence/spec.md
  artifact_id: spec-0134
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0134-agent-governance-canonical-convergence/spec.md; migrate 13 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/135-target-surface-delta-convergence/spec.md
  stable_path: docs/03.specs/spec-0135-target-surface-delta-convergence/spec.md
  artifact_id: spec-0135
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0135-target-surface-delta-convergence/spec.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/136-sdlc-taxonomy-convergence/spec.md
  stable_path: docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md
  artifact_id: spec-0136
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/136-sdlc-taxonomy-convergence/task.md
  stable_path: docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md
  artifact_id: task-0136-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0136-sdlc-taxonomy-convergence/task.md; migrate 0 resolved inbound link(s) with it.
- legacy_path: docs/03.specs/README.md
  stable_path: docs/03.specs/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 55 resolved inbound link(s).
- legacy_path: docs/04.execution/README.md
  stable_path: docs/03.specs/README.md
  artifact_id: null
  action: merge
  replacement: docs/03.specs/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge the active Stage 04 navigation source into the canonical Stage 03 capability index; migrate 15 resolved inbound link(s) before source removal.
- legacy_path: docs/04.execution/plans/2026-03-26-01-gateway-standardization.md
  stable_path: docs/98.archive/changes/chg-0002-01-gateway-standardization/plan.md
  artifact_id: plan-0002
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0002-01-gateway-standardization/plan.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-26-02-auth-standardization.md
  stable_path: docs/98.archive/changes/chg-0003-02-auth-standardization/plan.md
  artifact_id: plan-0003
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0003-02-auth-standardization/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-26-03-security-standardization.md
  stable_path: docs/98.archive/changes/chg-0004-03-security-standardization/plan.md
  artifact_id: plan-0004
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0004-03-security-standardization/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-26-04-data-standardization.md
  stable_path: docs/98.archive/changes/chg-0005-04-data-standardization/plan.md
  artifact_id: plan-0005
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0005-04-data-standardization/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-26-05-messaging-standardization.md
  stable_path: docs/98.archive/changes/chg-0006-05-messaging-standardization/plan.md
  artifact_id: plan-0006
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0006-05-messaging-standardization/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-26-06-observability-standardization.md
  stable_path: docs/98.archive/changes/chg-0007-06-observability-standardization/plan.md
  artifact_id: plan-0007
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0007-06-observability-standardization/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-26-07-workflow-standardization.md
  stable_path: docs/98.archive/changes/chg-0008-07-workflow-standardization/plan.md
  artifact_id: plan-0008
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0008-07-workflow-standardization/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-26-08-ai-standardization.md
  stable_path: docs/98.archive/changes/chg-0009-08-ai-standardization/plan.md
  artifact_id: plan-0009
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0009-08-ai-standardization/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-26-09-tooling-standardization.md
  stable_path: docs/98.archive/changes/chg-0010-09-tooling-standardization/plan.md
  artifact_id: plan-0010
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0010-09-tooling-standardization/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-26-10-communication-standardization.md
  stable_path: docs/98.archive/changes/chg-0011-10-communication-standardization/plan.md
  artifact_id: plan-0011
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0011-10-communication-standardization/plan.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-26-11-laboratory-standardization.md
  stable_path: docs/98.archive/changes/chg-0012-11-laboratory-standardization/plan.md
  artifact_id: plan-0012
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0012-11-laboratory-standardization/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-27-08-ai-open-webui-plan.md
  stable_path: docs/98.archive/changes/chg-0013-08-ai-open-webui/plan.md
  artifact_id: plan-0013
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0013-08-ai-open-webui/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-27-infra-service-optimization-priority-plan.md
  stable_path: docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  artifact_id: policy-0006
  action: merge
  replacement: docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge the active untyped umbrella roadmap into its linked current Operations policy; it has no owning Spec parent and must not be archived.
- legacy_path: docs/04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md
  stable_path: docs/98.archive/changes/chg-0015-01-gateway-optimization-hardening/plan.md
  artifact_id: plan-0015
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0015-01-gateway-optimization-hardening/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-28-02-auth-optimization-hardening-plan.md
  stable_path: docs/98.archive/changes/chg-0016-02-auth-optimization-hardening/plan.md
  artifact_id: plan-0016
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0016-02-auth-optimization-hardening/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md
  stable_path: docs/98.archive/changes/chg-0017-03-security-optimization-hardening/plan.md
  artifact_id: plan-0017
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0017-03-security-optimization-hardening/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md
  stable_path: docs/98.archive/changes/chg-0018-04-data-optimization-hardening/plan.md
  artifact_id: plan-0018
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0018-04-data-optimization-hardening/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-28-05-messaging-optimization-hardening-plan.md
  stable_path: docs/98.archive/changes/chg-0019-05-messaging-optimization-hardening/plan.md
  artifact_id: plan-0019
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0019-05-messaging-optimization-hardening/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-28-06-observability-optimization-hardening-plan.md
  stable_path: docs/98.archive/changes/chg-0020-06-observability-optimization-hardening/plan.md
  artifact_id: plan-0020
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0020-06-observability-optimization-hardening/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-28-07-workflow-optimization-hardening-plan.md
  stable_path: docs/98.archive/changes/chg-0021-07-workflow-optimization-hardening/plan.md
  artifact_id: plan-0021
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0021-07-workflow-optimization-hardening/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-28-08-ai-optimization-hardening-plan.md
  stable_path: docs/98.archive/changes/chg-0022-08-ai-optimization-hardening/plan.md
  artifact_id: plan-0022
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0022-08-ai-optimization-hardening/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-28-09-tooling-optimization-hardening-plan.md
  stable_path: docs/98.archive/changes/chg-0023-09-tooling-optimization-hardening/plan.md
  artifact_id: plan-0023
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0023-09-tooling-optimization-hardening/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-03-28-11-laboratory-optimization-hardening-plan.md
  stable_path: docs/98.archive/changes/chg-0024-11-laboratory-optimization-hardening/plan.md
  artifact_id: plan-0024
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0024-11-laboratory-optimization-hardening/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-04-01-standardize-infra-net.md
  stable_path: docs/98.archive/changes/chg-0025-standardize-infra-net/plan.md
  artifact_id: plan-0025
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0025-standardize-infra-net/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-04-10-infra-team-agent-cross-validation.md
  stable_path: docs/98.archive/changes/chg-0026-infra-team-agent-cross-validation/plan.md
  artifact_id: plan-0026
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0026-infra-team-agent-cross-validation/plan.md; migrate 12 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-09-harness-agent-first-engineering.md
  stable_path: docs/98.archive/changes/chg-0027-harness-agent-first-engineering/plan.md
  artifact_id: plan-0027
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0027-harness-agent-first-engineering/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-09-infra-secrets-docs-refresh.md
  stable_path: docs/98.archive/changes/chg-0028-infra-secrets-docs-refresh/plan.md
  artifact_id: plan-0028
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0028-infra-secrets-docs-refresh/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-09-scripts-lifecycle-contract-cleanup.md
  stable_path: docs/98.archive/changes/chg-0029-scripts-lifecycle-contract-cleanup/plan.md
  artifact_id: plan-0029
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0029-scripts-lifecycle-contract-cleanup/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-10-docs-taxonomy-agent-first-migration.md
  stable_path: docs/98.archive/changes/chg-0030-docs-taxonomy-agent-first-migration/plan.md
  artifact_id: plan-0030
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0030-docs-taxonomy-agent-first-migration/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-10-llm-wiki-agent-first-completion.md
  stable_path: docs/98.archive/changes/chg-0031-llm-wiki-agent-first-completion/plan.md
  artifact_id: plan-0031
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0031-llm-wiki-agent-first-completion/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-17-requirements-standardization.md
  stable_path: docs/98.archive/changes/chg-0032-requirements-standardization/plan.md
  artifact_id: plan-0032
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0032-requirements-standardization/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-17-scripts-ci-qa-cleanup.md
  stable_path: docs/98.archive/changes/chg-0033-scripts-ci-qa-cleanup/plan.md
  artifact_id: plan-0033
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0033-scripts-ci-qa-cleanup/plan.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-18-docs-05-operations-purpose-remediation.md
  stable_path: docs/98.archive/changes/chg-0034-docs-05-operations-purpose-remediation/plan.md
  artifact_id: plan-0034
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0034-docs-05-operations-purpose-remediation/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-18-docs-bounded-consistency-audit.md
  stable_path: docs/98.archive/changes/chg-0035-docs-bounded-consistency-audit/plan.md
  artifact_id: plan-0035
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0035-docs-bounded-consistency-audit/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-18-execution-stage-remediation.md
  stable_path: docs/98.archive/changes/chg-0036-execution-stage-remediation/plan.md
  artifact_id: plan-0036
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0036-execution-stage-remediation/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-18-targeted-docs-precision-remediation.md
  stable_path: docs/98.archive/changes/chg-0037-targeted-docs-precision-remediation/plan.md
  artifact_id: plan-0037
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0037-targeted-docs-precision-remediation/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-22-agent-hook-completion-style-automation.md
  stable_path: docs/98.archive/changes/chg-0038-agent-hook-completion-style-automation/plan.md
  artifact_id: plan-0038
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0038-agent-hook-completion-style-automation/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-22-data-analytics-execution-traceability.md
  stable_path: docs/98.archive/changes/chg-0039-data-analytics-execution-traceability/plan.md
  artifact_id: plan-0039
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0039-data-analytics-execution-traceability/plan.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-22-lifecycle-readme-debt-closure.md
  stable_path: docs/98.archive/changes/chg-0040-lifecycle-readme-debt-closure/plan.md
  artifact_id: plan-0040
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0040-lifecycle-readme-debt-closure/plan.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-22-spec-execution-implementation-audit.md
  stable_path: docs/98.archive/changes/chg-0041-spec-execution-implementation-audit/plan.md
  artifact_id: plan-0041
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0041-spec-execution-implementation-audit/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-22-workspace-docs-agent-governance-remediation.md
  stable_path: docs/98.archive/changes/chg-0042-workspace-docs-agent-governance-remediation/plan.md
  artifact_id: plan-0042
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0042-workspace-docs-agent-governance-remediation/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-22-workspace-governance-bounded-reaudit.md
  stable_path: docs/98.archive/changes/chg-0043-workspace-governance-bounded-reaudit/plan.md
  artifact_id: plan-0043
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0043-workspace-governance-bounded-reaudit/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-24-workspace-audit-grill-review.md
  stable_path: docs/98.archive/changes/chg-0044-workspace-audit-grill-review/plan.md
  artifact_id: plan-0044
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0044-workspace-audit-grill-review/plan.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-24-workspace-audit-improvement.md
  stable_path: docs/98.archive/changes/chg-0045-workspace-audit-improvement/plan.md
  artifact_id: plan-0045
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0045-workspace-audit-improvement/plan.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-24-workspace-audit-input-task-gap-closure.md
  stable_path: docs/98.archive/changes/chg-0046-workspace-audit-input-task-gap-closure/plan.md
  artifact_id: plan-0046
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0046-workspace-audit-input-task-gap-closure/plan.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-25-home-docker-revalidation-deferred-follow-up.md
  stable_path: docs/98.archive/changes/chg-0047-home-docker-revalidation-deferred-follow-up/plan.md
  artifact_id: plan-0047
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0047-home-docker-revalidation-deferred-follow-up/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-25-home-docker-workspace-audit-improvement.md
  stable_path: docs/98.archive/changes/chg-0048-home-docker-workspace-audit-improvement/plan.md
  artifact_id: plan-0048
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0048-home-docker-workspace-audit-improvement/plan.md; migrate 13 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-25-large-scale-authored-ssot-review.md
  stable_path: docs/98.archive/changes/chg-0049-large-scale-authored-ssot-review/plan.md
  artifact_id: plan-0049
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0049-large-scale-authored-ssot-review/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-26-workspace-audit-gap-closure.md
  stable_path: docs/98.archive/changes/chg-0050-workspace-audit-gap-closure/plan.md
  artifact_id: plan-0050
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0050-workspace-audit-gap-closure/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-26-workspace-audit.md
  stable_path: docs/98.archive/changes/chg-0051-workspace-audit/plan.md
  artifact_id: plan-0051
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0051-workspace-audit/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-28-workspace-doc-consistency.md
  stable_path: docs/98.archive/changes/chg-0052-workspace-doc-consistency/plan.md
  artifact_id: plan-0052
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0052-workspace-doc-consistency/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-29-workspace-consistency-2026-05b.md
  stable_path: docs/98.archive/changes/chg-0053-workspace-consistency-2026-05b/plan.md
  artifact_id: plan-0053
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0053-workspace-consistency-2026-05b/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-05-31-claude-harness-governance-verification.md
  stable_path: docs/98.archive/changes/chg-0054-claude-harness-governance-verification/plan.md
  artifact_id: plan-0054
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0054-claude-harness-governance-verification/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md
  stable_path: docs/98.archive/changes/chg-0055-agent-governance-decision-items/plan.md
  artifact_id: plan-0055
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0055-agent-governance-decision-items/plan.md; migrate 21 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-06-02-agent-governance-phase-1-revalidation.md
  stable_path: docs/98.archive/changes/chg-0056-agent-governance-phase-1-revalidation/plan.md
  artifact_id: plan-0056
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0056-agent-governance-phase-1-revalidation/plan.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-06-02-agent-governance-phase-2-strategy-integration.md
  stable_path: docs/98.archive/changes/chg-0057-agent-governance-phase-2-strategy-integration/plan.md
  artifact_id: plan-0057
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0057-agent-governance-phase-2-strategy-integration/plan.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-06-02-agent-governance-phase-3-approved-surface-activation.md
  stable_path: docs/98.archive/changes/chg-0058-agent-governance-phase-3-approved-surface-activation/plan.md
  artifact_id: plan-0058
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0058-agent-governance-phase-3-approved-surface-activation/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-06-02-agent-governance-phase-4-closure-reconciliation.md
  stable_path: docs/98.archive/changes/chg-0059-agent-governance-phase-4-closure-reconciliation/plan.md
  artifact_id: plan-0059
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0059-agent-governance-phase-4-closure-reconciliation/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-06-02-docs-implementation-reconciliation.md
  stable_path: docs/98.archive/changes/chg-0060-docs-implementation-reconciliation/plan.md
  artifact_id: plan-0060
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0060-docs-implementation-reconciliation/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-06-02-governance-optimization.md
  stable_path: docs/98.archive/changes/chg-0061-governance-optimization/plan.md
  artifact_id: plan-0061
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0061-governance-optimization/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-06-03-governance-surgical-reverification.md
  stable_path: docs/98.archive/changes/chg-0062-governance-surgical-reverification/plan.md
  artifact_id: plan-0062
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0062-governance-surgical-reverification/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-02-template-system-reorganization.md
  stable_path: docs/98.archive/changes/chg-0063-template-system-reorganization/plan.md
  artifact_id: plan-0063
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0063-template-system-reorganization/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-03-document-contract-remediation-batches.md
  stable_path: docs/98.archive/changes/chg-0064-document-contract-remediation-batches/plan.md
  artifact_id: plan-0064
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0064-document-contract-remediation-batches/plan.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-03-template-system-contract-standardization.md
  stable_path: docs/98.archive/changes/chg-0065-template-system-contract-standardization/plan.md
  artifact_id: plan-0065
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0065-template-system-contract-standardization/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-03-workspace-document-contract-audit-pack.md
  stable_path: docs/98.archive/changes/chg-0066-workspace-document-contract-audit-pack/plan.md
  artifact_id: plan-0066
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0066-workspace-document-contract-audit-pack/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-04-document-restructure-audit-contract-archive.md
  stable_path: docs/98.archive/changes/chg-0067-document-restructure-audit-contract-archive/plan.md
  artifact_id: plan-0067
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0067-document-restructure-audit-contract-archive/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-05-agent-output-eval-fixtures.md
  stable_path: docs/98.archive/changes/chg-0068-agent-output-eval-fixtures/plan.md
  artifact_id: plan-0068
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0068-agent-output-eval-fixtures/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-05-agentic-engineering-implementation-audit-pack.md
  stable_path: docs/98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/plan.md
  artifact_id: plan-0069
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/plan.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-05-agentic-research-pack-refresh.md
  stable_path: docs/98.archive/changes/chg-0070-agentic-research-pack-refresh/plan.md
  artifact_id: plan-0070
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0070-agentic-research-pack-refresh/plan.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-05-audit-pack-coverage-report.md
  stable_path: docs/98.archive/changes/chg-0071-audit-pack-coverage-report/plan.md
  artifact_id: plan-0071
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0071-audit-pack-coverage-report/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-05-compose-profile-service-coverage-snapshot.md
  stable_path: docs/98.archive/changes/chg-0072-compose-profile-service-coverage-snapshot/plan.md
  artifact_id: plan-0072
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0072-compose-profile-service-coverage-snapshot/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-05-gap-routing-recommendation.md
  stable_path: docs/98.archive/changes/chg-0073-gap-routing-recommendation/plan.md
  artifact_id: plan-0073
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0073-gap-routing-recommendation/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-05-provider-semantic-parity-validator.md
  stable_path: docs/98.archive/changes/chg-0074-provider-semantic-parity-validator/plan.md
  artifact_id: plan-0074
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0074-provider-semantic-parity-validator/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-05-provider-workspace-artifact-path-parity.md
  stable_path: docs/98.archive/changes/chg-0075-provider-workspace-artifact-path-parity/plan.md
  artifact_id: plan-0075
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0075-provider-workspace-artifact-path-parity/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-05-qa-gate-recommendation-ci-summary.md
  stable_path: docs/98.archive/changes/chg-0076-qa-gate-recommendation-ci-summary/plan.md
  artifact_id: plan-0076
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0076-qa-gate-recommendation-ci-summary/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-05-template-system-numbered-sdlc-paths.md
  stable_path: docs/98.archive/changes/chg-0077-template-system-numbered-sdlc-paths/plan.md
  artifact_id: plan-0077
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0077-template-system-numbered-sdlc-paths/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-05-workspace-support-surface-contract.md
  stable_path: docs/98.archive/changes/chg-0078-workspace-support-surface-contract/plan.md
  artifact_id: plan-0078
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0078-workspace-support-surface-contract/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-06-agent-output-eval-ci-gate.md
  stable_path: docs/98.archive/changes/chg-0079-agent-output-eval-ci-gate/plan.md
  artifact_id: plan-0079
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0079-agent-output-eval-ci-gate/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-06-agent-output-eval-runner.md
  stable_path: docs/98.archive/changes/chg-0080-agent-output-eval-runner/plan.md
  artifact_id: plan-0080
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0080-agent-output-eval-runner/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-06-audit-implementation-matrix-snapshot.md
  stable_path: docs/98.archive/changes/chg-0081-audit-implementation-matrix-snapshot/plan.md
  artifact_id: plan-0081
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0081-audit-implementation-matrix-snapshot/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-06-dependency-vulnerability-audit-gate.md
  stable_path: docs/98.archive/changes/chg-0082-dependency-vulnerability-audit-gate/plan.md
  artifact_id: plan-0082
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0082-dependency-vulnerability-audit-gate/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-06-llm-wiki-stage-category-coverage.md
  stable_path: docs/98.archive/changes/chg-0083-llm-wiki-stage-category-coverage/plan.md
  artifact_id: plan-0083
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0083-llm-wiki-stage-category-coverage/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-06-provider-hook-parity-matrix.md
  stable_path: docs/98.archive/changes/chg-0084-provider-hook-parity-matrix/plan.md
  artifact_id: plan-0084
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0084-provider-hook-parity-matrix/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-06-sdlc-document-contract-corpus-normalization.md
  stable_path: docs/98.archive/changes/chg-0085-sdlc-document-contract-corpus-normalization/plan.md
  artifact_id: plan-0085
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0085-sdlc-document-contract-corpus-normalization/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-06-security-automation-readiness-snapshot.md
  stable_path: docs/98.archive/changes/chg-0086-security-automation-readiness-snapshot/plan.md
  artifact_id: plan-0086
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0086-security-automation-readiness-snapshot/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-06-tech-stack-version-provenance.md
  stable_path: docs/98.archive/changes/chg-0087-tech-stack-version-provenance/plan.md
  artifact_id: plan-0087
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0087-tech-stack-version-provenance/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-10-agentic-research-pack-consolidation.md
  stable_path: docs/98.archive/changes/chg-0088-agentic-research-pack-consolidation/plan.md
  artifact_id: plan-0088
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0088-agentic-research-pack-consolidation/plan.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-11-agentic-engineering-audit-remediation.md
  stable_path: docs/98.archive/changes/chg-0089-agentic-engineering-audit-remediation/plan.md
  artifact_id: plan-0089
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0089-agentic-engineering-audit-remediation/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-11-compose-runtime-readiness-remediation.md
  stable_path: docs/98.archive/changes/chg-0090-compose-runtime-readiness-remediation/plan.md
  artifact_id: plan-0090
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0090-compose-runtime-readiness-remediation/plan.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-11-deployment-release-engineering-remediation.md
  stable_path: docs/98.archive/changes/chg-0091-deployment-release-engineering-remediation/plan.md
  artifact_id: plan-0091
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0091-deployment-release-engineering-remediation/plan.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-11-infrastructure-operations-readiness-remediation.md
  stable_path: docs/98.archive/changes/chg-0092-infrastructure-operations-readiness-remediation/plan.md
  artifact_id: plan-0092
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0092-infrastructure-operations-readiness-remediation/plan.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-11-security-supply-chain-remediation.md
  stable_path: docs/98.archive/changes/chg-0093-security-supply-chain-remediation/plan.md
  artifact_id: plan-0093
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0093-security-supply-chain-remediation/plan.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-12-agentic-audit-harness-consolidation.md
  stable_path: docs/98.archive/changes/chg-0094-agentic-audit-harness-consolidation/plan.md
  artifact_id: plan-0094
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0094-agentic-audit-harness-consolidation/plan.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-13-document-contract-canonicalization.md
  stable_path: docs/98.archive/changes/chg-0095-document-contract-canonicalization/plan.md
  artifact_id: plan-0095
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0095-document-contract-canonicalization/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-13-template-contract-system-canonicalization.md
  stable_path: docs/98.archive/changes/chg-0096-template-contract-system-canonicalization/plan.md
  artifact_id: plan-0096
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0096-template-contract-system-canonicalization/plan.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md
  stable_path: docs/98.archive/changes/chg-0097-document-corpus-lifecycle-migration-foundation/plan.md
  artifact_id: plan-0097
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0097-document-corpus-lifecycle-migration-foundation/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-15-agent-governance-harness-convergence.md
  stable_path: docs/98.archive/changes/chg-0098-agent-governance-harness-convergence/plan.md
  artifact_id: plan-0098
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0098-agent-governance-harness-convergence/plan.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-18-target-surface-contract-convergence.md
  stable_path: docs/98.archive/changes/chg-0099-target-surface-contract-convergence/plan.md
  artifact_id: plan-0099
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0099-target-surface-contract-convergence/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-19-operational-readiness-closure-program.md
  stable_path: docs/98.archive/changes/chg-0100-operational-readiness-closure-program/plan.md
  artifact_id: plan-0100
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0100-operational-readiness-closure-program/plan.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-26-agent-governance-canonical-convergence.md
  stable_path: docs/03.specs/spec-0134-agent-governance-canonical-convergence/plan.md
  artifact_id: plan-0134
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0134-agent-governance-canonical-convergence/plan.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-07-28-target-surface-delta-convergence.md
  stable_path: docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md
  artifact_id: plan-0135
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0135-target-surface-delta-convergence/plan.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/2026-08-07-sdlc-taxonomy-convergence.md
  stable_path: docs/03.specs/spec-0136-sdlc-taxonomy-convergence/plan.md
  artifact_id: plan-0136
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0136-sdlc-taxonomy-convergence/plan.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/plans/README.md
  stable_path: docs/03.specs/README.md
  artifact_id: null
  action: merge
  replacement: docs/03.specs/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge the active Stage 04 Plan navigation source into the canonical Stage 03 capability index; migrate 44 resolved inbound link(s) before source removal.
- legacy_path: docs/04.execution/tasks/2026-03-26-01-gateway-tasks.md
  stable_path: docs/98.archive/changes/chg-0104-01-gateway/task.md
  artifact_id: task-0104-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0104-01-gateway/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-26-02-auth-tasks.md
  stable_path: docs/98.archive/changes/chg-0105-02-auth/task.md
  artifact_id: task-0105-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0105-02-auth/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-26-03-security-tasks.md
  stable_path: docs/98.archive/changes/chg-0106-03-security/task.md
  artifact_id: task-0106-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0106-03-security/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-26-04-data-tasks.md
  stable_path: docs/98.archive/changes/chg-0107-04-data/task.md
  artifact_id: task-0107-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0107-04-data/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-26-05-messaging-tasks.md
  stable_path: docs/98.archive/changes/chg-0108-05-messaging/task.md
  artifact_id: task-0108-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0108-05-messaging/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-26-06-observability-tasks.md
  stable_path: docs/98.archive/changes/chg-0109-06-observability/task.md
  artifact_id: task-0109-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0109-06-observability/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-26-07-workflow-tasks.md
  stable_path: docs/98.archive/changes/chg-0110-07-workflow/task.md
  artifact_id: task-0110-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0110-07-workflow/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-26-08-ai-tasks.md
  stable_path: docs/98.archive/changes/chg-0111-08-ai/task.md
  artifact_id: task-0111-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0111-08-ai/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-26-09-tooling-tasks.md
  stable_path: docs/98.archive/changes/chg-0112-09-tooling/task.md
  artifact_id: task-0112-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0112-09-tooling/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-26-10-communication-tasks.md
  stable_path: docs/98.archive/changes/chg-0113-10-communication/task.md
  artifact_id: task-0113-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0113-10-communication/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-26-11-laboratory-tasks.md
  stable_path: docs/98.archive/changes/chg-0114-11-laboratory/task.md
  artifact_id: task-0114-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0114-11-laboratory/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-27-08-ai-open-webui-tasks.md
  stable_path: docs/98.archive/changes/chg-0013-08-ai-open-webui/task.md
  artifact_id: task-0013-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0013-08-ai-open-webui/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md
  stable_path: docs/98.archive/changes/chg-0015-01-gateway-optimization-hardening/task.md
  artifact_id: task-0015-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0015-01-gateway-optimization-hardening/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-28-02-auth-optimization-hardening-tasks.md
  stable_path: docs/98.archive/changes/chg-0016-02-auth-optimization-hardening/task.md
  artifact_id: task-0016-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0016-02-auth-optimization-hardening/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md
  stable_path: docs/98.archive/changes/chg-0017-03-security-optimization-hardening/task.md
  artifact_id: task-0017-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0017-03-security-optimization-hardening/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md
  stable_path: docs/98.archive/changes/chg-0018-04-data-optimization-hardening/task.md
  artifact_id: task-0018-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0018-04-data-optimization-hardening/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-28-05-messaging-optimization-hardening-tasks.md
  stable_path: docs/98.archive/changes/chg-0019-05-messaging-optimization-hardening/task.md
  artifact_id: task-0019-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0019-05-messaging-optimization-hardening/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-28-06-observability-optimization-hardening-tasks.md
  stable_path: docs/98.archive/changes/chg-0020-06-observability-optimization-hardening/task.md
  artifact_id: task-0020-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0020-06-observability-optimization-hardening/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md
  stable_path: docs/98.archive/changes/chg-0021-07-workflow-optimization-hardening/task.md
  artifact_id: task-0021-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0021-07-workflow-optimization-hardening/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-28-08-ai-optimization-hardening-tasks.md
  stable_path: docs/98.archive/changes/chg-0022-08-ai-optimization-hardening/task.md
  artifact_id: task-0022-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0022-08-ai-optimization-hardening/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md
  stable_path: docs/98.archive/changes/chg-0023-09-tooling-optimization-hardening/task.md
  artifact_id: task-0023-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0023-09-tooling-optimization-hardening/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md
  stable_path: docs/98.archive/changes/chg-0024-11-laboratory-optimization-hardening/task.md
  artifact_id: task-0024-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0024-11-laboratory-optimization-hardening/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-04-01-standardize-infra-net.md
  stable_path: docs/98.archive/changes/chg-0025-standardize-infra-net/task.md
  artifact_id: task-0025-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0025-standardize-infra-net/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-04-10-infra-team-agent-cross-validation.md
  stable_path: docs/98.archive/changes/chg-0026-infra-team-agent-cross-validation/task.md
  artifact_id: task-0026-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0026-infra-team-agent-cross-validation/task.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-09-harness-agent-first-engineering.md
  stable_path: docs/98.archive/changes/chg-0027-harness-agent-first-engineering/task.md
  artifact_id: task-0027-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0027-harness-agent-first-engineering/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md
  stable_path: docs/98.archive/changes/chg-0028-infra-secrets-docs-refresh/task.md
  artifact_id: task-0028-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0028-infra-secrets-docs-refresh/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-09-scripts-lifecycle-contract-cleanup.md
  stable_path: docs/98.archive/changes/chg-0029-scripts-lifecycle-contract-cleanup/task.md
  artifact_id: task-0029-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0029-scripts-lifecycle-contract-cleanup/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-10-docs-taxonomy-agent-first-migration.md
  stable_path: docs/98.archive/changes/chg-0030-docs-taxonomy-agent-first-migration/task.md
  artifact_id: task-0030-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0030-docs-taxonomy-agent-first-migration/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-10-llm-wiki-agent-first-completion.md
  stable_path: docs/98.archive/changes/chg-0031-llm-wiki-agent-first-completion/task.md
  artifact_id: task-0031-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0031-llm-wiki-agent-first-completion/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-17-requirements-standardization.md
  stable_path: docs/98.archive/changes/chg-0032-requirements-standardization/task.md
  artifact_id: task-0032-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0032-requirements-standardization/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-17-scripts-ci-qa-cleanup.md
  stable_path: docs/98.archive/changes/chg-0033-scripts-ci-qa-cleanup/task.md
  artifact_id: task-0033-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0033-scripts-ci-qa-cleanup/task.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-18-docs-05-operations-purpose-remediation.md
  stable_path: docs/98.archive/changes/chg-0034-docs-05-operations-purpose-remediation/task.md
  artifact_id: task-0034-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0034-docs-05-operations-purpose-remediation/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-18-docs-bounded-consistency-audit.md
  stable_path: docs/98.archive/changes/chg-0035-docs-bounded-consistency-audit/task.md
  artifact_id: task-0035-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0035-docs-bounded-consistency-audit/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-18-execution-stage-remediation.md
  stable_path: docs/98.archive/changes/chg-0036-execution-stage-remediation/task.md
  artifact_id: task-0036-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0036-execution-stage-remediation/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-18-targeted-docs-precision-remediation.md
  stable_path: docs/98.archive/changes/chg-0037-targeted-docs-precision-remediation/task.md
  artifact_id: task-0037-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0037-targeted-docs-precision-remediation/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-22-agent-hook-completion-style-automation.md
  stable_path: docs/98.archive/changes/chg-0038-agent-hook-completion-style-automation/task.md
  artifact_id: task-0038-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0038-agent-hook-completion-style-automation/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-22-data-analytics-execution-traceability.md
  stable_path: docs/98.archive/changes/chg-0039-data-analytics-execution-traceability/task.md
  artifact_id: task-0039-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0039-data-analytics-execution-traceability/task.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-22-lifecycle-readme-debt-closure.md
  stable_path: docs/98.archive/changes/chg-0040-lifecycle-readme-debt-closure/task.md
  artifact_id: task-0040-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0040-lifecycle-readme-debt-closure/task.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-22-spec-execution-implementation-audit.md
  stable_path: docs/98.archive/changes/chg-0041-spec-execution-implementation-audit/task.md
  artifact_id: task-0041-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0041-spec-execution-implementation-audit/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-22-workspace-docs-agent-governance-remediation.md
  stable_path: docs/98.archive/changes/chg-0042-workspace-docs-agent-governance-remediation/task.md
  artifact_id: task-0042-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0042-workspace-docs-agent-governance-remediation/task.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-22-workspace-governance-bounded-reaudit.md
  stable_path: docs/98.archive/changes/chg-0043-workspace-governance-bounded-reaudit/task.md
  artifact_id: task-0043-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0043-workspace-governance-bounded-reaudit/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-24-workspace-audit-grill-review.md
  stable_path: docs/98.archive/changes/chg-0044-workspace-audit-grill-review/task.md
  artifact_id: task-0044-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0044-workspace-audit-grill-review/task.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-24-workspace-audit-improvement.md
  stable_path: docs/98.archive/changes/chg-0045-workspace-audit-improvement/task.md
  artifact_id: task-0045-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0045-workspace-audit-improvement/task.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-24-workspace-audit-input-task-gap-closure.md
  stable_path: docs/98.archive/changes/chg-0046-workspace-audit-input-task-gap-closure/task.md
  artifact_id: task-0046-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0046-workspace-audit-input-task-gap-closure/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-25-home-docker-revalidation-deferred-follow-up.md
  stable_path: docs/98.archive/changes/chg-0047-home-docker-revalidation-deferred-follow-up/task.md
  artifact_id: task-0047-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0047-home-docker-revalidation-deferred-follow-up/task.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-25-home-docker-workspace-audit-improvement.md
  stable_path: docs/98.archive/changes/chg-0048-home-docker-workspace-audit-improvement/task.md
  artifact_id: task-0048-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0048-home-docker-workspace-audit-improvement/task.md; migrate 12 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-25-large-scale-authored-ssot-review.md
  stable_path: docs/98.archive/changes/chg-0049-large-scale-authored-ssot-review/task.md
  artifact_id: task-0049-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0049-large-scale-authored-ssot-review/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-26-workspace-audit-gap-closure.md
  stable_path: docs/98.archive/changes/chg-0050-workspace-audit-gap-closure/task.md
  artifact_id: task-0050-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0050-workspace-audit-gap-closure/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-26-workspace-audit.md
  stable_path: docs/98.archive/changes/chg-0051-workspace-audit/task.md
  artifact_id: task-0051-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0051-workspace-audit/task.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-28-workspace-doc-consistency.md
  stable_path: docs/98.archive/changes/chg-0052-workspace-doc-consistency/task.md
  artifact_id: task-0052-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0052-workspace-doc-consistency/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-29-workspace-consistency-2026-05b.md
  stable_path: docs/98.archive/changes/chg-0053-workspace-consistency-2026-05b/task.md
  artifact_id: task-0053-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0053-workspace-consistency-2026-05b/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-05-31-claude-harness-governance-verification.md
  stable_path: docs/98.archive/changes/chg-0054-claude-harness-governance-verification/task.md
  artifact_id: task-0054-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0054-claude-harness-governance-verification/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md
  stable_path: docs/98.archive/changes/chg-0115-agent-governance-missing-items-implementation/task.md
  artifact_id: task-0115-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0115-agent-governance-missing-items-implementation/task.md; migrate 28 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-02-agent-governance-phase-1-revalidation.md
  stable_path: docs/98.archive/changes/chg-0056-agent-governance-phase-1-revalidation/task.md
  artifact_id: task-0056-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0056-agent-governance-phase-1-revalidation/task.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-02-agent-governance-phase-2-strategy-integration.md
  stable_path: docs/98.archive/changes/chg-0057-agent-governance-phase-2-strategy-integration/task.md
  artifact_id: task-0057-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0057-agent-governance-phase-2-strategy-integration/task.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-02-agent-governance-phase-3-approved-surface-activation.md
  stable_path: docs/98.archive/changes/chg-0058-agent-governance-phase-3-approved-surface-activation/task.md
  artifact_id: task-0058-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0058-agent-governance-phase-3-approved-surface-activation/task.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-02-agent-governance-phase-4-closure-reconciliation.md
  stable_path: docs/98.archive/changes/chg-0059-agent-governance-phase-4-closure-reconciliation/task.md
  artifact_id: task-0059-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0059-agent-governance-phase-4-closure-reconciliation/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-02-docs-implementation-reconciliation.md
  stable_path: docs/98.archive/changes/chg-0060-docs-implementation-reconciliation/task.md
  artifact_id: task-0060-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0060-docs-implementation-reconciliation/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-02-governance-optimization.md
  stable_path: docs/98.archive/changes/chg-0061-governance-optimization/task.md
  artifact_id: task-0061-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0061-governance-optimization/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-03-governance-surgical-reverification.md
  stable_path: docs/98.archive/changes/chg-0062-governance-surgical-reverification/task.md
  artifact_id: task-0062-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0062-governance-surgical-reverification/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-04-docs-implementation-audit.md
  stable_path: docs/98.archive/changes/chg-0116-docs-implementation-audit/task.md
  artifact_id: task-0116-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0116-docs-implementation-audit/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-harness-engineering.md
  stable_path: docs/98.archive/changes/chg-0117-harness-engineering/task.md
  artifact_id: task-0117-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0117-harness-engineering/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-boundary-audit.md
  stable_path: docs/98.archive/changes/chg-0118-language-policy-boundary-audit/task.md
  artifact_id: task-0118-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0118-language-policy-boundary-audit/task.md; migrate 24 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-hard-enforcement.md
  stable_path: docs/98.archive/changes/chg-0119-language-policy-hard-enforcement/task.md
  artifact_id: task-0119-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0119-language-policy-hard-enforcement/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-1.md
  stable_path: docs/98.archive/changes/chg-0120-language-policy-normalization-batch-1/task.md
  artifact_id: task-0120-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0120-language-policy-normalization-batch-1/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-2.md
  stable_path: docs/98.archive/changes/chg-0121-language-policy-normalization-batch-2/task.md
  artifact_id: task-0121-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0121-language-policy-normalization-batch-2/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-normalization-batch-3.md
  stable_path: docs/98.archive/changes/chg-0122-language-policy-normalization-batch-3/task.md
  artifact_id: task-0122-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0122-language-policy-normalization-batch-3/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-1.md
  stable_path: docs/98.archive/changes/chg-0123-language-policy-plan-normalization-batch-1/task.md
  artifact_id: task-0123-02
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0123-language-policy-plan-normalization-batch-1/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-2.md
  stable_path: docs/98.archive/changes/chg-0124-language-policy-plan-normalization-batch-2/task.md
  artifact_id: task-0124-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0124-language-policy-plan-normalization-batch-2/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-3.md
  stable_path: docs/98.archive/changes/chg-0125-language-policy-plan-normalization-batch-3/task.md
  artifact_id: task-0125-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0125-language-policy-plan-normalization-batch-3/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-4.md
  stable_path: docs/98.archive/changes/chg-0126-language-policy-plan-normalization-batch-4/task.md
  artifact_id: task-0126-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0126-language-policy-plan-normalization-batch-4/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-5.md
  stable_path: docs/98.archive/changes/chg-0127-language-policy-plan-normalization-batch-5/task.md
  artifact_id: task-0127-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0127-language-policy-plan-normalization-batch-5/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-6.md
  stable_path: docs/98.archive/changes/chg-0128-language-policy-plan-normalization-batch-6/task.md
  artifact_id: task-0128-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0128-language-policy-plan-normalization-batch-6/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-7.md
  stable_path: docs/98.archive/changes/chg-0129-language-policy-plan-normalization-batch-7/task.md
  artifact_id: task-0129-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0129-language-policy-plan-normalization-batch-7/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-plan-normalization-batch-8.md
  stable_path: docs/98.archive/changes/chg-0130-language-policy-plan-normalization-batch-8/task.md
  artifact_id: task-0130-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0130-language-policy-plan-normalization-batch-8/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-reference-normalization.md
  stable_path: docs/98.archive/changes/chg-0131-language-policy-reference-normalization/task.md
  artifact_id: task-0131-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0131-language-policy-reference-normalization/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-1.md
  stable_path: docs/98.archive/changes/chg-0132-language-policy-task-normalization-batch-1/task.md
  artifact_id: task-0132-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0132-language-policy-task-normalization-batch-1/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-2.md
  stable_path: docs/98.archive/changes/chg-0133-language-policy-task-normalization-batch-2/task.md
  artifact_id: task-0133-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0133-language-policy-task-normalization-batch-2/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-3.md
  stable_path: docs/98.archive/changes/chg-0134-language-policy-task-normalization-batch-3/task.md
  artifact_id: task-0134-02
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0134-language-policy-task-normalization-batch-3/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-4.md
  stable_path: docs/98.archive/changes/chg-0135-language-policy-task-normalization-batch-4/task.md
  artifact_id: task-0135-02
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0135-language-policy-task-normalization-batch-4/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-5.md
  stable_path: docs/98.archive/changes/chg-0136-language-policy-task-normalization-batch-5/task.md
  artifact_id: task-0136-02
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0136-language-policy-task-normalization-batch-5/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-6.md
  stable_path: docs/98.archive/changes/chg-0137-language-policy-task-normalization-batch-6/task.md
  artifact_id: task-0137-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0137-language-policy-task-normalization-batch-6/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-06-05-language-policy-task-normalization-batch-7.md
  stable_path: docs/98.archive/changes/chg-0138-language-policy-task-normalization-batch-7/task.md
  artifact_id: task-0138-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0138-language-policy-task-normalization-batch-7/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-02-template-system-reorganization.md
  stable_path: docs/98.archive/changes/chg-0063-template-system-reorganization/task.md
  artifact_id: task-0063-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0063-template-system-reorganization/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-03-document-contract-remediation-batches.md
  stable_path: docs/98.archive/changes/chg-0064-document-contract-remediation-batches/task.md
  artifact_id: task-0064-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0064-document-contract-remediation-batches/task.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-03-template-system-contract-standardization.md
  stable_path: docs/98.archive/changes/chg-0065-template-system-contract-standardization/task.md
  artifact_id: task-0065-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0065-template-system-contract-standardization/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-03-workspace-document-contract-audit-pack.md
  stable_path: docs/98.archive/changes/chg-0066-workspace-document-contract-audit-pack/task.md
  artifact_id: task-0066-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0066-workspace-document-contract-audit-pack/task.md; migrate 21 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-04-document-restructure-audit-contract-archive.md
  stable_path: docs/98.archive/changes/chg-0067-document-restructure-audit-contract-archive/task.md
  artifact_id: task-0067-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0067-document-restructure-audit-contract-archive/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-04-examples-scaffold-contract-remediation.md
  stable_path: docs/98.archive/changes/chg-0139-examples-scaffold-contract-remediation/task.md
  artifact_id: task-0139-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0139-examples-scaffold-contract-remediation/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-04-frontmatter-routing-evidence-refresh.md
  stable_path: docs/98.archive/changes/chg-0140-frontmatter-routing-evidence-refresh/task.md
  artifact_id: task-0140-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0140-frontmatter-routing-evidence-refresh/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-04-github-branch-protection-reverification.md
  stable_path: docs/98.archive/changes/chg-0141-github-branch-protection-reverification/task.md
  artifact_id: task-0141-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0141-github-branch-protection-reverification/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-04-infra-tech-stack-version-refresh.md
  stable_path: docs/98.archive/changes/chg-0142-infra-tech-stack-version-refresh/task.md
  artifact_id: task-0142-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0142-infra-tech-stack-version-refresh/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-05-agent-output-eval-fixtures.md
  stable_path: docs/98.archive/changes/chg-0068-agent-output-eval-fixtures/task.md
  artifact_id: task-0068-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0068-agent-output-eval-fixtures/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-05-agentic-engineering-implementation-audit-pack.md
  stable_path: docs/98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/task.md
  artifact_id: task-0069-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0069-agentic-engineering-implementation-audit-pack/task.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md
  stable_path: docs/98.archive/changes/chg-0070-agentic-research-pack-refresh/task.md
  artifact_id: task-0070-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0070-agentic-research-pack-refresh/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-05-audit-pack-coverage-report.md
  stable_path: docs/98.archive/changes/chg-0071-audit-pack-coverage-report/task.md
  artifact_id: task-0071-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0071-audit-pack-coverage-report/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-05-compose-profile-service-coverage-snapshot.md
  stable_path: docs/98.archive/changes/chg-0072-compose-profile-service-coverage-snapshot/task.md
  artifact_id: task-0072-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0072-compose-profile-service-coverage-snapshot/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-05-gap-routing-recommendation.md
  stable_path: docs/98.archive/changes/chg-0073-gap-routing-recommendation/task.md
  artifact_id: task-0073-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0073-gap-routing-recommendation/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-05-provider-semantic-parity-validator.md
  stable_path: docs/98.archive/changes/chg-0074-provider-semantic-parity-validator/task.md
  artifact_id: task-0074-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0074-provider-semantic-parity-validator/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-05-provider-workspace-artifact-path-parity.md
  stable_path: docs/98.archive/changes/chg-0075-provider-workspace-artifact-path-parity/task.md
  artifact_id: task-0075-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0075-provider-workspace-artifact-path-parity/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-05-qa-gate-recommendation-ci-summary.md
  stable_path: docs/98.archive/changes/chg-0076-qa-gate-recommendation-ci-summary/task.md
  artifact_id: task-0076-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0076-qa-gate-recommendation-ci-summary/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-05-template-system-numbered-sdlc-paths.md
  stable_path: docs/98.archive/changes/chg-0077-template-system-numbered-sdlc-paths/task.md
  artifact_id: task-0077-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0077-template-system-numbered-sdlc-paths/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-05-workspace-support-surface-contract.md
  stable_path: docs/98.archive/changes/chg-0078-workspace-support-surface-contract/task.md
  artifact_id: task-0078-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0078-workspace-support-surface-contract/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-06-agent-output-eval-ci-gate.md
  stable_path: docs/98.archive/changes/chg-0079-agent-output-eval-ci-gate/task.md
  artifact_id: task-0079-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0079-agent-output-eval-ci-gate/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-06-agent-output-eval-runner.md
  stable_path: docs/98.archive/changes/chg-0080-agent-output-eval-runner/task.md
  artifact_id: task-0080-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0080-agent-output-eval-runner/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-06-audit-implementation-matrix-snapshot.md
  stable_path: docs/98.archive/changes/chg-0081-audit-implementation-matrix-snapshot/task.md
  artifact_id: task-0081-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0081-audit-implementation-matrix-snapshot/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-06-dependency-vulnerability-audit-gate.md
  stable_path: docs/98.archive/changes/chg-0082-dependency-vulnerability-audit-gate/task.md
  artifact_id: task-0082-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0082-dependency-vulnerability-audit-gate/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-06-llm-wiki-stage-category-coverage.md
  stable_path: docs/98.archive/changes/chg-0083-llm-wiki-stage-category-coverage/task.md
  artifact_id: task-0083-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0083-llm-wiki-stage-category-coverage/task.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-06-provider-hook-parity-matrix.md
  stable_path: docs/98.archive/changes/chg-0084-provider-hook-parity-matrix/task.md
  artifact_id: task-0084-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0084-provider-hook-parity-matrix/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-06-sdlc-document-contract-corpus-normalization.md
  stable_path: docs/98.archive/changes/chg-0085-sdlc-document-contract-corpus-normalization/task.md
  artifact_id: task-0085-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0085-sdlc-document-contract-corpus-normalization/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-06-security-automation-readiness-snapshot.md
  stable_path: docs/98.archive/changes/chg-0086-security-automation-readiness-snapshot/task.md
  artifact_id: task-0086-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0086-security-automation-readiness-snapshot/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-06-tech-stack-version-provenance.md
  stable_path: docs/98.archive/changes/chg-0087-tech-stack-version-provenance/task.md
  artifact_id: task-0087-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0087-tech-stack-version-provenance/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md
  stable_path: docs/98.archive/changes/chg-0088-agentic-research-pack-consolidation/task.md
  artifact_id: task-0088-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0088-agentic-research-pack-consolidation/task.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md
  stable_path: docs/98.archive/changes/chg-0089-agentic-engineering-audit-remediation/task.md
  artifact_id: task-0089-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0089-agentic-engineering-audit-remediation/task.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-12-agentic-audit-harness-consolidation.md
  stable_path: docs/98.archive/changes/chg-0094-agentic-audit-harness-consolidation/task.md
  artifact_id: task-0094-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0094-agentic-audit-harness-consolidation/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-13-document-contract-canonicalization.md
  stable_path: docs/98.archive/changes/chg-0095-document-contract-canonicalization/task.md
  artifact_id: task-0095-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0095-document-contract-canonicalization/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-13-template-contract-system-canonicalization.md
  stable_path: docs/98.archive/changes/chg-0096-template-contract-system-canonicalization/task.md
  artifact_id: task-0096-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0096-template-contract-system-canonicalization/task.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-14-document-corpus-lifecycle-migration-foundation.md
  stable_path: docs/98.archive/changes/chg-0097-document-corpus-lifecycle-migration-foundation/task.md
  artifact_id: task-0097-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0097-document-corpus-lifecycle-migration-foundation/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-15-agent-governance-harness-convergence.md
  stable_path: docs/98.archive/changes/chg-0098-agent-governance-harness-convergence/task.md
  artifact_id: task-0098-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0098-agent-governance-harness-convergence/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-18-target-surface-contract-convergence.md
  stable_path: docs/98.archive/changes/chg-0099-target-surface-contract-convergence/task.md
  artifact_id: task-0099-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0099-target-surface-contract-convergence/task.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-19-compose-runtime-readiness-remediation.md
  stable_path: docs/98.archive/changes/chg-0090-compose-runtime-readiness-remediation/task.md
  artifact_id: task-0090-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0090-compose-runtime-readiness-remediation/task.md; migrate 16 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-19-deployment-release-engineering-remediation.md
  stable_path: docs/98.archive/changes/chg-0091-deployment-release-engineering-remediation/task.md
  artifact_id: task-0091-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0091-deployment-release-engineering-remediation/task.md; migrate 23 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-19-infrastructure-operations-readiness-remediation.md
  stable_path: docs/98.archive/changes/chg-0092-infrastructure-operations-readiness-remediation/task.md
  artifact_id: task-0092-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0092-infrastructure-operations-readiness-remediation/task.md; migrate 17 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-19-operational-readiness-closure-program.md
  stable_path: docs/98.archive/changes/chg-0100-operational-readiness-closure-program/task.md
  artifact_id: task-0100-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0100-operational-readiness-closure-program/task.md; migrate 37 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-19-security-supply-chain-remediation.md
  stable_path: docs/98.archive/changes/chg-0093-security-supply-chain-remediation/task.md
  artifact_id: task-0093-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline completed source to stable typed target docs/98.archive/changes/chg-0093-security-supply-chain-remediation/task.md; migrate 18 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-23-security-supply-chain-runtime-closure.md
  stable_path: docs/98.archive/changes/chg-0093-security-supply-chain-remediation/task.md
  artifact_id: task-0093-01
  action: merge
  replacement: docs/98.archive/changes/chg-0093-security-supply-chain-remediation/task.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline completed source into canonical target docs/98.archive/changes/chg-0093-security-supply-chain-remediation/task.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/04.execution/tasks/2026-07-26-agent-governance-canonical-convergence.md
  stable_path: docs/03.specs/spec-0134-agent-governance-canonical-convergence/task.md
  artifact_id: task-0134-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0134-agent-governance-canonical-convergence/task.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-07-26-corrected-delivery-evidence-reconciliation.md
  stable_path: docs/98.archive/changes/chg-0091-deployment-release-engineering-remediation/task.md
  artifact_id: task-0091-01
  action: merge
  replacement: docs/98.archive/changes/chg-0091-deployment-release-engineering-remediation/task.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline completed source into canonical target docs/98.archive/changes/chg-0091-deployment-release-engineering-remediation/task.md; migrate 7 resolved inbound link(s) before source removal.
- legacy_path: docs/04.execution/tasks/2026-07-28-target-surface-delta-convergence.md
  stable_path: docs/03.specs/spec-0135-target-surface-delta-convergence/task.md
  artifact_id: task-0135-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0135-target-surface-delta-convergence/task.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/2026-08-07-agentic-research-pack-extension.md
  stable_path: docs/03.specs/spec-0123-agentic-engineering-audit-remediation/task.md
  artifact_id: task-0123-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/03.specs/spec-0123-agentic-engineering-audit-remediation/task.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/04.execution/tasks/README.md
  stable_path: docs/03.specs/README.md
  artifact_id: null
  action: merge
  replacement: docs/03.specs/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge the active Stage 04 Task navigation source into the canonical Stage 03 capability index; migrate 53 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/README.md
  stable_path: docs/05.operations/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 300 resolved inbound link(s).
- legacy_path: docs/05.operations/guides/00-workspace/README.md
  stable_path: docs/05.operations/00-workspace/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/00-workspace/README.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/00-workspace/developer-setup.md
  stable_path: docs/05.operations/00-workspace/ops-0002-developer-setup/guide.md
  artifact_id: guide-0002
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0002-developer-setup/guide.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/00-workspace/env-key-comparison.md
  stable_path: docs/05.operations/00-workspace/ops-0003-env-key-comparison/guide.md
  artifact_id: guide-0003
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0003-env-key-comparison/guide.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/00-workspace/harness-agent-first-engineering.md
  stable_path: docs/05.operations/00-workspace/ops-0004-harness-agent-first-engineering/guide.md
  artifact_id: guide-0004
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0004-harness-agent-first-engineering/guide.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/00-workspace/llm-wiki-maintenance.md
  stable_path: docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/guide.md
  artifact_id: guide-0007
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/guide.md; migrate 13 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/00-workspace/new-service-onboarding.md
  stable_path: docs/05.operations/00-workspace/ops-0008-new-service-onboarding/guide.md
  artifact_id: guide-0008
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0008-new-service-onboarding/guide.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/00-workspace/sensitive-env-vars-comparison.md
  stable_path: docs/05.operations/00-workspace/ops-0010-sensitive-env-vars-comparison/guide.md
  artifact_id: guide-0010
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0010-sensitive-env-vars-comparison/guide.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/01-gateway/README.md
  stable_path: docs/05.operations/01-gateway/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/01-gateway/README.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/01-gateway/nginx.md
  stable_path: docs/05.operations/01-gateway/ops-0011-nginx/guide.md
  artifact_id: guide-0011
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/01-gateway/ops-0011-nginx/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/01-gateway/setup.md
  stable_path: docs/05.operations/01-gateway/ops-0012-setup/guide.md
  artifact_id: guide-0012
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/01-gateway/ops-0012-setup/guide.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/01-gateway/traefik.md
  stable_path: docs/05.operations/01-gateway/ops-0013-traefik/guide.md
  artifact_id: guide-0013
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/01-gateway/ops-0013-traefik/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/02-auth/README.md
  stable_path: docs/05.operations/02-auth/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/02-auth/README.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/02-auth/keycloak.md
  stable_path: docs/05.operations/02-auth/ops-0014-keycloak/guide.md
  artifact_id: guide-0014
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/02-auth/ops-0014-keycloak/guide.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/02-auth/oauth2-proxy.md
  stable_path: docs/05.operations/02-auth/ops-0015-oauth2-proxy/guide.md
  artifact_id: guide-0015
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/02-auth/ops-0015-oauth2-proxy/guide.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/03-security/README.md
  stable_path: docs/05.operations/03-security/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/03-security/README.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/03-security/vault.md
  stable_path: docs/05.operations/03-security/ops-0016-vault/guide.md
  artifact_id: guide-0016
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/03-security/ops-0016-vault/guide.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/04-data/README.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/analytics/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 11 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/guides/04-data/analytics/influxdb.md
  stable_path: docs/05.operations/04-data/ops-0017-analytics-influxdb/guide.md
  artifact_id: guide-0017
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0017-analytics-influxdb/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/analytics/ksqldb.md
  stable_path: docs/05.operations/04-data/ops-0018-analytics-ksqldb/guide.md
  artifact_id: guide-0018
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0018-analytics-ksqldb/guide.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/analytics/opensearch.md
  stable_path: docs/05.operations/04-data/ops-0019-analytics-opensearch/guide.md
  artifact_id: guide-0019
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0019-analytics-opensearch/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/analytics/warehouses.md
  stable_path: docs/05.operations/04-data/ops-0020-analytics-warehouses/guide.md
  artifact_id: guide-0020
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0020-analytics-warehouses/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/cache-and-kv/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/guides/04-data/cache-and-kv/valkey-cluster.md
  stable_path: docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/guide.md
  artifact_id: guide-0022
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/lake-and-object/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/guides/04-data/lake-and-object/minio.md
  stable_path: docs/05.operations/04-data/ops-0023-lake-and-object-minio/guide.md
  artifact_id: guide-0023
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0023-lake-and-object-minio/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/lake-and-object/seaweedfs.md
  stable_path: docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/guide.md
  artifact_id: guide-0024
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/nosql/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/guides/04-data/nosql/cassandra.md
  stable_path: docs/05.operations/04-data/ops-0025-nosql-cassandra/guide.md
  artifact_id: guide-0025
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0025-nosql-cassandra/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/nosql/couchdb.md
  stable_path: docs/05.operations/04-data/ops-0026-nosql-couchdb/guide.md
  artifact_id: guide-0026
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0026-nosql-couchdb/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/nosql/mongodb.md
  stable_path: docs/05.operations/04-data/ops-0027-nosql-mongodb/guide.md
  artifact_id: guide-0027
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0027-nosql-mongodb/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/operational/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/guides/04-data/operational/mng-db.md
  stable_path: docs/05.operations/04-data/ops-0028-operational-mng-db/guide.md
  artifact_id: guide-0028
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0028-operational-mng-db/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/operational/supabase.md
  stable_path: docs/05.operations/04-data/ops-0029-operational-supabase/guide.md
  artifact_id: guide-0029
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0029-operational-supabase/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/optimization/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 2 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/guides/04-data/optimization/optimization-hardening.md
  stable_path: docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/guide.md
  artifact_id: guide-0030
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/guide.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/relational/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/guides/04-data/relational/postgresql-cluster.md
  stable_path: docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/guide.md
  artifact_id: guide-0031
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/specialized/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/guides/04-data/specialized/neo4j.md
  stable_path: docs/05.operations/04-data/ops-0033-specialized-neo4j/guide.md
  artifact_id: guide-0033
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0033-specialized-neo4j/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/04-data/specialized/qdrant.md
  stable_path: docs/05.operations/04-data/ops-0034-specialized-qdrant/guide.md
  artifact_id: guide-0034
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0034-specialized-qdrant/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/05-messaging/README.md
  stable_path: docs/05.operations/05-messaging/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/05-messaging/README.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/05-messaging/kafka.md
  stable_path: docs/05.operations/05-messaging/ops-0036-kafka/guide.md
  artifact_id: guide-0036
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/05-messaging/ops-0036-kafka/guide.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/05-messaging/optimization-hardening.md
  stable_path: docs/05.operations/05-messaging/ops-0037-optimization-hardening/guide.md
  artifact_id: guide-0037
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/05-messaging/ops-0037-optimization-hardening/guide.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/05-messaging/rabbitmq.md
  stable_path: docs/05.operations/05-messaging/ops-0038-rabbitmq/guide.md
  artifact_id: guide-0038
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/05-messaging/ops-0038-rabbitmq/guide.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/06-observability/README.md
  stable_path: docs/05.operations/06-observability/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/06-observability/README.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/06-observability/alertmanager.md
  stable_path: docs/05.operations/06-observability/ops-0039-alertmanager/guide.md
  artifact_id: guide-0039
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0039-alertmanager/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/06-observability/alloy.md
  stable_path: docs/05.operations/06-observability/ops-0040-alloy/guide.md
  artifact_id: guide-0040
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0040-alloy/guide.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/06-observability/grafana.md
  stable_path: docs/05.operations/06-observability/ops-0041-grafana/guide.md
  artifact_id: guide-0041
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0041-grafana/guide.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/06-observability/lgtm-stack.md
  stable_path: docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md
  artifact_id: guide-0042
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0042-lgtm-stack/guide.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/06-observability/loki.md
  stable_path: docs/05.operations/06-observability/ops-0043-loki/guide.md
  artifact_id: guide-0043
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0043-loki/guide.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/06-observability/optimization-hardening.md
  stable_path: docs/05.operations/06-observability/ops-0044-optimization-hardening/guide.md
  artifact_id: guide-0044
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0044-optimization-hardening/guide.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/06-observability/prometheus.md
  stable_path: docs/05.operations/06-observability/ops-0045-prometheus/guide.md
  artifact_id: guide-0045
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0045-prometheus/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/06-observability/pushgateway.md
  stable_path: docs/05.operations/06-observability/ops-0046-pushgateway/guide.md
  artifact_id: guide-0046
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0046-pushgateway/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/06-observability/pyroscope.md
  stable_path: docs/05.operations/06-observability/ops-0047-pyroscope/guide.md
  artifact_id: guide-0047
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0047-pyroscope/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/06-observability/tempo.md
  stable_path: docs/05.operations/06-observability/ops-0049-tempo/guide.md
  artifact_id: guide-0049
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0049-tempo/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/07-workflow/README.md
  stable_path: docs/05.operations/07-workflow/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/07-workflow/README.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/07-workflow/airflow-dag-basics.md
  stable_path: docs/05.operations/07-workflow/ops-0051-airflow-dag-basics/guide.md
  artifact_id: guide-0051
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/07-workflow/ops-0051-airflow-dag-basics/guide.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/07-workflow/airflow.md
  stable_path: docs/05.operations/07-workflow/ops-0050-airflow/guide.md
  artifact_id: guide-0050
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/07-workflow/ops-0050-airflow/guide.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/07-workflow/n8n.md
  stable_path: docs/05.operations/07-workflow/ops-0053-n8n/guide.md
  artifact_id: guide-0053
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/07-workflow/ops-0053-n8n/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/07-workflow/optimization-hardening.md
  stable_path: docs/05.operations/07-workflow/ops-0054-optimization-hardening/guide.md
  artifact_id: guide-0054
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/07-workflow/ops-0054-optimization-hardening/guide.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/08-ai/README.md
  stable_path: docs/05.operations/08-ai/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/08-ai/README.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/08-ai/ollama.md
  stable_path: docs/05.operations/08-ai/ops-0056-ollama/guide.md
  artifact_id: guide-0056
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/08-ai/ops-0056-ollama/guide.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/08-ai/open-webui.md
  stable_path: docs/05.operations/08-ai/ops-0057-open-webui/guide.md
  artifact_id: guide-0057
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/08-ai/ops-0057-open-webui/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/08-ai/optimization-hardening.md
  stable_path: docs/05.operations/08-ai/ops-0058-optimization-hardening/guide.md
  artifact_id: guide-0058
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/08-ai/ops-0058-optimization-hardening/guide.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/08-ai/rag-workflow.md
  stable_path: docs/05.operations/08-ai/ops-0059-rag-workflow/guide.md
  artifact_id: guide-0059
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/08-ai/ops-0059-rag-workflow/guide.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/09-tooling/README.md
  stable_path: docs/05.operations/09-tooling/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/09-tooling/README.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/09-tooling/k6.md
  stable_path: docs/05.operations/09-tooling/ops-0061-k6/guide.md
  artifact_id: guide-0061
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0061-k6/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/09-tooling/locust.md
  stable_path: docs/05.operations/09-tooling/ops-0062-locust/guide.md
  artifact_id: guide-0062
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0062-locust/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/09-tooling/optimization-hardening.md
  stable_path: docs/05.operations/09-tooling/ops-0063-optimization-hardening/guide.md
  artifact_id: guide-0063
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0063-optimization-hardening/guide.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/09-tooling/performance-testing.md
  stable_path: docs/05.operations/09-tooling/ops-0064-performance-testing/guide.md
  artifact_id: guide-0064
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0064-performance-testing/guide.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/09-tooling/registry.md
  stable_path: docs/05.operations/09-tooling/ops-0065-registry/guide.md
  artifact_id: guide-0065
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0065-registry/guide.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/09-tooling/sonarqube.md
  stable_path: docs/05.operations/09-tooling/ops-0066-sonarqube/guide.md
  artifact_id: guide-0066
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0066-sonarqube/guide.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/09-tooling/syncthing.md
  stable_path: docs/05.operations/09-tooling/ops-0067-syncthing/guide.md
  artifact_id: guide-0067
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0067-syncthing/guide.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/09-tooling/terraform.md
  stable_path: docs/05.operations/09-tooling/ops-0068-terraform/guide.md
  artifact_id: guide-0068
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0068-terraform/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/09-tooling/terrakube.md
  stable_path: docs/05.operations/09-tooling/ops-0069-terrakube/guide.md
  artifact_id: guide-0069
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0069-terrakube/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/10-communication/README.md
  stable_path: docs/05.operations/10-communication/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/10-communication/README.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/10-communication/mail.md
  stable_path: docs/05.operations/10-communication/ops-0070-mail/guide.md
  artifact_id: guide-0070
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/10-communication/ops-0070-mail/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/11-laboratory/README.md
  stable_path: docs/05.operations/11-laboratory/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/11-laboratory/README.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/11-laboratory/dashboard.md
  stable_path: docs/05.operations/11-laboratory/ops-0071-dashboard/guide.md
  artifact_id: guide-0071
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0071-dashboard/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/11-laboratory/dozzle.md
  stable_path: docs/05.operations/11-laboratory/ops-0072-dozzle/guide.md
  artifact_id: guide-0072
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0072-dozzle/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/11-laboratory/open-notebook.md
  stable_path: docs/05.operations/11-laboratory/ops-0073-open-notebook/guide.md
  artifact_id: guide-0073
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0073-open-notebook/guide.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/11-laboratory/optimization-hardening.md
  stable_path: docs/05.operations/11-laboratory/ops-0074-optimization-hardening/guide.md
  artifact_id: guide-0074
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0074-optimization-hardening/guide.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/11-laboratory/portainer.md
  stable_path: docs/05.operations/11-laboratory/ops-0075-portainer/guide.md
  artifact_id: guide-0075
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0075-portainer/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/11-laboratory/redisinsight.md
  stable_path: docs/05.operations/11-laboratory/ops-0076-redisinsight/guide.md
  artifact_id: guide-0076
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0076-redisinsight/guide.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/12-infra-net/README.md
  stable_path: docs/05.operations/12-infra-net/README.md
  artifact_id: null
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline untyped source to stable typed target docs/05.operations/12-infra-net/README.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/12-infra-net/standardize-infra-net.md
  stable_path: docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/guide.md
  artifact_id: guide-0077
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/guide.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/guides/README.md
  stable_path: docs/05.operations/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/README.md; migrate 26 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/incidents/README.md
  stable_path: docs/05.operations/incidents/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 69 resolved inbound link(s).
- legacy_path: docs/05.operations/policies/00-workspace/README.md
  stable_path: docs/05.operations/00-workspace/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/00-workspace/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/00-workspace/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/00-workspace/common-optimizations-template-exceptions.md
  stable_path: docs/05.operations/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md
  artifact_id: policy-0001
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0001-common-optimizations-template-exceptions/policy.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/00-workspace/harness-agent-first-engineering.md
  stable_path: docs/05.operations/00-workspace/ops-0004-harness-agent-first-engineering/policy.md
  artifact_id: policy-0004
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0004-harness-agent-first-engineering/policy.md; migrate 12 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/00-workspace/infra-service-optimization-catalog.md
  stable_path: docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md
  artifact_id: policy-0006
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0006-infra-service-optimization-catalog/policy.md; migrate 21 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/00-workspace/llm-wiki-maintenance.md
  stable_path: docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md
  artifact_id: policy-0007
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/policy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/01-gateway/README.md
  stable_path: docs/05.operations/01-gateway/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/01-gateway/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/01-gateway/README.md; migrate 5 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/01-gateway/nginx.md
  stable_path: docs/05.operations/01-gateway/ops-0011-nginx/policy.md
  artifact_id: policy-0011
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/01-gateway/ops-0011-nginx/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/01-gateway/traefik.md
  stable_path: docs/05.operations/01-gateway/ops-0013-traefik/policy.md
  artifact_id: policy-0013
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/01-gateway/ops-0013-traefik/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/02-auth/README.md
  stable_path: docs/05.operations/02-auth/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/02-auth/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/02-auth/README.md; migrate 5 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/02-auth/keycloak.md
  stable_path: docs/05.operations/02-auth/ops-0014-keycloak/policy.md
  artifact_id: policy-0014
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/02-auth/ops-0014-keycloak/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/02-auth/oauth2-proxy.md
  stable_path: docs/05.operations/02-auth/ops-0015-oauth2-proxy/policy.md
  artifact_id: policy-0015
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/02-auth/ops-0015-oauth2-proxy/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/03-security/README.md
  stable_path: docs/05.operations/03-security/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/03-security/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/03-security/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/03-security/vault.md
  stable_path: docs/05.operations/03-security/ops-0016-vault/policy.md
  artifact_id: policy-0016
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/03-security/ops-0016-vault/policy.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 7 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/04-data/analytics/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 7 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/04-data/analytics/influxdb.md
  stable_path: docs/05.operations/04-data/ops-0017-analytics-influxdb/policy.md
  artifact_id: policy-0017
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0017-analytics-influxdb/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/analytics/ksqldb.md
  stable_path: docs/05.operations/04-data/ops-0018-analytics-ksqldb/policy.md
  artifact_id: policy-0018
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0018-analytics-ksqldb/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/analytics/opensearch.md
  stable_path: docs/05.operations/04-data/ops-0019-analytics-opensearch/policy.md
  artifact_id: policy-0019
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0019-analytics-opensearch/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/analytics/warehouses.md
  stable_path: docs/05.operations/04-data/ops-0020-analytics-warehouses/policy.md
  artifact_id: policy-0020
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0020-analytics-warehouses/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/backup/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 2 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/04-data/backup/backup-policy.md
  stable_path: docs/05.operations/04-data/ops-0021-backup-backup-policy/policy.md
  artifact_id: policy-0021
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0021-backup-backup-policy/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/cache-and-kv/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/04-data/cache-and-kv/valkey-cluster.md
  stable_path: docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/policy.md
  artifact_id: policy-0022
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/lake-and-object/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/04-data/lake-and-object/minio.md
  stable_path: docs/05.operations/04-data/ops-0023-lake-and-object-minio/policy.md
  artifact_id: policy-0023
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0023-lake-and-object-minio/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/lake-and-object/seaweedfs.md
  stable_path: docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/policy.md
  artifact_id: policy-0024
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/nosql/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/04-data/nosql/cassandra.md
  stable_path: docs/05.operations/04-data/ops-0025-nosql-cassandra/policy.md
  artifact_id: policy-0025
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0025-nosql-cassandra/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/nosql/couchdb.md
  stable_path: docs/05.operations/04-data/ops-0026-nosql-couchdb/policy.md
  artifact_id: policy-0026
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0026-nosql-couchdb/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/nosql/mongodb.md
  stable_path: docs/05.operations/04-data/ops-0027-nosql-mongodb/policy.md
  artifact_id: policy-0027
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0027-nosql-mongodb/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/operational/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/04-data/operational/mng-db.md
  stable_path: docs/05.operations/04-data/ops-0028-operational-mng-db/policy.md
  artifact_id: policy-0028
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0028-operational-mng-db/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/operational/supabase.md
  stable_path: docs/05.operations/04-data/ops-0029-operational-supabase/policy.md
  artifact_id: policy-0029
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0029-operational-supabase/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/optimization/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 2 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/04-data/optimization/optimization-hardening.md
  stable_path: docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/policy.md
  artifact_id: policy-0030
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/policy.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/relational/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/04-data/relational/postgresql-cluster.md
  stable_path: docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/policy.md
  artifact_id: policy-0031
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/specialized/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/04-data/specialized/neo4j.md
  stable_path: docs/05.operations/04-data/ops-0033-specialized-neo4j/policy.md
  artifact_id: policy-0033
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0033-specialized-neo4j/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/04-data/specialized/qdrant.md
  stable_path: docs/05.operations/04-data/ops-0034-specialized-qdrant/policy.md
  artifact_id: policy-0034
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0034-specialized-qdrant/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/05-messaging/README.md
  stable_path: docs/05.operations/05-messaging/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/05-messaging/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/05-messaging/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/05-messaging/kafka.md
  stable_path: docs/05.operations/05-messaging/ops-0036-kafka/policy.md
  artifact_id: policy-0036
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/05-messaging/ops-0036-kafka/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/05-messaging/optimization-hardening.md
  stable_path: docs/05.operations/05-messaging/ops-0037-optimization-hardening/policy.md
  artifact_id: policy-0037
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/05-messaging/ops-0037-optimization-hardening/policy.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/05-messaging/rabbitmq.md
  stable_path: docs/05.operations/05-messaging/ops-0038-rabbitmq/policy.md
  artifact_id: policy-0038
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/05-messaging/ops-0038-rabbitmq/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/06-observability/README.md
  stable_path: docs/05.operations/06-observability/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/06-observability/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/06-observability/README.md; migrate 5 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/06-observability/alertmanager.md
  stable_path: docs/05.operations/06-observability/ops-0039-alertmanager/policy.md
  artifact_id: policy-0039
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0039-alertmanager/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/06-observability/alloy.md
  stable_path: docs/05.operations/06-observability/ops-0040-alloy/policy.md
  artifact_id: policy-0040
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0040-alloy/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/06-observability/grafana.md
  stable_path: docs/05.operations/06-observability/ops-0041-grafana/policy.md
  artifact_id: policy-0041
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0041-grafana/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/06-observability/loki.md
  stable_path: docs/05.operations/06-observability/ops-0043-loki/policy.md
  artifact_id: policy-0043
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0043-loki/policy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/06-observability/optimization-hardening.md
  stable_path: docs/05.operations/06-observability/ops-0044-optimization-hardening/policy.md
  artifact_id: policy-0044
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0044-optimization-hardening/policy.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/06-observability/prometheus.md
  stable_path: docs/05.operations/06-observability/ops-0045-prometheus/policy.md
  artifact_id: policy-0045
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0045-prometheus/policy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/06-observability/pushgateway.md
  stable_path: docs/05.operations/06-observability/ops-0046-pushgateway/policy.md
  artifact_id: policy-0046
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0046-pushgateway/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/06-observability/pyroscope.md
  stable_path: docs/05.operations/06-observability/ops-0047-pyroscope/policy.md
  artifact_id: policy-0047
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0047-pyroscope/policy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/06-observability/retention.md
  stable_path: docs/05.operations/06-observability/ops-0048-retention/policy.md
  artifact_id: policy-0048
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0048-retention/policy.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/06-observability/tempo.md
  stable_path: docs/05.operations/06-observability/ops-0049-tempo/policy.md
  artifact_id: policy-0049
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0049-tempo/policy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/07-workflow/README.md
  stable_path: docs/05.operations/07-workflow/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/07-workflow/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/07-workflow/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/07-workflow/airflow.md
  stable_path: docs/05.operations/07-workflow/ops-0050-airflow/policy.md
  artifact_id: policy-0050
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/07-workflow/ops-0050-airflow/policy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/07-workflow/dag-deployment.md
  stable_path: docs/05.operations/07-workflow/ops-0052-dag-deployment/policy.md
  artifact_id: policy-0052
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/07-workflow/ops-0052-dag-deployment/policy.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/07-workflow/n8n.md
  stable_path: docs/05.operations/07-workflow/ops-0053-n8n/policy.md
  artifact_id: policy-0053
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/07-workflow/ops-0053-n8n/policy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/07-workflow/optimization-hardening.md
  stable_path: docs/05.operations/07-workflow/ops-0054-optimization-hardening/policy.md
  artifact_id: policy-0054
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/07-workflow/ops-0054-optimization-hardening/policy.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/08-ai/README.md
  stable_path: docs/05.operations/08-ai/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/08-ai/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/08-ai/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/08-ai/ollama.md
  stable_path: docs/05.operations/08-ai/ops-0056-ollama/policy.md
  artifact_id: policy-0056
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/08-ai/ops-0056-ollama/policy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/08-ai/open-webui.md
  stable_path: docs/05.operations/08-ai/ops-0057-open-webui/policy.md
  artifact_id: policy-0057
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/08-ai/ops-0057-open-webui/policy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/08-ai/optimization-hardening.md
  stable_path: docs/05.operations/08-ai/ops-0058-optimization-hardening/policy.md
  artifact_id: policy-0058
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/08-ai/ops-0058-optimization-hardening/policy.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/09-tooling/README.md
  stable_path: docs/05.operations/09-tooling/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/09-tooling/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/09-tooling/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/09-tooling/iac-deployment-policy.md
  stable_path: docs/05.operations/09-tooling/ops-0060-iac-deployment-policy/policy.md
  artifact_id: policy-0060
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0060-iac-deployment-policy/policy.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/09-tooling/k6.md
  stable_path: docs/05.operations/09-tooling/ops-0061-k6/policy.md
  artifact_id: policy-0061
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0061-k6/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/09-tooling/locust.md
  stable_path: docs/05.operations/09-tooling/ops-0062-locust/policy.md
  artifact_id: policy-0062
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0062-locust/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/09-tooling/optimization-hardening.md
  stable_path: docs/05.operations/09-tooling/ops-0063-optimization-hardening/policy.md
  artifact_id: policy-0063
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0063-optimization-hardening/policy.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/09-tooling/performance-testing.md
  stable_path: docs/05.operations/09-tooling/ops-0064-performance-testing/policy.md
  artifact_id: policy-0064
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0064-performance-testing/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/09-tooling/registry.md
  stable_path: docs/05.operations/09-tooling/ops-0065-registry/policy.md
  artifact_id: policy-0065
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0065-registry/policy.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/09-tooling/sonarqube.md
  stable_path: docs/05.operations/09-tooling/ops-0066-sonarqube/policy.md
  artifact_id: policy-0066
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0066-sonarqube/policy.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/09-tooling/syncthing.md
  stable_path: docs/05.operations/09-tooling/ops-0067-syncthing/policy.md
  artifact_id: policy-0067
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0067-syncthing/policy.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/09-tooling/terraform.md
  stable_path: docs/05.operations/09-tooling/ops-0068-terraform/policy.md
  artifact_id: policy-0068
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0068-terraform/policy.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/09-tooling/terrakube.md
  stable_path: docs/05.operations/09-tooling/ops-0069-terrakube/policy.md
  artifact_id: policy-0069
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0069-terrakube/policy.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/10-communication/README.md
  stable_path: docs/05.operations/10-communication/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/10-communication/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/10-communication/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/10-communication/mail.md
  stable_path: docs/05.operations/10-communication/ops-0070-mail/policy.md
  artifact_id: policy-0070
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/10-communication/ops-0070-mail/policy.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/11-laboratory/README.md
  stable_path: docs/05.operations/11-laboratory/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/11-laboratory/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/11-laboratory/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/11-laboratory/dashboard.md
  stable_path: docs/05.operations/11-laboratory/ops-0071-dashboard/policy.md
  artifact_id: policy-0071
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0071-dashboard/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/11-laboratory/dozzle.md
  stable_path: docs/05.operations/11-laboratory/ops-0072-dozzle/policy.md
  artifact_id: policy-0072
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0072-dozzle/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/11-laboratory/open-notebook.md
  stable_path: docs/05.operations/11-laboratory/ops-0073-open-notebook/policy.md
  artifact_id: policy-0073
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0073-open-notebook/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/11-laboratory/optimization-hardening.md
  stable_path: docs/05.operations/11-laboratory/ops-0074-optimization-hardening/policy.md
  artifact_id: policy-0074
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0074-optimization-hardening/policy.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/11-laboratory/portainer.md
  stable_path: docs/05.operations/11-laboratory/ops-0075-portainer/policy.md
  artifact_id: policy-0075
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0075-portainer/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/11-laboratory/redisinsight.md
  stable_path: docs/05.operations/11-laboratory/ops-0076-redisinsight/policy.md
  artifact_id: policy-0076
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0076-redisinsight/policy.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/12-infra-net/README.md
  stable_path: docs/05.operations/12-infra-net/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/12-infra-net/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/12-infra-net/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/policies/12-infra-net/standardize-infra-net.md
  stable_path: docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/policy.md
  artifact_id: policy-0077
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/policy.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/policies/README.md
  stable_path: docs/05.operations/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/README.md; migrate 26 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/releases/README.md
  stable_path: docs/05.operations/releases/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 4 resolved inbound link(s).
- legacy_path: docs/05.operations/runbooks/00-workspace/README.md
  stable_path: docs/05.operations/00-workspace/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/00-workspace/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/00-workspace/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/00-workspace/harness-agent-first-engineering-validation.md
  stable_path: docs/05.operations/00-workspace/ops-0005-harness-agent-first-engineering-validation/runbook.md
  artifact_id: runbook-0005
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0005-harness-agent-first-engineering-validation/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/00-workspace/llm-wiki-maintenance.md
  stable_path: docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md
  artifact_id: runbook-0007
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0007-llm-wiki-maintenance/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/00-workspace/release-management.md
  stable_path: docs/05.operations/00-workspace/ops-0009-release-management/runbook.md
  artifact_id: runbook-0009
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/00-workspace/ops-0009-release-management/runbook.md; migrate 12 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/01-gateway/README.md
  stable_path: docs/05.operations/01-gateway/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/01-gateway/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/01-gateway/README.md; migrate 6 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/01-gateway/nginx.md
  stable_path: docs/05.operations/01-gateway/ops-0011-nginx/runbook.md
  artifact_id: runbook-0011
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/01-gateway/ops-0011-nginx/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/01-gateway/traefik.md
  stable_path: docs/05.operations/01-gateway/ops-0013-traefik/runbook.md
  artifact_id: runbook-0013
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/01-gateway/ops-0013-traefik/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/02-auth/README.md
  stable_path: docs/05.operations/02-auth/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/02-auth/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/02-auth/README.md; migrate 6 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/02-auth/keycloak.md
  stable_path: docs/05.operations/02-auth/ops-0014-keycloak/runbook.md
  artifact_id: runbook-0014
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/02-auth/ops-0014-keycloak/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/02-auth/oauth2-proxy.md
  stable_path: docs/05.operations/02-auth/ops-0015-oauth2-proxy/runbook.md
  artifact_id: runbook-0015
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/02-auth/ops-0015-oauth2-proxy/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/03-security/README.md
  stable_path: docs/05.operations/03-security/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/03-security/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/03-security/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/03-security/vault.md
  stable_path: docs/05.operations/03-security/ops-0016-vault/runbook.md
  artifact_id: runbook-0016
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/03-security/ops-0016-vault/runbook.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 7 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/04-data/analytics/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 6 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/04-data/analytics/influxdb.md
  stable_path: docs/05.operations/04-data/ops-0017-analytics-influxdb/runbook.md
  artifact_id: runbook-0017
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0017-analytics-influxdb/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/analytics/ksqldb.md
  stable_path: docs/05.operations/04-data/ops-0018-analytics-ksqldb/runbook.md
  artifact_id: runbook-0018
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0018-analytics-ksqldb/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/analytics/opensearch.md
  stable_path: docs/05.operations/04-data/ops-0019-analytics-opensearch/runbook.md
  artifact_id: runbook-0019
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0019-analytics-opensearch/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/analytics/warehouses.md
  stable_path: docs/05.operations/04-data/ops-0020-analytics-warehouses/runbook.md
  artifact_id: runbook-0020
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0020-analytics-warehouses/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/cache-and-kv/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/04-data/cache-and-kv/valkey-cluster.md
  stable_path: docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/runbook.md
  artifact_id: runbook-0022
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0022-cache-and-kv-valkey-cluster/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/lake-and-object/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/04-data/lake-and-object/minio.md
  stable_path: docs/05.operations/04-data/ops-0023-lake-and-object-minio/runbook.md
  artifact_id: runbook-0023
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0023-lake-and-object-minio/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/lake-and-object/seaweedfs.md
  stable_path: docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/runbook.md
  artifact_id: runbook-0024
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0024-lake-and-object-seaweedfs/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/nosql/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/04-data/nosql/cassandra.md
  stable_path: docs/05.operations/04-data/ops-0025-nosql-cassandra/runbook.md
  artifact_id: runbook-0025
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0025-nosql-cassandra/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/nosql/couchdb.md
  stable_path: docs/05.operations/04-data/ops-0026-nosql-couchdb/runbook.md
  artifact_id: runbook-0026
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0026-nosql-couchdb/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/nosql/mongodb.md
  stable_path: docs/05.operations/04-data/ops-0027-nosql-mongodb/runbook.md
  artifact_id: runbook-0027
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0027-nosql-mongodb/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/operational/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/04-data/operational/mng-db.md
  stable_path: docs/05.operations/04-data/ops-0028-operational-mng-db/runbook.md
  artifact_id: runbook-0028
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0028-operational-mng-db/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/operational/supabase.md
  stable_path: docs/05.operations/04-data/ops-0029-operational-supabase/runbook.md
  artifact_id: runbook-0029
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0029-operational-supabase/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/optimization/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 2 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/04-data/optimization/optimization-hardening.md
  stable_path: docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/runbook.md
  artifact_id: runbook-0030
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0030-optimization-optimization-hardening/runbook.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/relational/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 5 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/04-data/relational/postgresql-cluster.md
  stable_path: docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/runbook.md
  artifact_id: runbook-0031
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0031-relational-postgresql-cluster/runbook.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/relational/postgresql-logical-upgrade-restore-rehearsal.md
  stable_path: docs/05.operations/04-data/ops-0032-relational-postgresql-logical-upgrade-restore-rehearsal/runbook.md
  artifact_id: runbook-0032
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0032-relational-postgresql-logical-upgrade-restore-rehearsal/runbook.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/specialized/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/04-data/specialized/neo4j.md
  stable_path: docs/05.operations/04-data/ops-0033-specialized-neo4j/runbook.md
  artifact_id: runbook-0033
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0033-specialized-neo4j/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/specialized/qdrant.md
  stable_path: docs/05.operations/04-data/ops-0034-specialized-qdrant/runbook.md
  artifact_id: runbook-0034
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0034-specialized-qdrant/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/04-data/storage/README.md
  stable_path: docs/05.operations/04-data/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/04-data/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/04-data/README.md; migrate 2 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/04-data/storage/storage-exhaustion.md
  stable_path: docs/05.operations/04-data/ops-0035-storage-storage-exhaustion/runbook.md
  artifact_id: runbook-0035
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/04-data/ops-0035-storage-storage-exhaustion/runbook.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/05-messaging/README.md
  stable_path: docs/05.operations/05-messaging/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/05-messaging/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/05-messaging/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/05-messaging/kafka.md
  stable_path: docs/05.operations/05-messaging/ops-0036-kafka/runbook.md
  artifact_id: runbook-0036
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/05-messaging/ops-0036-kafka/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/05-messaging/optimization-hardening.md
  stable_path: docs/05.operations/05-messaging/ops-0037-optimization-hardening/runbook.md
  artifact_id: runbook-0037
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/05-messaging/ops-0037-optimization-hardening/runbook.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/05-messaging/rabbitmq.md
  stable_path: docs/05.operations/05-messaging/ops-0038-rabbitmq/runbook.md
  artifact_id: runbook-0038
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/05-messaging/ops-0038-rabbitmq/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/06-observability/README.md
  stable_path: docs/05.operations/06-observability/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/06-observability/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/06-observability/README.md; migrate 5 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/06-observability/alertmanager.md
  stable_path: docs/05.operations/06-observability/ops-0039-alertmanager/runbook.md
  artifact_id: runbook-0039
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0039-alertmanager/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/06-observability/alloy.md
  stable_path: docs/05.operations/06-observability/ops-0040-alloy/runbook.md
  artifact_id: runbook-0040
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0040-alloy/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/06-observability/grafana.md
  stable_path: docs/05.operations/06-observability/ops-0041-grafana/runbook.md
  artifact_id: runbook-0041
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0041-grafana/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/06-observability/loki.md
  stable_path: docs/05.operations/06-observability/ops-0043-loki/runbook.md
  artifact_id: runbook-0043
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0043-loki/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/06-observability/optimization-hardening.md
  stable_path: docs/05.operations/06-observability/ops-0044-optimization-hardening/runbook.md
  artifact_id: runbook-0044
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0044-optimization-hardening/runbook.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/06-observability/prometheus.md
  stable_path: docs/05.operations/06-observability/ops-0045-prometheus/runbook.md
  artifact_id: runbook-0045
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0045-prometheus/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/06-observability/pushgateway.md
  stable_path: docs/05.operations/06-observability/ops-0046-pushgateway/runbook.md
  artifact_id: runbook-0046
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0046-pushgateway/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/06-observability/pyroscope.md
  stable_path: docs/05.operations/06-observability/ops-0047-pyroscope/runbook.md
  artifact_id: runbook-0047
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0047-pyroscope/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/06-observability/tempo.md
  stable_path: docs/05.operations/06-observability/ops-0049-tempo/runbook.md
  artifact_id: runbook-0049
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/06-observability/ops-0049-tempo/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/07-workflow/README.md
  stable_path: docs/05.operations/07-workflow/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/07-workflow/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/07-workflow/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/07-workflow/airflow.md
  stable_path: docs/05.operations/07-workflow/ops-0050-airflow/runbook.md
  artifact_id: runbook-0050
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/07-workflow/ops-0050-airflow/runbook.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/07-workflow/n8n.md
  stable_path: docs/05.operations/07-workflow/ops-0053-n8n/runbook.md
  artifact_id: runbook-0053
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/07-workflow/ops-0053-n8n/runbook.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/07-workflow/optimization-hardening.md
  stable_path: docs/05.operations/07-workflow/ops-0054-optimization-hardening/runbook.md
  artifact_id: runbook-0054
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/07-workflow/ops-0054-optimization-hardening/runbook.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/08-ai/README.md
  stable_path: docs/05.operations/08-ai/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/08-ai/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/08-ai/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/08-ai/gpu-recovery.md
  stable_path: docs/05.operations/08-ai/ops-0055-gpu-recovery/runbook.md
  artifact_id: runbook-0055
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/08-ai/ops-0055-gpu-recovery/runbook.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/08-ai/ollama.md
  stable_path: docs/05.operations/08-ai/ops-0056-ollama/runbook.md
  artifact_id: runbook-0056
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/08-ai/ops-0056-ollama/runbook.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/08-ai/open-webui.md
  stable_path: docs/05.operations/08-ai/ops-0057-open-webui/runbook.md
  artifact_id: runbook-0057
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/08-ai/ops-0057-open-webui/runbook.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/08-ai/optimization-hardening.md
  stable_path: docs/05.operations/08-ai/ops-0058-optimization-hardening/runbook.md
  artifact_id: runbook-0058
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/08-ai/ops-0058-optimization-hardening/runbook.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/09-tooling/README.md
  stable_path: docs/05.operations/09-tooling/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/09-tooling/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/09-tooling/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/09-tooling/k6.md
  stable_path: docs/05.operations/09-tooling/ops-0061-k6/runbook.md
  artifact_id: runbook-0061
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0061-k6/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/09-tooling/locust.md
  stable_path: docs/05.operations/09-tooling/ops-0062-locust/runbook.md
  artifact_id: runbook-0062
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0062-locust/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/09-tooling/optimization-hardening.md
  stable_path: docs/05.operations/09-tooling/ops-0063-optimization-hardening/runbook.md
  artifact_id: runbook-0063
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0063-optimization-hardening/runbook.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/09-tooling/performance-testing.md
  stable_path: docs/05.operations/09-tooling/ops-0064-performance-testing/runbook.md
  artifact_id: runbook-0064
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0064-performance-testing/runbook.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/09-tooling/registry.md
  stable_path: docs/05.operations/09-tooling/ops-0065-registry/runbook.md
  artifact_id: runbook-0065
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0065-registry/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/09-tooling/sonarqube.md
  stable_path: docs/05.operations/09-tooling/ops-0066-sonarqube/runbook.md
  artifact_id: runbook-0066
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0066-sonarqube/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/09-tooling/syncthing.md
  stable_path: docs/05.operations/09-tooling/ops-0067-syncthing/runbook.md
  artifact_id: runbook-0067
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0067-syncthing/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/09-tooling/terraform.md
  stable_path: docs/05.operations/09-tooling/ops-0068-terraform/runbook.md
  artifact_id: runbook-0068
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0068-terraform/runbook.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/09-tooling/terrakube.md
  stable_path: docs/05.operations/09-tooling/ops-0069-terrakube/runbook.md
  artifact_id: runbook-0069
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/09-tooling/ops-0069-terrakube/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/10-communication/README.md
  stable_path: docs/05.operations/10-communication/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/10-communication/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/10-communication/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/10-communication/mail.md
  stable_path: docs/05.operations/10-communication/ops-0070-mail/runbook.md
  artifact_id: runbook-0070
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/10-communication/ops-0070-mail/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/11-laboratory/README.md
  stable_path: docs/05.operations/11-laboratory/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/11-laboratory/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/11-laboratory/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/11-laboratory/dashboard.md
  stable_path: docs/05.operations/11-laboratory/ops-0071-dashboard/runbook.md
  artifact_id: runbook-0071
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0071-dashboard/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/11-laboratory/dozzle.md
  stable_path: docs/05.operations/11-laboratory/ops-0072-dozzle/runbook.md
  artifact_id: runbook-0072
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0072-dozzle/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/11-laboratory/open-notebook.md
  stable_path: docs/05.operations/11-laboratory/ops-0073-open-notebook/runbook.md
  artifact_id: runbook-0073
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0073-open-notebook/runbook.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/11-laboratory/optimization-hardening.md
  stable_path: docs/05.operations/11-laboratory/ops-0074-optimization-hardening/runbook.md
  artifact_id: runbook-0074
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0074-optimization-hardening/runbook.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/11-laboratory/portainer.md
  stable_path: docs/05.operations/11-laboratory/ops-0075-portainer/runbook.md
  artifact_id: runbook-0075
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0075-portainer/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/11-laboratory/redisinsight.md
  stable_path: docs/05.operations/11-laboratory/ops-0076-redisinsight/runbook.md
  artifact_id: runbook-0076
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/11-laboratory/ops-0076-redisinsight/runbook.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/12-infra-net/README.md
  stable_path: docs/05.operations/12-infra-net/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/12-infra-net/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/12-infra-net/README.md; migrate 4 resolved inbound link(s) before source removal.
- legacy_path: docs/05.operations/runbooks/12-infra-net/standardize-infra-net.md
  stable_path: docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/runbook.md
  artifact_id: runbook-0077
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/05.operations/12-infra-net/ops-0077-standardize-infra-net/runbook.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/05.operations/runbooks/README.md
  stable_path: docs/05.operations/README.md
  artifact_id: null
  action: merge
  replacement: docs/05.operations/README.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Merge duplicate baseline untyped source into canonical target docs/05.operations/README.md; migrate 30 resolved inbound link(s) before source removal.
- legacy_path: docs/90.references/README.md
  stable_path: docs/90.references/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 36 resolved inbound link(s).
- legacy_path: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/README.md
  stable_path: docs/90.references/audits/ref-0001-readme.md
  artifact_id: ref-0001
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0001-readme.md; migrate 16 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/automation-coverage-map.md
  stable_path: docs/90.references/audits/ref-0002-automation-coverage-map.md
  artifact_id: ref-0002
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0002-automation-coverage-map.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/ci-qa-parser-graphify-decision.md
  stable_path: docs/90.references/audits/ref-0003-ci-qa-parser-graphify-decision.md
  artifact_id: ref-0003
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0003-ci-qa-parser-graphify-decision.md; migrate 2 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/contract-governance-map.md
  stable_path: docs/90.references/audits/ref-0004-contract-governance-map.md
  artifact_id: ref-0004
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0004-contract-governance-map.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-inventory.md
  stable_path: docs/90.references/audits/ref-0005-frontmatter-inventory.md
  artifact_id: ref-0005
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0005-frontmatter-inventory.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/frontmatter-routing-profile.md
  stable_path: docs/90.references/audits/ref-0006-frontmatter-routing-profile.md
  artifact_id: ref-0006
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0006-frontmatter-routing-profile.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md
  stable_path: docs/90.references/audits/ref-0007-gap-register.md
  artifact_id: ref-0007
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0007-gap-register.md; migrate 18 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/historical-evidence-preservation.md
  stable_path: docs/90.references/audits/ref-0008-historical-evidence-preservation.md
  artifact_id: ref-0008
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0008-historical-evidence-preservation.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/readme-profile-inventory.md
  stable_path: docs/90.references/audits/ref-0009-readme-profile-inventory.md
  artifact_id: ref-0009
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0009-readme-profile-inventory.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/section-profile-inventory.md
  stable_path: docs/90.references/audits/ref-0010-section-profile-inventory.md
  artifact_id: ref-0010
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0010-section-profile-inventory.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-03-workspace-document-contract-audit-pack/template-application-gaps.md
  stable_path: docs/90.references/audits/ref-0011-template-application-gaps.md
  artifact_id: ref-0011
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0011-template-application-gaps.md; migrate 6 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/README.md
  stable_path: docs/90.references/audits/ref-0012-readme.md
  artifact_id: ref-0012
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0012-readme.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/ci-qa-formatting-contract.md
  stable_path: docs/90.references/audits/ref-0013-ci-qa-formatting-contract.md
  artifact_id: ref-0013
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0013-ci-qa-formatting-contract.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/frontmatter-profile-inventory.md
  stable_path: docs/90.references/audits/ref-0014-frontmatter-profile-inventory.md
  artifact_id: ref-0014
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0014-frontmatter-profile-inventory.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/operations-bucket-restructure.md
  stable_path: docs/90.references/audits/ref-0015-operations-bucket-restructure.md
  artifact_id: ref-0015
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0015-operations-bucket-restructure.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/restructure-gap-register.md
  stable_path: docs/90.references/audits/ref-0016-restructure-gap-register.md
  artifact_id: ref-0016
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0016-restructure-gap-register.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/sdlc-spec-archive-candidates.md
  stable_path: docs/90.references/audits/ref-0017-sdlc-spec-archive-candidates.md
  artifact_id: ref-0017
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0017-sdlc-spec-archive-candidates.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-04-document-restructure-audit-contract-archive/template-contract-drift.md
  stable_path: docs/90.references/audits/ref-0018-template-contract-drift.md
  artifact_id: ref-0018
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0018-template-contract-drift.md; migrate 7 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/README.md
  stable_path: docs/90.references/audits/ref-0019-readme.md
  artifact_id: ref-0019
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0019-readme.md; migrate 89 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/agent-instructions-catalog-vibe-models.md
  stable_path: docs/90.references/audits/ref-0020-agent-instructions-catalog-vibe-models.md
  artifact_id: ref-0020
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0020-agent-instructions-catalog-vibe-models.md; migrate 12 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md
  stable_path: docs/90.references/audits/ref-0021-automation-candidates.md
  artifact_id: ref-0021
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0021-automation-candidates.md; migrate 70 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/compose-infrastructure-operations-readiness.md
  stable_path: docs/90.references/audits/ref-0022-compose-infrastructure-operations-readiness.md
  artifact_id: ref-0022
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0022-compose-infrastructure-operations-readiness.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-semantic-inventory.md
  stable_path: docs/90.references/audits/ref-0023-frontmatter-semantic-inventory.md
  artifact_id: ref-0023
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0023-frontmatter-semantic-inventory.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/frontmatter-template-readme-implementation.md
  stable_path: docs/90.references/audits/ref-0024-frontmatter-template-readme-implementation.md
  artifact_id: ref-0024
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0024-frontmatter-template-readme-implementation.md; migrate 12 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/harness-engineering-implementation.md
  stable_path: docs/90.references/audits/ref-0025-harness-engineering-implementation.md
  artifact_id: ref-0025
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0025-harness-engineering-implementation.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md
  stable_path: docs/90.references/audits/ref-0026-implementation-overview.md
  artifact_id: ref-0026
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0026-implementation-overview.md; migrate 16 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/loop-engineering-implementation.md
  stable_path: docs/90.references/audits/ref-0027-loop-engineering-implementation.md
  artifact_id: ref-0027
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0027-loop-engineering-implementation.md; migrate 12 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/provider-harness-loop-implementation.md
  stable_path: docs/90.references/audits/ref-0028-provider-harness-loop-implementation.md
  artifact_id: ref-0028
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0028-provider-harness-loop-implementation.md; migrate 14 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-document-contracts-implementation.md
  stable_path: docs/90.references/audits/ref-0029-sdlc-document-contracts-implementation.md
  artifact_id: ref-0029
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0029-sdlc-document-contracts-implementation.md; migrate 13 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/sdlc-quality-formatting-implementation.md
  stable_path: docs/90.references/audits/ref-0030-sdlc-quality-formatting-implementation.md
  artifact_id: ref-0030
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0030-sdlc-quality-formatting-implementation.md; migrate 19 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/security-framework-maturity.md
  stable_path: docs/90.references/audits/ref-0031-security-framework-maturity.md
  artifact_id: ref-0031
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0031-security-framework-maturity.md; migrate 26 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/workspace-rules-environment-implementation.md
  stable_path: docs/90.references/audits/ref-0032-workspace-rules-environment-implementation.md
  artifact_id: ref-0032
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/audits/ref-0032-workspace-rules-environment-implementation.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/README.md
  stable_path: docs/90.references/audits/ref-0033-readme.md
  artifact_id: ref-0033
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline superseded source to stable typed target docs/90.references/audits/ref-0033-readme.md; migrate 11 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/agent-catalog-audit.md
  stable_path: docs/90.references/audits/ref-0034-agent-catalog-audit.md
  artifact_id: ref-0034
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline superseded source to stable typed target docs/90.references/audits/ref-0034-agent-catalog-audit.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/automation-candidates.md
  stable_path: docs/90.references/audits/ref-0035-automation-candidates.md
  artifact_id: ref-0035
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline superseded source to stable typed target docs/90.references/audits/ref-0035-automation-candidates.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/harness-loop-audit.md
  stable_path: docs/90.references/audits/ref-0036-harness-loop-audit.md
  artifact_id: ref-0036
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline superseded source to stable typed target docs/90.references/audits/ref-0036-harness-loop-audit.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/implementation-overview.md
  stable_path: docs/90.references/audits/ref-0037-implementation-overview.md
  artifact_id: ref-0037
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline superseded source to stable typed target docs/90.references/audits/ref-0037-implementation-overview.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/2026-07-07-agentic-engineering-implementation-audit-pack-update/sdlc-qa-security-audit.md
  stable_path: docs/90.references/audits/ref-0038-sdlc-qa-security-audit.md
  artifact_id: ref-0038
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline superseded source to stable typed target docs/90.references/audits/ref-0038-sdlc-qa-security-audit.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/90.references/audits/README.md
  stable_path: docs/90.references/audits/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 18 resolved inbound link(s).
- legacy_path: docs/90.references/data/README.md
  stable_path: docs/90.references/data/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 13 resolved inbound link(s).
- legacy_path: docs/90.references/data/docker/README.md
  stable_path: docs/90.references/data/docker/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 10 resolved inbound link(s).
- legacy_path: docs/90.references/data/docker/compose-profile-service-coverage.md
  stable_path: docs/90.references/data/docker/ref-0059-compose-profile-service-coverage.md
  artifact_id: ref-0059
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 17 resolved inbound link(s).
- legacy_path: docs/90.references/data/docker/image-version-interpretation.md
  stable_path: docs/90.references/data/docker/ref-0060-image-version-interpretation.md
  artifact_id: ref-0060
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 8 resolved inbound link(s).
- legacy_path: docs/90.references/data/docker/tech-stack-version-provenance.md
  stable_path: docs/90.references/data/docker/ref-0061-tech-stack-version-provenance.md
  artifact_id: ref-0061
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 14 resolved inbound link(s).
- legacy_path: docs/90.references/data/glossary/README.md
  stable_path: docs/90.references/data/glossary/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 5 resolved inbound link(s).
- legacy_path: docs/90.references/data/glossary/stable-reference-terms.md
  stable_path: docs/90.references/data/glossary/ref-0062-stable-reference-terms.md
  artifact_id: ref-0062
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 9 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/README.md
  stable_path: docs/90.references/data/governance/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 8 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/agent-governance-retirement-ledger.yaml
  stable_path: docs/90.references/data/governance/ref-0063-agent-governance-retirement-ledger.yaml
  artifact_id: ref-0063
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 2 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/agent-output-eval-fixtures.md
  stable_path: docs/90.references/data/governance/ref-0064-agent-output-eval-fixtures.md
  artifact_id: ref-0064
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 23 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/audit-implementation-matrix.md
  stable_path: docs/90.references/data/governance/ref-0065-audit-implementation-matrix.md
  artifact_id: ref-0065
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 15 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/document-corpus-lifecycle/README.md
  stable_path: docs/90.references/data/governance/document-corpus-lifecycle/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 4 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/document-corpus-lifecycle/foundation-summary.md
  stable_path: docs/90.references/data/governance/document-corpus-lifecycle/ref-0066-foundation-summary.md
  artifact_id: ref-0066
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 4 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/document-corpus-lifecycle/foundation.yaml
  stable_path: docs/90.references/data/governance/document-corpus-lifecycle/ref-0067-foundation.yaml
  artifact_id: ref-0067
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 4 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence-summary.md
  stable_path: docs/90.references/data/governance/document-corpus-lifecycle/ref-0068-target-surface-convergence-summary.md
  artifact_id: ref-0068
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 1 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml
  stable_path: docs/90.references/data/governance/document-corpus-lifecycle/ref-0069-target-surface-convergence.yaml
  artifact_id: ref-0069
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 3 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/gap-to-stage-routing.md
  stable_path: docs/90.references/data/governance/ref-0070-gap-to-stage-routing.md
  artifact_id: ref-0070
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 10 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/github-actions-control-plane-observation.yaml
  stable_path: docs/90.references/data/governance/ref-0071-github-actions-control-plane-observation.yaml
  artifact_id: ref-0071
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 9 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/provider-hook-parity-matrix.md
  stable_path: docs/90.references/data/governance/ref-0072-provider-hook-parity-matrix.md
  artifact_id: ref-0072
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 11 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/target-surface-delta-manifest.yaml
  stable_path: docs/90.references/data/governance/ref-0073-target-surface-delta-manifest.yaml
  artifact_id: ref-0073
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 2 resolved inbound link(s).
- legacy_path: docs/90.references/data/governance/target-surface-delta-summary.md
  stable_path: docs/90.references/data/governance/ref-0074-target-surface-delta-summary.md
  artifact_id: ref-0074
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 2 resolved inbound link(s).
- legacy_path: docs/90.references/data/hads/README.md
  stable_path: docs/90.references/data/hads/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 4 resolved inbound link(s).
- legacy_path: docs/90.references/data/hads/profile.md
  stable_path: docs/90.references/data/hads/ref-0075-profile.md
  artifact_id: ref-0075
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 6 resolved inbound link(s).
- legacy_path: docs/90.references/data/knowledge/README.md
  stable_path: docs/90.references/data/knowledge/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 4 resolved inbound link(s).
- legacy_path: docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md
  stable_path: docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md
  artifact_id: ref-0076
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 11 resolved inbound link(s).
- legacy_path: docs/90.references/data/kubernetes/README.md
  stable_path: docs/90.references/data/kubernetes/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 4 resolved inbound link(s).
- legacy_path: docs/90.references/data/kubernetes/docker-compose-to-k3s-migration.md
  stable_path: docs/90.references/data/kubernetes/ref-0077-docker-compose-to-k3s-migration.md
  artifact_id: ref-0077
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 5 resolved inbound link(s).
- legacy_path: docs/90.references/data/security/README.md
  stable_path: docs/90.references/data/security/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 5 resolved inbound link(s).
- legacy_path: docs/90.references/data/security/security-automation-readiness.md
  stable_path: docs/90.references/data/security/ref-0078-security-automation-readiness.md
  artifact_id: ref-0078
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 23 resolved inbound link(s).
- legacy_path: docs/90.references/data/security/supply-chain-sample-service.md
  stable_path: docs/90.references/data/security/ref-0079-supply-chain-sample-service.md
  artifact_id: ref-0079
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 3 resolved inbound link(s).
- legacy_path: docs/90.references/learning/README.md
  stable_path: docs/90.references/learning/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 8 resolved inbound link(s).
- legacy_path: docs/90.references/learning/roadmap-v1.md
  stable_path: docs/90.references/learning/ref-0080-roadmap-v1.md
  artifact_id: ref-0080
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline superseded source in place for the approved target profile; preserve 3 resolved inbound link(s).
- legacy_path: docs/90.references/learning/roadmap.md
  stable_path: docs/90.references/learning/ref-0081-roadmap.md
  artifact_id: ref-0081
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 6 resolved inbound link(s).
- legacy_path: docs/90.references/llm-wiki/README.md
  stable_path: docs/90.references/llm-wiki/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 18 resolved inbound link(s).
- legacy_path: docs/90.references/llm-wiki/llm-wiki-index.md
  stable_path: docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md
  artifact_id: ref-0082
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 16 resolved inbound link(s).
- legacy_path: docs/90.references/llm-wiki/repository-map.md
  stable_path: docs/90.references/llm-wiki/ref-0083-repository-map.md
  artifact_id: ref-0083
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 10 resolved inbound link(s).
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/README.md
  stable_path: docs/90.references/research/ref-0039-readme.md
  artifact_id: ref-0039
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0039-readme.md; migrate 69 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-instructions-vibe-coding.md
  stable_path: docs/90.references/research/ref-0040-agent-instructions-vibe-coding.md
  artifact_id: ref-0040
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0040-agent-instructions-vibe-coding.md; migrate 9 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md
  stable_path: docs/90.references/research/ref-0041-agent-model-selection.md
  artifact_id: ref-0041
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0041-agent-model-selection.md; migrate 10 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md
  stable_path: docs/90.references/research/ref-0042-ai-agent-catalogs.md
  artifact_id: ref-0042
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0042-ai-agent-catalogs.md; migrate 14 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md
  stable_path: docs/90.references/research/ref-0043-automation-pipeline-workflow.md
  artifact_id: ref-0043
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0043-automation-pipeline-workflow.md; migrate 16 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md
  stable_path: docs/90.references/research/ref-0044-docker-compose-infrastructure.md
  artifact_id: ref-0044
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0044-docker-compose-infrastructure.md; migrate 19 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/document-metadata-lifecycle.md
  stable_path: docs/90.references/research/ref-0045-document-metadata-lifecycle.md
  artifact_id: ref-0045
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0045-document-metadata-lifecycle.md; migrate 12 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/documentation-architecture.md
  stable_path: docs/90.references/research/ref-0046-documentation-architecture.md
  artifact_id: ref-0046
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0046-documentation-architecture.md; migrate 8 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md
  stable_path: docs/90.references/research/ref-0047-harness-engineering.md
  artifact_id: ref-0047
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0047-harness-engineering.md; migrate 20 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/llm-wiki-system.md
  stable_path: docs/90.references/research/ref-0048-llm-wiki-system.md
  artifact_id: ref-0048
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0048-llm-wiki-system.md; migrate 5 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md
  stable_path: docs/90.references/research/ref-0049-loop-engineering.md
  artifact_id: ref-0049
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0049-loop-engineering.md; migrate 21 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/memory-hierarchy.md
  stable_path: docs/90.references/research/ref-0050-memory-hierarchy.md
  artifact_id: ref-0050
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0050-memory-hierarchy.md; migrate 4 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md
  stable_path: docs/90.references/research/ref-0051-provider-implementation-comparison.md
  artifact_id: ref-0051
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0051-provider-implementation-comparison.md; migrate 23 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md
  stable_path: docs/90.references/research/ref-0052-provider-model-landscape.md
  artifact_id: ref-0052
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0052-provider-model-landscape.md; migrate 12 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md
  stable_path: docs/90.references/research/ref-0053-quality-ci-formatting.md
  artifact_id: ref-0053
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0053-quality-ci-formatting.md; migrate 29 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/scope-application-matrix.md
  stable_path: docs/90.references/research/ref-0054-scope-application-matrix.md
  artifact_id: ref-0054
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0054-scope-application-matrix.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md
  stable_path: docs/90.references/research/ref-0055-sdlc-document-roles.md
  artifact_id: ref-0055
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0055-sdlc-document-roles.md; migrate 15 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md
  stable_path: docs/90.references/research/ref-0056-security-governance.md
  artifact_id: ref-0056
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0056-security-governance.md; migrate 26 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md
  stable_path: docs/90.references/research/ref-0057-spec-driven-sdlc.md
  artifact_id: ref-0057
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0057-spec-driven-sdlc.md; migrate 19 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md
  stable_path: docs/90.references/research/ref-0058-workspace-baseline.md
  artifact_id: ref-0058
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline active source to stable typed target docs/90.references/research/ref-0058-workspace-baseline.md; migrate 30 resolved inbound link(s) with it.
- legacy_path: docs/90.references/research/README.md
  stable_path: docs/90.references/research/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline active source in place for the approved target profile; preserve 28 resolved inbound link(s).
- legacy_path: docs/98.archive/03.specs/099-template-system-numbered-sdlc-paths/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0099-template-system-numbered-sdlc-paths.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0099-template-system-numbered-sdlc-paths.md.
- legacy_path: docs/98.archive/03.specs/099-template-system-numbered-sdlc-paths/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0099-template-system-numbered-sdlc-paths.md
  artifact_id: spec-0099
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0099-template-system-numbered-sdlc-paths.md; remove 10 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/100-template-system-contract-standardization/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0100-template-system-contract-standardization.md
  artifact_id: spec-0100
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0100-template-system-contract-standardization.md; remove 14 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/101-template-system-reorganization/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0101-template-system-reorganization.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 4 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0101-template-system-reorganization.md.
- legacy_path: docs/98.archive/03.specs/101-template-system-reorganization/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0101-template-system-reorganization.md
  artifact_id: spec-0101
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0101-template-system-reorganization.md; remove 9 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/104-agentic-research-pack-refresh/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0104-agentic-research-pack-refresh.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 3 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0104-agentic-research-pack-refresh.md.
- legacy_path: docs/98.archive/03.specs/104-agentic-research-pack-refresh/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0104-agentic-research-pack-refresh.md
  artifact_id: spec-0104
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0104-agentic-research-pack-refresh.md; remove 15 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/106-workspace-support-surface-contract/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0106-workspace-support-surface-contract.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 3 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0106-workspace-support-surface-contract.md.
- legacy_path: docs/98.archive/03.specs/106-workspace-support-surface-contract/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0106-workspace-support-surface-contract.md
  artifact_id: spec-0106
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0106-workspace-support-surface-contract.md; remove 13 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/107-provider-semantic-parity-validator/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0107-provider-semantic-parity-validator.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0107-provider-semantic-parity-validator.md.
- legacy_path: docs/98.archive/03.specs/107-provider-semantic-parity-validator/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0107-provider-semantic-parity-validator.md
  artifact_id: spec-0107
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0107-provider-semantic-parity-validator.md; remove 8 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/108-compose-profile-service-coverage-snapshot/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0108-compose-profile-service-coverage-snapshot.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0108-compose-profile-service-coverage-snapshot.md.
- legacy_path: docs/98.archive/03.specs/108-compose-profile-service-coverage-snapshot/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0108-compose-profile-service-coverage-snapshot.md
  artifact_id: spec-0108
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0108-compose-profile-service-coverage-snapshot.md; remove 7 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/109-gap-routing-recommendation/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0109-gap-routing-recommendation.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0109-gap-routing-recommendation.md.
- legacy_path: docs/98.archive/03.specs/109-gap-routing-recommendation/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0109-gap-routing-recommendation.md
  artifact_id: spec-0109
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0109-gap-routing-recommendation.md; remove 7 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/110-agent-output-eval-fixtures/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0110-agent-output-eval-fixtures.md
  artifact_id: spec-0110
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0110-agent-output-eval-fixtures.md; remove 6 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/111-qa-gate-recommendation-ci-summary/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0111-qa-gate-recommendation-ci-summary.md
  artifact_id: spec-0111
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0111-qa-gate-recommendation-ci-summary.md; remove 5 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/112-audit-pack-coverage-report/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0112-audit-pack-coverage-report.md
  artifact_id: spec-0112
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0112-audit-pack-coverage-report.md; remove 5 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/113-llm-wiki-stage-category-coverage/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0113-llm-wiki-stage-category-coverage.md
  artifact_id: spec-0113
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0113-llm-wiki-stage-category-coverage.md; remove 5 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/114-tech-stack-version-provenance/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0114-tech-stack-version-provenance.md
  artifact_id: spec-0114
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0114-tech-stack-version-provenance.md; remove 5 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/115-provider-hook-parity-matrix/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0115-provider-hook-parity-matrix.md
  artifact_id: spec-0115
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0115-provider-hook-parity-matrix.md; remove 6 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/116-agent-output-eval-runner/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0116-agent-output-eval-runner.md
  artifact_id: spec-0116
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0116-agent-output-eval-runner.md; remove 13 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/117-security-automation-readiness-snapshot/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0117-security-automation-readiness-snapshot.md
  artifact_id: spec-0117
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0117-security-automation-readiness-snapshot.md; remove 5 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/118-audit-implementation-matrix-snapshot/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0118-audit-implementation-matrix-snapshot.md
  artifact_id: spec-0118
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0118-audit-implementation-matrix-snapshot.md; remove 6 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/119-sdlc-document-contract-corpus-normalization/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0119-sdlc-document-contract-corpus-normalization.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 3 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0119-sdlc-document-contract-corpus-normalization.md.
- legacy_path: docs/98.archive/03.specs/119-sdlc-document-contract-corpus-normalization/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0119-sdlc-document-contract-corpus-normalization.md
  artifact_id: spec-0119
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0119-sdlc-document-contract-corpus-normalization.md; remove 6 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/120-agent-output-eval-ci-gate/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0120-agent-output-eval-ci-gate.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0120-agent-output-eval-ci-gate.md.
- legacy_path: docs/98.archive/03.specs/120-agent-output-eval-ci-gate/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0120-agent-output-eval-ci-gate.md
  artifact_id: spec-0120
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0120-agent-output-eval-ci-gate.md; remove 7 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/121-dependency-vulnerability-audit-gate/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0121-dependency-vulnerability-audit-gate.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0121-dependency-vulnerability-audit-gate.md.
- legacy_path: docs/98.archive/03.specs/121-dependency-vulnerability-audit-gate/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0121-dependency-vulnerability-audit-gate.md
  artifact_id: spec-0121
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0121-dependency-vulnerability-audit-gate.md; remove 7 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/122-agentic-research-pack-consolidation/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0122-agentic-research-pack-consolidation.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 3 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0122-agentic-research-pack-consolidation.md.
- legacy_path: docs/98.archive/03.specs/122-agentic-research-pack-consolidation/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0122-agentic-research-pack-consolidation.md
  artifact_id: spec-0122
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0122-agentic-research-pack-consolidation.md; remove 12 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/123-agentic-engineering-audit-remediation/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/03.specs/spec-0123-agentic-engineering-audit-remediation/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 4 resolved inbound link(s) to docs/03.specs/spec-0123-agentic-engineering-audit-remediation/spec.md.
- legacy_path: docs/98.archive/03.specs/123-agentic-engineering-audit-remediation/spec.md
  stable_path: docs/03.specs/spec-0123-agentic-engineering-audit-remediation/spec.md
  artifact_id: spec-0123
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Restore current capability Spec 0123 to Stage 03; an active Task or tracked validator/test still consumes its contract.
- legacy_path: docs/98.archive/03.specs/124-compose-runtime-readiness-remediation/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0124-compose-runtime-readiness-remediation.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0124-compose-runtime-readiness-remediation.md.
- legacy_path: docs/98.archive/03.specs/124-compose-runtime-readiness-remediation/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0124-compose-runtime-readiness-remediation.md
  artifact_id: spec-0124
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0124-compose-runtime-readiness-remediation.md; remove 21 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/125-infrastructure-operations-readiness-remediation/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0125-infrastructure-operations-readiness-remediation.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0125-infrastructure-operations-readiness-remediation.md.
- legacy_path: docs/98.archive/03.specs/125-infrastructure-operations-readiness-remediation/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0125-infrastructure-operations-readiness-remediation.md
  artifact_id: spec-0125
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0125-infrastructure-operations-readiness-remediation.md; remove 25 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/126-security-supply-chain-remediation/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0126-security-supply-chain-remediation.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0126-security-supply-chain-remediation.md.
- legacy_path: docs/98.archive/03.specs/126-security-supply-chain-remediation/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0126-security-supply-chain-remediation.md
  artifact_id: spec-0126
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0126-security-supply-chain-remediation.md; remove 27 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/127-deployment-release-engineering-remediation/README.md
  stable_path: null
  artifact_id: null
  action: delete
  replacement: docs/98.archive/tombstones/03.specs/spec-0127-deployment-release-engineering-remediation.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Delete redundant baseline untyped index after its typed owner is established; redirect 2 resolved inbound link(s) to docs/98.archive/tombstones/03.specs/spec-0127-deployment-release-engineering-remediation.md.
- legacy_path: docs/98.archive/03.specs/127-deployment-release-engineering-remediation/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0127-deployment-release-engineering-remediation.md
  artifact_id: spec-0127
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0127-deployment-release-engineering-remediation.md; remove 24 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/128-agentic-audit-harness-consolidation/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0128-agentic-audit-harness-consolidation.md
  artifact_id: spec-0128
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0128-agentic-audit-harness-consolidation.md; remove 8 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/129-document-contract-canonicalization/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0129-document-contract-canonicalization.md
  artifact_id: spec-0129
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0129-document-contract-canonicalization.md; remove 14 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/130-template-contract-system-canonicalization/spec.md
  stable_path: docs/98.archive/tombstones/03.specs/spec-0130-template-contract-system-canonicalization.md
  artifact_id: spec-0130
  action: archive
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/03.specs/spec-0130-template-contract-system-canonicalization.md; remove 9 resolved inbound archive link(s); no active replacement is declared for this retired capability.
- legacy_path: docs/98.archive/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md
  stable_path: docs/03.specs/spec-0131-document-corpus-lifecycle-migration-foundation/spec.md
  artifact_id: spec-0131
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Restore current capability Spec 0131 to Stage 03; an active Task or tracked validator/test still consumes its contract.
- legacy_path: docs/98.archive/03.specs/132-agent-governance-harness-convergence/spec.md
  stable_path: docs/03.specs/spec-0132-agent-governance-harness-convergence/spec.md
  artifact_id: spec-0132
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Restore current capability Spec 0132 to Stage 03; an active Task or tracked validator/test still consumes its contract.
- legacy_path: docs/98.archive/03.specs/133-target-surface-contract-convergence/spec.md
  stable_path: docs/03.specs/spec-0133-target-surface-contract-convergence/spec.md
  artifact_id: spec-0133
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Restore current capability Spec 0133 to Stage 03; an active Task or tracked validator/test still consumes its contract.
- legacy_path: docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md
  stable_path: docs/98.archive/changes/chg-0017-ai-governance-reorg/plan.md
  artifact_id: plan-0017
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline archived source to stable typed target docs/98.archive/changes/chg-0017-ai-governance-reorg/plan.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md
  stable_path: docs/98.archive/changes/chg-0018-standardizing-agent-governance/plan.md
  artifact_id: plan-0018
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline archived source to stable typed target docs/98.archive/changes/chg-0018-standardizing-agent-governance/plan.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md
  stable_path: docs/98.archive/changes/chg-0019-agent-governance-phase1-diagnostic/plan.md
  artifact_id: plan-0019
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline archived source to stable typed target docs/98.archive/changes/chg-0019-agent-governance-phase1-diagnostic/plan.md; migrate 3 resolved inbound link(s) with it.
- legacy_path: docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md
  stable_path: docs/98.archive/changes/chg-0020-agent-governance-phase2-alignment/plan.md
  artifact_id: plan-0020
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline archived source to stable typed target docs/98.archive/changes/chg-0020-agent-governance-phase2-alignment/plan.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/98.archive/04.execution/tasks/2026-05-30-standardizing-agent-governance.md
  stable_path: docs/98.archive/changes/chg-0021-standardizing-agent-governance/task.md
  artifact_id: task-0021-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline archived source to stable typed target docs/98.archive/changes/chg-0021-standardizing-agent-governance/task.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase1-diagnostic.md
  stable_path: docs/98.archive/changes/chg-0022-agent-governance-phase1-diagnostic/task.md
  artifact_id: task-0022-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline archived source to stable typed target docs/98.archive/changes/chg-0022-agent-governance-phase1-diagnostic/task.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-implementation.md
  stable_path: docs/98.archive/changes/chg-0023-agent-governance-phase3-implementation/task.md
  artifact_id: task-0023-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline archived source to stable typed target docs/98.archive/changes/chg-0023-agent-governance-phase3-implementation/task.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-stage01-02-continuation.md
  stable_path: docs/98.archive/changes/chg-0024-agent-governance-phase3-stage01-02-continuation/task.md
  artifact_id: task-0024-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline archived source to stable typed target docs/98.archive/changes/chg-0024-agent-governance-phase3-stage01-02-continuation/task.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-strategy-integration.md
  stable_path: docs/98.archive/changes/chg-0025-agent-governance-phase3-strategy-integration/task.md
  artifact_id: task-0025-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline archived source to stable typed target docs/98.archive/changes/chg-0025-agent-governance-phase3-strategy-integration/task.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase4-closure.md
  stable_path: docs/98.archive/changes/chg-0026-agent-governance-phase4-closure/task.md
  artifact_id: task-0026-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline archived source to stable typed target docs/98.archive/changes/chg-0026-agent-governance-phase4-closure/task.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-stage01-02-alignment.md
  stable_path: docs/98.archive/changes/chg-0027-agent-governance-stage01-02-alignment/task.md
  artifact_id: task-0027-01
  action: move
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Move baseline archived source to stable typed target docs/98.archive/changes/chg-0027-agent-governance-stage01-02-alignment/task.md; migrate 1 resolved inbound link(s) with it.
- legacy_path: docs/98.archive/05.operations/guides/03-security/01.setup.md
  stable_path: docs/98.archive/tombstones/05.operations/ref-0028-01-setup.md
  artifact_id: ref-0028
  action: archive
  replacement: docs/05.operations/03-security/ops-0016-vault/guide.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline source as typed provenance; both the baseline archive index and tombstone declare docs/05.operations/guides/03-security/vault.md, translated through its ledger row to active target docs/05.operations/03-security/ops-0016-vault/guide.md; remove 1 resolved inbound archive link(s).
- legacy_path: docs/98.archive/05.operations/guides/05-messaging/ksql-streaming.md
  stable_path: docs/98.archive/tombstones/05.operations/ref-0029-ksql-streaming.md
  artifact_id: ref-0029
  action: archive
  replacement: docs/05.operations/04-data/ops-0018-analytics-ksqldb/guide.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline source as typed provenance; both the baseline archive index and tombstone declare docs/05.operations/guides/04-data/analytics/ksqldb.md, translated through its ledger row to active target docs/05.operations/04-data/ops-0018-analytics-ksqldb/guide.md; remove 1 resolved inbound archive link(s).
- legacy_path: docs/98.archive/05.operations/guides/07-workflow/01.airflow-dag-dev.md
  stable_path: docs/98.archive/tombstones/05.operations/ref-0030-01-airflow-dag-dev.md
  artifact_id: ref-0030
  action: archive
  replacement: docs/05.operations/07-workflow/ops-0051-airflow-dag-basics/guide.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/05.operations/ref-0030-01-airflow-dag-dev.md; remove 1 resolved inbound archive link(s); redirect consumers to active replacement docs/05.operations/07-workflow/ops-0051-airflow-dag-basics/guide.md.
- legacy_path: docs/98.archive/05.operations/guides/07-workflow/airbyte.md
  stable_path: docs/98.archive/tombstones/05.operations/ref-0031-airbyte.md
  artifact_id: ref-0031
  action: archive
  replacement: docs/03.specs/spec-0008-workflow/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/05.operations/ref-0031-airbyte.md; remove 1 resolved inbound archive link(s); redirect consumers to active replacement docs/03.specs/spec-0008-workflow/spec.md.
- legacy_path: docs/98.archive/05.operations/guides/08-ai/01.llm-inference.md
  stable_path: docs/98.archive/tombstones/05.operations/ref-0032-01-llm-inference.md
  artifact_id: ref-0032
  action: archive
  replacement: docs/05.operations/08-ai/ops-0056-ollama/guide.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline source as typed provenance; both the baseline archive index and tombstone declare docs/05.operations/guides/08-ai/ollama.md, translated through its ledger row to active target docs/05.operations/08-ai/ops-0056-ollama/guide.md; remove 1 resolved inbound archive link(s).
- legacy_path: docs/98.archive/05.operations/guides/08-ai/local-llm-setup.md
  stable_path: docs/98.archive/tombstones/05.operations/ref-0033-local-llm-setup.md
  artifact_id: ref-0033
  action: archive
  replacement: docs/05.operations/08-ai/ops-0056-ollama/guide.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline source as typed provenance; both the baseline archive index and tombstone declare docs/05.operations/guides/08-ai/ollama.md, translated through its ledger row to active target docs/05.operations/08-ai/ops-0056-ollama/guide.md; remove 1 resolved inbound archive link(s).
- legacy_path: docs/98.archive/05.operations/guides/09-tooling/01.iac-automation.md
  stable_path: docs/98.archive/tombstones/05.operations/ref-0034-01-iac-automation.md
  artifact_id: ref-0034
  action: archive
  replacement: docs/05.operations/09-tooling/ops-0069-terrakube/guide.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline source as typed provenance; the baseline archive index and tombstone declare both docs/05.operations/guides/09-tooling/terrakube.md and docs/05.operations/guides/09-tooling/terraform.md in that order. Preserve the primary declaration as active target docs/05.operations/09-tooling/ops-0069-terrakube/guide.md; merge the secondary declaration into active target docs/05.operations/09-tooling/ops-0068-terraform/guide.md; remove 1 resolved inbound archive link(s).
- legacy_path: docs/98.archive/05.operations/policies/07-workflow/airbyte.md
  stable_path: docs/98.archive/tombstones/05.operations/ref-0035-airbyte.md
  artifact_id: ref-0035
  action: archive
  replacement: docs/03.specs/spec-0008-workflow/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/05.operations/ref-0035-airbyte.md; remove 1 resolved inbound archive link(s); redirect consumers to active replacement docs/03.specs/spec-0008-workflow/spec.md.
- legacy_path: docs/98.archive/05.operations/runbooks/07-workflow/airbyte.md
  stable_path: docs/98.archive/tombstones/05.operations/ref-0036-airbyte.md
  artifact_id: ref-0036
  action: archive
  replacement: docs/03.specs/spec-0008-workflow/spec.md
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Archive terminal baseline archived source as typed provenance at docs/98.archive/tombstones/05.operations/ref-0036-airbyte.md; remove 1 resolved inbound archive link(s); redirect consumers to active replacement docs/03.specs/spec-0008-workflow/spec.md.
- legacy_path: docs/98.archive/README.md
  stable_path: docs/98.archive/README.md
  artifact_id: null
  action: rewrite
  replacement: null
  source_commit: 232effd9a5e00907bdbe30efc6665023fb2d07f4
  reason: Rewrite baseline untyped source in place for the approved target profile; preserve 68 resolved inbound link(s).
```

## Execution Evidence

| Wave | Mapping state | Git provenance | Consumer state | Commit |
| :-- | :-- | :-- | :-- | :-- |
| Task 4 — Stage 01/02 | 76 moves executed: 25 PRDs, 25 Architecture Descriptions, 25 ADRs, and the Description README; the original README rewrite-row defect is corrected above | Git rename index preserves every source-to-target relation | Tracked inbound links migrated to stable targets; final validation evidence is recorded in the Task 4 report | pending root-controller commit |
| Task 5 — Stage 03/04 boundary | Executed all 337 approved rows in the bounded wave: 262 moves, 28 archives, 8 merges, 38 direct deletes, and 1 README rewrite. The result contains 31 current Specs, 7 current Plan/Task documents, 137 completed change packets with 223 physical documents, and 28 concise Spec tombstones. The authorized cycle-breaking exception executed both frozen rows that converge on `policy-0006`: the policy move and the Stage 04 roadmap merge. | All 290 move/archive sources resolve at their recorded `source_commit`; all 290 resolve to blobs, with 290 unique source blobs. Moved change evidence and tombstones retain the recorded commit/blob provenance. | The atomic inbound migration rewrote 2,103 links in 494 files and converted 612 active-to-archive links to non-link evidence labels. Merge sources and all 38 capability child READMEs are absent; Stage 04 is absent. Final validation evidence is recorded in the Task 5 report. | pending root-controller commit |
| Task 6A — Operations 00–03 | Completed the frozen 41-row slice: `33` move rows and `8` README merge rows. The Task 5 `policy-0006` exception was already at target; Task 6A's earlier README move plus the controller's remaining `31` Git moves reconciled every move disposition. The controller then removed all eight merge sources with exact `git rm -f` after navigation merge verification. | Every domain-first target is present, all eight merge sources and all 00–03 role roots are absent, and no collision or emulated copy/delete was used. Before removal the controller saved the eight modified merge sources to `/tmp/task6a-readme-merge-sources.OWvDIE.tar` (8 entries; SHA-256 `086d3937903f9ed3de070fe1d679365b848dc7f79eefe9e03895fbaf4a7604ef`). | RED `4` tests/`30` failures then bounded taxonomy GREEN `5/5`; final staged changed metadata `selected=108 violations=0`, contracts `0`; traceability `46` pairs/`0` failures; alignment `2,498` links/`0` failures; taxonomy `14/14`, manifest `23/23`, provider drift `0`, and both diff checks pass. The active inbound resolver has no stale destination; preserved archive-only evidence is excluded. | DONE_UNCOMMITTED — pending root-controller commit |

## Related Documents

- [Approved specification](../../03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md)
- [Approved plan](../../03.specs/spec-0136-sdlc-taxonomy-convergence/plan.md)
- [Archive retention contract](../../99.templates/support/archive-retention-contract.md)
