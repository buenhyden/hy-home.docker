---
title: "Performance Testing Operations Policy"
version: "1.1.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0064"
parent_ids:
- "AD-0009"
created: "2026-05-17"
---

# Performance Testing Operations Policy

## Overview

이 문서는 로드 테스팅 및 벤치마킹 작업 시 시스템의 가용성과 안정성을 유지하기 위한 운영 정책을 정의합니다. 특히, 부하 테스트가 실제 운영 중인 다른 서비스에 미치는 영향을 최소화하고 지표의 무결성을 보장하는 방법을 다룹니다.

### Policy Goals

- **재현 가능성**: 모든 부하 테스트는 동일한 조건에서 재현될 수 있도록 관리되어야 함.
- **가용성 보존**: 테스트 중 임계 시스템(Gateway, Identity)의 다운타임을 방지해야 함.
- **데이터 보존**: 테스트 결과 지표와 evidence를 벤치마킹 자산으로 안전하게 보관해야 함.

## Scope

- `infra/11-quality/k6/`와 실행별 원본·판정·적재 계약
- `infra/11-quality/wiremock/`의 기능/부하 모의 모드
- `labs/locust.yml`의 독립 실습 실행
- 개발 `perf_db`의 프로젝트별 조회·적재·판정 권한
- 승인된 local·development·homelab 성능 테스트 시간대

적용 대상 역할은 Operator, Performance Engineer, Infrastructure Admin이다.

## Rules

- **Required**: 연결된 가이드와 구현 원본의 운영 계약을 유지한다.
- **Allowed**: 링크와 검증 근거를 갱신하는 문서 수정을 허용한다.
- **Disallowed**: 비밀 값, 자격 증명 덤프와 승인되지 않은 실행 환경 변경을 금지한다.

### Operational Standards

#### 1. 테스트 예약 및 사전 공지 (Pre-testing)

- **대상 승인**: 규모와 무관하게 실제 트래픽을 만들기 전에 대상 서비스 소유자와 플랫폼 책임자 `@buenhyden`이 정확한 origin·네트워크, 사용자/요청률·지속 시간·자원 상한·중단 조건을 승인해야 함. 공개 API와 관리 endpoint는 대상에서 제외한다.
- **영향 범위**: 테스트 대상 서비스뿐만 아니라 공유 자원(데이터베이스, 네트워크 대역폭)에 대한 부하를 고려해야 함.

#### 2. 환경 격리 (Environment Isolation)

- **네트워크**: k6의 기존 Prometheus remote write는 `obs_net`을 사용한다. Locust는 별도 LAB Compose 프로젝트와 네트워크에서만 실행한다. 프로필·네트워크 구분만으로 호스트 자원이나 물리 장애가 격리되지는 않는다.
- **데이터베이스**: 가능한 경우 실제 운영 DB가 아닌 복제본 또는 테스트 전용 환경을 대상으로 테스트를 수행해야 함.

#### 3. 지표 관리 및 보존 (Retention)

- **이력 관리**: 공식 결과는 run_id·attempt·project_id·시나리오/fixture revision·도구 이미지·target origin·부하 모델·종료 코드·원본 checksum을 연결한다. 실행 상태, 시험 판정, 증거 완전성, 적재 상태는 각각 기록한다. 0표본·중단·부분 flush를 통과로 바꾸지 않는다.
- **보존 경계**: 원본과 보고서는 제한된 객체 범위에 두고 `perf_db`에는 정규화 결과·권한·객체 참조만 둔다. 보존/삭제 기간과 백업은 승인된 프로젝트 계약을 따른다. 결과 파일의 URL query, Authorization, cookie, 개인정보는 생성 단계부터 제외한다. 이 정책에서 별도 백업 주기를 단정하지 않는다.

### Security Controls

- **접근 제어**: k6에는 Traefik route가 없다. Locust LAB는 headless 기본 계약이며 UI를 공개하지 않는다. WireMock admin API는 인증이 없으므로 공용 경로로 노출하지 않고 내부 peer 접근도 통제한다. `perf_db`의 프로젝트별 reader/writer/verdict 권한은 SQL에서 검사한다.
- **데이터 무결성**: 테스트 자료는 합성·비식별 fixture로 분리한다. 같은 artifact checksum의 재적재만 멱등적으로 허용하며 같은 run_id·attempt에 다른 내용이 오면 충돌로 거절한다. 성공 적재는 성능 시험 통과를 뜻하지 않는다.

### Governance & Compliance

이 정책은 플랫폼의 전체 성능 가용성 기준을 따르며, 모든 테스트 수행 이력은 감사(Audit) 대상이 될 수 있습니다.

## Exceptions

현재 승인된 예외는 없다. 예외가 필요하면 대상, 위험, 만료 조건, 소유자를 기록하고 target owner와 `@buenhyden`의 승인을 받는다.

### Verification

- 중요한 운영 변경 전에는 같은 주제의 가이드·런북 및 연결된 구현 설정과 함께 정책을 검토한다.
- 정책이나 연결된 운영 문서를 변경하면 원격 PR public `changed` 검사 ([quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix))로 검증한다.
- 실행·운영 링크를 바꾸면 `python3 scripts/validation/check-document-links.py --mode traceability`로 검증한다.

### Review Cadence

- 연결된 서비스 설정, 아키텍처 또는 런북 동작이 바뀔 때 검토한다.

### Traceability

- 상위 문서: [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- 동일 주제 문서: [Guide](../guides/0064-performance-testing.md) (`GDE-0064`), [Runbook](../runbooks/0064-performance-testing.md) (`RUN-0064`)

## Related Documents

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0064-performance-testing.md)
- [Recovery runbook](../runbooks/0064-performance-testing.md)
