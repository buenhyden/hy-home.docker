# Plan: Data Tier Documentation Standardization (04-data)

## Overview (KR)

`04-data` 티어의 다중 모델 영속성 계층에 대한 문서 체계를 표준화한다. PostgreSQL HA, Valkey Cluster, MinIO 등의 하형 설계를 기반으로 PRD, ARD, ADR, Spec을 통합하고, 실행 및 검증 가능한 작업 기반을 구축한다.

## User Review Required

> [!IMPORTANT]
> 본 계획은 기존 `infra/04-data`에 구현된 구성을 역설계하여 문서화하는 것이며, 실제 인프라의 파괴적인 변경을 포함하지 않는다.

## Proposed Changes

### 1. Document Creation
- **PRD**: [2026-03-26-04-data.md](../01.prd/2026-03-26-04-data.md)
- **ARD**: [0004-data-architecture.md](../02.ard/0004-data-architecture.md)
- **ADR**: [0004-postgresql-ha-patroni.md](../03.adr/0004-postgresql-ha-patroni.md)
- **Spec**: [04-data/spec.md](../04.specs/04-data/spec.md)

### 2. README Refactoring
- 레이어 01~06의 `README.md`에 `04-data` 항목 추가.

## Work Breakdown

### Phase 1: Reverse Engineering & Technical Design (Done)
- `infra/04-data` 구성 파일 분석 및 핵심 문서 생성.

### Phase 2: Traceability & Integration (In Progress)
- 레이어별 README 리팩토링 및 상호 참조 링크 검증.

### Phase 3: Final Audit (Planned)
- 문서 무결성 검사 및 최종 walkthrough 업데이트.

## Verification Plan

### Automated Verification
- `grep`을 통한 모든 문서의 `Overview (KR)` 섹션 존재 확인.
- 상대 경로 링크 유효성 검사.

### Manual Verification
- AI 에이전트가 생성된 문서를 통해 04-data의 HA 구성을 완벽히 설명할 수 있는지 확인.
