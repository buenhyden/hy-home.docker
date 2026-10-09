---
title: "OpenSearch Operations Policy"
version: "2.1.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0019"
parent_ids:
- "AD-0012"
created: "2026-05-17"
---

# OpenSearch Operations Policy

## Overview

이 문서는 정상 root의 단일 OpenSearch와 별도 standalone LAB 클러스터의 운영 경계를 정의합니다. 정상 구성은 `infra/04-data/opensearch/docker-compose.yml`의 선언된 OpenSearch custom build와 Dashboards 이미지입니다. 세 노드는 [LAB Compose](../../../labs/opensearch-cluster.yml)에서만 선택하며 root에는 include되지 않습니다. 소스나 문서의 변경은 기동·중단·복구 승인을 부여하지 않습니다.

## Scope

- **Systems**: 정상 `opensearch`/`opensearch-dashboards`; 별도 LAB의 `opensearch-node1..3`/`lab-opensearch-dashboards`
- **Secrets**: 정상은 기존 `opensearch_*` 및 `oauth2_proxy_client_secret`; LAB는 `${LAB_SECRET_DIR}/opensearch-cluster/`의 별도 `lab_opensearch_*`만 사용
- **Persistence**: 정상 bind-backed `opensearch-data`/`opensearch-dashboards-data`; LAB는 `${LAB_DATA_DIR}/opensearch-cluster/` 아래 네 bind volume
- **Environments**: repo-local, development, homelab, production-like rehearsal

## Rules

- **Activation**: 정상은 `docker compose --profile opensearch config --quiet`, LAB는 `docker compose --env-file labs/.env.example -f labs/opensearch-cluster.yml --profile opensearch-cluster config --quiet`로 각각 정적 검증합니다. LAB에는 별도 `LAB_SECRET_DIR` 및 `LAB_OPENSEARCH_CERT_DIR`가 필요합니다. 두 project의 선택과 실행 승인을 따로 기록합니다.
- **Security**: 정상 TLS, 인증서, security plugin, secret-backed user, gateway middleware를 보존합니다. LAB는 별도 CA/node 인증서와 secret, 내부 네트워크, 기본 내부 인증만 사용하며 정상 gateway/OIDC 및 데이터를 연결하지 않습니다. `.opendistro_security`를 유일한 security backup으로 snapshot하지 않는다; 검토된 security configuration을 별도로 보존하고 그 credential을 제한한다.
- **Retention and backup**: ingest 전에 index/ISM retention을 정의한다. live data volume 밖에 repository를 등록하고, 완료된 snapshot state를 요구하며, storage class에 맞게 repository를 암호화·제한하고, 격리된 restore를 rehearse한다.
- **Resources**: LAB 노드당 2 CPU/2 GiB, Dashboard, disk, JVM overhead를 재측정하지 않고 시작하지 않습니다. Promotion에는 측정된 shard와 restore capacity가 필요하다.
- **Upgrade**: source pin을 변경하기 전에 지원되는 version path, plugin/build 호환성, Dashboards 호환성, 인증서, snapshot restore를 검증한다. 더 새롭고 호환되지 않는 version이 기록한 index를 downgrade하지 않는다.
- **Removal**: consumer와 index retention을 확인하고, 검증된 snapshot과 security configuration을 보존한 다음, primary 또는 cluster data volume을 삭제하기 전에 승인을 받는다.
- **Required**: OpenSearch API check는 HTTPS와 secret-backed admin authentication을 사용해야 한다.
- **Required**: 정상 작업은 root의 `opensearch`를, LAB 작업은 별도 project의 `opensearch-node1..3`과 `lab-opensearch-dashboards`를 명시적으로 대상으로 합니다.
- **Required**: secret 값과 생성된 internal user material은 문서나 command history에 복사하지 않는다.
- **Allowed**: `-f labs/opensearch-cluster.yml --profile opensearch-cluster`를 명시한 LAB 정적 render. 이는 기동 허가가 아닙니다.
- **Disallowed**: unauthenticated bulk load, HTTP-only health check, 또는 index/ISM evidence 없이 replica policy가 존재한다는 주장.

### Accountable lifecycle boundary

적용 identity: 정상 `opensearch`, `opensearch-dashboards`; LAB `opensearch-node1..3`, `lab-opensearch-dashboards`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

## Exceptions

임시 index setting, LAB cluster 실험, security config 변경은 owner의 별도 실행 승인과 before/after health evidence가 필요하다. custom Dockerfile의 OpenSearch 기본 이미지와 exporter plugin 선언 버전의 실제 빌드 호환성 및 LAB 인증서 검증은 아직 확인되지 않았으며 (미검증), runtime admission blocker로 남는다.

### Verification

- `test -f infra/04-data/opensearch/docker-compose.yml`
- `test -f labs/opensearch-cluster.yml`
- 원격 PR public `changed` 검사 ([quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix))

### Review Cadence

- image/build, 인증서, secret, security config, cluster topology 변경 시
- 분기별 문서화된 recovery evidence 검토

### Traceability

- Declared parent: [Analytics Tier Architecture Description](../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](../guides/0019-opensearch.md) (`GDE-0019`), [Runbook](../runbooks/0019-opensearch.md) (`RUN-0019`)

## Related Documents

- [Compose implementation: infra/04-data/opensearch/docker-compose.yml](../../../infra/04-data/opensearch/docker-compose.yml)
- [Custom image source: infra/04-data/opensearch/Dockerfile](../../../infra/04-data/opensearch/Dockerfile)
- [LAB Compose](../../../labs/opensearch-cluster.yml) 및 [LAB 설명](../../../labs/opensearch-cluster.md)

- [OpenSearch snapshot and restore](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
- [Operations policies index](../README.md)
- [Usage guide](../guides/0019-opensearch.md)
- [Recovery runbook](../runbooks/0019-opensearch.md)
- [Infra README](../../../infra/04-data/opensearch/README.md)
