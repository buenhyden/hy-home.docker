<!-- Target: docs/07.guides/10-communication/mail.md -->

# Mail Services Guide

> `hy-home.docker` 환경에서 메일 서버(Stalwart) 및 개발용 트랩(MailHog)을 관리하고 사용하는 통합 가이드입니다.

---

## Overview (KR)

이 문서는 시스템의 메일 인프라 구성과 개발 워크플로우에 대한 가이드를 제공합니다. 실제 메일 서비스 운영을 위한 **Stalwart** 설정과 안전한 개발 테스트를 위한 **MailHog** 사용법을 다룹니다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator
- Agent-tuner

## Purpose

이 가이드는 사용자가 메일 서버의 운영 환경을 구성하고, 개발 과정에서 안전하게 이메일 발송 기능을 테스트할 수 있도록 돕는 것을 목적으로 합니다.

## Prerequisites

- **호스트 포트 점검**: 25, 465, 587, 993 포트가 호스트에서 사용 가능해야 합니다.
- **SSL 인증서**: `secrets/certs` 내에 유효한 도메인 인증서가 존재해야 합니다.
- **관리자 암호**: Docker Secret `stalwart_password`가 사전에 생성되어 있어야 합니다.

## Step-by-step Instructions

### 1. Stalwart 운영 서버 설정 (Production)
1. `infra/10-communication/mail` 디렉토리로 이동합니다.
2. 서비스를 시작합니다: `docker-compose --profile communication up -d stalwart`
3. 관리자 UI(`https://mail.${DEFAULT_URL}`)에 접속하여 로그인이 정상적으로 수행되는지 확인합니다.
4. **DNS 연동**: 관리자 UI의 `Settings > Domains` 메뉴에서 제공하는 MX, SPF, DKIM, DMARC 레코드를 DNS 공급자에 등록합니다.

### 2. MailHog 개발 워크플로우 (Development)
1. 안전한 테스트를 위해 애플리케이션의 SMTP 설정을 다음과 같이 구성합니다:
   - **Host**: `mailhog`
   - **Port**: `1025`
   - **Encryption**: None
2. 하위 앱에서 발송된 모든 메일은 외부로 나가지 않고 `https://mailhog.${DEFAULT_URL}` 웹 UI에서 확인할 수 있습니다.
3. **참고**: MailHog는 데이터를 메모리에 저장하므로 컨테이너 재시작 시 큐가 초기화됩니다.

## Client Configuration (Stalwart)

| Setting | Value |
| :--- | :--- |
| **IMAP Server** | `mail.${DEFAULT_URL}` |
| **IMAP Port** | `993` (SSL/TLS) |
| **SMTP Server** | `mail.${DEFAULT_URL}` |
| **SMTP Port** | `465` (SSL/TLS) or `587` (STARTTLS) |

## Common Pitfalls

- **ISP 포트 차단**: 많은 웹 호스팅/ISP는 포트 25(SMTP)를 기본적으로 차단합니다. 발송 실패 시 릴레이 서비스를 검토하거나 ISP에 해제를 요청하십시오.
- **인증서 만료**: `secrets/certs` 내의 인증서가 만료되면 SMTP/IMAP 연결이 실패할 수 있습니다.

## Related Documents

- **Operation**: [Mail Operations Policy](../08.operations/10-communication/mail.md)
- **Runbook**: [Mail Recovery Runbook](../09.runbooks/10-communication/mail.md)
