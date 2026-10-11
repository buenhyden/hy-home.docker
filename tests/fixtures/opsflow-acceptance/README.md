---
title: "Opsflow acceptance synthetic fixtures"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
created: "2026-10-11"
---

# Opsflow 수용 계약 합성 입력

## Overview

기존 P04 게시 adapter와 P05 통지 계약을 연결하는 오프라인 시험 입력입니다.
소스 revision과 내용 hash는 합성 문자열이며 실제 원문 검증 결과가 아닙니다.

## Scope

SDK·driver는 기존 시험 double을 재사용합니다. PostgreSQL·S3·Airflow·n8n·SMTP에
접속하지 않으며 DB claim·발송·복원·운영 권한을 모의 구현하지 않습니다.
P05 결과 함수는 기존 합성 oracle이며 실제 lease·outbox 상태의 증거가 아닙니다.
Wiki·학습 앱·LAB runtime은 대상에 포함하지 않습니다.

## Structure

- `manifest.valid.json`: 합성 문서 한 건과 결정적인 게시 identity 입력.
- `cases.json`: 경로·partition 거부, ack 유실·잘못된 receipt·재시도 경계.
  UUID와 숫자는 합성 caller 입력이며 실제 lease나 소비자 식별자가 아닙니다.

## Usage

저장소 root에서 실행합니다.

```sh
python3 -m unittest tests.validation.test_opsflow_e2e_acceptance -v
```

조건부 객체 생성·readback 후 게시, DB 실패 뒤 객체 보존·재사용, 게시 identity의
다섯 필드 통지 projection, 성공을 허용하지 않는 실패 결과와 필수 CI 등록을
검증합니다. 잘못된 객체 내용이 있어도 덮어쓰지 않고 게시를 차단합니다.
현재 native binding이 비어 있으면 합성 게시 성공 이후에도 native 실행은 보류됩니다.

## Related Documents

- [합성 fixture family](../README.md)
- [P04 배치](../../../infra/07-workflow/airflow/workloads/manifest-pipeline/README.md)
- [P05 통지](../../../infra/07-workflow/n8n/workloads/manifest-outbox-notifier/README.md)
- [문서 탐색](../../../docs/README.md): 진행 정본은 `SPEC-0204-TSK-0016`입니다.
