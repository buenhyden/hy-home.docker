# 08-operations Security

> Security and compliance operational policies for the 03-security tier.

---

## Overview (KR)

이 디렉토리는 보안 계층(Vault 등)의 운영 표준 및 보안 준수 사항을 정의하는 문서를 포함한다.

## Structure

```text
03-security/
├── vault.md    # Vault Operations Policy (Unseal, Token TTL, Audit)
└── README.md   # This file
```

## Available Policies

- **[Vault Operations Policy](vault.md)**: Unseal Key 관리, 토큰 만료 정책, 그리고 시스템 감사 체계.

## AI Agent Guidance

1. **Policy Enforcement**: 모든 자동화 프로세스는 `vault.md`에 명시된 토큰 TTL 및 인증 정책을 준수해야 함.
2. **Access Audit**: 권한 상승(Privilege Escalation) 작업 시 반드시 감사 로그가 생성되는지 확인하시오.
