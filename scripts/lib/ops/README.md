---
title: "Operations Library"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
created: "2026-10-10"
---

# 운영 공통 라이브러리

## Overview

운영 명령이 재사용하는 범위 제한 helper를 둡니다. 실행 권한과 운영 증거는
각 작업의 owning Task에서 정하며 라이브러리 자체가 권한을 부여하지 않습니다.

## Structure

- `compose-core-readiness.sh`: Compose 핵심 서비스 readiness와 격리 복구 검사.
- `wiki_preparation.py`: P09의 parsed 계약·caller 정책·합성 bytes를 오프라인으로
  검증하는 유일한 공개 API이며 `PreparationError`를 re-export합니다.
- `wiki_preparation_semantics.py`: 위 공개 helper가 사용하는 private validator
  구현입니다. 직접 소비 API가 아니며 실제 Wiki 자원이나 비밀값을 읽거나 만들지
  않습니다.

## Usage

P09 helper는 전용 합성 단위·계약 시험으로 호출합니다. 그 결과는 native Wiki,
실제 자원 생성, HOME 복구 또는 배포 증거가 아닙니다.

## Related Documents

- [스크립트 안내](../../README.md)
- [라이브러리 회귀시험](../../../tests/lib/README.md)
