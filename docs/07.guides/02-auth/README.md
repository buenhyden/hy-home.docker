# 07-guides Auth

> User and deployment guides for the 02-auth tier.

---

## Overview (KR)

이 디렉토리는 인증 및 권한 관리 시스템(Keycloak, OAuth2 Proxy 등)의 구축, 설정 및 서비스 연동을 위한 가이드를 포함한다.

## Structure

```text
02-auth/
├── keycloak.md     # Keycloak Setup, Realm, OIDC, IdP Configuration
├── oauth2-proxy.md  # OAuth2 Proxy Implementation & SSO Integration
└── README.md        # This file
```

## Available Guides

- **[Keycloak IAM Guide](keycloak.md)**: 중앙 인증 시스템 구축 및 관리 가이드.
- **[OAuth2 Proxy Guide](oauth2-proxy.md)**: 전역 SSO 적용 및 Traefik 미들웨어 연동 가이드.

## AI Agent Guidance

1. **Identity Provisioning**: 신규 서비스 보호가 필요한 경우 `oauth2-proxy.md`를 참고하여 Traefik 미들웨어를 연동하시오.
2. **Authentication Flow**: 사용자 인증에 문제가 있을 경우 `keycloak.md`의 Redirect URI 설정을 먼저 확인하시오.
