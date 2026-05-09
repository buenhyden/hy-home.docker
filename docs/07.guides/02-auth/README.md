# 02-Auth Guides

> `02-auth`(Keycloak/OAuth2 Proxy) 설정·운영 이해를 위한 가이드 인덱스.

## Overview (KR)

이 디렉터리는 인증 계층 구성과 운영 변경 방법을 설명한다. 정책은 `08.operations`, 즉시 복구 절차는 `09.runbooks`를 참조한다.

## Structure

```text
02-auth/
├── keycloak.md      # Keycloak setup and operational guide
├── oauth2-proxy.md  # OAuth2 Proxy integration and hardening guide
└── README.md
```

## Related Documents

- [Spec](../../04.specs/02-auth/spec.md)
- [Operations](../../08.operations/02-auth/README.md)
- [Runbooks](../../09.runbooks/02-auth/README.md)
- [Plan](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)

---

## Overview

`docs/07.guides/02-auth`는 사용자와 운영자가 재현 가능한 작업 방법을 이해하도록 돕는 guide 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- how-to, onboarding, troubleshooting guide
- 관련 infra/operation/runbook 링크
- 작업 전제조건과 흔한 실수

### Out of Scope

- 운영 통제 정책 원문
- 실시간 장애 대응 절차
- secret 값 또는 credential 원문

## How to Work in This Area

1. 관련 `infra/` 서비스 README와 같은 tier의 operation/runbook 문서를 함께 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
