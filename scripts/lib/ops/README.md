---
title: "Operations Library"
version: "0.1.7"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-20"
created: "2026-10-10"
---

# 운영 공통 라이브러리

## Overview

운영 명령이 재사용하는 범위 제한 helper를 둡니다. 실행 권한과 운영 증거는
각 작업의 owning Task에서 정하며 라이브러리 자체가 권한을 부여하지 않습니다.

## Structure

- `compose-core-readiness.sh`: Compose 핵심 서비스 readiness와 격리 복구 검사.
- `memory_sources.py`: 공유 memory CLI가 caller worktree의 tracked 일반 파일
  pin을 확인하는 helper입니다. source 크기·경로·symlink·FIFO를 제한하고 개인
  native memory나 외부 URL을 읽지 않습니다. 검토 상태와 현재성을 구분합니다.
- `root_resource_assessment.py`: 공개 JSON의 측정 선언·unknown·기존 공통 통제를
  범위 제한 평가합니다. 출력의 runtime 수용·변경 승인 플래그는 항상 false이며,
  정본 예외 등록과 실제 서비스의 결합은 후속 검증 대상입니다.
- `openbao_consumer_migration.py`: P06 공개 wave·receipt와 P02 API 선택 거부를
  검증하고, 별도 controller가 권한과 입력을 제공한 경우 같은 bytes의 KV-v2 copy
  primitive를 호출합니다. CAS=0·기존 값 확인·불확실 readback을 구분하고 POST 뒤
  실패 또는 FD 정리 실패가 쓰기 사실을 지우지 않도록 보존합니다. 공개 CLI는
  validation 전용이며 운영 P02 adapter·P01 token/ACL/custody는 별도입니다.
- `_openbao_copy_io.py`, `_openbao_copy_transport.py`: 위 primitive 전용 내부
  보호 입력·고정 HTTPS 전송 경계입니다. origin·numeric connect IP·held CA를
  분리하고 역할의 경로/inode 충돌과 proxy·redirect·ambient 인증을 거부합니다.
- `smtp_contract.py`: SMTP Compose 모델 검사와 정확한 중복 파일 퇴역 처리.
- `storage_write_rate.py`: SPEC-0246 W7의 읽기 전용 쓰기율 snapshot과 24시간
  비교·SSD 내구성 추정. 표본 무효는 `DEFER`이며 이동 결정을 대신하지 않습니다.
  모델·비밀값은 출력하지 않고 canonical 파일은 변경하지 않습니다.
- `smtp_public_source.py`: ROOT·LAB의 추적된 공개 Compose와 선택된 상속
  설정을 검증합니다. 비밀값을 읽지 않으며 인증·발송·운영 수용을 증명하지 않습니다.
- `wiki_preparation.py`: P09의 parsed 계약·caller 정책·합성 bytes를 오프라인으로
  검증하는 유일한 공개 API이며 `PreparationError`를 re-export합니다.
- `wiki_preparation_semantics.py`: 위 공개 helper가 사용하는 private validator
  구현입니다. 직접 소비 API가 아니며 실제 Wiki 자원이나 비밀값을 읽거나 만들지
  않습니다.

## Usage

P09 helper는 전용 합성 단위·계약 시험으로 호출합니다. 그 결과는 native Wiki,
실제 자원 생성, HOME 복구 또는 배포 증거가 아닙니다.

SMTP 검사는 `scripts/operations/gen-secrets.sh --retire-supabase-smtp-check`로
호출합니다. 적용은 현재 호스트·Git SHA·공개 Compose source와 소비자 검사에
묶인 짧은 유효기간의 운영자 소유 audit receipt가 필요합니다. SMTP01이 정확한
COMM-003 경로의 유일한 삭제 executor이고 CLN01은 소비자 판정과 보류를 소유합니다.
SMTP01과 CLN01의 잠금은 별개이므로 공통 잠금 검증으로 해석하지 않습니다.
실제 삭제는 현재 소비자·백업·복구 및 운영자 실행 권한 확인 전까지 미실행입니다.

- `secret_catalog.py`: P02의 값 없는 공개 카탈로그·분류·별칭·재생성 거부와 staging view를 검증합니다. 실제 secret/env/KV를 읽거나 변경하지 않습니다.

- `port_inventory.py`: 공개 선언의 네 위치 포트 metadata와 명명된 합성 Compose config를 검증합니다. 실제 listener·인증·HOME 수용은 별도입니다.

## Related Documents

- [스크립트 안내](../../README.md)
- [라이브러리 회귀시험](../../../tests/lib/README.md)
