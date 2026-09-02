---
title: Gateway Tier (01-gateway) Product Requirements
type: sdlc/requirement
layer: requirements
status: active
owner: "@buenhyden"
artifact_id: REQ-0001
parent_ids: []
created: 2026-03-26
updated: 2026-08-13
---
# Gateway Tier (01-gateway) Product Requirements

## Problem and Goals

이 문서는 `hy-home.docker` 에코시스템의 통합 진입점인 `01-gateway` 티어의 제품 요구사항을 정의한다. 현재 구현은 root-active Traefik edge router와 profile-only Nginx 특수 경로 프록시 leaf로 구성되며, 트래픽 라우팅, TLS 종료, 보안 미들웨어 체인(SSO, Rate Limit 등)을 오케스트레이션한다.

## Stakeholders and User Needs

모든 외부 트래픽에 대해 단일화되고 안전하며 관찰 가능한 진입점을 제공하여 시스템의 보안을 강화하고 서비스 노출을 단순화한다.

## Problem Statement

- 여러 마이크로서비스가 분산되어 있어 각각에 대한 개별적인 보안 설정(TLS, Auth)을 관리하기 어려움.
- 서비스 Discovery가 자동화되지 않으면 운영 복잡도가 증가함.
- 외부 노출 경로에 대한 중앙 집중식 제어와 가시성(Logging/Metrics)이 부족함.

## Personas

- **Infrastructure Engineer**: 시스템 전체의 트래픽 흐름을 설계하고 TLS 및 네트워크 보안을 관리함.
- **Backend Developer**: 자신의 서비스를 외부로 쉽고 안전하게 노출하고자 함.
- **Security Auditor**: 모든 진입 트래픽에 대한 인증 및 인가 정책 준수를 모니터링함.

## Key Use Cases

- **STORY-01**: 사용자가 브라우저를 통해 서비스에 접속하면 자동으로 HTTPS로 연결되고, 유효한 인증서가 제공되어야 함.
- **STORY-02**: 관리자는 Traefik 대시보드를 통해 현재 라우팅 규칙과 서비스 상태를 실시간으로 확인할 수 있어야 함.
- **STORY-03**: 특정 경로(예: `/keycloak/`, `/minio/`)에 대해 Nginx leaf를 통한 정교한 경로 재작성 및 헤더 조작이 가능해야 하며, Nginx runtime은 명시적 root network/dependency context에서만 다뤄야 함.

## Functional Requirements

- **REQ-0001-FR-0001**: HTTP(80) 트래픽을 HTTPS(443)로 강제 리다이렉트해야 함.
- **REQ-0001-FR-0002**: Docker Provider를 통해 컨테이너 생성을 감지하고 라우트를 자동 생성해야 함.
- **REQ-0001-FR-0003**: TLS 1.2/1.3 및 최신 Cipher Suite를 지원하여 통신 보안을 보장해야 함.
- **REQ-0001-FR-0004**: OAuth2 Proxy와 연동하여 특정 경로에 대한 인증(SSO) 미들웨어를 제공해야 함.

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.
## Acceptance Criteria

- **REQ-0001-FR-0001**: 모든 외부 노출 서비스는 100% TLS를 통해 접근되어야 함.
- **REQ-0001-FR-0002**: 신규 컨테이너 배포 시 별도의 설정 파일 수정 없이 60초 이내에 라우팅이 활성화되어야 함.

## Constraints

- **In Scope**:
  - Traefik (Edge Router) 기반 root-active 동적 라우팅.
  - Nginx 기반 profile-only 특수 경로 프록시 및 헤더 조작.
  - TLS 종료 및 인증서 관리.
- **Out of Scope**:
  - 개별 서비스 내부의 비즈니스 로직.
  - 장기 로그 저장 (Observability 티어 담당).
- **Non-goals**:
  - 자체 인증 서버 구현 (Auth 티어 담당).

## Risks

- **Dependency**: 컨테이너 Discovery를 위해 Docker Socket 접근 권한이 필요함.
- **Assumption**: `scripts/operations/gen-secrets.sh`를 통해 필요한 인증서와 파일들이 사전에 준비되어 있음.

## AI Agent Requirements

- **Allowed Actions**: Analyze routing rules, execute health checks, read non-sensitive configuration files.
- **Disallowed Actions**: Accessing or exfiltrating private keys/certificates, modifying global security policies without human approval.
- **Human-in-the-loop Requirement**: Critical security policy changes and certificate renewals.
- **Evaluation Expectation**: 100% routing accuracy for new services within 60 seconds.

## Traceability

- **Architecture Description**: [Gateway architecture descriptions](../02.architecture/descriptions/0001-gateway-architecture.md)
- **Spec**: [Gateway technical specification](../03.specs/0001-gateway/spec.md)
- **Plan**: Gateway standardization plan
- **ADR**: [Traefik and Nginx hybrid decision](../02.architecture/decisions/0001-traefik-nginx-hybrid.md)
