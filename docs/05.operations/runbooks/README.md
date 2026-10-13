---
title: "운영 런북"
version: "0.2.4"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "operations"
---

# 운영 런북

## Overview

Runbook은 적용 조건, 실행 순서, 기대 결과, 중단·검증·복구와 에스컬레이션을 소유한다. 이 인덱스는 현재 목적별 폴더의 README로 연결하고 개별 절차는 각 폴더에서 찾는다.

## Scope

- 포함: 아래 15개 목적별 폴더의 현재 문서와 폴더 README.
- 각 폴더에서 subject 번호·slug와 문서 역할로 대상을 찾는다. 같은 subject는
  Guide·Policy·Runbook에서 같은 번호와 slug를 사용한다.
- LAB는 문서 형식·경로·설명만 포함한다. LAB runtime·서비스 설정·이미지·비밀값·
  데이터의 변경이나 실행을 이 인덱스가 승인하지 않는다.

## Structure

현재 문서는 아래 표의 `01-common/`부터 `15-labs/`까지 실제 번호 폴더에 있다.
폴더 README가 개별 문서 목록을 소유하고 서비스별 적용 조건·다른 역할·구현 원본을
연결한다. 기존 01–13 서비스 티어 제목은 `infra/` 분류의 탐색 anchor이며, 문서
목적 폴더의 번호와 구분한다. 이 인덱스는 subject나 구현 소유권을 추가하지 않는다.

### Cross-cutting system and lifecycle

현재 문서는 아래의 목적별 번호 폴더에서 찾습니다.

### Cross-cutting workspace

작업 공간과 공통 운영 문서도 해당 번호 폴더에서 찾습니다.

### 01 Gateway

게이트웨이와 네트워크 문서는 `02-gateway-and-networking/`에 있습니다.

### 02 Auth

인증과 접근 문서는 `03-identity-and-access/`에 있습니다.

### 03 Security

보안과 비밀값 문서는 `04-security-and-secrets/`에 있습니다.

### 04 Data

데이터베이스와 저장소 문서는 `05-databases-and-storage/`에 있습니다.

### 05 Messaging

메시징과 CDC 문서는 `06-messaging-and-cdc/`에 있습니다.

### 06 Observability

관측 문서는 `07-observability/`에 있습니다.

### 07 Workflow

워크플로와 자동화 문서는 `08-workflows-and-automation/`에 있습니다.

### 08 AI

AI와 검색 문서는 `09-ai-and-search/`에 있습니다.

### 09 Platform Operations

플랫폼과 백업 문서는 `10-platform-and-backup/`에 있습니다.

### 10 Communication

메일과 통지 문서는 `11-mail-and-notifications/`에 있습니다.

### 11 Quality

시험과 품질 문서는 `12-testing-and-quality/`에 있습니다.

### 12 Analytics

분석과 데이터 품질 문서는 `13-analytics-and-data-quality/`에 있습니다.

### 13 Experience

디자인 시스템 문서는 `14-design-system/`에 있습니다.

### Cross-cutting connectivity

교차 연결 문서는 해당 번호 폴더에서 찾습니다.

### 목적별 폴더

| Path | Purpose |
| --- | --- |
| [공통 운영](01-common/README.md) | 초기 점검, 공통 변경과 장애 시 확인·복구의 진입점을 찾는다. |
| [게이트웨이와 네트워크](02-gateway-and-networking/README.md) | Gateway, 인증서, 라우팅과 연결 장애의 점검 절차를 찾는다. |
| [인증과 접근](03-identity-and-access/README.md) | 로그인, client 연결과 인증·세션 실패의 점검 절차를 찾는다. |
| [보안과 비밀값](04-security-and-secrets/README.md) | TLS 점검, 발급·이관과 장애·복구의 승인 조건을 찾는다. |
| [데이터베이스와 저장소](05-databases-and-storage/README.md) | Provision, 접속 장애, backup과 빈 대상 복원 절차를 찾는다. |
| [메시징과 CDC](06-messaging-and-cdc/README.md) | 기동, 수집·소비 장애와 offset·상태 복구 절차를 찾는다. |
| [관측](07-observability/README.md) | Scrape, 대시보드·경보와 로그·추적 장애의 점검 절차를 찾는다. |
| [워크플로와 자동화](08-workflows-and-automation/README.md) | DAG, 게시·통지 실패와 제한 재처리의 점검 절차를 찾는다. |
| [AI와 검색](09-ai-and-search/README.md) | 모델·앱 기동, 인증·GPU 장애와 기존 자료 복구 절차를 찾는다. |
| [플랫폼과 백업](10-platform-and-backup/README.md) | 도구 실행, backup 확인, 복원과 제한 rollback 절차를 찾는다. |
| [메일과 통지](11-mail-and-notifications/README.md) | SMTP·capture 연결과 통지 실패의 점검 절차를 찾는다. |
| [시험과 품질](12-testing-and-quality/README.md) | 품질 도구 실행, 결과 확인과 실패 진단의 절차를 찾는다. |
| [분석과 데이터 품질](13-analytics-and-data-quality/README.md) | SQL·모델·품질 검사와 분석 도구 장애의 절차를 찾는다. |
| [디자인 시스템](14-design-system/README.md) | 빌드·로그인·MCP 호출과 디자인 연동 장애의 절차를 찾는다. |
| [독립 LAB 문서](15-labs/README.md) | 기존 LAB 절차를 찾되 문서 수정이 runtime 실행 권한을 주지는 않는다. |

## Usage

### Audience

- 운영자
- 개발자
- SREs
- 보안 담당자
- AI 에이전트

1. 새 Runbook는 [Runbook template](../../99.templates/templates/operations/runbook.template.md)으로 시작한다.
2. 새 subject 번호는 subject마다 하나를 발급하고, 그 subject의 역할 문서가 같은 번호와 slug를 쓴다.
3. 문서를 추가, 이동, 삭제하면 이 인덱스에 한 줄로 반영한다. 검증기는 모든 구성원이 정확히 한 번 연결되었는지 확인한다.
4. Compose 서비스가 연결된 subject는 Guide/Policy/Runbook 세 역할을 모두 유지한다.
   서비스 연결이 없는 공통·작업 공간 subject는 필요한 역할만 두고 빈 문서를 만들지 않는다.
   공통 통제·절차는 소유 문서로 연결하고 서비스별 적용 조건과 차이를 각 역할에 남긴다.

## Related Documents

- [Operations](../README.md)
- [Guides](../guides/README.md)
- [Policies](../policies/README.md)
- [Runbooks](../runbooks/README.md)
- [Incidents](../incidents/README.md)
- [Documentation protocol](../../../.agents/governance/documentation-protocol.md#role-specific-authoring)
