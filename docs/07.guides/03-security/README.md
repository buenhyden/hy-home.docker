# 03-Security Guides

> Vault 운영/개발 가이드 모음

## Overview (KR)

이 디렉터리는 `03-security` 계층의 Vault 사용 가이드를 제공한다. 시크릿 경로 규약, AppRole 부트스트랩, 렌더 출력 확인 절차를 중심으로 optimization/hardening 기준을 설명한다.

## Structure

```text
03-security/
├── 01.setup.md  # 초기 셋업 절차
├── vault.md     # Vault 운영/개발 가이드(최적화/하드닝 반영)
└── README.md    # This file
```

## Available Guides

- [Vault Guide](vault.md): 템플릿 경로 계약, AppRole bootstrap, 렌더 검증 절차
- [Setup Guide](01.setup.md): 보안 티어 초기 구성 절차

## Related References

- [03-security Spec](../../04.specs/03-security/spec.md)
- [03-security Plan](../../05.plans/2026-03-28-03-security-optimization-hardening-plan.md)
- [03-security Tasks](../../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- [03-security Operation](../../08.operations/03-security/vault.md)
- [03-security Runbook](../../09.runbooks/03-security/vault.md)
