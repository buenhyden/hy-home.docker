---
title: "Operations Library Tests"
version: "0.1.6"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-20"
created: "2026-10-10"
---

# Operations Library Tests

## Overview

`tests/lib/ops/`는 운영 helper의 순수 동작과 합성 입력을 검증합니다. 실제
비밀값, HOME 서비스와 업무 데이터는 시험 입력이 아닙니다.

## Scope

- `test_compose_core_readiness.py`는 Compose readiness helper를 검증합니다.
- `test_root_resource_assessment.py`는 P07의 공개 입력 경계·측정 unknown·통제
  불일치와 합성 provenance 거부를 검증합니다. 실제 부하나 HOME 결과는 별도입니다.
- `test_storage_write_rate.py`는 W7 쓰기율 비교의 24시간 창·재시작·카운터 감소·
  재부팅·SMART 누락 거부와 t0 호환 집계를 합성 입력으로 검증합니다.
- `test_wiki_preparation.py`는 P09 준비 계약 helper의 허용·거절 경계를 검증합니다.

- `test_smtp_contract.py`와 `test_smtp_proof.py`는 SMTP 모델·grant·metadata 전환과
  안전한 퇴역 거부를 합성 입력으로 검증합니다.
- 단위 결과는 native SMTP, 실제 파일 삭제나 HOME 복구 증거가 아닙니다.

- `test_secret_catalog.py`: malformed metadata·별칭·복구/암호화/LAB 보호·재생성 거부와 합성 Git 루트의 staging/CLI 경계를 검증합니다.

- `test_port_inventory.py`: IPv6·범위·unknown·DEV/MNG 독립성 및 bounded 합성 렌더 경계를 검증합니다.

- `test_opsflow_manifest.py`, `test_opsflow_adapters.py`,
  `test_opsflow_provision_contract.py`: P04 합성 매니페스트·보호된 접속 설정·SQL 권한
  소스 계약을 검증합니다. 실제 Airflow·DEV 게시나 빈 복원 수용은 별도입니다.

- `test_openbao_issuance.py`, `test_openbao_issuance_trust.py`,
  `test_openbao_issuance_custody.py`: 발급 journal, 제한 신원과 tmpfs token 파일,
  검증한 request bytes·Git blob 설치의 결속을 합성 시험합니다.
- `test_openbao_consumer_migration.py`: P06 공개 계약·P02 API binding과 승인되지
  않은 이관 선택의 거부를 검증합니다. 실제 KV·pilot·복구 시험은 별도입니다.
- `test_openbao_copy_runtime.py`: 보호된 합성 파일과 loopback TLS fixture로
  CAS0·metadata 확인·equal/conflict·POST 불확실성과 version 보존, CA/SAN/만료·
  경로/inode 역할 충돌·전송 시간 상한·값 없는 진단을 검증합니다. 실제 HOME
  인증·소비·이관 수용은 증명하지 않습니다.

## Related Documents

- [Library tests](../README.md)
- [Operations libraries](../../../scripts/lib/ops/README.md)
