---
title: "OpenSearch Operations Policy"
version: "1.0.5"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0019"
parent_ids:
- "AD-0012"
created: "2026-05-17"
---

# OpenSearch Operations Policy

## Overview

이 문서는 `infra/04-data/opensearch`의 OpenSearch 운영 정책을 정의한다. current implementation은 OpenSearch 3.x custom build primary stack과 OpenSearch Dashboards 3.8.0을 사용하며 three-node cluster topology는 같은 Compose 파일의 `opensearch-cluster` profile로 선택한다.

## Policy Scope

- **Systems**: `opensearch` profile의 primary `opensearch`, `opensearch-cluster` profile의 `opensearch-node1..3`, 두 profile에 포함된 `opensearch-dashboards`
- **Secrets**: `opensearch_admin_password`, `opensearch_dashboard_password`, `opensearch_exporter_password`, `opensearch_security_cookie`, `oauth2_proxy_client_secret`
- **Persistence**: `opensearch-data`, `opensearch-dashboards-data`, `opensearch-cluster` profile node volume
- **Environments**: repo-local, development, homelab, production-like rehearsal

## Controls

- **Activation**: primary는 `docker compose --profile opensearch config --quiet`, LAB topology는 `docker compose --profile opensearch-cluster config --quiet`를 사용한다. 어떤 topology를 선택했는지 기록한다.
- **Security**: TLS, 인증서, security plugin, secret-backed user, gateway middleware를 보존한다. `.opendistro_security`를 유일한 security backup으로 snapshot하지 않는다; 검토된 security configuration을 별도로 보존하고 그 credential을 제한한다.
- **Retention and backup**: ingest 전에 index/ISM retention을 정의한다. live data volume 밖에 repository를 등록하고, 완료된 snapshot state를 요구하며, storage class에 맞게 repository를 암호화·제한하고, 격리된 restore를 rehearse한다.
- **Resources**: per-node 2 CPU/2 GiB 한도, Dashboards, disk, JVM overhead를 고려하지 않고 LAB cluster를 함께 선택하지 않는다. Promotion에는 측정된 shard와 restore capacity가 필요하다.
- **Upgrade**: source pin을 변경하기 전에 지원되는 version path, plugin/build 호환성, Dashboards 호환성, 인증서, snapshot restore를 검증한다. 더 새롭고 호환되지 않는 version이 기록한 index를 downgrade하지 않는다.
- **Removal**: consumer와 index retention을 확인하고, 검증된 snapshot과 security configuration을 보존한 다음, primary 또는 cluster data volume을 삭제하기 전에 승인을 받는다.
- **Required**: OpenSearch API check는 HTTPS와 secret-backed admin authentication을 사용해야 한다.
- **Required**: primary stack 작업은 `opensearch`를 대상으로 해야 하고, cluster-variant 작업은 `opensearch-node1..3`을 명시적으로 대상으로 해야 한다.
- **Required**: secret 값과 생성된 internal user material은 문서나 command history에 복사하지 않는다.
- **Allowed**: command가 `opensearch-cluster` profile을 선택할 때의 cluster topology validation.
- **Disallowed**: unauthenticated bulk load, HTTP-only health check, 또는 index/ISM evidence 없이 replica policy가 존재한다는 주장.


### Accountable lifecycle boundary

적용 identity: `opensearch`, `opensearch-dashboards`, `opensearch-node1`, `opensearch-node2`, `opensearch-node3`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

## Exceptions

임시 index setting, cluster variant 실험, security config 변경은 owner 승인과 before/after health evidence가 필요하다.

## Verification

- `test -f infra/04-data/opensearch/docker-compose.yml`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Review Cadence

- image/build, 인증서, secret, security config, cluster topology 변경 시
- 분기별 문서화된 recovery evidence 검토

## Traceability

- Declared parent: [Analytics Tier Architecture Description](../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](../guides/0019-opensearch.md) (`GDE-0019`), [Runbook](../runbooks/0019-opensearch.md) (`RUN-0019`)

## Related Documents

- [Compose implementation: infra/04-data/opensearch/docker-compose.yml](../../../infra/04-data/opensearch/docker-compose.yml)
- [Custom image source: infra/04-data/opensearch/Dockerfile](../../../infra/04-data/opensearch/Dockerfile)

- [OpenSearch snapshot and restore](https://docs.opensearch.org/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/)
- [Compose implementation](../../../infra/04-data/opensearch/docker-compose.yml)

- [Operations policies index](../README.md)
- [Usage guide](../guides/0019-opensearch.md)
- [Recovery runbook](../runbooks/0019-opensearch.md)
- [Infra README](../../../infra/04-data/opensearch/README.md)
