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
