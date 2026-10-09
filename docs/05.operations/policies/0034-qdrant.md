---
title: "Qdrant Operations Policy"
version: "1.2.4"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0034"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Qdrant Operations Policy

## Overview

이 정책은 root-active `HOME` Qdrant 운영 기준을 정의한다. 기준은 [Qdrant Compose 구현](../../../infra/04-data/qdrant/docker-compose.yml)의 단일 service, exact `ai`/`ai-llm`/`qdrant` profiles, `ai_net`, API key secret, SSO 뒤의 REST route와 `/readyz` healthcheck다.

## Scope

- `infra/04-data/qdrant/docker-compose.yml`
- `qdrant` service와 `qdrant-data` volume
- SSO(`sso-auth@file`)와 API key 뒤에 있는 REST route `qdrant.${DEFAULT_URL}`; gRPC route는 없음
- `qdrant_api_key`(AI-008)에서 나온 API key; health endpoint만 이 키 없이 응답한다
- `qdrant_read_only_api_key`(AI-009)에서 나온 read-only API key로, Prometheus가 보유하는 유일한 키다; full key와 달라야 한다
- `QDRANT__STORAGE__SNAPSHOTS_PATH=/qdrant/storage/snapshots`
- `docs/05.operations` 아래에 연결된 guide와 runbook

## Rules

- **Required**: 문서는 Qdrant를 cluster가 아니라 단일 unprivileged service로 설명해야 한다.
- **Required**: 모든 Qdrant client는 secret file에서 key를 읽어야 하며 key가 Compose environment 값, logs, evidence에 절대 나타나서는 안 된다.
- **Required**: 외부 접근 가이드는 선언된 SSO REST route 안에 머물러야 하며, host port publishing이나 gRPC route를 암시해서는 안 된다.
- **Required**: persistence와 snapshot-path 표현은 `qdrant-data:/qdrant/storage:rw`와 `/qdrant/storage/snapshots`와 일치해야 한다.
- **Required**: 백업 inventory는 collection이나 full-storage snapshot identifier, engine minor version, aliases, vector counts/config, checksum, retention, restore evidence를 기록한다. snapshot file은 디스크에서 보호되며, API key는 그 파일에 대한 API 접근만 보호한다.
- **Required**: Restore rehearsal은 동일 minor 또는 다음 minor compatibility를 가진 새로운 isolated target을 사용하고, 명시적으로 검토된 force action이 아니면 target collection이 없어야 하며, snapshot 크기의 약 2배에 해당하는 여유 디스크가 필요하다.
- **Required**: promotion 전에 aliases, collection config/status, point counts, representative searches를 검증한다. Upgrade/removal에는 restore-tested snapshot과 capacity review가 필요하다.
- **Allowed**: read-only `/readyz`, `/collections`(secret file의 key 사용), compose config rendering, service logs, evidence 수집을 위한 `docker compose ps`.
- **Allowed**: image tag, profile, route, healthcheck, volume 설명을 compose와 일치시키는 문서 전용 수정.
- **Disallowed**: 별도의 owner 승인과 검증된 runbook evidence 없이 승인된 정책으로 제시되는 collection delete, snapshot restore, volume replacement, cluster repair, data mutation 단계.
- **Disallowed**: API key를 제거하거나 key 없이 Qdrant를 호출하는 client를 추가하는 행위.

### Accountable lifecycle boundary

적용 identity: `qdrant`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

## Exceptions

N/A - 현재 승인된 예외 없음.

### Verification

- compose 변경 후 이 정책을 [Qdrant guide](../guides/0034-qdrant.md), [Qdrant runbook](../runbooks/0034-qdrant.md), [infra README](../../../infra/04-data/qdrant/README.md)와 비교한다.
- service-name, image, route, secret, healthcheck, volume 문서 갱신을 승인하기 전에 `docker compose --profile qdrant config --quiet`를 실행한다.
- 정책이나 연결된 운영 문서 갱신 후 `python3 scripts/validation/check-document-links.py --mode all`을 실행한다.

### Review Cadence

- Qdrant compose image/profile/secret/route/snapshot-path 변경 시 검토한다.
- Stage 05 운영 문서 audit 주기 동안 검토한다.

### Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0034-qdrant.md) (`GDE-0034`), [Runbook](../runbooks/0034-qdrant.md) (`RUN-0034`)

## Related Documents

- [Qdrant snapshots](https://qdrant.tech/documentation/operations/snapshots/)
- [Qdrant migration and recovery](https://qdrant.tech/documentation/migration-recovery-options/)

- [Operations index](../README.md)
- [Usage guide](../guides/0034-qdrant.md)
- [Recovery runbook](../runbooks/0034-qdrant.md)
- [Infra README](../../../infra/04-data/qdrant/README.md)
