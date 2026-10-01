---
title: "Cassandra Operations Policy"
version: "1.0.5"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0025"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Cassandra Operations Policy

## Overview

이 정책은 `hy-home.docker`의 `LAB` Cassandra 단일 노드와 exporter 운영 기준을 정의한다. runtime image/version은 Compose declaration이 소유하며, 정책은 `cassandra` profile, 제한된 `lab_net` 접근, 실제 적용되는 인증·권한과 명시적 recoverable persistence를 요구한다. 현 source의 Bitnami 환경 변수/경로는 공식 image와 불일치하여 두 통제 모두 미준수다.

## Policy Scope

- `infra/04-data/cassandra/docker-compose.yml`
- `cassandra-node1` service and `cassandra-exporter` service
- `cassandra-node1-volume`, `cassandra-exporter-volume`
- `cassandra_password` Docker Secret and `CASSANDRA_USERNAME` identity variable
- Linked guide and runbook under `docs/05.operations`

## Controls

- **Required**: Cassandra 문서는 현재 구현을 정확한 `cassandra` profile로 선택되는 단일
  node로 기술해야 하며, 동작 중인 multi-node high-availability cluster로 기술해서는
  안 된다.
- **Required**: Credential 처리는 `/run/secrets/cassandra_password`를 참조해야
  한다. 문서, 예시, evidence에는 plaintext password 변수나 복사된 secret 값을
  허용하지 않는다.
- **Required**: 실제 data directory를 명시적 bind/named volume에 보존해야 한다. 공식 image의 `/var/lib/cassandra`와 현재 `/bitnami/cassandra` bind 불일치를 먼저 해소하고 기존 data ownership을 검증한다. anonymous volume을 충족 근거로 인정하지 않는다.
- **Required**: password authentication과 authorization을 명시적으로 적용해야 한다. 현 공식 image는 `CASSANDRA_USER`/`CASSANDRA_PASSWORD_FILE`을 처리하지 않아 AllowAll 기본값이며, 운영 활성화 전에 별도 구현 변경과 무인증/오인증 거부 검증이 필요하다.
- **Required**: Monitoring 참조는 `cassandra-exporter`를 동일한 `cassandra`
  profile의 별도 서비스로 식별해야 한다.
- **Required**: Backup 세트는 스냅샷 tag를 schema, keyspace/replication metadata,
  release 호환성, topology/token evidence, 필요한 모든 SSTable에 묶어야
  한다. Credential은 별도로 보호되는 artifact로 유지한다.
- **Required**: Restore rehearsal은 비어 있는 isolated, compatible target을
  사용한다. Schema를 먼저 생성하고, upstream이 지원하는 방법으로 SSTable을
  load하며, ownership/permission을 검증하고, table 누락이나 읽기 실패가 있으면
  rehearsal을 reject한다.
- **Required**: Retention은 backup identifier, capture 시각, scope,
  checksum/location, restore test, expiry를 기록한다. 용량은 snapshot과
  compaction을 위한 여유를 남겨야 하며, resource나 retention 변경은 검토가
  필요하다.
- **Required**: Upgrade는 release/schema/SSTable 호환성 검토와 성공한 isolated
  restore를 요구한다. Removal은 consumer shutdown 확인, 보관된 backup evidence,
  expiry/owner, volume 삭제 전 별도 승인을 요구한다.
- **Allowed**: 검증을 위한 로컬 status 확인, `nodetool status`, compose 렌더링,
  read-only CQL query.
- **Allowed**: 서비스 이름, image tag, profile, 링크를 compose와 일치시키는
  문서 전용 수정.
- **Disallowed**: 현재 구현으로 제시되는 검증되지 않은 multi-node repair, quorum,
  zero-downtime rotation 절차. 추적된 volume 위에서 in-place restore를 하는 것도
  금지한다.
- **Disallowed**: 이 정책 문서만으로 runtime data mutation, volume 교체,
  credential rotation, backup restore를 수행하는 것.

### Accountable lifecycle boundary

적용 identity: `cassandra-exporter`, `cassandra-node1`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

## Exceptions

N/A - 현재 승인된 예외 없음.

## Verification

- Compose 변경 후 이 정책을 [Cassandra guide](../guides/0025-cassandra.md),
  [Cassandra runbook](../runbooks/0025-cassandra.md),
  [infra README](../../../infra/04-data/cassandra/README.md)와 비교한다.
- 서비스 이름, volume, profile, secret 문서 갱신을 승인하기 전에
  `docker compose --profile cassandra config --quiet`를 실행한다.
- 정책이나 연결된 운영 문서 갱신 후 `python3 scripts/validation/check-document-links.py --mode all`을 실행한다.

## Review Cadence

- Cassandra compose image/profile/secret/volume 변경 시 검토한다.
- Stage 05 운영 문서 audit 주기 동안 검토한다.

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0025-cassandra.md) (`GDE-0025`), [Runbook](../runbooks/0025-cassandra.md) (`RUN-0025`)

## Related Documents

- [Compose implementation: infra/04-data/cassandra/docker-compose.yml](../../../infra/04-data/cassandra/docker-compose.yml)

- [Cassandra backup and restore](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/backups.html)
- [Cassandra security](https://cassandra.apache.org/doc/stable/cassandra/managing/operating/security.html)

- [Operations index](../README.md)
- [Usage guide](../guides/0025-cassandra.md)
- [Recovery runbook](../runbooks/0025-cassandra.md)
- [Infra README](../../../infra/04-data/cassandra/README.md)
