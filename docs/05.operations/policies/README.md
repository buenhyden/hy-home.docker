---
title: "운영 정책"
version: "0.2.3"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "operations"
---

# 운영 정책

## Overview

### Overview

Policy는 무엇이 허용되고 금지되는지, 누가 승인하는지, 예외와 검토 주기를 소유한다. 명령 순서는 소유하지 않고 같은 slug의 Runbook에 둔다. 에이전트 실행 규칙은 `.agents/`가 소유한다.

## Scope

### Scope

- 이 디렉터리의 모든 Policy를 도메인별로 한 번씩 나열한다.
- 파일 이름은 `####-<slug>.md`이고 `####`는 문서 자신의 artifact 번호다.
- 같은 slug는 다른 역할 디렉터리에서 같은 subject를 가리킨다.

## Structure

### Structure

도메인은 경로가 아니라 이 인덱스의 분류다. `관련 문서` 열은 같은 subject의
다른 역할 문서를 가리킨다.

시스템 전반의 기동·인증·복구·용량·업데이트는 아래 공통 분류에서 시작한다.
티어별 서비스는 01–13 분류에서 찾고, 행의 관련 문서로 같은 subject의 다른 역할을
확인한다. 작업 공간과 공통 연결은 번호 없는 분류이며 별도 인프라 티어가 아니다.
서비스와 공통 문서의 연결은 적용 범위를 설명하며 서비스 소유권을 추가하지 않는다.

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

| 운영 범위 | 문서 역할 |
| --- | --- |
| [공통 운영](01-common/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [게이트웨이와 네트워크](02-gateway-and-networking/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [인증과 접근](03-identity-and-access/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [보안과 비밀값](04-security-and-secrets/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [데이터베이스와 저장소](05-databases-and-storage/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [메시징과 CDC](06-messaging-and-cdc/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [관측](07-observability/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [워크플로와 자동화](08-workflows-and-automation/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [AI와 검색](09-ai-and-search/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [플랫폼과 백업](10-platform-and-backup/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [메일과 통지](11-mail-and-notifications/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [시험과 품질](12-testing-and-quality/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [분석과 데이터 품질](13-analytics-and-data-quality/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [디자인 시스템](14-design-system/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |
| [독립 LAB 문서](15-labs/README.md) | 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다. |

## Usage

### Audience

- 운영자
- 개발자
- SREs
- 보안 담당자
- AI 에이전트

### Usage

1. 새 Policy는 [Policy template](../../99.templates/templates/operations/policy.template.md)으로 시작한다.
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
