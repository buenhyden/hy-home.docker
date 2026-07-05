---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-07-04-infra-tech-stack-version-refresh.md -->

# Task: Infra Tech-Stack Version Refresh

## Overview

This task records the approved infra version refresh for curated Docker runtime
images. The work updates Docker Compose image declarations, aligns
`infra/tech-stack.versions.json` to the resulting Compose truth, and refreshes
nearby active documentation plus validation expectations.

## Inputs

- **Gap Register**: [WDC gap register](../../90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md)
- **Version Registry**: [infra/tech-stack.versions.json](../../../infra/tech-stack.versions.json)
- **Sync Script**: [sync-tech-stack-versions.sh](../../../scripts/operations/sync-tech-stack-versions.sh)
- **Infra Scope**: [Infrastructure Operational Scope](../../00.agent-governance/scopes/infra.md)

## Working Rules

- Update pinned Compose image tags only; do not start, stop, rebuild, pull, or
  recreate live containers in this task.
- Keep `infra/tech-stack.versions.json` downstream of Docker Compose image
  declarations.
- Preserve local/custom image semantics by updating custom image tags only when
  the corresponding Dockerfile upstream version already changed or the local
  build argument changed.
- Do not read, print, or infer secret values.
- Record unavailable-but-desired upstream versions as residual watch items
  instead of inventing tags.

## Approved Surface Evidence

| Surface | Approval Source | Target | Before Evidence | After Evidence | Rollback / Recovery | Redaction Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Compose image declarations | User request to update Compose to newer versions | Curated infra Compose files | Several Compose images lagged current stable tags or custom build tags | Compose declarations updated to pinned current stable tags where available | `git revert` this commit; restore prior tags | Image tags only |
| Tech-stack registry | User request to update `infra/tech-stack.versions.json` | `infra/tech-stack.versions.json` | Registry drifted from Compose declarations | `sync-tech-stack-versions.sh --check` reports in sync | Re-run sync script after rollback | Image tags only |
| Hardening/contract expectations | User request plus WDC-GAP-020/021 closure | `scripts/hardening/check-all-hardening.sh`, `scripts/validation/check-repo-contracts.sh` | Expected stale Keycloak/Vault/RedisInsight/contract versions | Expectations match updated Compose truth | Revert script changes with image rollback | No secrets |

## Version Evidence

| Component | Previous Active Tag | Selected Tag | Evidence Basis |
| --- | --- | --- | --- |
| Traefik | `traefik:v3.7.5` | `traefik:v3.7.6` | Docker Hub official image supported tags showed `v3.7.6`. |
| Keycloak | `quay.io/keycloak/keycloak:26.6.4-0` | `quay.io/keycloak/keycloak:26.6.4-1` | Keycloak downloads page listed release `26.6.4`; Quay tag API listed active `26.6.4-1`. |
| OAuth2 Proxy | `quay.io/oauth2-proxy/oauth2-proxy:v7.15.3` | `quay.io/oauth2-proxy/oauth2-proxy:v7.15.3` | Dockerfiles already used `v7.15.3`; hardening/docs expectations were aligned to the current source image. |
| Vault | `hashicorp/vault:2.0.3` | `hashicorp/vault:2.0.3` | Docker Hub tag data kept `2.0.3` as the current 2.0 patch tag. |
| PostgreSQL init jobs | `postgres:18-alpine` | `postgres:18.4-alpine` | Docker Hub official Postgres supported tags listed `18.4-alpine`. |
| Supabase Postgres | `supabase/postgres:17.6.1.139` | `supabase/postgres:17.6.1.142` | Docker Hub tag data listed `17.6.1.142`. |
| Kafka stack | `confluentinc/cp-kafka:8.3.0` | `confluentinc/cp-kafka:8.3.0` | Docker Hub has `8.3.0`; Confluent docs note 8.3.1 as a Kafka Streams leak fix, but Docker Hub did not publish 8.3.1 tags during this check. |
| Prometheus | `prom/prometheus:v3.12.0` | `prom/prometheus:v3.13.0` | Docker Hub/GitHub release evidence listed stable `v3.13.0`. |
| Loki custom | `hy/loki:3.6.6-custom` | `hy/loki:3.7.3-custom` | Local Dockerfile already uses upstream `grafana/loki:3.7.3`; Compose custom tag now matches. |
| Tempo custom | `hy/tempo:2.10.1-custom` | `hy/tempo:3.0.2-custom` | Local Dockerfile already uses upstream `grafana/tempo:3.0.2`; Compose custom tag now matches. |
| Grafana | `grafana/grafana:13.1.0` | `grafana/grafana:13.1.0` | GitHub/Docker Hub evidence kept `13.1.0` current. |
| Alloy | `grafana/alloy:v1.17.0` | `grafana/alloy:v1.17.1` | Docker Hub tag data listed stable `v1.17.1`. |
| Airflow | `apache/airflow:3.2.2` | `apache/airflow:3.2.2` | Docker Hub newer `3.3.0` tags were RC/beta only, so no stable bump was applied. |
| n8n custom | `hyhome/n8n:2.15.0-local` | `hyhome/n8n:2.29.5-local` | Docker Hub tag data listed stable `n8nio/runners:2.29.5`; local n8n build arg was updated to the same application release family. |
| n8n runners | `n8nio/runners:2.27.5` | `n8nio/runners:2.29.5` | Docker Hub tag data listed stable `2.29.5`. |
| Ollama | `ollama/ollama:0.30.11` | `ollama/ollama:0.31.1` | Docker Hub/GitHub release evidence listed stable `0.31.1`. |
| Open WebUI | `ghcr.io/open-webui/open-webui:v0.10.1-cuda` | `ghcr.io/open-webui/open-webui:v0.10.2-cuda` | GitHub latest release was `v0.10.2`; GHCR manifest check confirmed the `v0.10.2-cuda` tag exists. |
| RedisInsight | `redis/redisinsight:3.6.0` | `redis/redisinsight:3.6.0` | Docker Hub and Redis release notes kept `3.6.0` current. |
| Dozzle | `amir20/dozzle:v10.6.6` | `amir20/dozzle:v10.6.6` | Compose already used `v10.6.6`; hardening/docs expectations were aligned to the current tag. |

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Verify current stable image candidates from upstream registries/releases | ops | N/A | WDC-GAP-020/021 follow-up | Docker Hub, Quay, GitHub, and vendor docs checks summarized in Version Evidence | hy | Done |
| T-002 | Update curated Compose image declarations and local Dockerfile defaults | impl | Infra scope | WDC-GAP-020/021 follow-up | Compose/Dockerfile diffs in infra tier files | hy | Done |
| T-003 | Sync `infra/tech-stack.versions.json` from Compose declarations | impl | Tech-stack registry contract | WDC-GAP-021 | `bash scripts/operations/sync-tech-stack-versions.sh` wrote 16 changes; `--check` in sync | hy | Done |
| T-004 | Refresh active docs and validation expectations | doc | Active docs/contract expectations | WDC-GAP-020/021 | README/spec/policy updates plus hardening and repo-contract expectation updates | hy | Done |
| T-005 | Run validation gates and record residual watch items | ops | QA/CI contracts | Closure | Compose, hardening, sync, doc, wiki, provider, and repo-contract gates passed | hy | Done |

## Phase View

### Phase 1

- [x] Gather upstream version evidence.
- [x] Select stable pinned tags and preserve variants.
- [x] Apply Compose and Dockerfile version changes.

### Phase 2

- [x] Sync the tech-stack registry.
- [x] Update active docs and validation expectations.
- [x] Run final validation gates.

## Verification Summary

- **Test Commands**: `bash scripts/validation/validate-docker-compose.sh` -> PASS (`services_total=5`); `HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh` -> PASS (`services_total=11`); `HYHOME_COMPOSE_PROFILES='obs dev' bash scripts/validation/validate-docker-compose.sh` -> PASS (`services_total=45`); `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh` -> PASS (`services_total=45`); `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh` -> PASS (`services_total=4`); `HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh` -> PASS (`services_total=8`); `HYHOME_COMPOSE_PROFILES=ai bash scripts/validation/validate-docker-compose.sh` -> PASS (`services_total=1`); `HYHOME_COMPOSE_PROFILES=data bash scripts/validation/validate-docker-compose.sh` -> PASS (`services_total=15`); `bash scripts/hardening/check-all-hardening.sh` -> PASS.
- **Eval Commands**: `bash scripts/operations/sync-tech-stack-versions.sh --check` -> in sync; `git diff --cached --check` -> no output; `bash scripts/knowledge/generate-llm-wiki-index.sh --check` -> PASS; `bash scripts/operations/sync-provider-surfaces.sh --check` -> no drift; `bash scripts/validation/check-doc-traceability.sh` -> `failures=0`; `bash scripts/validation/check-doc-implementation-alignment.sh` -> `failures=0`; `bash -n scripts/validation/check-repo-contracts.sh` -> no output; `bash scripts/validation/check-repo-contracts.sh` -> `failures=0`.
- **Logs / Evidence Location**: This task, the gap register remediation row, and the latest row in `docs/00.agent-governance/memory/progress.md`.

### Residual Watch Items

- Confluent documentation states that the Kafka Streams native memory leak in
  Confluent Platform `8.3.0` is fixed in `8.3.1`, but Docker Hub did not expose
  `8.3.1` tags for `cp-kafka`, `cp-schema-registry`, `cp-kafka-connect`, or
  `cp-kafka-rest` during this check. Keep the Kafka stack on `8.3.0` and watch
  for published `8.3.1` image tags before changing Compose.
- Airflow `3.3.0` images were visible only as RC/beta tags during this check, so
  `apache/airflow:3.2.2` remains the selected stable tag.
- No live runtime mutation was performed. Service pull/recreate and health
  checks remain a separate runtime operation.

### Deviation Notes

- The original WDC-GAP-020/021 follow-up could have been solved by syncing the
  registry down to current Compose only. The user clarified that Compose should
  also be advanced to newer versions, so this task updated Compose declarations
  first and then re-synced the registry from Compose.
- The root validation profile name for observability is `obs`; an attempted
  `HYHOME_COMPOSE_PROFILES=observability` render returned zero services and was
  replaced by the correct `obs` and `obs dev` validations.

## Source Links

- [Traefik Docker Hub official image](https://hub.docker.com/_/traefik/)
- [Keycloak downloads](https://www.keycloak.org/downloads)
- [Keycloak Quay tags](https://quay.io/repository/keycloak/keycloak?tab=tags)
- [Postgres Docker Hub official image](https://hub.docker.com/_/postgres/)
- [Confluent Platform release notes](https://docs.confluent.io/platform/current/release-notes/index.html)
- [Confluent Docker image reference](https://docs.confluent.io/platform/current/installation/docker/image-reference.html)
- [Prometheus Docker Hub tags](https://hub.docker.com/r/prom/prometheus/tags)
- [Grafana Alloy releases](https://github.com/grafana/alloy/releases)
- [Open WebUI releases](https://github.com/open-webui/open-webui/releases)
- [RedisInsight release notes](https://redis.io/docs/latest/develop/tools/insight/release-notes/v.3.6.0/)
- [Valkey releases](https://valkey.io/download/releases/)
- [Spilo package evidence](https://github.com/orgs/zalando/packages/container/package/spilo-17)

## Related Documents

- [Task README](./README.md)
- [Gap register](../../90.references/audits/2026-07-03-workspace-document-contract-audit-pack/gap-register.md)
- [Tech-stack registry](../../../infra/tech-stack.versions.json)
- [Infrastructure Operational Scope](../../00.agent-governance/scopes/infra.md)
