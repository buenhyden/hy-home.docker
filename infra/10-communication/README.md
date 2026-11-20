---
title: "Communication Tier (10-communication)"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2025-11-12"
---

# Communication Tier (10-communication)

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

이 tier에는 현재 root Compose가 include하는 패키지가 없다. 운영 메일 서버
Stalwart와 설정 helper는 SPEC-0262에서 독립 [Stalwart LAB](../../labs/stalwart/docker-compose.yml)으로
옮겼다. 개발용 SMTP 캡처 Mailpit은 [11 Quality](../11-quality/README.md)에서
`dev`, `local`, `mail-dev` profile로 관리하며 `mail_net`을 계속 사용한다.

###### Audience
<!-- core-payload-level:4 -->

애플리케이션 개발자, 메일 서비스 운영자와 인프라 담당자.

###### Scope
<!-- core-payload-level:4 -->

ADR-0062 capability tier 이름과 메일 경계 안내만 유지한다. 메일 내용, 비밀 원문,
도메인 공급자 설정 변경은 범위 밖이다.

###### Structure
<!-- core-payload-level:4 -->

| 대상 | 위치 | 운영 소유자 |
| --- | --- | --- |
| Stalwart LAB | [labs/stalwart/docker-compose.yml](../../labs/stalwart/docker-compose.yml), [설정 자산](../../labs/stalwart/README.md) | `GDE-0070`, `POL-0070`, `RUN-0070` (`docs/05.operations/*/15-labs/`) |
| Mailpit | [11 Quality](../11-quality/mailpit/README.md) | `GDE-0084`, `POL-0084`, `RUN-0084` |

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

없음: 이 tier는 입출력을 제공하지 않는다. HOME 컨테이너의 SMTP는 Mailpit 캡처로만 전달되고 Stalwart LAB은 HOME network에 연결되지 않는다.

###### Security Boundary
<!-- core-payload-level:4 -->

메일 내용과 비밀 원문은 이 tier의 범위 밖이다. Stalwart LAB은 HOME network에 연결되지 않으며 Opsflow notifier는 `stalwart` 호스트를 거부하고 Mailpit으로만 보낸다.

#### Usage

##### Prerequisites

없음: 이 tier에는 root Compose가 include하는 패키지가 없어 지원 런타임이 없다. 메일 서버는 독립 Stalwart LAB이, 개발용 SMTP 캡처는 Mailpit이 맡는다.

##### Selected Start

1. HOME 컨테이너의 SMTP는 Mailpit 캡처를 사용한다. Opsflow notifier도 `stalwart`
   호스트를 거부하고 Mailpit으로만 보낸다.
2. Stalwart LAB은 HOME network에 연결되지 않으므로 HOME 컨테이너가 제출할 수 없다.
   외부 송수신은 DNS·평판을 포함한 새 요구사항이 필요하다.

#### Checks

##### Readiness

저장소 루트에서 실행한다.

```bash
docker compose --env-file .env.example --profile mail-dev config --services
bash scripts/hardening/check-all-hardening.sh 10-communication
```

정적 통과는 실제 메일 배달·수신 또는 데이터 복원 성공의 증거가 아니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

- [LAB source](../../labs/README.md)
- [Infrastructure index](../README.md)
- [11-mail-and-notifications runbooks](../../docs/05.operations/03.runbooks/11.mail-and-notifications/README.md): RUN-0084 mailpit
- [15-labs runbooks](../../docs/05.operations/03.runbooks/15.labs/README.md): RUN-0070 mail

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 이 tier에는 실행 서비스가 없다. 메일 관련 운영은 [Stalwart LAB README](../../labs/stalwart/README.md)와 [11-mail-and-notifications runbooks](../../docs/05.operations/03.runbooks/11.mail-and-notifications/README.md)의 RUN-0084 Mailpit Runbook를 따른다.

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
