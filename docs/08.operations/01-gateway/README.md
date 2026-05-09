# 01-Gateway Operations Policies

> `01-gateway` 티어(Traefik/Nginx) 운영 정책 인덱스.

## Overview (KR)

이 디렉터리는 `infra/01-gateway`의 운영 통제 기준을 정의한다. 기본 진입점은 Traefik이며, Nginx는 특수 경로 프록시로 운용한다.

## Scope

### In Scope

- Traefik 라우터/미들웨어 표준 정책
- Nginx readonly/timeout/failover 정책
- 변경 승인 및 검증 기준

### Out of Scope

- 즉시 실행 절차(런북)
- 튜토리얼/온보딩 가이드

## Structure

```text
01-gateway/
├── traefik.md   # Traefik primary gateway operations policy
├── nginx.md     # Nginx special-path proxy operations policy
└── README.md
```

## Related Documents

- [Gateway Plan](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- [Gateway Tasks](../../06.tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)
- [Gateway Runbooks](../../09.runbooks/01-gateway/README.md)
- [Gateway Guides](../../07.guides/01-gateway/README.md)
- [Infra Source](../../../infra/01-gateway/README.md)

---

## Overview

`docs/08.operations/01-gateway`는 운영 정책, 통제 기준, 검증 방법을 정의하는 operation 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

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
