---
title: "n8n 독립 워크로드"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# n8n 독립 워크로드

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Service

##### Purpose

###### Overview
<!-- core-payload-level:4 -->

기존 n8n의 독립 DEV 통지 소비자 소스와 합성 시험을 보관합니다.

###### Scope
<!-- core-payload-level:4 -->

공개 소스·비활성 workflow·합성 fixture에 한정합니다. SQL과 게시 배치는
Airflow의 P04가 소유하며, 실제 import·예약·자격 증명 작업은 Task의 선행 조건을 따릅니다.

###### Structure
<!-- core-payload-level:4 -->

- [매니페스트 outbox 통지](manifest-outbox-notifier/README.md): 결정적 생성기,
  제한된 SMTP node와 합성 시험입니다.
- [Hermes 수집 전송](hermes-blog-ingestion/README.md): Hermes 호스트의 직접 제출을
  서버 A의 Blog-data Gateway로 전달하는 비활성 흐름과 복구용 로컬 영속 대기함입니다.
- [Task Runner 예열](task-runner-warmup/README.md): Hermes 정기 실행 전에 JS runner를
  미리 띄우는 비활성 흐름입니다.

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

없음: 이 디렉터리 자체는 포트나 API를 노출하지 않으며, 워크로드별 입출력은 `hermes-blog-ingestion/`, `manifest-outbox-notifier/`, `task-runner-warmup/` 각 README를 따른다.

###### Security Boundary
<!-- core-payload-level:4 -->

없음: 이 디렉터리에는 secret 정의와 자격 증명 값이 없다. 실제 import·예약·자격 증명 작업은 Purpose의 Scope가 정한 대로 Task의 선행 조건을 따른다.

#### Usage

##### Prerequisites

없음: 이 디렉터리는 소스, 비활성 workflow, 합성 fixture만 보관하며 `infra/07-workflow/n8n/docker-compose.yml`은 이 폴더를 참조하지 않는다.

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

각 워크로드 README에서 소스 검증 명령과 운영 대기 조건을 확인합니다.
공통 이미지·Compose·네트워크·CI 등록은 총괄 통합 제안으로 전달합니다.

#### Checks

##### Readiness

없음: 이 디렉터리 자체의 검사는 없으며, 소스 검증 명령은 각 워크로드 README의 Selected Start를 따른다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

이 서비스의 런북은 다음과 같다.

- RUN-0053: `docs/05.operations/03.runbooks/08.workflows-and-automation/0053-n8n.md`

###### Related Documents
<!-- core-payload-level:4 -->

- [기존 n8n](../README.md)
- [Spec Package 탐색](../../../../docs/03.specs/README.md): 정본 Task는 SPEC-0204-TSK-0013입니다.

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 이 디렉터리의 workflow는 비활성이며 자체 헬스체크가 없다. 기존 n8n 서비스의 상태와 복구는 RUN-0053이 소유한다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
