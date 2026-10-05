---
title: "SurrealDB Runbook"
version: "0.2.2"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0080"
parent_ids:
- "POL-0080"
created: "2026-09-19"
---

# SurrealDB Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

이 런북은 헬스 트리아지와 계획된 격리 export/import 리허설을 제공한다. 이 문서를 고치면서 런타임, export, import, 스토리지 변경은 전혀 실행하지 않았다.

### Purpose

안전한 증거를 수집하고, namespace, database, auth scope, 스키마와 데이터를 보존하는 반복 가능한 복구 테스트를 정의한다.

### When to Use

- `surrealdb`가 없거나, 비정상이거나, 접근 불가한 경우.
- 인증, namespace/database 선택, 영속성이 의심되는 경우.
- 승인된 backup, upgrade, 또는 격리 restore 리허설을 계획 중인 경우.

## Procedure

### Procedure

### Checklist

- [ ] 저장소 루트에서 작업하고 선택한 정확한 profile을 기록한다.
- [ ] configuration commit, Dockerfile/[Compose](../../../infra/08-ai/open-notebook/docker-compose.yml) 버전 권한과 [runtime version projection](../../../infra/tech-stack.versions.json), 엔진 버전(Open Notebook에는 SurrealDB v2가 필수), namespace, database, 예상 스키마와 record invariant를 기록한다.
- [ ] `surreal_db_password`와 원본 레코드는 증거에서 제외한다.
- [ ] export, import, stop, upgrade, volume 작업 전에 별도 승인을 받는다.

### Steps

1. 설정 렌더링: `docker compose --profile surrealdb config --quiet`.
2. 상태 확인: `docker compose --profile surrealdb ps surrealdb`.
3. 접근성 확인: `docker compose exec -T surrealdb /usr/local/bin/surreal is-ready --endpoint http://127.0.0.1:8000`.
4. 정제된 로그 검토: `docker compose --profile surrealdb logs --tail=120 surrealdb`.
5. mount, 버전, namespace/database, 또는 인증이 선언된 상태와 다르면 증거 수집 후 중단한다.

### Planned Isolated Restore Rehearsal

1. 승인을 받아 소스 버전, namespace/database, auth level, table/schema/permission 인벤토리, record-count invariant, export 옵션과 여유 용량을 기록한다. 보호된 credential 입력을 사용한다.
2. 명시적으로 지정한 namespace와 database에 대해 업스트림 `surreal export` 워크플로를 실행한다. manifest, checksum, 버전, scope, 캡처 시각, 보존 기간, 만료 시점과 함께 export를 보존한다. credential은 아티팩트에 export하지 않는다.
3. 프로덕션 port, network, volume, secret을 전혀 공유하지 않고 현재 배포의 v2 유지 정책에 맞는 새 호환 target을 준비한다. import에 필요한 auth scope로 별도 테스트 credential을 생성한다. 선택한 Open Notebook 이미지와의 v3 호환성을 단정하지 않으며, 정확한 이미지 조합의 근거와 별도 승인 전에는 v3를 사용하지 않는다.
4. 선택한 v2 CLI의 옵션·인증 및 import 처리 동작을 확인하고, 비어 있는 target과 명시적 namespace/database에 대해 업스트림 `surreal import` 워크플로를 실행한다.
5. readiness, 인증된 namespace/database 접근, table, 스키마 정의, permission, record-count invariant, 대표 read-only 쿼리를 검증한다. 증거를 정제한다.
6. import가 오류나 invariant 불일치를 보고하면 target을 부분 변경된 것으로 간주하고 격리 보존한다. 재시도는 별도의 빈 대상으로 하며 기존 volume 삭제는 진단·보존 종료 후 따로 승인받는다. 같은 target에서는 절대 재시도하지 않는다.

### Verification Steps

- Compose 렌더링과 서비스 상태가 정확한 source/profile과 일치한다.
- Export checksum과 선언된 scope가 리허설 입력과 일치한다.
- 격리된 target이 스키마, permission, count, 대표 read 검사를 통과한다.
- source volume, route, credential, runtime이 전혀 변경되지 않았다.

### Safe Rollback or Recovery Procedure

문서 변경은 범위가 한정된 diff로 되돌린다. 리허설이 실패하면 target과 전용 volume을 격리 보존하고 추가 쓰기를 중지한다. 삭제는 별도의 승인된 정리이며 자동 롤백이 아니다. source와 보호된 export는 그대로 둔다.

## Verification

### Evidence

날짜, configuration commit, 서비스/profile, source와 target 버전, namespace/database 식별자, backup checksum, exit status, 정제된 invariant, 그리고 명시적 미실행/실행 상태를 기록한다. secret 값이나 원본 database 콘텐츠는 절대 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

restore 증거는 위의 계획된 격리 리허설로만 확보한다. 프로덕션 cutover, route 변경, secret rotation, upgrade, 스토리지 교체는 별도 승인이 필요하며 여기서는 실행하지 않았다.

### Escalation

credential, 버전/스토리지 형식 호환성, namespace/database scope, 부분 import, 파괴적 스토리지 변경, 또는 backup 부재로 안전한 진행이 불가능하면 중단하고 `@buenhyden`에게 연락한다.

### Traceability

- 선언된 parent: [SurrealDB Policy](../policies/0080-surrealdb.md) (`POL-0080`)
- 관장 architecture: [AD-0011](../../02.architecture/descriptions/0011-laboratory-architecture.md)
- 대상 peer 문서: [Guide](../guides/0080-surrealdb.md), [Policy](../policies/0080-surrealdb.md)

## Related Documents

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [SurrealDB import](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/import)
- [SurrealDB upgrades and patching](https://surrealdb.com/docs/manage/self-hosted/upgrades-and-patching)
- [SurrealDB authentication](https://surrealdb.com/docs/learn/security/authentication/summary)
- [SurrealDB licensing](https://surrealdb.com/license)
- [운영 인덱스](../README.md)
- [Infrastructure README](../../../infra/08-ai/open-notebook/README.md)
