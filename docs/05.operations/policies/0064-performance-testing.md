---
title: "Performance Testing Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0064"
parent_ids:
- "AD-0009"
created: "2026-05-17"
---

# Performance Testing Operations Policy

> `hy-home.docker` 환경에서 Locust/k6 기반 성능 테스트를 실행하기 위한 운영 지침 및 거버넌스입니다.

---

## Overview

이 문서는 로드 테스팅 및 벤치마킹 작업 시 시스템의 가용성과 안정성을 유지하기 위한 운영 정책을 정의합니다. 특히, 부하 테스트가 실제 운영 중인 다른 서비스에 미치는 영향을 최소화하고 지표의 무결성을 보장하는 방법을 다룹니다.

### Policy Goals

- **재현 가능성**: 모든 부하 테스트는 동일한 조건에서 재현될 수 있도록 관리되어야 함.
- **가용성 보존**: 테스트 중 임계 시스템(Gateway, Identity)의 다운타임을 방지해야 함.
- **데이터 보존**: 테스트 결과 지표와 evidence를 벤치마킹 자산으로 안전하게 보관해야 함.

## Policy Scope

- `infra/11-quality/locust/docker-compose.yml`
- `infra/11-quality/k6/docker-compose.yml`
- Locust 요청 통계와 테스트 근거
- 승인된 local·development·homelab 성능 테스트 시간대

### Target Audience

- Operator
- Performance Engineer
- Infrastructure Admin

## Controls

- **Required**: 연결된 가이드와 구현 원본의 운영 계약을 유지한다.
- **Allowed**: 링크와 검증 근거를 갱신하는 문서 수정을 허용한다.
- **Disallowed**: 비밀 값, 자격 증명 덤프와 승인되지 않은 실행 환경 변경을 금지한다.

### Operational Standards

#### 1. 테스트 예약 및 사전 공지 (Pre-testing)

- **부하 규모**: 초당 10,000 요청 이상의 대규모 테스트 시 사전에 플랫폼 책임자 `@buenhyden` 및 대상 서비스 소유자와 협조해야 함.
- **영향 범위**: 테스트 대상 서비스뿐만 아니라 공유 자원(데이터베이스, 네트워크 대역폭)에 대한 부하를 고려해야 함.

#### 2. 환경 격리 (Environment Isolation)

- **네트워크**: Locust는 기본 네트워크, k6는 `obs_net`에서 실행된다. 별도 네트워크나 워커 배치는 영향 범위 검토와 승인을 거친다. 프로필 선택만으로 물리적으로 격리되지 않는다.
- **데이터베이스**: 가능한 경우 실제 운영 DB가 아닌 복제본 또는 테스트 전용 환경을 대상으로 테스트를 수행해야 함.

#### 3. 지표 관리 및 보존 (Retention)

- **이력 관리**: 공식 테스트 결과는 실행 시간, target, users, spawn rate, 시나리오, Locust 요청 통계, 결과 요약을 evidence로 남긴다.
- **보존 경계**: 결과 보존은 관련 Task/Incident 정책을 따른다. 이 정책에서 별도 백업 주기를 단정하지 않는다.

### Security Controls

- **UI 접근 제어**: 현재 Locust/k6 leaf에는 Traefik route가 없다. UI 접근은 승인된 host port 경계에서만 수행한다.
- **데이터 무결성**: 테스트 중 주입되는 가상 데이터가 실제 사용자 데이터와 혼용되지 않도록 프리픽스(e.g., `test_user_`)를 사용해야 함.

### Governance & Compliance

이 정책은 플랫폼의 전체 성능 가용성 기준을 따르며, 모든 테스트 수행 이력은 감사(Audit) 대상이 될 수 있습니다.

## Exceptions

N/A — 현재 승인된 예외 없음.

## Verification

- 중요한 운영 변경 전에는 같은 주제의 가이드·런북 및 연결된 구현 설정과 함께 정책을 검토한다.
- 정책이나 연결된 운영 문서를 변경하면 `python3 scripts/validation/run-ci-gate.py --profile changed`로 검증한다.
- 실행·운영 링크를 바꾸면 `python3 scripts/validation/check-document-links.py --mode traceability`로 검증한다.

## Review Cadence

- 연결된 서비스 설정, 아키텍처 또는 런북 동작이 바뀔 때 검토한다.

## Traceability

- 상위 문서: [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- 동일 주제 문서: [Guide](../guides/0064-performance-testing.md) (`GDE-0064`), [Runbook](../runbooks/0064-performance-testing.md) (`RUN-0064`)

## Related Documents

- 실행 버전의 원본은 Compose/Dockerfile 선언이며, [파생 버전 목록](../../../infra/tech-stack.versions.json)은 변경 누락 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0064-performance-testing.md)
- [Recovery runbook](../runbooks/0064-performance-testing.md)
