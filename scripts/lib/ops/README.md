---
title: "Operations Library"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# 운영 공통 라이브러리

## Overview

운영 명령이 재사용하는 범위 제한 helper를 둡니다. 실행 권한과 운영 증거는
각 작업의 owning Task에서 정하며 라이브러리 자체가 권한을 부여하지 않습니다.

## Structure

- `compose-core-readiness.sh`: Compose 핵심 서비스 readiness와 격리 복구 검사.
- `smtp_contract.py`: SMTP Compose 모델 검사와 정확한 중복 파일 퇴역 처리.
  모델·비밀값은 출력하지 않고 canonical 파일은 변경하지 않습니다.

## Usage

SMTP 검사는 `scripts/operations/gen-secrets.sh --retire-supabase-smtp-check`로
호출합니다. 적용은 현재 호스트·Git SHA·공개 Compose source와 소비자 검사에
묶인 audit receipt가 필요합니다. 실제 삭제는 SMTP01 전환 이후 CLN01이 소유합니다.

## Related Documents

- [스크립트 안내](../../README.md)
- [라이브러리 회귀시험](../../../tests/lib/README.md)
