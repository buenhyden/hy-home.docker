---
title: "OpenBao Consumer Migration and Secret Catalog"
version: "0.2.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-28"
layer: "operations"
artifact_id: "RUN-0106"
parent_ids:
- "POL-0085"
created: "2026-10-28"
---

# OpenBao Consumer Migration and Secret Catalog

## Overview

이 런북은 P06 소비자 이관 runtime의 운영 경계와 P02 공개 secret catalog 점검을 다룬다. 실제 소비자 전환 절차는 [consumer-migration README](../../../../infra/03-security/openbao/consumer-migration/README.md)가 소유한다.

## Trigger

소비자를 OpenBao Agent 출력으로 옮기거나, secret catalog를 점검·렌더·생성 점검할 때 사용한다.

## Prerequisites

저장소 루트에서 작업하고, 실제 copy·전환·삭제·회전은 P06 Task의 별도 입력·검토·수용을 거친다.

## Procedure

### P06 Consumer Migration Boundary

이 Runbook은 [copy runtime](../../../../scripts/lib/ops/openbao_consumer_migration.py)과
[HTTPS transport](../../../../scripts/lib/ops/_openbao_copy_transport.py)의 운영 실행 경계를 소유합니다.
두 모듈은 controller가 현재 trusted user 또는 native authorization origin을 확인하고
고정 P02·P01·P03·P04 입력에 결속한 뒤에만 실행하는 runtime primitive입니다.
직접 library를 호출했다는 사실은 실행 승인이 아닙니다. 공개
`scripts/operations/openbao-consumer-migration.py` CLI는 validate-only이며 production catalog
adapter·controller factory·runtime copy CLI는 아직 제공하지 않습니다. 실제 private/native copy,
consumer 렌더·pilot·authority 전환·복구·삭제·회전은
[P06 Task](../../../03.specs/0204-service-integration-security-and-operations/tasks/tsk-0014-p06-openbao-consumer-migration.md)의
별도 입력·검토·수용 전까지 **NOT_RUN**입니다. source/unit 통과로 이 경계를 완료 처리하지 않습니다.

## Verification

### P02 Public Catalog Checks

이 절차는 검토된 checkout의 공개 metadata와 staging view만 확인한다. OpenBao API,
private metadata·환경·credential 파일, HOME 서비스에 접속하지 않는다. 저장소 루트의
물리적 절대 경로에서 검증 의존성이 설치된 Python으로 실행하며, symlink 경로나 다른
checkout을 `--root`로 지정하지 않는다. 먼저 읽기 전용 검사를 실행한다.

```bash
rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check
```

네 입력은 catalog, schema, `secrets/SENSITIVE_ENV_VARS.md.example`,
`infra/secret-file-support.json`이다. 형식·분류·원본 표 일치가 유효하면 JSON의
`result`는 `P02_METADATA_VALID`, `entries`와 `aliases`는 실제 입력의 개수이며 exit 0이다.
`P02_METADATA_BLOCKED`와 exit 2는 형식·원본·경로·의존성 등 검사 실패이므로 중단한다.
이 결과는 credential 값 또는 권리·운영 상태를 검사한 결과가 아니다.

staging이 필요한 경우에만 operator-owned `.agent-work`와 그 안의 regular, single-link,
동일 소유자 `README.md`를 먼저 확인한다. 기존 타 작업자의 경로를 교체하거나 symlink,
공유 inode, 다른 소유자의 파일 권한을 고쳐서 통과시키지 않는다. 새 경로를 준비할 때는
소유자가 확인된 전용 checkout에서만 만들고 그 목적을 README에 기록한다.

```bash
rtk python3 scripts/operations/secret-catalog.py --root "$PWD" render
rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check-views
```

`render`는 `.agent-work/p02-views`에 정확히 네 공개 출력 파일을 만들며
`STAGING_RENDERED`와 파일명 목록, exit 0을 반환한다. `check-views`는 네 입력에서 유도한
bytes와 모두 일치할 때만 `P02_VIEWS_MATCH`, exit 0이다. 불일치는 `P02_VIEW_DRIFT`,
exit 2다. 경로·소유권 등 안전 검사 실패는 `P02_METADATA_BLOCKED`, exit 2다.
파일별 교체는 전체 네 파일의 원자적 transaction을 뜻하지 않는다. 실패 후 부분 결과를
소비하지 말고 원인과 공개 입력을 검토한 뒤 동일 전용 staging을 다시 생성·검사한다.
private 파일 삭제나 runtime rollback을 이 절차의 정리로 수행하지 않는다.

아래 두 거절 probe는 각각 독립적으로 실행한다. `check-generation`은 생성 적격성만
검사하며 secret을 발급하지 않는다. 두 명령 모두 `P02_GENERATION_BLOCKED`, exit 2가
정상 예상 결과이며, 일반 shell의 실패 코드와 구별해 기록한다.

```bash
rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check-generation COMM-002
rtk python3 scripts/operations/secret-catalog.py --root "$PWD" check-generation COMM-003
```

거절 대신 성공하거나 예상 출력과 다르면 중단하고 P02 catalog 담당자와 검토한다.
alias COMM-003은 실제 폐기 완료가 아니며 별도 credential/KV 대상을 만들 수 없다.
다른 crypto/bootstrap/recovery/LAB/unknown/migrated/retired 항목과 observed/consumed 항목도
guard가 거부해야 한다. 공개 staging만으로 실제 발급·수집·이관·delivery·reload·rotation·
복구를 수용하지 않는다. ACL mapping은 `BLOCKED_P01`이고 delivery는 Agent 전달이 확인된
`DEPLOYED` 항목만 `openbao_agent`다. 실제 pilot은 대상 ID·KV
path·P01 인증/복구·P03 신원·P04 DEV/S3 증거가 있어야 한다. 현재 HOME/P06 hold를 유지한다.

## Failure and Recovery

### Rollback or Recovery

catalog 점검이 실패하면 생성·전환을 멈추고 원인을 고친 뒤 다시 점검한다. 소비자 전환의 rollback은 consumer-migration README의 `rollback` 절차를 따른다.

### Escalation

credential, 파괴적 스토리지 변경, remote 변경, 또는 backup 부재로 안전한 진행이 불가능하면
중단하고 @buenhyden에게 연락한다.

## Related Documents

### Traceability

- 공통 OpenBao 운영: [RUN-0085](0085-openbao.md)
- [Implementation](../../../../infra/03-security/openbao/docker-compose.yml)과 [version projection](../../../../infra/tech-stack.versions.json)이 런타임 고정 버전을 소유한다.
- [Guide](../../guides/04-security-and-secrets/0085-openbao.md), [Policy](../../policies/04-security-and-secrets/0085-openbao.md)
- 관장 architecture: [AD-0003](../../../02.architecture/descriptions/0003-security-architecture.md)

- [운영 인덱스](../../README.md)
