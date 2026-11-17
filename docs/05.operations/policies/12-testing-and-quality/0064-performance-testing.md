---
title: "Performance Testing Operations Policy"
version: "1.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0064"
parent_ids:
- "AD-0009"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Performance Testing Operations Policy

## Purpose and Scope

### Objective

이 문서는 로드 테스팅 및 벤치마킹 작업 시 시스템의 가용성과 안정성을 유지하기 위한 운영 정책을 정의합니다. 특히, 부하 테스트가 실제 운영 중인 다른 서비스에 미치는 영향을 최소화하고 지표의 무결성을 보장하는 방법을 다룹니다.

#### Policy Goals

- **재현 가능성**: 모든 부하 테스트는 동일한 조건에서 재현될 수 있도록 관리되어야 함.
- **가용성 보존**: 테스트 중 임계 시스템(Gateway, Identity)의 다운타임을 방지해야 함.
- **데이터 보존**: 테스트 결과 지표와 evidence를 벤치마킹 자산으로 안전하게 보관해야 함.

#### Authority

- 상위 문서: [Platform Operations·Quality 아키텍처](../../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

### Applies To

- `infra/11-quality/k6/`와 실행별 원본·판정·적재 계약
- `infra/11-quality/wiremock/`의 기능/부하 모의 모드
- `labs/locust/docker-compose.yml`의 독립 실습 실행
- 개발 `perf_db`의 프로젝트별 조회·적재·판정 권한
- 승인된 local·development·homelab 성능 테스트 시간대

적용 대상 역할은 Operator, Performance Engineer, Infrastructure Admin이다.

#### Exclusions

공개 API와 관리 endpoint는 성능 시험 대상에서 제외하며, k6·WireMock·Locust 서비스별 통제는 POL-0061, POL-0092, Locust 정책이 소유한다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0064-R1 | 항상 | 금지: 비밀 값과 자격 증명 덤프를 어떤 실행에서도 기록 | none | none |
| POL-0064-R2 | 실제 트래픽 생성 전(규모 무관) | 필수: 대상 서비스 소유자와 `@buenhyden`이 정확한 origin·네트워크, 사용자/요청률·지속 시간·자원 상한·중단 조건을 승인한다 | 수동 | none |
| POL-0064-R3 | 항상 | 금지: 공개 API와 관리 endpoint를 시험 대상으로 삼음 | none | none |
| POL-0064-R4 | 부하 시험 시 | 필수: 테스트 대상 서비스뿐 아니라 공유 자원(데이터베이스, 네트워크 대역폭) 부하를 고려한다 | none | none |
| POL-0064-R5 | k6 부하 실행 시 | 필수: `quality_run.py`가 검증한 전용 internal network와 단일 WireMock peer에서만 실행한다 | `quality_run.py` 검증 | none |
| POL-0064-R6 | k6 지표 전송 시 | 필수: run별 relay가 internal `quality_otlp_net`으로만 보낸다 | `quality_run.py` 검증 | none |
| POL-0064-R7 | 항상 | 금지: root `k6` inventory job으로 트래픽·지표 생성 | none | none |
| POL-0064-R8 | Locust 실행 시 | 필수: 별도 LAB Compose 프로젝트와 네트워크에서만 실행한다 | none | none |
| POL-0064-R9 | 데이터베이스 대상 시험 시 | 필수: 가능한 경우 운영 DB가 아닌 복제본 또는 테스트 전용 환경을 대상으로 한다 | none | none |
| POL-0064-R10 | 공식 결과 기록 시 | 필수: run_id·attempt·project_id·시나리오/fixture revision·도구 이미지·target origin·부하 모델·종료 코드·원본 checksum을 연결한다 | none | none |
| POL-0064-R11 | 공식 결과 기록 시 | 필수: 실행 상태·시험 판정·증거 완전성·적재 상태를 각각 기록한다 | none | none |
| POL-0064-R12 | 항상 | 금지: 0표본·중단·부분 flush를 통과로 변환 | none | none |
| POL-0064-R13 | 결과 보존 시 | 필수: 원본과 보고서는 제한된 객체 범위에 둔다 | none | none |
| POL-0064-R14 | 결과 보존 시 | 필수: `perf_db`에는 정규화 결과·권한·객체 참조만 둔다 | none | none |
| POL-0064-R15 | 보존/삭제 기간과 백업 결정 시 | 필수: 승인된 프로젝트 계약을 따른다 | none | none |
| POL-0064-R16 | 결과 파일 생성 시 | 필수: URL query·Authorization·cookie·개인정보를 생성 단계부터 제외한다 | none | none |
| POL-0064-R17 | 항상 | 금지: 이 정책에서 별도 백업 주기를 단정 | none | none |
| POL-0064-R18 | 항상 | 필수: k6에는 Traefik route와 게시 port를 두지 않는다 | none | none |
| POL-0064-R19 | 항상 | 금지: Locust UI 공개(LAB는 headless 기본 계약) | none | none |
| POL-0064-R20 | 항상 | 금지: 인증 없는 WireMock admin API를 공용 경로로 노출 | none | none |
| POL-0064-R21 | 항상 | 필수: WireMock 내부 peer 접근을 통제한다 | none | none |
| POL-0064-R22 | 항상 | 필수: `perf_db`의 프로젝트별 reader/writer/verdict 권한을 SQL에서 검사한다 | `perf_db` SQL 권한 검사 | none |
| POL-0064-R23 | 테스트 자료 사용 시 | 필수: 합성·비식별 fixture로 분리한다 | none | none |
| POL-0064-R24 | 적재 시 | 허용: 같은 artifact checksum의 재적재(멱등) | none | none |
| POL-0064-R25 | 같은 run_id·attempt에 다른 내용이 올 때 | 필수: 충돌로 거절한다 | none | none |
| POL-0064-R26 | 항상 | 금지: 성공 적재를 성능 시험 통과로 해석 | none | none |

아래 기준은 k6·WireMock·Locust 서비스별 정책(POL-0061, POL-0092, Locust 정책)이 소유한
통제 위에 성능 시험 공통 경계만 더한다. 비밀 값과 자격 증명 덤프는 어떤 실행에서도
기록하지 않는다.

#### Operational Standards

##### 1. 테스트 예약 및 사전 공지 (Pre-testing)

- **대상 승인**: 규모와 무관하게 실제 트래픽을 만들기 전에 대상 서비스 소유자와 플랫폼 책임자 `@buenhyden`이 정확한 origin·네트워크, 사용자/요청률·지속 시간·자원 상한·중단 조건을 승인해야 함. 공개 API와 관리 endpoint는 대상에서 제외한다.
- **영향 범위**: 테스트 대상 서비스뿐만 아니라 공유 자원(데이터베이스, 네트워크 대역폭)에 대한 부하를 고려해야 함.

##### 2. 환경 격리 (Environment Isolation)

- **네트워크**: k6 부하는 `quality_run.py`가 검증한 전용 internal network와 단일 WireMock peer에서만 실행하고, 지표는 run별 relay가 internal `quality_otlp_net`으로만 보낸다. root `k6` inventory job은 트래픽과 지표를 만들지 않는다. Locust는 별도 LAB Compose 프로젝트와 네트워크에서만 실행한다. 프로필·네트워크 구분만으로 호스트 자원이나 물리 장애가 격리되지는 않는다.
- **데이터베이스**: 가능한 경우 실제 운영 DB가 아닌 복제본 또는 테스트 전용 환경을 대상으로 테스트를 수행해야 함.

##### 3. 지표 관리 및 보존 (Retention)

- **이력 관리**: 공식 결과는 run_id·attempt·project_id·시나리오/fixture revision·도구 이미지·target origin·부하 모델·종료 코드·원본 checksum을 연결한다. 실행 상태, 시험 판정, 증거 완전성, 적재 상태는 각각 기록한다. 0표본·중단·부분 flush를 통과로 바꾸지 않는다.
- **보존 경계**: 원본과 보고서는 제한된 객체 범위에 두고 `perf_db`에는 정규화 결과·권한·객체 참조만 둔다. 보존/삭제 기간과 백업은 승인된 프로젝트 계약을 따른다. 결과 파일의 URL query, Authorization, cookie, 개인정보는 생성 단계부터 제외한다. 이 정책에서 별도 백업 주기를 단정하지 않는다.

#### Security Controls

- **접근 제어**: k6에는 Traefik route와 게시 port가 없다. Locust LAB는 headless 기본 계약이며 UI를 공개하지 않는다. WireMock admin API는 인증이 없으므로 공용 경로로 노출하지 않고 내부 peer 접근도 통제한다. `perf_db`의 프로젝트별 reader/writer/verdict 권한은 SQL에서 검사한다.
- **데이터 무결성**: 테스트 자료는 합성·비식별 fixture로 분리한다. 같은 artifact checksum의 재적재만 멱등적으로 허용하며 같은 run_id·attempt에 다른 내용이 오면 충돌로 거절한다. 성공 적재는 성능 시험 통과를 뜻하지 않는다.

### Exceptions

#### Exception Conditions

현재 승인된 예외는 없다. 예외가 필요하면 대상, 위험, 만료 조건, 소유자를 기록하고 target owner와 `@buenhyden`의 승인을 받는다.

#### Approval and Review

- 중요한 운영 변경 전에는 같은 주제의 가이드·런북 및 연결된 구현 설정과 함께 정책을 검토한다.
- 연결된 서비스 설정, 아키텍처 또는 런북 동작이 바뀔 때 검토한다.

## Enforcement

### Mechanisms

- 정책이나 연결된 운영 문서를 변경하면 원격 PR public `changed` 검사 ([quality policy](../../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix))로 검증한다.
- 실행·운영 링크를 바꾸면 `python3 scripts/validation/check-document-links.py --mode traceability`로 검증한다.

### Limits

다음 규칙은 정책이 이름 있는 자동 검사를 연결하지 않았다.

- 이름 있는 검사 없음(비밀): `POL-0064-R1`
- 이름 있는 검사 없음(승인): `POL-0064-R3`
- 이름 있는 검사 없음(영향): `POL-0064-R4`
- 이름 있는 검사 없음(격리): `POL-0064-R7`, `POL-0064-R8`, `POL-0064-R9`
- 이름 있는 검사 없음(결과 기록): `POL-0064-R10`, `POL-0064-R11`, `POL-0064-R12`
- 이름 있는 검사 없음(보존): `POL-0064-R13`, `POL-0064-R14`, `POL-0064-R15`, `POL-0064-R16`, `POL-0064-R17`
- 이름 있는 검사 없음(접근): `POL-0064-R18`, `POL-0064-R19`, `POL-0064-R20`, `POL-0064-R21`
- 이름 있는 검사 없음(무결성): `POL-0064-R23`, `POL-0064-R24`, `POL-0064-R25`, `POL-0064-R26`
- 수동 검토·승인에 의존(승인): `POL-0064-R2`
- 정책이 스스로 밝힌 한계: 프로필·네트워크 구분만으로는 호스트 자원이나 물리 장애가 격리되지 않는다.
- 성공 적재는 성능 시험 통과를 뜻하지 않으며 보존·삭제 기간과 백업 주기는 승인된 프로젝트 계약에 맡긴다.
- Mechanisms의 원격 PR public `changed` 검사와 `check-document-links.py --mode traceability`는 정책 문서와 링크를 변경할 때의 검사이며 어느 규칙도 직접 강제하지 않는다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- 동일 주제 문서: [Guide](../../guides/12-testing-and-quality/0064-performance-testing.md) (`GDE-0064`), [Runbook](../../runbooks/12-testing-and-quality/0064-performance-testing.md) (`RUN-0064`)
- [Operations index](../../README.md)
- [Usage guide](../../guides/12-testing-and-quality/0064-performance-testing.md)
- [Recovery runbook](../../runbooks/12-testing-and-quality/0064-performance-testing.md)
