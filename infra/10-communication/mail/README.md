<!-- [ID:10-communication:mail] -->
# ✉️ Mail Infrastructure (mail)

> Production-grade mail server (Stalwart) and development-safe SMTP interceptor (MailHog).

## Overview

이 서비스 유닛은 이메일 송수신을 위한 핵심 인프라를 제공합니다. **Stalwart**는 실제 메일 서비스를 위한 엔터프라이즈급 기능을 제공하며, **MailHog**는 개발 과정에서 외부로 메일이 발송되는 것을 차단하고 로컬에서 확인할 수 있도록 돕습니다.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- **Stalwart Mail Server**: SMTP, IMAP, JMAP 프로토콜 지원 및 관리 UI.
- **MailHog**: 개발용 SMTP 트랩 및 메일 뷰어 UI.
- **Secrets Management**: 관리자 패스워드 주입 로직.
- **Network Configuration**: `infra_net` 연동 및 포트 매핑.

### Out of Scope

- **Domain DNS Management**: DNS 레코드(A, MX) 자체 관리 (클라우드/DNS 공급자 담당).
- **SSL/TLS Certificates Production**: 인증서 발급 프로세스 (Certbot/ZeroSSL 담당).
- **Application Level SMTP Client Logic**: 개별 앱 내의 SMTP 발송 로직.

## Structure

```text
mail/
├── docker-compose.yml    # 서비스 정의 (Stalwart, MailHog)
└── README.md             # This file
```

## Available Scripts

| Command                                        | Description                |
| ---------------------------------------------- | -------------------------- |
| `docker compose --profile communication up -d` | 통신 티어 서비스 전체 시작 |
| `docker compose logs -f stalwart`              | Stalwart 로그 모니터링     |
| `docker compose restart mailhog`               | MailHog 큐 초기화 및 재시작 |

## Configuration

### Environment Variables

| Variable                | Required | Description                                  |
| ----------------------- | -------- | -------------------------------------------- |
| `DEFAULT_URL`           | Yes      | 서비스 접속 주소 베이스 도메인               |
| `DEFAULT_COMMUNICATION_DIR` | Yes  | Stalwart 데이터 저장을 위한 호스트 경로      |
| `SMTP_HOST_PORT`        | No       | 외부 SMTP 수신 포트 (기본: 25)               |
| `STALWART_PORT`         | No       | Stalwart 관리 UI 내부 포트 (기본: 8080)       |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect mail services.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking mail documentation ready.

## Troubleshooting

- Start with `docker compose config` to confirm mail service ports, volumes, and secret references render.
- Check mail service logs and the linked runbook before changing SMTP, IMAP, JMAP, or credential settings.

## Related Documents

- **Guide**: [Mail Services Guide](../../../docs/05.operations/guides/10-communication/mail.md)
- **Operation**: [Mail Operations Policy](../../../docs/05.operations/guides/10-communication/mail.md)
- **Runbook**: [Mail Recovery Runbook](../../../docs/05.operations/guides/10-communication/mail.md)

---

Copyright (c) 2026. Licensed under the MIT License.

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | ✉️ Mail Infrastructure (mail) service leaf in `10-communication`; services: `stalwart`, `mailhog`; root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/10-communication/mail/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | env keys: `STALWART_ADMIN_USER`; profiles: `communication` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/10-communication/mail/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `stalwart-data:/opt/stalwart:rw`, `../../../secrets/certs:/opt/stalwart/certs:ro`, `stalwart-data` |
| Ports | `${SMTP_HOST_PORT:-25}:${SMTP_PORT:-25}`, `${SUBMISSION_HOST_PORT:-587}:${SUBMISSION_PORT:-587}`, `${SMTPS_HOST_PORT:-465}:${SMTPS_PORT:-465}`, `${IMAPS_HOST_PORT:-993}:${IMAPS_PORT:-993}`, `${MANAGESIEVE_HOST_PORT:-4190}:${MANAGESIEVE_PORT:-4190}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.stalwart-ui.rule`, `traefik.http.routers.stalwart-ui.entrypoints`, `traefik.http.routers.stalwart-ui.tls`, `traefik.http.routers.stalwart-ui.middlewares`, `traefik.http.services.stalwart-ui.loadbalancer.server.port`, `traefik.http.routers.mailhog.rule`, plus 4 more |
| Secret refs | names: `stalwart_password`; mounts: `/run/secrets/stalwart_password` |
| Healthcheck | Compose healthcheck declared for `stalwart`, `mailhog` |
| Operations | [Guide](../../../docs/05.operations/guides/10-communication/mail.md), [Policy](../../../docs/05.operations/policies/10-communication/mail.md), [Runbook](../../../docs/05.operations/runbooks/10-communication/mail.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
