---
title: "OpenSearch Operations Policy"
version: "2.2.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "operations"
artifact_id: "POL-0019"
parent_ids:
- "AD-0012"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# OpenSearch Operations Policy

## Purpose and Scope

### Objective

이 문서는 정상 root의 단일 OpenSearch와 별도 standalone LAB 클러스터의 운영 경계를 정의합니다. 정상 구성은 `infra/04-data/opensearch/docker-compose.yml`의 선언된 OpenSearch custom build와 Dashboards 이미지입니다. 세 노드는 [LAB Compose](../../../../labs/opensearch-cluster/docker-compose.yml)에서만 선택하며 root에는 include되지 않습니다. 소스나 문서의 변경은 기동·중단·복구 승인을 부여하지 않습니다.

#### Authority

- Declared parent: [Analytics Tier Architecture Description](../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)

- [Compose implementation: infra/04-data/opensearch/docker-compose.yml](../../../../infra/04-data/opensearch/docker-compose.yml)
- [Custom image source: infra/04-data/opensearch/Dockerfile](../../../../infra/04-data/opensearch/Dockerfile)
- [LAB Compose](../../../../labs/opensearch-cluster/docker-compose.yml) 및 [LAB 설명](../../../../labs/opensearch-cluster/README.md)

### Applies To

- **Systems**: 정상 `opensearch`/`opensearch-dashboards`; 별도 LAB의 `opensearch-node1..3`/`lab-opensearch-dashboards`
- **Secrets**: 정상은 `opensearch_admin_password`, `opensearch_dashboard_password`, `opensearch_exporter_password`, `opensearch_security_cookie`, `oauth2_proxy_client_secret`와 API route basic auth `traefik_opensearch_basicauth_password`; LAB는 `${LAB_SECRET_DIR}/opensearch-cluster/`의 별도 `lab_opensearch_*`만 사용
- **Persistence**: 정상 bind-backed `opensearch-data`/`opensearch-dashboards-data`; LAB는 `${LAB_DATA_DIR}/opensearch-cluster/` 아래 네 bind volume
- **Environments**: repo-local, development, homelab, production-like rehearsal

#### Exclusions

애플리케이션 인증 연동은 이 정책이 아니라 [POL-0079](../03-identity-and-access/0079-application-auth-integration.md)가 정한다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0019-R1 | 정상/LAB 활성화 | 필수: 정상은 `docker compose --profile opensearch config --quiet`, LAB는 `docker compose --env-file labs/.env.example -f labs/opensearch-cluster/docker-compose.yml --profile opensearch-cluster config --quiet`로 각각 정적 검증한다 | `docker compose --profile opensearch config --quiet` / `docker compose --env-file labs/.env.example -f labs/opensearch-cluster/docker-compose.yml --profile opensearch-cluster config --quiet` | none |
| POL-0019-R2 | LAB 활성화 | 필수: 별도 `LAB_SECRET_DIR`와 `LAB_OPENSEARCH_CERT_DIR`를 준비한다 | none | none |
| POL-0019-R3 | 정상/LAB 활성화 | 필수: 두 project의 선택과 실행 승인을 따로 기록한다 | none | none |
| POL-0019-R4 | 정상 구성 | 필수: TLS/인증서/security plugin/secret-backed user/gateway middleware를 보존한다 | none | none |
| POL-0019-R5 | LAB 구성 | 필수: 별도 CA/node 인증서와 secret/내부 네트워크/기본 내부 인증만 사용한다 | none | none |
| POL-0019-R6 | LAB 구성 | 금지: LAB를 정상 gateway/OIDC 및 데이터에 연결 | none | none |
| POL-0019-R7 | security backup | 금지: `.opendistro_security`를 유일한 security backup으로 snapshot | none | none |
| POL-0019-R8 | security configuration | 필수: 검토된 security configuration을 별도로 보존하고 그 credential을 제한한다 | none | none |
| POL-0019-R9 | ingest 전 | 필수: index/ISM retention을 정의한다 | none | none |
| POL-0019-R10 | snapshot repository | 필수: live data volume 밖에 repository를 등록한다 | none | none |
| POL-0019-R11 | snapshot | 필수: 완료된 snapshot state를 요구한다 | none | none |
| POL-0019-R12 | snapshot repository | 필수: storage class에 맞게 repository를 암호화/제한한다 | none | none |
| POL-0019-R13 | restore | 필수: 격리된 restore를 rehearse한다 | none | none |
| POL-0019-R14 | LAB 시작 전 | 필수: LAB 노드당 2 CPU/2 GiB, Dashboard, disk, JVM overhead를 재측정한다 | none | none |
| POL-0019-R15 | Promotion | 필수: 측정된 shard와 restore capacity를 갖춘다 | none | none |
| POL-0019-R16 | source pin 변경 전 | 필수: 지원되는 version path/plugin·build 호환성/Dashboards 호환성/인증서/snapshot restore를 검증한다 | none | none |
| POL-0019-R17 | 항상 | 금지: 더 새롭고 호환되지 않는 version이 기록한 index의 downgrade | none | none |
| POL-0019-R18 | 제거 시 | 필수: consumer와 index retention을 확인한다 | none | none |
| POL-0019-R19 | 제거 시 | 필수: 검증된 snapshot과 security configuration을 보존한다 | none | none |
| POL-0019-R20 | primary/cluster data volume 삭제 전 | 필수: 승인을 받는다 | 수동 | none |
| POL-0019-R21 | OpenSearch API check | 필수: HTTPS와 secret-backed admin authentication을 사용한다 | none | none |
| POL-0019-R22 | 작업 대상 지정 | 필수: 정상 작업은 root의 `opensearch`를, LAB 작업은 별도 project의 `opensearch-node1..3`과 `lab-opensearch-dashboards`를 명시적으로 대상으로 한다 | none | none |
| POL-0019-R23 | 항상 | 금지: secret 값과 생성된 internal user material을 문서나 command history에 복사 | none | none |
| POL-0019-R24 | LAB 정적 render | 허용: `-f labs/opensearch-cluster/docker-compose.yml --profile opensearch-cluster`를 명시한 LAB 정적 render(기동 허가가 아니다) | none | none |
| POL-0019-R25 | 항상 | 금지: unauthenticated bulk load | none | none |
| POL-0019-R26 | 항상 | 금지: HTTP-only health check | none | none |
| POL-0019-R27 | 항상 | 금지: index/ISM evidence 없이 replica policy가 존재한다고 주장 | none | none |
| POL-0019-R28 | 적용 identity 변경/운영 | 필수: 문서의 정적 검증과 runtime 운영 승인을 분리한다 | none | none |
| POL-0019-R29 | service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 | 필수: 이 Policy와 linked Guide/Runbook을 함께 검토한다 | 수동 | none |
| POL-0019-R30 | engine secret/certificate | 필수: 이 subject의 credential 계약을 따른다 | none | none |
| POL-0019-R31 | 앱 인증 연동 | 필수: 적용되는 `POL-0079`의 통제를 따른다 | none | none |
| POL-0019-R32 | source 반영/재기동 | 필수: `POL-0006`의 적용 통제를 따른다 | none | none |
| POL-0019-R33 | 보존/삭제 | 필수: `POL-0021`의 적용 통제를 따른다 | none | none |
| POL-0019-R34 | exporter/stateless job | 필수: 설정·credential과 그 작업이 변경하는 upstream state를 통제 대상에서 제외하지 않고 포함한다 | none | none |
| POL-0019-R35 | 소유 artifact·복구 지점·expiry가 불명확할 때 | 필수: 삭제/재생성을 중단한다 | none | none |
| POL-0019-R36 | 항상 | 금지: 기존 Exceptions 외의 새 예외를 승인된 것으로 간주 | none | none |

- **Activation**: 정상은 `docker compose --profile opensearch config --quiet`, LAB는 `docker compose --env-file labs/.env.example -f labs/opensearch-cluster/docker-compose.yml --profile opensearch-cluster config --quiet`로 각각 정적 검증합니다. LAB에는 별도 `LAB_SECRET_DIR` 및 `LAB_OPENSEARCH_CERT_DIR`가 필요합니다. 두 project의 선택과 실행 승인을 따로 기록합니다.
- **Security**: 정상 TLS, 인증서, security plugin, secret-backed user, gateway middleware를 보존합니다. LAB는 별도 CA/node 인증서와 secret, 내부 네트워크, 기본 내부 인증만 사용하며 정상 gateway/OIDC 및 데이터를 연결하지 않습니다. `.opendistro_security`를 유일한 security backup으로 snapshot하지 않는다; 검토된 security configuration을 별도로 보존하고 그 credential을 제한한다.
- **Retention and backup**: ingest 전에 index/ISM retention을 정의한다. live data volume 밖에 repository를 등록하고, 완료된 snapshot state를 요구하며, storage class에 맞게 repository를 암호화·제한하고, 격리된 restore를 rehearse한다.
- **Resources**: LAB 노드당 2 CPU/2 GiB, Dashboard, disk, JVM overhead를 재측정하지 않고 시작하지 않습니다. Promotion에는 측정된 shard와 restore capacity가 필요하다.
- **Upgrade**: source pin을 변경하기 전에 지원되는 version path, plugin/build 호환성, Dashboards 호환성, 인증서, snapshot restore를 검증한다. 더 새롭고 호환되지 않는 version이 기록한 index를 downgrade하지 않는다.
- **Removal**: consumer와 index retention을 확인하고, 검증된 snapshot과 security configuration을 보존한 다음, primary 또는 cluster data volume을 삭제하기 전에 승인을 받는다.
- **Required**: OpenSearch API check는 HTTPS와 secret-backed admin authentication을 사용해야 한다.
- **Required**: 정상 작업은 root의 `opensearch`를, LAB 작업은 별도 project의 `opensearch-node1..3`과 `lab-opensearch-dashboards`를 명시적으로 대상으로 합니다.
- **Required**: secret 값과 생성된 internal user material은 문서나 command history에 복사하지 않는다.
- **Allowed**: `-f labs/opensearch-cluster/docker-compose.yml --profile opensearch-cluster`를 명시한 LAB 정적 render. 이는 기동 허가가 아닙니다.
- **Disallowed**: unauthenticated bulk load, HTTP-only health check, 또는 index/ISM evidence 없이 replica policy가 존재한다는 주장.

#### Accountable lifecycle boundary

적용 identity: 정상 `opensearch`, `opensearch-dashboards`; LAB `opensearch-node1..3`, `lab-opensearch-dashboards`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](../03-identity-and-access/0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

### Exceptions

#### Exception Conditions

임시 index setting, LAB cluster 실험, security config 변경은 owner의 별도 실행 승인과 before/after health evidence가 필요하다.

#### Approval and Review

- image/build, 인증서, secret, security config, cluster topology 변경 시
- 분기별 문서화된 recovery evidence 검토

## Enforcement

### Mechanisms

- `test -f infra/04-data/opensearch/docker-compose.yml`
- `test -f labs/opensearch-cluster/docker-compose.yml`
- `docker compose --profile opensearch config --quiet`
- `docker compose --env-file labs/.env.example -f labs/opensearch-cluster/docker-compose.yml --profile opensearch-cluster config --quiet`
- 원격 PR public `changed` 검사 ([quality policy](../../../00.workspace/03.quality/quality-standards.md#canonical-delivery-phase-matrix))

custom Dockerfile의 OpenSearch 기본 이미지와 exporter plugin 선언 버전의 실제 빌드 호환성 및 LAB 인증서 검증은 아직 확인되지 않았으며 (미검증), runtime admission blocker로 남는다.

### Limits

이 정책은 아래 규칙에 명명된 자동 검사를 연결하지 않으며, 해당 규칙은 사전 검증·검토·승인 절차에 의존합니다.

- 활성화: 자동 검사 없음(none) `POL-0019-R2`, `POL-0019-R3`
- 보안: 자동 검사 없음(none) `POL-0019-R4`, `POL-0019-R5`, `POL-0019-R6`, `POL-0019-R7`, `POL-0019-R8`
- 보존/백업: 자동 검사 없음(none) `POL-0019-R9`, `POL-0019-R10`, `POL-0019-R11`, `POL-0019-R12`, `POL-0019-R13`
- 자원: 자동 검사 없음(none) `POL-0019-R14`, `POL-0019-R15`
- 업그레이드: 자동 검사 없음(none) `POL-0019-R16`, `POL-0019-R17`
- 제거: 자동 검사 없음(none) `POL-0019-R18`, `POL-0019-R19`; 수동 검토/승인 `POL-0019-R20`
- API/대상/secret: 자동 검사 없음(none) `POL-0019-R21`, `POL-0019-R22`, `POL-0019-R23`, `POL-0019-R24`
- 금지 행위: 자동 검사 없음(none) `POL-0019-R25`, `POL-0019-R26`, `POL-0019-R27`
- lifecycle: 자동 검사 없음(none) `POL-0019-R28`, `POL-0019-R30`, `POL-0019-R31`, `POL-0019-R32`, `POL-0019-R33`, `POL-0019-R34`, `POL-0019-R35`, `POL-0019-R36`; 수동 검토/승인 `POL-0019-R29`
- 정책이 밝힌 공백: custom Dockerfile의 OpenSearch 기본 이미지와 exporter plugin 선언 버전의 실제 빌드 호환성 및 LAB 인증서 검증은 미검증이며 runtime admission blocker로 남는다.

## Ownership

### Owner

@buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다.

### Review Triggers

- Subject peers: [Guide](../../guides/05-databases-and-storage/0019-opensearch.md) (`GDE-0019`), [Runbook](../../runbooks/05-databases-and-storage/0019-opensearch.md) (`RUN-0019`)

- [OpenSearch snapshot and restore](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
- [Operations policies index](../../README.md)
- [Infra README](../../../../infra/04-data/opensearch/README.md)
