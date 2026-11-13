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

#### Overview

기존 n8n의 독립 DEV 통지 소비자 소스와 합성 시험을 보관합니다.

#### Scope

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

없음: 이 디렉터리는 소스, 비활성 workflow, 합성 fixture만 보관하며 `infra/07-workflow/n8n/docker-compose.yml`은 이 폴더를 참조하지 않는다.

## Interfaces

### Inputs and Outputs

없음: 이 디렉터리 자체는 포트나 API를 노출하지 않으며, 워크로드별 입출력은 `hermes-blog-ingestion/`, `manifest-outbox-notifier/`, `task-runner-warmup/` 각 README를 따른다.

### Security Boundary

없음: 이 디렉터리에는 secret 정의와 자격 증명 값이 없다. 실제 import·예약·자격 증명 작업은 Service Role의 Scope가 정한 대로 Task의 선행 조건을 따른다.

## Development

### Local Workflow

#### Usage

각 워크로드 README에서 소스 검증 명령과 운영 대기 조건을 확인합니다.
공통 이미지·Compose·네트워크·CI 등록은 총괄 통합 제안으로 전달합니다.

### Checks

없음: 이 디렉터리 자체의 검사는 없으며, 소스 검증 명령은 각 워크로드 README의 Local Workflow를 따른다.

## Operations

### Runbook Links

이 서비스의 런북은 다음과 같다.

- RUN-0053: `docs/05.operations/runbooks/08-workflows-and-automation/0053-n8n.md`

#### Related Documents

- [기존 n8n](../README.md)
- [Spec Package 탐색](../../../../docs/03.specs/README.md): 정본 Task는 SPEC-0204-TSK-0013입니다.

### Observability and Recovery

없음: 이 디렉터리의 workflow는 비활성이며 자체 헬스체크가 없다. 기존 n8n 서비스의 상태와 복구는 RUN-0053이 소유한다.
