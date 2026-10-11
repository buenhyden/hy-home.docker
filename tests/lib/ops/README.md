---
title: "Operations Library Tests"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
created: "2026-10-10"
---

# Operations Library Tests

## Overview

`tests/lib/ops/`는 운영 helper의 순수 동작과 합성 입력을 검증합니다. 실제
비밀값, HOME 서비스와 업무 데이터는 시험 입력이 아닙니다.

## Scope

- `test_compose_core_readiness.py`는 Compose readiness helper를 검증합니다.
- `test_wiki_preparation.py`는 P09 준비 계약 helper의 허용·거절 경계를 검증합니다.

- `test_smtp_contract.py`와 `test_smtp_proof.py`는 SMTP 모델·grant·metadata 전환과
  안전한 퇴역 거부를 합성 입력으로 검증합니다.
- 단위 결과는 native SMTP, 실제 파일 삭제나 HOME 복구 증거가 아닙니다.

- `test_secret_catalog.py`: malformed metadata·별칭·복구/암호화/LAB 보호·재생성 거부와 합성 Git 루트의 staging/CLI 경계를 검증합니다.

- `test_port_inventory.py`: IPv6·범위·unknown·DEV/MNG 독립성 및 bounded 합성 렌더 경계를 검증합니다.

- `test_opsflow_manifest.py`, `test_opsflow_adapters.py`,
  `test_opsflow_provision_contract.py`: P04 합성 매니페스트·보호된 접속 설정·SQL 권한
  소스 계약을 검증합니다. 실제 Airflow·DEV 게시나 빈 복원 수용은 별도입니다.

## Related Documents

- [Library tests](../README.md)
- [Operations libraries](../../../scripts/lib/ops/README.md)
