---
title: "OpenBao Consumer Migration Contracts"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
created: "2026-10-11"
---

# OpenBao 소비자 이관 공개 계약

## Overview

소비자별 이관을 준비하는 값 없는 공개 계약과 합성 검사 경로입니다. 현재 구현은
공개 형식과 선택 거부 조건을 검증하며, 실제 이관·소비·복구·삭제·회전 영수증은
발급하지 않습니다. 실행 증거와 선행 조건은 [문서 인덱스](../../../../docs/README.md)를
통해 현재 작업에서 확인합니다.

## Audience

이관 계약을 통합하는 개발자와 공개 검사 결과를 확인하는 운영자.

## Scope

현재 계약은 합성 준비 단계에 한정됩니다. 기존 catalog 소유자가 발급한 실제
항목과 승인된 목적지, 인증·전달·소비·복구 계약의 통합이 후속 실행의 입력입니다.
형식 검사 통과와 입력의 hash 일치는 운영 승인이나 실제 수용 증거가 아닙니다.

## Structure

- [wave.schema.json](wave.schema.json): 한 소비자의 공개 ID 선택과 공개 catalog 입력
  바인딩을 선언합니다. 임의 필드, 중복 ID, wildcard와 비밀값 칸은 거부합니다.
- [receipt.schema.json](receipt.schema.json): 합성 준비 결과만 선언합니다. 상태는
  `inventoried`와 `classified`, KV version은 `null`입니다. native 표시나 실제 복사
  이후 상태는 거부하며, 후속 단계는 소유자가 검토한 별도 계약 확장이 필요합니다.

## Tech Stack

기존 Python과 `jsonschema` 검증기를 재사용합니다. 별도 Agent, catalog, 분류기,
workflow 또는 운영 자원을 만들지 않습니다.

## Configuration

`catalog`의 `revision`, `schema_version`, `catalog_sha256`, `schema_sha256`,
`source_sha256`은 공개 catalog·schema·API 소스의 바인딩입니다. 비밀값이나 비밀값에서
계산한 hash를 넣지 않습니다. 호출자가 후보 문서와 별도로 고정한 입력과 대조합니다.

`FrozenAuthority`와 `CatalogSelection`은 합성 시험용 임시 주입 인터페이스입니다.
실제 catalog API 연결이 아닙니다. `APPROVED`는 합성 projection의 상태이며 기존
catalog의 `BLOCKED_P01` 항목이나 초안 목적지 경로를 승인으로 바꾸지 않습니다.
선택 검사는 alias, 미확인 소비자, 복구용·bootstrap·암호화·미사용·LAB 항목,
안전하지 않은 경로와 중복 목적지를 거부합니다. 원본 파일은 열지 않습니다.

## Validation

저장소 루트에서 공개 합성 JSON을 표준 입력으로 전달합니다. 입력은 128 KiB,
깊이 12, node 4096으로 제한하며 표준 입력 대기는 총 5초로 제한합니다.
오류에는 입력 본문·argv·경로·예외 payload를 출력하지 않습니다.

```sh
python3 scripts/operations/openbao-consumer-migration.py --help
```

전용 시험은 `tests/lib/ops/test_openbao_consumer_migration.py`와
`tests/validation/test_openbao_consumer_migration_contract.py`입니다. 공통 Script
Manifest·QA 등록과 상위 README 변경은 단일 통합 작성자가 적용해야 합니다.

## Usage

`validate-wave`와 `validate-receipt`는 공개 형식만 검사합니다. 파일 읽기·KV 복사·삭제·
비밀번호 변경 실행 옵션은 없습니다. 실제 단계의 계약과 영수증이 없으면 대기하며,
이 합성 결과를 HOME·이관·복구·배포 성공으로 사용하지 않습니다.

## Related Documents

- [OpenBao 구현 안내](../README.md)
- [운영 라이브러리](../../../../scripts/lib/ops/README.md)
- [검증 시험 안내](../../../../tests/validation/README.md)
