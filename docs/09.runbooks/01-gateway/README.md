# 01-Gateway Runbooks

> `01-gateway`(Traefik/Nginx) 즉시 실행 절차 인덱스.

## Overview (KR)

이 디렉터리는 게이트웨이 장애/회귀 상황에서 운영자가 즉시 수행할 복구 절차를 제공한다.

## Structure

```text
01-gateway/
├── traefik.md   # Traefik middleware/auth/route recovery
├── nginx.md     # Nginx readonly/tmpfs/config recovery
└── README.md
```

## Related Documents

- [Gateway Operations](../../08.operations/01-gateway/README.md)
- [Gateway Plan](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- [Gateway Tasks](../../06.tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)
- [Gateway Guides](../../07.guides/01-gateway/README.md)

---

## Overview

`docs/09.runbooks/01-gateway`는 운영자가 즉시 실행할 수 있는 runbook 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 실행 절차와 checklist
- 검증 명령과 evidence source
- rollback 또는 recovery 기준

### Out of Scope

- 정책 결정 자체
- 학습용 튜토리얼
- postmortem 분석

## How to Work in This Area

1. 관련 operation policy를 확인한 뒤 절차, 검증, rollback 항목을 갱신한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
