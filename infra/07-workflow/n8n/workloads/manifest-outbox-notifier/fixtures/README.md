---
title: "독립 통지 합성 fixture"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# 독립 통지 합성 fixture

## Purpose

### Service Role

[cases.json](cases.json)은 공개 합성 claim·수락/ack 유실·retry/stale lease 기대 결과입니다.

#### Scope

UUID·run ID·주소는 합성이며 운영 token이나 credential이 아닙니다. DB/SMTP/native 수용 증거를 포함하지 않습니다.

#### Structure

닫힌 claim, 상태별 기대 결과, 개인정보 누출 검사 marker와 아직 필요한 native 실패·복구 사례를 둡니다.

### Supported Environment

별도 런타임이나 이미지가 없습니다. `cases.json`은 전용 Python 상태 시험과 제한된 SMTP node 시험이 읽는 JSON 데이터입니다.

## Interfaces

### Inputs and Outputs

이 디렉터리 자체의 입력은 없고, `cases.json`이 소비 시험에 합성 claim·수락/ack 유실·retry/stale lease 사례와 기대 결과를 제공합니다.

### Security Boundary

없음: UUID·run ID·주소는 합성이며 credential·token을 담지 않고 네트워크 리스너도 없습니다.

## Development

### Local Workflow

전용 Python 상태 시험과 제한된 SMTP node 시험에서 사용합니다. malformed·다중 claim·header injection·
수락 목록·timeout·취소와 원문 오류 누출도 각각 부정 사례로 검사합니다.
lease 만료·동시 claim·attempt cap/dead·공식 requeue는 실제 SQL/native 시험에서 별도
검증합니다. SQL007은 개별 승인마다 한 번의 no-send 추가 claim과 복원 sending의 unknown
격리를 제공하지만 이 fixture 목록 자체가 실제 SQL·SMTP 검증은 아닙니다.

### Checks

독립 실행 검사는 없습니다. 이 fixture를 읽는 전용 Python 상태 시험과 [SMTP node 시험](../nodes/OpsflowSmtp/tests/README.md)이 검사 경로입니다.

## Operations

### Runbook Links

- [워크로드](../README.md)
- [초안 계약](../outbox-contract.json)

### Observability and Recovery

없음: 데이터 파일이라 헬스체크·지표가 없고 복구할 상태도 없습니다. 사례가 어긋나면 이를 읽는 시험이 실패하며, 복구는 Git 이력에서 파일 변경을 되돌리는 것입니다.
