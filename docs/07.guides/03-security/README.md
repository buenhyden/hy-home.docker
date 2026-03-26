# 03-security Guides

> Operational and setup guides for the security infrastructure tier.

---

## Overview (KR)

이 디렉토리는 `03-security` 계층(Vault 등)의 설정, 연동 및 활용을 위한 상세 가이드를 포함한다.

## Structure

```text
03-security/
├── 01.setup.md # Initial bootstrapping
├── vault.md    # Comprehensive Vault Guide (OIDC, Secrets Migration)
└── README.md   # This file
```

## Available Guides

- **[Vault Guide](vault.md)**: Vault 초기화, 봉인 해제, Keycloak 연동 및 비밀 마이그레이션 방법.
- **[Setup Guide](01.setup.md)**: 보안 티어의 전반적인 초기 구축 절차.

## AI Agent Guidance

1. **Task Context**: 보안 관련 작업 시 반드시 `vault.md`의 Unseal 절차를 우선 참조하시오.
2. **Migration**: 비밀 정보의 영구 저장소로 Vault KV-v2 엔진을 사용함을 원칙으로 함.
