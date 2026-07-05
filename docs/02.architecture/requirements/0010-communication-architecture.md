---
status: active
---
<!-- Target: docs/02.architecture/requirements/0010-communication-architecture.md -->

# Communication Tier Architecture Reference Document (ARD)

## Communication Tier Reference Document

## Overview

이 문서는 `10-communication` 계층의 참조 아키텍처와 품질 속성을 정의한다. 개발용 샌드박스와 실운영용 메일 서버 간의 격리, 보안 프로토콜, 그리고 데이터 지속성 전략을 다룬다.

## Summary

`10-communication` 계층은 현재 구현된 메일 통신을 전담한다. 분리된 두 가지 핵심 엔진(sandbox, backend)으로 구성되며, 외부 네트워크로의 안전한 데이터 전송과 개발 편의성을 동시에 제공한다.

## Boundaries & Non-goals

- **Owns**:
  - SMTP 샌드박스 엔진 (`MailHog`)
  - 고성능 메일 서버 (`Stalwart`)
  - 메일 전송 데이터 지속성 및 볼륨 관리
  - SPF/DKIM/DMARC 운영 요구사항 문서화 및 승격 전 검증
- **Consumes**:
  - 공통 인증 서비스 (`02-auth` / Keycloak)
  - 중앙 인증서 저장소 (`secrets/certs`)
  - 호스트 네트워크 리소스 (표준 메일 포트 점유)
- **Does Not Own**:
  - 인라인 메시지 큐 (05-messaging 담당)
  - 외부 푸시 알림 서비스 (FCM 등)
- **Non-goals**:
  - 대규모 뉴스레터 발송 시스템.

## Quality Attributes

- **Security**: Stalwart의 관리 UI는 Traefik SSO 미들웨어로 보호하고, 메일 프로토콜 TLS/DNS 검증은 운영 승격 전 evidence로 확인한다.
- **Isolation**: 개발 환경(MailHog)과 운영 환경(Stalwart)을 엄격히 구분하여 테스트 코드가 실제 메일을 발송하지 못하도록 함.
- **Reliability**: Stalwart 데이터의 정기적 백업 및 영구 볼륨 동기화를 통한 메시지 소실 방지.
- **Performance**: Rust 기반 Stalwart를 활용하여 저지연, 고성능 메일 처리 보장.

## System Overview & Context

시스템은 '가상화된 샌드박스'와 '신뢰할 수 있는 백엔드'로 이원화되어 운영된다.

1. **Sandbox (MailHog)**: 컨테이너 내부에서 SMTP 1025 포트를 통해 유입되는 모든 메일을 가로채며, 외부 인터넷으로 릴레이하지 않고 메모리/UI에만 노출한다.
2. **Backend (Stalwart)**: 실제 도메인과 연결되어 외부 SMTP 서버와 통신하며, JMAP 및 IMAP 프로토콜을 통한 메시지 접근을 제공한다.

## Data Architecture

- **Key Flows**: Application → SMTP (25/1025) → Communication Tier → (Sink/Storage) → External Mail Server.
- **Storage Strategy**:
  - MailHog는 휘발성 저장소(In-memory)를 사용하여 데이터 누적 방지.
  - Stalwart는 `${DEFAULT_COMMUNICATION_DIR}/stalwart/data`가 바인드된 `stalwart-data` 볼륨에 메일 데이터, 인덱스, 설정 정보를 보관한다. 저장소 암호화는 현재 compose에 선언되어 있지 않으므로 호스트/볼륨 계층 정책으로 별도 검증한다.

## Infrastructure & Deployment

- **Runtime**: Docker Compose 기반 컨테이너.
- **Deployment Model**: `communication` 프로필로 그룹화. root `docker-compose.yml`의 mail include는 현재 optional/commented 상태이며, 운영 승격 시 DNS, 인증서, 포트 개방, secret evidence를 함께 검증한다.
- **Networking**: Traefik Reverse Proxy를 통해 Stalwart/MailHog 관리 UI를 노출하며, Stalwart는 SMTP/Submission/SMTPS/IMAPS/ManageSieve 포트(25, 587, 465, 993, 4190)를 직접 바인딩한다.

## Related Documents

- **PRD**: [011-communication.md](../../01.requirements/011-communication.md)
- **Spec**: [011-communication/spec.md](../../03.specs/011-communication/spec.md)
- **Plan**: [2026-03-26-10-communication-standardization.md](../../04.execution/plans/2026-03-26-10-communication-standardization.md)
- **ADR**: [0010-communication-services.md](../decisions/0010-communication-services.md)
