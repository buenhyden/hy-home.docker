# ADR: HashiCorp Vault as Centralized Secrets Manager

## Overview (KR)

플랫폼 전체의 민감한 정보(비밀번호, API 키, 인증서 등)를 관리하기 위해 전용 비밀 정보 관리 솔루션이 필요하다. 이에 대한 결정으로 HashiCorp Vault를 채택하며, 구체적인 이유와 대안을 기록한다.

## Status

- **Proposed**: 2026-03-26
- **Accepted**: 2026-03-26

## Context

- 기존의 하드코딩된 설정이나 `.env` 파일 방식은 보안 취약성이 높고 secrets 노출 위험이 있음.
- Docker Secrets는 기능이 제한적이며, 복잡한 비밀 정보 갱신(Rotation)이나 세밀한 권한 제어(ACL)가 어려움.
- 클라우드 네이티브 환경에서 서비스 간의 신뢰 관계를 바탕으로 동적인 시크릿 주입이 요구됨.

## Decision

**HashiCorp Vault**를 플랫폼의 표준 비밀 정보 관리 도구로 채택한다.

1. **Raft Storage**: 외부 DB 없이 고가용성 클러스터 구축 가능.
2. **AppRole Mechanism**: 컨테이너 기반 서비스에 최적화된 인증 방식 제공.
3. **Template Support**: Vault Agent를 통한 기존 애플리케이션과의 원활한 통합.
4. **Encryption-as-a-Service**: 단순 저장을 넘어 데이터 암호화 API 제공 가능.

## Consequences

### Positive

- 모든 비밀 정보의 중앙 집중화 및 암호화 저장.
- 상세한 Audit 로그를 통한 보안 준수(Compliance) 강화.
- 시크릿 노출 없이 인프라 코드를 공용 저장소에 안전하게 보관 가능.

### Negative

- Vault 서버의 초기 Unseal 등 운영 복잡도 증가.
- Vault 서버 장애가 전체 서비스의 "Single Point of Failure"가 될 수 있으므로 HA 구성이 필수적임.

## Alternatives Considered

1. **Docker Secrets**: 사용이 간편하나 기능이 부족하고 유연성이 낮음.
2. **SOPS**: 파일 기반 암호화에는 좋으나 동적 주입 및 API 기반 관리가 어려움.
3. **AWS/GCP Secrets Manager**: 클라우드 종속성이 생기며, 온프레미스/도커 환경에서 비용 및 가용성 이슈.
