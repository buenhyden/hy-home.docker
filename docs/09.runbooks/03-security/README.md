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
