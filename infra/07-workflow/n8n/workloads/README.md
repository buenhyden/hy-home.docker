---
title: "n8n 독립 워크로드"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# n8n 독립 워크로드

## Purpose

### Service Role

기존 n8n의 독립 DEV 통지 소비자 소스와 합성 시험을 보관합니다.

공개 소스·비활성 workflow·합성 fixture에 한정합니다. SQL과 게시 배치는
Airflow의 P04가 소유하며, 실제 import·예약·자격 증명 작업은 Task의 선행 조건을 따릅니다.

#### Structure

- [매니페스트 outbox 통지](manifest-outbox-notifier/README.md): 결정적 생성기,
  제한된 SMTP node와 합성 시험입니다.
- [Hermes 수집 전송](hermes-blog-ingestion/README.md): Hermes 호스트의 직접 제출을
  서버 A의 Blog-data Gateway로 전달하는 비활성 흐름과 복구용 로컬 영속 대기함입니다.
- [Task Runner 예열](task-runner-warmup/README.md): Hermes 정기 실행 전에 JS runner를
  미리 띄우는 비활성 흐름입니다.

### Supported Environment

없음: 이 디렉터리에는 Compose 파일이나 Dockerfile이 없어 독립 런타임 환경을 선언하지 않는다. 포함 항목은 `hermes-blog-ingestion/`, `manifest-outbox-notifier/`, `task-runner-warmup/`이다.

## Interfaces

### Inputs and Outputs

없음: 이 디렉터리는 자체 포트나 네트워크 인터페이스를 선언하지 않으며, 인터페이스는 하위 `hermes-blog-ingestion/`, `manifest-outbox-notifier/`, `task-runner-warmup/`가 각자 선언한다.

### Security Boundary

없음: 이 디렉터리는 Compose 서비스나 secret 참조를 직접 선언하지 않으며, 하위 `hermes-blog-ingestion/`, `manifest-outbox-notifier/`, `task-runner-warmup/`가 각자 선언한다.

## Development

### Local Workflow

각 워크로드 README에서 소스 검증 명령과 운영 대기 조건을 확인합니다.
공통 이미지·Compose·네트워크·CI 등록은 총괄 통합 제안으로 전달합니다.

### Checks

없음: 이 디렉터리는 자체 테스트나 검증 스크립트를 두지 않으며, 하위 `hermes-blog-ingestion/`, `manifest-outbox-notifier/`, `task-runner-warmup/`가 각자 둔다.

## Operations

### Runbook Links

#### Related Documents

- [기존 n8n](../README.md)
- [Spec Package 탐색](../../../../docs/03.specs/README.md): 정본 Task는 SPEC-0204-TSK-0013입니다.

### Observability and Recovery

없음: 이 디렉터리는 자체 헬스체크나 관측 대상을 선언하지 않으며, 하위 `hermes-blog-ingestion/`, `manifest-outbox-notifier/`, `task-runner-warmup/`가 각자 선언한다.
