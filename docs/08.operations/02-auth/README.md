# 08-operations Auth

> Operational and security policies for the 02-auth tier.

---

## Overview (KR)

이 디렉토리는 인증 계층(Keycloak, OAuth2 Proxy 등)의 운영 표준 및 거버넌스 사항을 정의하는 문서를 포함한다.

## Structure

```text
02-auth/
├── keycloak.md     # Keycloak Operations Policy (User, Realm, IdP)
├── oauth2-proxy.md  # OAuth2 Proxy Operational Controls & Sessions
└── README.md        # This file
```

## Available Policies

- **[Keycloak Operations Policy](keycloak.md)**: 사용자 계정 관리, 렐름 변경 통제 및 보안 감사 기준.
- **[OAuth2 Proxy Operational Policy](oauth2-proxy.md)**: 세션 저장소(Valkey) 및 쿠키 만료 정책.

## AI Agent Guidance

1. **Policy Enforcement**: 모든 자동화된 사용자 생성 절차는 `keycloak.md`에 명시된 그룹 계층을 따라야 함.
2. **Access Control**: 비밀번호 초기화 또는 시크릿 갱신 작업 시 승인된 절차를 준수하시오.
