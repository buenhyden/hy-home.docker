# 01-Gateway Guides

> `01-gateway`(Traefik/Nginx) 설정/운영 이해를 위한 가이드 인덱스.

## Overview (KR)

이 디렉터리는 게이트웨이 구성 이해와 변경 작업 방법을 설명한다. 정책은 `08.operations`, 즉시 복구 절차는 `09.runbooks`를 참조한다.

## Structure

```text
01-gateway/
├── 01.setup.md   # 초기 구성 및 실행 절차
├── traefik.md    # Traefik primary gateway guide
├── nginx.md      # Nginx special-path proxy guide
└── README.md
```

## Related Documents

- [Spec](../../04.specs/01-gateway/spec.md)
- [Operations](../../08.operations/01-gateway/README.md)
- [Runbooks](../../09.runbooks/01-gateway/README.md)
- [Plan](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)

---

## Overview

`docs/07.guides/01-gateway`는 사용자와 운영자가 재현 가능한 작업 방법을 이해하도록 돕는 guide 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

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
