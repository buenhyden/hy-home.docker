---
title: "비활성 통지 workflow"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# 비활성 통지 workflow

## Purpose

### Service Role

[manifest-outbox-mailpit.json](manifest-outbox-mailpit.json)은 생성기가 소유하는 공개 초안입니다.

#### Scope

`active:false`와 credential placeholder를 유지합니다. 과거 import·manual·예약 수용은 SPEC-0204 C19/C22의
당시 범위로 보존합니다. 이번 P05 변경의 실제 실행 수용은 Task0044에서 별도 기록합니다.
기본 capture profile은 `mailpit-plain-v1`이며 인증 fixture만
`mailpit-starttls-auth-v1`을 명시 선택합니다. 공개 JSON을 운영 활성화하지 않습니다.

#### Structure

Manual 또는 단일 1분 polling → claim → 입력 검사 → 제한된 SMTP → 수락 확인 → ack입니다.
불확실·오류·stale lease는 retry 결과 확인 또는 고정 오류 경로로 처리합니다.
빈 claim은 downstream item을 만들지 않습니다. ack 실패는 이전 SMTP node에서 재개하지 않습니다.

### Supported Environment

n8n import JSON 하나입니다. 선택 이미지의 native node schema·loader·credential binding 호환성은 선행 계약 이후에 검증하며 이 디렉터리에는 런타임 정의가 없습니다.

## Interfaces

### Inputs and Outputs

입력은 Manual 또는 단일 1분 polling 트리거이고, 출력은 제한된 SMTP node를 거친 Mailpit 캡처 메일과 ack·retry 결과입니다(Structure 참조).

### Security Boundary

`active:false`와 credential placeholder를 유지하고 성공·오류·수동·진행 데이터 저장을 끕니다. output·pinData에 원문 driver 오류나 credential을 넣지 않으며 공개 JSON을 운영 활성화하지 않습니다.

## Development

### Local Workflow

[생성기](../tools/README.md)의 명시적 CLI로 갱신하고 `--check`로 byte parity를 검사합니다.
선택 이미지의 native node schema·loader·credential binding은 선행 계약 이후 검증합니다.
성공·오류·수동·진행 데이터 저장을 끄며, output·pinData에 원문 driver 오류나 credential을 넣지 않습니다.

### Checks

[생성기](../tools/README.md)의 `--check`로 생성 결과와 byte parity를 검사합니다(위 Local Workflow).

## Operations

### Runbook Links

- [워크로드](../README.md)
- [제한된 SMTP node](../nodes/README.md)

### Observability and Recovery

없음: 비활성 JSON이라 이 디렉터리에는 헬스체크·지표가 없습니다. 실행 중 오류·불확실 결과는 workflow의 고정 오류 경로로 처리되며, 복구 절차는 [워크로드 README](../README.md)의 Local Workflow가 소유합니다.
