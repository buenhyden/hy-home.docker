<!-- Target: docs/01.prd/2026-03-26-10-communication.md -->

# Communication Tier (10-communication) Product Requirements

## Overview (KR)

이 문서는 `10-communication` 계층의 제품 요구사항을 정의한다. 이 계층은 시스템의 모든 메일 및 메시지 통신 인프라를 담당하며, 개발용 SMTP 샌드박스와 운영용 메일 서버를 통합하여 안전하고 신뢰할 수 있는 메시징 환경을 구축하는 것을 목표로 한다.

## Vision

모든 알림 및 통신 데이터가 보안 가이드라인에 따라 안전하게 처리되고, 개발 단계에서의 실수로 인한 오발송을 원천 차단하는 지능형 통신 허브를 제공한다.

## Problem Statement

현재 메일 발송 로직이 파편화되어 있고, 성능 및 보안 정책이 일관되지 않아 대규모 알림 처리 시 신뢰성을 보장하기 어렵다. 또한 개발 환경에서 실제 운영 메일이 발송될 위험이 존재한다.

## Personas

- **Developer**: 개발 과정에서 서버에서 발송되는 메일을 실제 수신함이 아닌 로컬 샌드박스에서 즉시 확인하고 싶어 한다.
- **Admin**: 운영 메일 서버의 전송 성공률(Deliverability)을 높이고, 스팸 차단 정책(SPF, DKIM)을 중앙에서 관리하고 싶어 한다.
- **Security Officer**: 모든 외부 통신이 암호화되고 인증된 사용자만 메일을 발송할 수 있도록 통제하고 싶어 한다.

## Key Use Cases

- **STORY-01**: 개발자는 MailHog UI를 통해 테스트용 메일이 실제로 외부로 나가지 않고 정상적으로 캡처되었는지 확인한다.
- **STORY-02**: 시스템은 Stalwart를 통해 사용자 가입 환영 메일을 암호화된 채널로 안전하게 발송한다.
- **STORY-03**: 관리자는 외부 메일 서비스로의 발송 시 스팸으로 분류되지 않도록 Stalwart에 SPF/DKIM 설정을 적용한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: 개발용 SMTP 트랩 서비스 제공 (MailHog).
- **REQ-PRD-FUN-02**: 운영용 고성능 IMAP/SMTP/JMAP 메일 서버 제공 (Stalwart).
- **REQ-PRD-FUN-03**: 메일 전송 데이터의 실시간 UI 모니터링 및 검색 지원.
- **REQ-PRD-FUN-04**: TLS 암호화를 통한 보안 통신 보장.
- **REQ-PRD-FUN-05**: 시스템 SSO(Keycloak) 기반의 관리 UI 접근 제어.

## Success Criteria

- **REQ-PRD-MET-01**: 개발 환경에서의 운영 메일 오발송 제로(Zero).
- **REQ-PRD-MET-02**: 외부 메일 서버로의 전송 성공률 99.9% 이상 유지.
- **REQ-PRD-MET-03**: 모든 메일 통신의 TLS 1.3 적용률 100%.

## Scope and Non-goals

- **In Scope**:
  - SMTP 트래핑 및 운영 메일 서비스.
  - 메일 프로토콜 보안 및 인증 정책.
  - 전송 이력 및 데이터 지속성 관리.
- **Out of Scope**:
  - 그룹웨어 또는 메신저 클라이언트 (웹메일 UI 등은 별도 계층 고려 가능).
  - 마케팅 자동화 도구.
- **Non-goals**:
  - 퍼블릭 이메일 서비스(Gmail 등)의 완전한 대체.

## Risks, Dependencies, and Assumptions

- **Risks**: 메일 서버 IP 차단(Blacklist) 시 외부 발송 중단 위험.
- **Dependencies**: `02-auth` (SSO 인증), `secrets/certs` (TLS 인증서).

## Related Documents

- **ARD**: [0010-communication-architecture.md](../02.ard/0010-communication-architecture.md)
- **Spec**: [10-communication/spec.md](../04.specs/10-communication/spec.md)
- **Plan**: [2026-03-26-10-communication-standardization.md](../05.plans/2026-03-26-10-communication-standardization.md)
- **ADR**: [0010-communication-services.md](../03.adr/0010-communication-services.md)
