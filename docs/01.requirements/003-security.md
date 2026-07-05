---
status: active
---

<!-- Target: docs/01.requirements/003-security.md -->

# Security Tier (03-security) Product Requirements

## Overview

`03-security` 티어는 하이홈 도커 플랫폼의 "Root of Trust" 역할을 하며, HashiCorp Vault를 통해 민감한 데이터(비밀번호, API 키, 인증서 등)를 중앙에서 관리하고 암호화한다. 모든 서비스는 소스 코드나 환경 변수에 비밀 정보를 직접 노출하지 않고, Vault를 통해 동적으로 주입받거나 참조하는 보안 체계를 구축한다.

## Vision

- **보안성**: 모든 비밀 정보의 암호화 저장 및 접근 제어 자동화.
- **투명성**: 누가, 언제, 어떤 비밀 정보에 접근했는지에 대한 감사 로그 확보.
- **편의성**: Vault Agent를 활용한 사이드카 패턴으로 애플리케이션 수정 최소화.

## Problem Statement

서비스별 비밀 정보가 파일, 환경 변수, 수동 절차로 분산되면 노출 위험과 감사 공백이 커진다. `03-security`는 Vault를 중심으로 비밀 저장, 접근 제어, 주입, 감사 로그를 통합해 모든 서비스가 동일한 신뢰 경계를 따르게 해야 한다.

## Personas

| Persona        | Role                   | Needs                                                                 |
| -------------- | ---------------------- | --------------------------------------------------------------------- |
| Security Admin | 보안 정책 수립 및 감사 | 세밀한 ACL 정책 설정, Unseal 키 관리, 감사 로그 모니터링.             |
| Infra Engineer | 플랫폼 운영 및 관리    | Vault 서버의 고가용성(Raft) 유지 및 서비스별 접근 권한 할당.          |
| App Developer  | 서비스 개발 및 배포    | 환경 변수 대신 Vault에서 동적으로 비밀 정보를 주입받는 메커니즘 제공. |

## Key Use Cases

| ID    | Case              | Description                                                                     |
| ----- | ----------------- | ------------------------------------------------------------------------------- |
| UC-01 | Secret Storage    | KV(Key-Value) 엔진을 사용하여 서비스별 비밀 정보를 안전하게 저장.               |
| UC-02 | Sidecar Injection | Vault Agent를 통해 컨테이너 시작 시 템플릿 기반으로 설정 파일에 비밀 정보 주입. |
| UC-03 | Dynamic Access    | AppRole 또는 Userpass를 통한 애플리케이션/사용자별 권한 기반 접근 통제.         |

## Functional Requirements

| ID    | Requirement           | Priority                                           |
| ----- | --------------------- | -------------------------------------------------- |
| FR-01 | Raft Storage          | 현재 단일 노드 Raft 통합 스토리지를 사용하고, HA 확장은 별도 전환 절차로 준비. |
| FR-02 | Forward Proxy Support | Traefik을 통한 Vault UI/API 외부 노출 및 SSL 적용. |
| FR-03 | Unseal Protocols      | 수동 Unseal 절차 및 정책 수립.                     |
| FR-04 | Audit Logging         | 모든 요청에 대한 Audit 로그 활성화 및 보관.        |

## Non-functional Requirements

| ID     | Requirement  | Description                                                            |
| ------ | ------------ | ---------------------------------------------------------------------- |
| NFR-01 | Availability | 단일 노드 Vault 장애 시 영향을 명확히 감지하고, 향후 Raft quorum 확장을 위한 운영 절차를 유지. |
| NFR-02 | Reliability  | 비밀 정보 암호화 알고리즘의 최신성 유지 (AES-256-GCM).                 |
| NFR-03 | Performance  | 비밀 정보 조회 레이턴시 최소화 (Local API 캐싱).                       |

## Scope and Non-goals

- **In Scope**: Vault Server(Raft), Vault Agent, ACL Policies, KV Engine.
- **Out of Scope**: 외부 IdP(Keycloak) 직접 관리, Let's Encrypt 인증서 발급 자동화(Gateway 역할).
- **Non-goals**: 외부 IdP(Keycloak) 직접 관리, Let's Encrypt 인증서 발급 자동화(Gateway 역할).

## Success Criteria

- 현재 Vault/Agent compose와 문서가 root `security`/`core` profile 검증 및 hardening gate로 관리됨.
- 서비스 컨테이너가 직접 비밀 정보를 알지 못해도 Vault Agent를 통해 주입받아 성공적으로 구동됨.
- 감사 로그/원격 audit 고도화는 정책 승인 후 단계적으로 전환됨.

## Risks, Dependencies, and Assumptions

- **Risk**: Vault 쿼럼이나 Unseal 절차가 실패하면 비밀 정보 주입이 중단될 수 있음.
- **Dependency**: Traefik 기반 외부 노출과 Docker/Vault Agent 사이드카 패턴에 의존함.
- **Assumption**: 서비스별 secret path와 ACL 정책은 Vault KV 및 AppRole/Userpass 권한 모델로 관리됨.

## AI Agent Requirements (If Applicable)

N/A

## Related Documents

- **ARD**: [Security architecture requirements](../02.architecture/requirements/0003-security-architecture.md)
- **Spec**: [Security technical specification](../03.specs/003-security/spec.md)
- **Plan**: [Security standardization plan](../04.execution/plans/2026-03-26-03-security-standardization.md)
- **ADR**: [Vault as secrets manager decision](../02.architecture/decisions/0003-vault-as-secrets-manager.md)
