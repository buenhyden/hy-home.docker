# 02-Auth Operations Policies

> `02-auth` 티어(Keycloak/OAuth2 Proxy) 운영 정책 인덱스.

## Overview (KR)

이 디렉터리는 인증 계층의 운영 통제 기준을 정의한다. 기본 정책은 fail-closed이며, degraded-mode는 승인된 절차에서만 제한적으로 허용한다.

## Scope

### In Scope

- Keycloak 시크릿/헬스체크/운영 변경 통제
- OAuth2 Proxy 시크릿 주입/non-root/세션 정책 통제
- 인증 계층 변경 승인 및 검증 기준

### Out of Scope

- 즉시 복구 절차(런북)
- 구현 튜토리얼(가이드)

## Structure

```text
02-auth/
├── keycloak.md      # Keycloak operations policy
├── oauth2-proxy.md  # OAuth2 Proxy operations policy
└── README.md
```

## Related Documents

- [Auth Plan](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- [Auth Tasks](../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- [Auth Spec](../../04.specs/02-auth/spec.md)
- [Auth Procedures](../../07.operations/02-auth/README.md)
- [Auth Usages](../../07.operations/02-auth/README.md)
- [Infra Source](../../../infra/02-auth/README.md)

---

## Overview

`docs/07.operations/02-auth`는 운영 정책, 통제 기준, 검증 방법을 정의하는 operation 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## How to Work in This Area

1. 같은 서비스의 guide와 runbook을 확인해 정책과 실행 절차가 분리되어 있는지 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Usage

> Migrated from `docs/07.operations/02-auth/README.md` during the 2026-05-10 operations taxonomy consolidation.

### 02-Auth Usages

> `02-auth`(Keycloak/OAuth2 Proxy) 설정·운영 이해를 위한 가이드 인덱스.

#### Overview (KR)

이 디렉터리는 인증 계층 구성과 운영 변경 방법을 설명한다. 정책은 `07.operations`, 즉시 복구 절차는 `07.operations`를 참조한다.

#### Structure

```text
02-auth/
├── keycloak.md      # Keycloak setup and operational guide
├── oauth2-proxy.md  # OAuth2 Proxy integration and hardening guide
└── README.md
```

#### Related Documents

- [Spec](../../04.specs/02-auth/spec.md)
- [Operations](../../07.operations/02-auth/README.md)
- [Procedures](../../07.operations/02-auth/README.md)
- [Plan](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)

---

#### Overview

`docs/07.operations/02-auth`는 사용자와 운영자가 재현 가능한 작업 방법을 이해하도록 돕는 guide 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

#### Scope

##### In Scope

- how-to, onboarding, troubleshooting guide
- 관련 infra/operation/runbook 링크
- 작업 전제조건과 흔한 실수

##### Out of Scope

- 운영 통제 정책 원문
- 실시간 장애 대응 절차
- secret 값 또는 credential 원문

#### How to Work in This Area

1. 관련 `infra/` 서비스 README와 같은 tier의 operation/runbook 문서를 함께 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Procedure

> Migrated from `docs/07.operations/02-auth/README.md` during the 2026-05-10 operations taxonomy consolidation.

### 02-Auth Procedures

> `02-auth`(Keycloak/OAuth2 Proxy) 즉시 실행 절차 인덱스.

#### Overview (KR)

이 디렉터리는 인증 장애/회귀 상황에서 운영자가 즉시 수행할 복구 절차를 제공한다.

#### Structure

```text
02-auth/
├── keycloak.md      # Keycloak runtime and secret incident recovery
├── oauth2-proxy.md  # OAuth2 Proxy session loop / degraded-mode recovery
└── README.md
```

#### Related Documents

- [Auth Operations](../../07.operations/02-auth/README.md)
- [Auth Plan](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- [Auth Tasks](../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- [Auth Usages](../../07.operations/02-auth/README.md)
- [Auth Spec](../../04.specs/02-auth/spec.md)

---

#### Overview

`docs/07.operations/02-auth`는 운영자가 즉시 실행할 수 있는 runbook 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

#### Scope

##### In Scope

- 실행 절차와 checklist
- 검증 명령과 evidence source
- rollback 또는 recovery 기준

##### Out of Scope

- 정책 결정 자체
- 학습용 튜토리얼
- postmortem 분석

#### How to Work in This Area

1. 관련 operation policy를 확인한 뒤 절차, 검증, rollback 항목을 갱신한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
