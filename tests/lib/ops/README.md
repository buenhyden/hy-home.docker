---
title: "Operations Library Tests"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
created: "2026-10-10"
---

# Operations Library Tests

## Overview

`tests/lib/ops/`는 운영 helper의 순수 동작과 합성 filesystem 사례를 검증합니다.
실제 비밀값, HOME 서비스와 업무 데이터는 시험 입력이 아닙니다.

## Scope

- SMTP 모델 변환, grant 충돌, 안전한 metadata 전환과 퇴역 거부를 검증합니다.
- 단위 결과는 native SMTP, 실제 파일 삭제나 HOME 복구 증거가 아닙니다.

## Related Documents

- [Library tests](../README.md)
- [Operations libraries](../../../scripts/lib/ops/README.md)
