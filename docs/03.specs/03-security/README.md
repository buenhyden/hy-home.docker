# 03-security Specifications

> 보안 및 비밀 관리 서비스 기술 사양

## Overview

`docs/03.specs/03-security`는 HashiCorp Vault 기반 시크릿 관리 서비스의 기술 사양을 포함합니다.

## Scope

### In Scope

- Vault 시크릿 엔진, 정책, AppRole 인증 사양
- 시크릿 마운트 패턴 및 접근 경계

### Out of Scope

- 운영 절차 (`docs/05.operations/guides/03-security/` 담당)

## Structure

```text
03-security/
├── spec.md      # Security service technical specification
└── README.md    # This file
```

## Related Documents

- [spec.md](./spec.md)
- [docs/03.specs/README.md](../README.md)
- [infra/03-security/README.md](../../../infra/03-security/README.md)
- [docs/05.operations/guides/03-security/](../../05.operations/guides/03-security/)
