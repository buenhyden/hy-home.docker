---
title: "운영 런북"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
---

# 운영 런북

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

#### Responsibility

##### Purpose

###### Purpose and Readers
<!-- core-payload-level:4 -->

Runbook은 적용 조건, 실행 순서, 기대 결과, 중단·검증·복구와 에스컬레이션을 소유한다. 이 인덱스는 현재 목적별 폴더의 README로 연결하고 개별 절차는 각 폴더에서 찾는다.

###### Audience
<!-- core-payload-level:4 -->

- 운영자
- 개발자
- SREs
- 보안 담당자

###### Inputs and Outputs
<!-- core-payload-level:4 -->

- 포함: 아래 15개 목적별 폴더의 현재 문서와 폴더 README.
- 각 폴더에서 subject 번호·slug와 문서 역할로 대상을 찾는다. 같은 subject는
  Guide·Policy·Runbook에서 같은 번호와 slug를 사용한다.

##### Excluded Responsibilities

- LAB는 문서 형식·경로·설명만 포함한다. LAB runtime·서비스 설정·이미지·비밀값·
  데이터의 변경이나 실행을 이 인덱스가 승인하지 않는다.

#### Current Contents

##### Paths

###### Current Items
<!-- core-payload-level:4 -->

현재 문서는 아래 표의 `01.common/`부터 `15.labs/`까지 실제 번호 폴더에 있다.
폴더 README가 개별 문서 목록을 소유하고 서비스별 적용 조건·다른 역할·구현 원본을
연결한다. 기존 01–13 서비스 티어 제목은 `infra/` 분류의 탐색 anchor이며, 문서
목적 폴더의 번호와 구분한다. 이 인덱스는 subject나 구현 소유권을 추가하지 않는다.

###### Cross-cutting system and lifecycle
<!-- core-payload-level:4 -->

현재 문서는 아래의 목적별 번호 폴더에서 찾습니다.

###### Cross-cutting workspace
<!-- core-payload-level:4 -->

작업 공간과 공통 운영 문서도 해당 번호 폴더에서 찾습니다.

###### 01 Gateway
<!-- core-payload-level:4 -->

게이트웨이와 네트워크 문서는 `02.gateway-and-networking/`에 있습니다.

###### 02 Auth
<!-- core-payload-level:4 -->

인증과 접근 문서는 `03.identity-and-access/`에 있습니다.

###### 03 Security
<!-- core-payload-level:4 -->

보안과 비밀값 문서는 `04.security-and-secrets/`에 있습니다.

###### 04 Data
<!-- core-payload-level:4 -->

데이터베이스와 저장소 문서는 `05.databases-and-storage/`에 있습니다.

###### 05 Messaging
<!-- core-payload-level:4 -->

메시징과 CDC 문서는 `06.messaging-and-cdc/`에 있습니다.

###### 06 Observability
<!-- core-payload-level:4 -->

관측 문서는 `07.observability/`에 있습니다.

###### 07 Workflow
<!-- core-payload-level:4 -->

워크플로와 자동화 문서는 `08.workflows-and-automation/`에 있습니다.

###### 08 AI
<!-- core-payload-level:4 -->

AI와 검색 문서는 `09.ai-and-search/`에 있습니다.

###### 09 Platform Operations
<!-- core-payload-level:4 -->

플랫폼과 백업 문서는 `10.platform-and-backup/`에 있습니다.

###### 10 Communication
<!-- core-payload-level:4 -->

메일과 통지 문서는 `11.mail-and-notifications/`에 있습니다.

###### 11 Quality
<!-- core-payload-level:4 -->

시험과 품질 문서는 `12.testing-and-quality/`에 있습니다.

###### 12 Analytics
<!-- core-payload-level:4 -->

분석과 데이터 품질 문서는 `13.analytics-and-data-quality/`에 있습니다.

###### 13 Experience
<!-- core-payload-level:4 -->

디자인 시스템 문서는 `14.design-system/`에 있습니다.

###### Cross-cutting connectivity
<!-- core-payload-level:4 -->

교차 연결 문서는 해당 번호 폴더에서 찾습니다.

###### 목적별 폴더
<!-- core-payload-level:4 -->

| Path | Purpose |
| --- | --- |
| [공통 운영](01.common/README.md) | 초기 점검, 공통 변경과 장애 시 확인·복구의 진입점을 찾는다. |
| [게이트웨이와 네트워크](02.gateway-and-networking/README.md) | Gateway, 인증서, 라우팅과 연결 장애의 점검 절차를 찾는다. |
| [인증과 접근](03.identity-and-access/README.md) | 로그인, client 연결과 인증·세션 실패의 점검 절차를 찾는다. |
| [보안과 비밀값](04.security-and-secrets/README.md) | TLS 점검, 발급·이관과 장애·복구의 승인 조건을 찾는다. |
| [데이터베이스와 저장소](05.databases-and-storage/README.md) | Provision, 접속 장애, backup과 빈 대상 복원 절차를 찾는다. |
| [메시징과 CDC](06.messaging-and-cdc/README.md) | 기동, 수집·소비 장애와 offset·상태 복구 절차를 찾는다. |
| [관측](07.observability/README.md) | Scrape, 대시보드·경보와 로그·추적 장애의 점검 절차를 찾는다. |
| [워크플로와 자동화](08.workflows-and-automation/README.md) | DAG, 게시·통지 실패와 제한 재처리의 점검 절차를 찾는다. |
| [AI와 검색](09.ai-and-search/README.md) | 모델·앱 기동, 인증·GPU 장애와 기존 자료 복구 절차를 찾는다. |
| [플랫폼과 백업](10.platform-and-backup/README.md) | 도구 실행, backup 확인, 복원과 제한 rollback 절차를 찾는다. |
| [메일과 통지](11.mail-and-notifications/README.md) | SMTP·capture 연결과 통지 실패의 점검 절차를 찾는다. |
| [시험과 품질](12.testing-and-quality/README.md) | 품질 도구 실행, 결과 확인과 실패 진단의 절차를 찾는다. |
| [분석과 데이터 품질](13.analytics-and-data-quality/README.md) | MLflow 추적 서버 장애와 복구의 절차를 찾는다. |
| [디자인 시스템](14.design-system/README.md) | 빌드·로그인·MCP 호출과 디자인 연동 장애의 절차를 찾는다. |
| [독립 LAB 문서](15.labs/README.md) | 기존 LAB 절차를 찾되 문서 수정이 runtime 실행 권한을 주지는 않는다. |

###### Classification
<!-- core-payload-level:4 -->

분류는 `01.common/`부터 `15.labs/`까지 15개 번호 폴더이며 이 인덱스는 Runbook 역할만 소유한다. 같은 subject의 다른 역할 문서는 있는 경우 같은 번호와 slug로 다른 역할 인덱스에 있다.

##### Owners

이 README의 소유자는 frontmatter `owner`의 `@buenhyden`이다. 목록에 있는 각 항목의 소유자는 이 README가 따로 기록하지 않는다.

#### Usage

##### Entry Points

###### Upstream and Downstream
<!-- core-payload-level:4 -->

- [Operations](../README.md)
- [Guides](../01.guides/README.md)
- [Policies](../02.policies/README.md)
- [Incidents](../04.incidents/README.md)

###### Policy and Templates
<!-- core-payload-level:4 -->

- [Documentation protocol](../../00.workspace/03.process/documentation-protocol.md#role-specific-authoring)
- [README 템플릿](../../99.templates/02.templates/93.common/readme-stage.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다

##### Checks

###### Create and Review
<!-- core-payload-level:4 -->

1. 새 Runbook는 [Runbook template](../../99.templates/02.templates/05.operations/runbook.template.md)으로 시작한다.
2. 새 subject 번호는 subject마다 하나를 발급하고, 그 subject의 역할 문서가 같은 번호와 slug를 쓴다.
3. 문서를 추가, 이동, 삭제하면 이 인덱스에 한 줄로 반영한다. 검증기는 모든 구성원이 정확히 한 번 연결되었는지 확인한다.
4. Compose 서비스가 연결된 subject는 Guide/Policy/Runbook 세 역할을 모두 유지한다.
   서비스 연결이 없는 공통·작업 공간 subject는 필요한 역할만 두고 빈 문서를 만들지 않는다.
   공통 통제·절차는 소유 문서로 연결하고 서비스별 적용 조건과 차이를 각 역할에 남긴다.

###### Transition and Exit
<!-- core-payload-level:4 -->

문서는 `operational-policy` 수명주기(draft, in-review, active, deprecated, superseded, retired)를 따른다. superseded 또는 retired에 이른 문서는 [은퇴 전제 조건](../../00.workspace/03.process/documentation-protocol.md#retirement-preconditions)을 모두 충족할 때에만 남아야 할 내용을 소유 문서에 요약한 뒤 삭제하고, 번호를 Registry `reserved_history`에 추가하며, 이 목록의 행과 링크를 같은 변경에서 제거한다. 검증기는 모든 구성원이 정확히 한 번 연결되었는지 확인한다.

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
