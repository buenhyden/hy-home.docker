# 09-runbooks Auth

> Incident response and maintenance runbooks for the 02-auth tier.

---

## Overview (KR)

이 디렉토리는 인증 계층(Keycloak, OAuth2 Proxy 등)의 장애 대응 및 정기 유지보수를 위한 실행 지침서를 포함한다.

## Structure

```text
02-auth/
├── keycloak.md     # Keycloak Runbook (Seal Recovery, IdP Sync)
├── oauth2-proxy.md  # OAuth2 Proxy Troubleshooting (Session loops)
└── README.md        # This file
```

## Available Runbooks

- **[Keycloak Runbook](keycloak.md)**: 헬스체크 실패 대응, OIDC 리다이렉션 오류 수동 복구.
- **[OAuth2 Proxy Runbook](oauth2-proxy.md)**: 세션 루프 분석 및 쿠키 설정 오류 조치 방법.

## AI Agent Guidance

1. **Recovery Flow**: OIDC 인증 링크 중단 시 `keycloak.md` 및 `oauth2-proxy.md`를 동시에 참조하여 세션 흐름을 분석하시오.
2. **Log Evidence**: 장애 분석 시 `/opt/keycloak/data/log`의 Audit 로그와 Graylog의 인증 실패 메트릭을 먼저 확보하시오.
