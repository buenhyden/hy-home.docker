---
title: "Mailpit Implementation"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
---

# Mailpit

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

개발용 SMTP 트래픽을 캡처합니다. UI와 SMTP 호스트 포트는 loopback에
바인딩되며 UI는 인증된 Traefik을 통해 라우팅됩니다. `MAILPIT_UI_PORT`와
`MAILPIT_SMTP_PORT`는 컨테이너 리스너를 소유하고 `HOST_PORT` 변형은 게시를
소유합니다. `mailpit-data`는 `/data/mailpit.db`를 영속화합니다. 테스트 SMTP는
임의의 인증을 허용하므로 외부에 노출해서는 안 됩니다.

###### Audience
<!-- core-payload-level:4 -->

서비스 설정을 검토하는 운영자와 개발자.

###### Scope
<!-- core-payload-level:4 -->

Lifecycle: **DEV**. 운영 통제와 복구는 [documentation index](../../../docs/README.md)를 거쳐 `docs/05.operations/01.guides/11.mail-and-notifications/0084-mailpit.md`, `docs/05.operations/02.policies/11.mail-and-notifications/0084-mailpit.md`, `docs/05.operations/03.runbooks/11.mail-and-notifications/0084-mailpit.md`(ID: `GDE-0084`, `POL-0084`, `RUN-0084`)가 담당합니다.

###### Structure
<!-- core-payload-level:4 -->

[Compose](docker-compose.yml)가 서비스, 마운트, 네트워크 권한, 엔트리포인트를 소유합니다.

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| UI `127.0.0.1:${MAILPIT_UI_HOST_PORT:-8025}`와 Traefik 라우트 | `mailpit` | 이 README는 소비자를 기록하지 않는다. | Traefik 라우트는 `sso-auth` 게이트웨이 체인을 거치며 loopback·peer 직접 접속에는 native UI 인증이 없다. | Compose 헬스체크가 있고 RUN-0084 Mailpit 런북을 따른다. |
| SMTP `127.0.0.1:${MAILPIT_SMTP_HOST_PORT:-1025}` | `mailpit` | `mail_net` peer와 `opsflow_capture_net`의 n8n-worker | 임의 인증을 허용하는 개발용 SMTP 캡처이며 `mailpit-data`가 `/data/mailpit.db`를 영속화한다. | SMTP 캡처 확인과 복구는 RUN-0084 Mailpit 런북을 따른다. |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

프로필: `mail-dev / local / dev`. 루트 Compose가 이 정의를 include하지만, include 자체만으로는 서비스가 시작되지 않습니다. 네트워크는 Traefik만 함께 붙는 전용 내부 ingress망인 `mailpit_ingress_net`(SPEC-0266), `mail_net`, n8n-worker와만 공유하는 내부 `opsflow_capture_net`입니다. 게이트웨이 인증은 해당 라우트에만 적용되며, loopback UI와 peer의 직접 접속에는 native UI 인증이 선언되어 있지 않습니다. 비공개 값을 출력하지 않고 [공개 환경 변수 키](../../../.env.example)와 [시크릿 참조](../../../secrets/README.md)를 검토합니다.

###### Security Boundary
<!-- core-payload-level:4 -->

UI(`${MAILPIT_UI_HOST_PORT:-8025}`)와 SMTP(`${MAILPIT_SMTP_HOST_PORT:-1025}`)는 `127.0.0.1`에만 게시하고, UI 라우트는 `sso-auth`가 포함된 게이트웨이 체인을 거친다. Compose에는 secret 참조가 선언되어 있지 않다.

#### Usage

##### Prerequisites

런타임 고정 값은 [Compose](docker-compose.yml)에 속합니다. [버전 레지스트리](../../../infra/tech-stack.versions.json)는 파생된 Compose 이미지 프로젝션이며 배포 매니페스트가 아닙니다.

##### Selected Start

변경 작업 중에는 데이터와 자격 증명을 보존합니다. 배포 전에 정확한 런타임 대상을 검토합니다. 운영 절차는 기존 운영 주제(operations subject) 안에 유지합니다.

#### Checks

##### Readiness

저장소 루트에서 문서화된 프로필을 선택하고 `scripts/validation/validate-docker-compose.sh`를 실행합니다. 런타임 확인은 소유 Runbook을 사용합니다. 설정 검증만으로는 유지보수 작업의 성공이나 SMTP 캡처를 증명하지 못합니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
- [11-mail-and-notifications runbooks](../../../docs/05.operations/03.runbooks/11.mail-and-notifications/README.md): RUN-0084 mailpit

###### Observability and Recovery
<!-- core-payload-level:4 -->

Compose에 헬스체크가 선언되어 있으며 SMTP 캡처 확인과 복구는 [11-mail-and-notifications runbooks](../../../docs/05.operations/03.runbooks/11.mail-and-notifications/README.md)의 RUN-0084 Mailpit Runbook을 따른다.

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
