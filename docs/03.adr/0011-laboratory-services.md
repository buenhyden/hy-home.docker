# ADR-0011: 11-laboratory 서비스 선정 및 구성

## Overview (KR)

이 문서는 `11-laboratory` 티어의 주요 관리 도구 선정에 대한 아키텍처 결정 기록이다.

## Context

시스템 운영 효율성을 높이기 위해 컨테이너 관리, 데이터베이스 조회, 서비스 내비게이션 환경을 구축해야 한다. 이를 위해 가볍고 신뢰할 수 있으며, Traefik 및 Keycloak과 원활하게 통합되는 도구들을 선정해야 한다.

## Decision

다음과 같은 서비스 스택을 `11-laboratory`의 표준 도구로 선정한다.

1. **Dashboard (Homer)**: 정적 설정 기반의 초경량 대시보드.
2. **Container Management (Portainer)**: 직관적인 컨테이너 리소스 제어 및 상태 모니터링.
3. **Data Inspection (RedisInsight)**: Redis/Valkey 데이터 구조 시각화 및 분석.
4. **Log Viewer (Dozzle)**: 다중 컨테이너 실시간 로그 스트리밍.

## Consequences

- **Positive**:
  - 운영자의 인프라 가시성 및 디버깅 속도 대폭 향상.
  - 별도 계정 관리 없이 SSO 통합 로그인 사용.
- **Trade-offs**:
  - `docker.sock` 노출이 필요하므로, SSO를 통한 강력한 접근 제어가 필수적임.

## Related Documents

- **PRD**: `[../01.prd/2026-03-26-11-laboratory.md]`
- **ARD**: `[../02.ard/0011-laboratory-architecture.md]`
- **Spec**: `[../04.specs/11-laboratory/spec.md]`
