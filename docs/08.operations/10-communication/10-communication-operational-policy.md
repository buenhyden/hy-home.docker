<!-- Target: docs/08.operations/10-communication-operational-policy.md -->

# Operational Policy - 10-communication

## Overview (KR)
이 문서는 전자우편 서비스의 안정적인 운영과 보안을 위한 가이드라인 및 정책을 정의한다.

## Service Level Objectives (SLO)

- **Availability**: 메일 수발신 서비스 가동률 99.5% 유지.
- **Performance**: 내부 SMTP 릴레이 지연 시간 5초 이내.
- **Storage**: 사용자별 메일함 용량 쿼터 관리 가능.

## Maintenance Policy

- **Certificate Renewal**: Stalwart에서 사용하는 TLS 인증서는 Let's Encrypt를 통해 자동 갱신되도록 구성한다.
- **Spam Filtering**: Rspamd 등을 연동하여 스팸 지수 5.0 이상의 메일은 자동으로 스팸함으로 이동시킨다.
- **Data Backup**: `/var/lib/stalwart` 볼륨을 주기적으로 백업하여 메일 데이터 손실을 방지한다.

## Compliance & Security

- **SPF/DKIM/DMARC**: 모든 발신 도메인에 대해 표준 인증 설정을 강제한다.
- **Audit Logging**: 메일 수발신 로그는 최소 90일간 보관한다.
- **Encryption**: 모든 외부 통신은 TLS 1.2 이상을 사용하여 암호화되어야 한다.
