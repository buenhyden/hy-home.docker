---
title: "Mailpit Policy"
version: "0.4.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0084"
parent_ids:
- "AD-0010"
created: "2026-09-19"
next_review_at: "2027-05-13"
---

# Mailpit Policy

## Purpose and Scope

### Objective

Mailpit은 개발용 이메일을 캡처한다. 일부러 느슨하게 둔 SMTP 설정은 현재 DEV 분류와 loopback/internal 네트워크 경계 안에서만 허용된다.

#### Authority

- [Communication architecture](../../../02.architecture/descriptions/0010-communication-architecture.md)

- [Mailpit Compose source](../../../../infra/11-quality/mailpit/docker-compose.yml)
- [Derived Compose image projection](../../../../infra/tech-stack.versions.json)

### Applies To

`mailpit` 서비스의 활성화, SMTP/UI 접근, 캡처된 메시지 데이터, SQLite 보존, 백업,
업그레이드, 제거를 다룬다.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0084-R1 | Mailpit 선택 시 | 필수: `mail-dev`, `dev`, `local` profile만 쓰고 HOME에 추가하거나 운영 메일함/전송 서비스로 표시하지 않는다 | none | none |
| POL-0084-R2 | 항상 | 필수: loopback host bind와 인증된 gateway 접근을 유지하고 `ACCEPT_ANY`와 안전하지 않은 SMTP 인증 때문에 외부 공개를 금지한다 | none | none |
| POL-0084-R3 | 메시지 캡처 시 | 필수: 캡처 본문·헤더·주소·첨부를 민감 정보로 다루고 가능하면 합성 데이터를 쓰며 최대 5000개 메시지까지만 보존한다 | none | none |
| POL-0084-R4 | 백업 시 | 필수: 실시간 HTTP export를 우선하고 DB 파일 복사 시 Mailpit을 중지해 SQLite DB/WAL sidecar를 일관되게 캡처한다 | 수동 | none |
| POL-0084-R5 | 복원 시 | 필수: 격리된 DEV 인스턴스에만 반입하고 본문을 노출하지 않은 채 개수와 샘플로 검증한 뒤 필요하면 승격을 승인한다 | 수동 | 합성 식별자/개수와 최종 상태 |
| POL-0084-R6 | 자원 운영 | 필수: stateful 매체 템플릿을 유지하고 데이터베이스 크기를 모니터링한다 | none | none |
| POL-0084-R7 | 업그레이드 시 | 필수: 먼저 export하고 릴리스/저장소 변경을 검토한 뒤 Mailpit만 재생성하고 readyz, UI 접근, SMTP 캡처, 보존 개수를 검증한다 | 수동 | 합성 식별자/개수와 최종 상태 |
| POL-0084-R8 | 제거 시 | 필수: bind 디렉터리를 삭제하기 전에 export하거나 보존 메시지의 폐기를 명시적으로 승인받는다 | 수동 | none |

- **Activation:** `mail-dev`, `dev`, `local`을 사용한다. Mailpit을 HOME에 추가하거나
  운영 메일함/전송 서비스로 표시하지 않는다.
- **Access:** loopback host bind와 인증된 gateway 접근을 유지한다. `ACCEPT_ANY`와
  안전하지 않은 SMTP 인증 때문에 외부 공개를 금지한다.
- **Data:** 캡처된 본문, 헤더, 주소, 첨부파일은 민감 정보다. 가능하면 합성 데이터를
  사용하고, 검토된 요구사항이 그 한도를 바꾸지 않는 한 설정된 최대 5000개 메시지까지만
  보존한다.
- **Backup:** 실시간 HTTP export를 우선한다. 데이터베이스 파일을 복사하려면 Mailpit을 중지하고
  SQLite 데이터베이스/WAL sidecar를 일관되게 캡처해야 한다.
- **Restore:** 격리된 DEV 인스턴스에만 반입하고, 메시지 본문을 노출하지 않고 개수와
  샘플을 검증한 뒤 필요하면 승격을 승인한다.
- **Resources:** stateful 매체 템플릿을 유지하고 데이터베이스 크기를 모니터링한다.
  pruning/vacuum 작업은 CPU와 디스크를 소모할 수 있다.
- **Upgrade:** 먼저 export하고, 릴리스/저장소 변경사항을 검토하고, Mailpit만 재생성한
  뒤 readyz, UI 접근, SMTP 캡처, 보존된 개수를 검증한다.
- **Removal:** bind 디렉터리를 삭제하기 전에 export하거나 보존된 메시지의 폐기를 명시적으로
  승인받는다. 컨테이너를 중지/제거해도 데이터는 제거되지 않는다.

#### 접근 경계의 의미

gateway 경로만 SSO를 거친다. 직접 loopback UI와 두 네트워크의 peer listener에는
동등한 네이티브 UI 인증이 선언되지 않았다. 테스트용 SMTP의 임의 인증 수락을
실제 인증으로 해석하지 않는다. 책임자 `@buenhyden`은 이 경계와 테스트 데이터
소유자를 확인해야 하며 신뢰하지 않는 consumer의 연결을 허용해서는 안 된다.

### Exceptions

#### Exception Conditions

외부 노출, SMTP relay/forwarding, 실제 메일, 완화된 보존 요구는 별도의 보안 및 데이터
승인이 필요하다. 일상적인 예외로는 승인할 수 없다.

#### Approval and Review

포트, 인증, 보존, 데이터베이스 경로, 프로필, 이미지가 변경될 때 검토한다.

## Enforcement

### Mechanisms

정적 검사는 메일 캡처나 restore를 증명하지 않는다. 런타임 증거에는 메시지 내용을 남기지 않고
합성 식별자/개수와 최종 상태만 기록해야 한다.

### Limits

다음은 정책이 이름 있는 검사를 보이지 않는 부분이다.

- 정적 검사는 메일 캡처나 restore를 증명하지 않으며 런타임 증거는 합성 식별자/개수와 최종 상태만 남긴다.
- profile 한정, 접근 경계, 보존 한도, 백업/복원/업그레이드/제거 절차는 이름 있는 자동 검사 없이 검토와 승인에 의존한다.
- gateway 경로만 SSO를 거치며 직접 loopback UI와 peer listener에는 동등한 UI 인증이 선언되지 않았다.
- 테스트용 SMTP의 임의 인증 수락은 실제 인증이 아니며 신뢰하지 않는 consumer의 연결은 책임자가 막아야 한다.

## Ownership

### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

### Review Triggers

- [Guide](../../guides/11-mail-and-notifications/0084-mailpit.md) (`GDE-0084`)
- [Runbook](../../runbooks/11-mail-and-notifications/0084-mailpit.md) (`RUN-0084`)

- [Mailpit storage](https://mailpit.axllent.org/docs/configuration/email-storage/)
- [Mailpit runtime options](https://mailpit.axllent.org/docs/configuration/runtime-options/)
- [Operations index](../../README.md)
