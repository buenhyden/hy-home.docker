# Analytics Operations (04-Data)

> Operational policies and governance for the analytical data tier.

## Overview (KR)

이 경로는 플랫폼의 분석 및 특수 목적 데이터 엔진(InfluxDB, ksqlDB, OpenSearch, StarRocks)에 대한 운영 정책을 관리한다. 자원 통제, 보안 규약, 백업 주기 및 보존 정책을 정의하여 시스템의 안정성과 규정 준수를 보장한다.

## Audience

이 README의 주요 독자:

- **Operators**: 시스템 자원 관리 및 백업/보안 정책 실행
- **Compliance Officers**: 데이터 보존 및 보안 규정 준수 확인
- **AI Agents**: 자원 최적화 및 정책 기반 자동화 수행

## Scope

### In Scope

- 데이터 엔진별 자원 할당 정책 (JVM, CPU, Memory)
- 데이터 백업 및 보존(Retention) 주기 정책
- 접근 제한 및 보안 통제 기준
- 운영 감사 및 규정 준수 확인 절차

### Out of Scope

- 실시간 장애 대응 절차 (-> `05.operations/` 담당)
- 시스템 이해 및 사용법 (-> `05.operations/` 담당)
- 인프라 배포 코드 관리 (-> `infra/` 담당)

## Structure

```text
analytics/
├── influxdb.md      # InfluxDB Operations Policy
├── ksqldb.md        # ksqlDB Operations Policy
├── opensearch.md    # OpenSearch Operations Policy
├── warehouses.md    # StarRocks Operations Policy
└── README.md        # This file
```

## How to Work in This Area

1. 정책 변경 시 반드시 **ARD-0012** 분석 아키텍처 원칙과 대조한다.
2. 모든 정책 문서는 `operation.template.md`를 기반으로 작성한다.
3. 정책 수정 후에는 반드시 관련 런북(`05.operations/`)의 실행 절차와의 일치 여부를 확인한다.
4. AI Agent는 정책 위반 사례 발견 시 즉시 사용자에게 보고하고 대응 시나리오를 제안한다.

## Related References

- **PRD**: [2026-03-26-04-data-analytics.md](../../../../01.requirements/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../../02.architecture/requirements/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../../02.architecture/decisions/0015-analytics-engine-selection.md)
- **Usages**: [docs/05.operations/04-data/analytics/](./README.md)
- **Procedures**: [docs/05.operations/04-data/analytics/](./README.md)

## AI Agent Guidance

1. 운영 정책은 시스템의 제약 사항을 정의하므로, 인프라 변경 제안 시 이 폴더의 정책을 우선적으로 참조한다.
2. 정책 문서의 `Controls` 섹션을 분석하여 자동화된 가드레일을 구축한다.
3. 중복된 정책이 존재할 경우 SSoT로 통합하고 상호 참조 링크를 갱신한다.

---
Copyright (c) 2026. Analytics Tier Operations.

---

## Overview

`docs/05.operations/04-data/analytics`는 운영 정책, 통제 기준, 검증 방법을 정의하는 operation 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Usage

> Migrated from `docs/05.operations/04-data/analytics/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Analytics Documentation (04-Data)

> Usages, operations, and runbooks for the analytical data tier.

#### Overview (KR)

이 경로는 플랫폼의 분석 및 특수 목적 데이터 엔진(InfluxDB, ksqlDB, OpenSearch, StarRocks)에 대한 시스템 가이드, 운영 정책 및 복구 절차를 관리한다. 시스템 이해(Usage)와 실행 지침(Operation/Procedure)을 분리하여 관리함으로써 운영 효율성을 극대화한다.

#### Audience

이 README의 주요 독자:

- **Architects**: 데이터 분석 파이프라인 설계 및 엔진 선택
- **Operators**: 분석 노드 상태 점검 및 장애 복구
- **Data Engineers**: 분석 스키마 및 쿼리 인터페이스 활용
- **AI Agents**: 분석 데이터 추출 및 시스템 최적화 제안

#### Scope

##### In Scope

- 분석 엔진 설정 가이드 및 기술 규약
- 엔진별 데이터 보존 정책 및 실시간 처리 규약
- 운영 업무 자동화를 위한 복구 절차
- 하위 엔진별 세부 가이드 파일 아카이브

##### Out of Scope

- 핵심 트랜잭션 데이터베이스 관리 (-> `04-data/relational` 담당)
- 시각화 대시보드 UI 디자인 가이드
- 인프라 배포 코드 관리 (-> `infra/04-data/analytics/` 담당)

#### Structure

```text
analytics/
├── influxdb.md      # InfluxDB (TSDB) Usage
├── ksqldb.md        # ksqlDB (Stream) Usage
├── opensearch.md    # OpenSearch (Logs) Usage
├── warehouses.md    # StarRocks (OLAP) Usage
└── README.md        # This file
```

#### How to Work in This Area

1. 신규 기술 도입 시 반드시 **ADR-0015** 기술 선택 기록을 먼저 확인한다.
2. 모든 가이드 문서는 `operation.template.md`를 기반으로 작성한다.
3. 문서 수정 시 관련 운영 정책(`05.operations/`) 및 런북(`05.operations/`)과 상호 참조 무결성을 확인한다.
4. AI Agent는 문서 생성 시 한국어 요약(Overview KR)을 반드시 포함한다.

#### Related References

- **PRD**: [2026-03-26-04-data-analytics.md](../../../../01.requirements/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../../02.architecture/requirements/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../../02.architecture/decisions/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../../03.specs/04-data-analytics/spec.md)
- **Implementation**: [infra/04-data/analytics/](../../../../../infra/04-data/analytics)
- **Operations**: [docs/05.operations/04-data/analytics/](./README.md)
- **Procedures**: [docs/05.operations/04-data/analytics/](./README.md)

#### AI Agent Guidance

1. 문서 계층 구조를 유지하기 위해 상위 README와 하위 문서 간의 링크를 반드시 검증한다.
2. 기술적 용어는 명확하게 사용하되, 의사결정의 원천은 항상 ADR을 참조한다.
3. 중복된 정보를 생성하기보다 SSoT 문서를 확장하는 방식으로 작업한다.

---
Copyright (c) 2026. Analytics Tier Documentation.

---

#### Overview

`docs/05.operations/04-data/analytics`는 사용자와 운영자가 재현 가능한 작업 방법을 이해하도록 돕는 guide 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Procedure

> Migrated from `docs/05.operations/04-data/analytics/README.md` during the 2026-05-10 operations taxonomy consolidation.

### Analytics Procedures (04-Data)

> Step-by-step recovery and maintenance procedures for the analytical data tier.

#### Overview (KR)

이 경로는 플랫폼의 분석 및 특수 목적 데이터 엔진(InfluxDB, ksqlDB, OpenSearch, StarRocks)에 대한 실행 런북을 관리한다. 장애 발생 시 즉각적으로 대응할 수 있는 단계별 절차와 일상적인 유지보수 작업 지침을 제공한다.

#### Audience

이 README의 주요 독자:

- **Operators**: 장애 복구 및 유지보수 작업 수행
- **SREs**: 시스템 안정성 보장을 위한 런북 유지보수
- **AI Agents**: 장애 상황 감지 시 자동 대응 절차 실행

#### Scope

##### In Scope

- 분석 엔진 노드 복구 및 재시작 절차
- 데이터 손상 시 복구 및 동기화 작업
- 성능 저하 시 진단 및 튜닝 단계
- 인프라 리전 이동 또는 클러스터 마이그레이션

##### Out of Scope

- 시스템 설계 및 기본 가이드 (-> `05.operations/` 담당)
- 운영 정책 정의 (-> `05.operations/` 담당)
- 일반 사용자 지원 업무

#### Structure

```text
analytics/
├── influxdb.md      # InfluxDB Recovery Procedure
├── ksqldb.md        # ksqlDB Recovery Procedure
├── opensearch.md    # OpenSearch Recovery Procedure
├── warehouses.md    # StarRocks Recovery Procedure
└── README.md        # This file
```

#### How to Work in This Area

1. 모든 런북은 즉시 실행 가능한 형태(Bash 명령어 등 포함)로 작성한다.
2. 모든 런북은 `operation.template.md`를 기반으로 작성한다.
3. 런북 실행 전 반드시 관련 운영 정책(`05.operations/`)의 제약 사항을 확인한다.
4. AI Agent는 장애 탐지 시 관련 런북을 검색하여 대응 방안을 즉시 제시한다.

#### Related References

- **PRD**: [2026-03-26-04-data-analytics.md](../../../../01.requirements/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../../02.architecture/requirements/0012-data-analytics-architecture.md)
- **Usages**: [docs/05.operations/04-data/analytics/](./README.md)
- **Operations**: [docs/05.operations/04-data/analytics/](./README.md)
- **Incidents**: [docs/05.operations/incidents/](../../../incidents/README.md)

#### AI Agent Guidance

1. 런북의 명령어는 시스템 상태에 따라 파라미터를 동적으로 조정해야 할 수 있으므로 실행 전 반드시 사용자 주의 문구를 포함한다.
2. 실행된 모든 단계와 결과는 `05.operations/incidents/`에 기록하여 향후 Postmortem의 기반이 되도록 한다.
3. 복구가 완료된 후에는 `Verification Steps`를 통해 정상 작동 여부를 반드시 확인한다.

---
Copyright (c) 2026. Analytics Tier Procedures.

---

#### Overview

`docs/05.operations/04-data/analytics`는 운영자가 즉시 실행할 수 있는 runbook 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.
