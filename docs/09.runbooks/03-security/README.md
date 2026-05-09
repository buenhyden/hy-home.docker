# 03-Security Runbooks

> Vault 장애 대응 및 복구 실행 절차

## Overview (KR)

이 디렉터리는 `03-security` 계층의 실행형 복구 문서를 제공한다. Vault seal/unseal, raft 상태 점검, audit 점검, agent 렌더 실패 복구 절차를 포함한다.

## Structure

```text
03-security/
├── vault.md   # Vault recovery and maintenance runbook
└── README.md  # This file
```

## Available Runbooks

- [Vault Runbook](vault.md): seal/unseal, raft, audit, render 복구, 안전 롤백 절차

## Related References

- [03-security Spec](../../04.specs/03-security/spec.md)
- [03-security Plan](../../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)
- [03-security Tasks](../../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- [03-security Guide](../../07.guides/03-security/vault.md)
- [03-security Operation](../../08.operations/03-security/vault.md)

---

## Overview

`docs/09.runbooks/03-security`는 운영자가 즉시 실행할 수 있는 runbook 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

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
