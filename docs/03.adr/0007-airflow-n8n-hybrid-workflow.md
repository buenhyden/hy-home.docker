<!-- Target: docs/03.adr/0007-airflow-n8n-hybrid-workflow.md -->

# ADR-0007: Airflow & n8n Hybrid Workflow Strategy

## Overview (KR)

이 문서는 워크플로 엔진으로 Apache Airflow와 n8n을 동시에 채택한 배경과 하이브리드 운영 전략에 대한 아키텍처 결정 기록이다.

## Context

프로젝트는 두 가지 상이한 워크플로 요구사항에 직면해 있다.
1. **복잡한 데이터 엔지니어링**: 엄격한 스케줄링, 재시도, 실패 처리, 그리고 Python 생태계와의 깊은 통합이 필요한 ETL 작업.
2. **신속한 API 통합**: 다양한 외부 서비스(Slack, Google Sheets 등)와 간단한 비즈니스 로직을 코드 작성 없이 빠르게 연결해야 하는 요구사항.

단일 솔루션으로 이를 모두 해결하기에는 Airflow는 간단한 연동에 너무 무겁고, n8n은 복잡한 데이터 파이프라인 관리에 한계가 있다.

## Decision

- **Apache Airflow**를 "Core Orchestrator"로 채택하여 복잡한 데이터 파이프라인과 시스템 배치 작업을 담당한다.
- **n8n**을 "Integration Automator"로 채택하여 외부 서비스 연합 및 이벤트 기반의 가벼운 자동화를 담당한다.
- **공통 브로커(Valkey)**와 **데이터베이스(PostgreSQL)**를 공유하여 인프라 복잡도를 제어한다.

## Explicit Non-goals

- 두 엔진 간의 직접적인 상호 호출 표준화 (필요 시 API를 통해서만 수행).
- n8n을 대용량 데이터 처리용으로 사용하지 않음.

## Consequences

- **Positive**:
  - 목적에 맞는 최적의 도구 활용으로 개발 및 운영 생산성 향상.
  - 비개발자(또는 AI 에이전트)의 자동화 참여 문턱 낮춤 (n8n).
  - 강력한 데이터 거버넌스 및 추적성 확보 (Airflow).
- **Trade-offs**:
  - 두 종류의 엔진을 관리해야 하므로 운영 오버헤드 발생.
  - 리소스(메모리, CPU) 소비 증가.

## Alternatives

### [Alternative 1: Airflow Only]

- Good: 단일 엔진 운영으로 단순함, 강력한 제어권.
- Bad: 단순한 API 연동에도 많은 코드 작성이 필요하며, UI 기반의 빠른 수정이 불가능함.

### [Alternative 2: n8n Only]

- Good: 매우 빠른 개발 속도, 직관적인 시각화.
- Bad: 복잡한 의존성 관리 및 커스텀 Python 로직 적용이 어렵고, 대규모 배치 작업 가시성이 낮음.

## Related Documents

- **PRD**: [2026-03-26-07-workflow.md](../01.prd/2026-03-26-07-workflow.md)
- **ARD**: [0007-workflow-architecture.md](../02.ard/0007-workflow-architecture.md)
- **Spec**: [07-workflow/spec.md](../04.specs/07-workflow/spec.md)
