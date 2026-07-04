---
status: active
---
<!-- Target: docs/05.operations/policies/10-communication/mail.md -->

# Mail Operations Policy

## Overview

이 문서는 `10-communication` 티어의 메일 서비스 운영 정책을 정의합니다. 시스템 가용성, 데이터 보존, 보안 통제 기준 및 검증 방법을 포함합니다.

## Policy Scope

메일 서버(Stalwart)의 보안 설정, 계정 관리, 데이터 보존 경계 및 개발용 트랩(MailHog)의 운영 범위를 규정합니다.

- **Systems**: Stalwart, MailHog
- **Agents**: Docker Operator, AI Agent
- **Environments**: Optional production promotion path (Stalwart), development mail trapping (MailHog)

## Controls

- **Required**:
  - 모든 발신 도메인에 대해 SPF, DKIM, DMARC 레코드를 DNS에 유지해야 함.
  - SMTP Submission(587), SMTPS(465), IMAPS(993) 연결은 운영 승격 전에 TLS evidence를 확보해야 함.
  - 관리자 패스워드는 Docker Secrets를 통해 관리해야 함.
  - Stalwart Admin/JMAP UI와 MailHog UI는 Traefik `gateway-standard-chain@file,sso-errors@file,sso-auth@file` 미들웨어 체인으로 보호해야 함.
  - `infra_net` static IP는 authoritative mapping `172.19.0.228`(Stalwart), `172.19.0.229`(MailHog)를 사용해야 함.
- **Allowed**:
  - 개발 환경에서의 MailHog를 통한 자유로운 메일 캡처 및 테스트.
  - 운영 승격 전 optional/commented root include 상태로 static hardening 검증만 수행.
- **Disallowed**:
  - 인증되지 않은 릴레이(Open Relay) 설정은 엄격히 금지됨.
  - 서비스 로컬 standalone compose render를 root readiness evidence로 사용하는 행위.

## Persistence & Backups

- **Data Retention**: Stalwart의 메일 데이터는 `${DEFAULT_COMMUNICATION_DIR}/stalwart/data`가 바인드된 `stalwart-data` 볼륨에 보존됩니다.
- **Backup Schedule**: 현재 compose에는 백업 스케줄이 선언되어 있지 않다. 운영 승격 전 백업/복구 방식과 evidence를 별도 승인해야 한다.
- **MailHog Data**: MailHog는 인메모리 저장소를 사용하므로 별도의 데이터 보존 정책을 두지 않습니다.

## Exceptions

N/A — 현재 승인된 예외 없음.

## Verification

- `bash scripts/hardening/check-all-hardening.sh 10-communication`
- `bash scripts/validation/check-repo-contracts.sh`
- 운영 승격 시 DNS(MX/SPF/DKIM/DMARC), TLS, host port 개방, Docker Secret evidence를 별도로 기록한다.

## Review Cadence

- Quarterly (분기별 보안 및 운영 정책 검토)

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/10-communication/mail.md)
- [Recovery runbook](../../runbooks/10-communication/mail.md)
