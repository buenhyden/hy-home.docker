# 03-Security Operations

> Vault 운영 정책 문서 모음

## Overview (KR)

이 디렉터리는 `03-security` 계층의 운영 정책을 관리한다. Vault 하드닝 기준, 단계적 auto-unseal/원격 audit 도입 조건, 검증 기준을 정의한다.

## Structure

```text
03-security/
├── vault.md   # Vault Operations Policy (hardening + phase adoption)
└── README.md  # This file
```

## Available Policies

- [Vault Operations Policy](vault.md): Required/Allowed/Disallowed, 승인 조건, 검증 기준

## Related References

- [03-security Spec](../../04.specs/03-security/spec.md)
- [03-security Plan](../../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)
- [03-security Tasks](../../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- [03-security Guide](../../07.guides/03-security/vault.md)
- [03-security Runbook](../../09.runbooks/03-security/vault.md)

---

## Overview

`docs/08.operations/03-security`는 운영 정책, 통제 기준, 검증 방법을 정의하는 operation 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 운영 정책과 controls
- 허용/금지/예외 기준
- 검증 방법과 review cadence

### Out of Scope

- 단계별 복구 절차
- 튜토리얼 문서
- incident timeline

## How to Work in This Area

1. 같은 서비스의 guide와 runbook을 확인해 정책과 실행 절차가 분리되어 있는지 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
