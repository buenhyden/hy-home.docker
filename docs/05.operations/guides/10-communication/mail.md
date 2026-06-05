---
status: active
---
<!-- Target: docs/05.operations/guides/10-communication/mail.md -->

# Mail Usage Guide

## Usage

### Overview (KR)

이 문서는 `10-communication` 메일 구현을 사용하는 방법을 설명한다. 현재 구현은 optional/commented root include인 `infra/10-communication/mail/docker-compose.yml`에 있으며, Stalwart 운영 메일 서버와 MailHog 개발 SMTP 트랩을 제공한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- AI Agent

### Purpose

이 가이드는 사용자가 현재 compose 경계를 이해하고, 개발 메일은 MailHog로 안전하게 캡처하며, Stalwart 운영 승격 전에 필요한 검증 항목을 확인할 수 있도록 돕는다.

### Prerequisites

- root `docker-compose.yml`에서 mail include가 optional/commented 상태임을 확인한다.
- `DEFAULT_COMMUNICATION_DIR`, `DEFAULT_URL`, Docker Secret `stalwart_password`, `secrets/certs` 경계가 운영 환경에 준비되어 있어야 한다.
- Stalwart 직접 바인딩 포트 `25`, `465`, `587`, `993`, `4190`은 운영 승격 전에 호스트/방화벽/DNS 정책과 함께 검증한다.

### Step-by-step Instructions

#### 1. Compose 경계 확인

1. [root docker-compose.yml](../../../../docker-compose.yml)에서 `infra/10-communication/mail/docker-compose.yml` include가 현재 optional/commented인지 확인한다.
2. static 검증은 서비스 로컬 standalone compose가 아니라 root network/secret/template context를 보존하는 검증으로 수행한다.
3. 하드닝 기준을 확인한다: `bash scripts/hardening/check-all-hardening.sh 10-communication`.

#### 2. Stalwart 운영 서버 사용

1. 운영 승격 전에 DNS(MX/SPF/DKIM/DMARC), 인증서, host port 개방, secret evidence를 확보한다.
2. 관리자 UI는 `https://mail.${DEFAULT_URL}` route를 사용하며 Traefik SSO 미들웨어 체인으로 보호된다.
3. 클라이언트는 운영 승인 후 `mail.${DEFAULT_URL}`의 `465` 또는 `587` SMTP Submission과 `993` IMAPS를 사용한다.

#### 3. MailHog 개발 워크플로우

1. 안전한 테스트를 위해 애플리케이션의 SMTP 설정을 다음과 같이 구성합니다:
   - **Host**: `mailhog`
   - **Port**: `1025`
   - **Encryption**: None
2. 하위 앱에서 발송된 모든 메일은 외부로 나가지 않고 `https://mailhog.${DEFAULT_URL}` 웹 UI에서 확인할 수 있습니다.
3. **참고**: MailHog는 데이터를 메모리에 저장하므로 컨테이너 재시작 시 큐가 초기화됩니다.

### Client Configuration (Stalwart)

| Setting | Value |
| :--- | :--- |
| **IMAP Server** | `mail.${DEFAULT_URL}` |
| **IMAP Port** | `993` (SSL/TLS) |
| **SMTP Server** | `mail.${DEFAULT_URL}` |
| **SMTP Port** | `465` (SSL/TLS) or `587` (STARTTLS) |

### Common Pitfalls

- **ISP 포트 차단**: 많은 웹 호스팅/ISP는 포트 25(SMTP)를 기본적으로 차단합니다. 발송 실패 시 릴레이 서비스를 검토하거나 ISP에 해제를 요청하십시오.
- **인증서 만료**: `secrets/certs` 내의 인증서가 만료되면 SMTP/IMAP 연결이 실패할 수 있습니다.
- **standalone compose 검증**: `infra/10-communication/mail/docker-compose.yml`은 root `infra_net`과 secret context에 의존하므로 서비스 로컬 `docker compose config`를 readiness evidence로 사용하지 않는다.

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 10-communication`
- `bash scripts/validation/check-repo-contracts.sh`
- 기대 결과: `10-communication` 하드닝 기준과 문서 stale guard가 실패 없이 통과한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/10-communication/mail.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/10-communication/mail.md)
- [Recovery runbook](../../runbooks/10-communication/mail.md)
