---
status: active
---
<!-- Target: docs/05.operations/policies/09-tooling/performance-testing.md -->

# Performance Testing Operations Policy

> `hy-home.docker` 환경에서 Locust 기반 성능 테스트를 실행하기 위한 운영 지침 및 거버넌스입니다.

---

## Overview

이 문서는 로드 테스팅 및 벤치마킹 작업 시 시스템의 가용성과 안정성을 유지하기 위한 운영 정책을 정의합니다. 특히, 부하 테스트가 실제 운영 중인 다른 서비스에 미치는 영향을 최소화하고 지표의 무결성을 보장하는 방법을 다룹니다.

## Policy Scope

- `infra/09-tooling/locust/docker-compose.yml`
- `infra/09-tooling/k6/docker-compose.yml`
- Locust request statistics and test evidence
- Approved local, development, and homelab performance-test windows

## Target Audience

- Operator
- Performance Engineer
- Infrastructure Admin

## Policy Goals

- **재현 가능성**: 모든 부하 테스트는 동일한 조건에서 재현될 수 있도록 관리되어야 함.
- **가용성 보존**: 테스트 중 임계 시스템(Gateway, Identity)의 다운타임을 방지해야 함.
- **데이터 보존**: 테스트 결과 지표와 evidence를 벤치마킹 자산으로 안전하게 보관해야 함.

## Operational Standards

### 1. 테스트 예약 및 사전 공지 (Pre-testing)

- **부하 규모**: 초당 10,000 요청 이상의 대규모 테스트 시 사전에 인프라 팀과 협조해야 함.
- **영향 범위**: 테스트 대상 서비스뿐만 아니라 공유 자원(데이터베이스, 네트워크 대역폭)에 대한 부하를 고려해야 함.

### 2. 환경 격리 (Environment Isolation)

- **네트워크**: `infra_net` 내에서 실행되며, 필요한 경우 부하 생성을 위한 전용 워커 노드를 분리하여 배치함.
- **데이터베이스**: 가능한 경우 실제 운영 DB가 아닌 복제본 또는 테스트 전용 환경을 대상으로 테스트를 수행해야 함.

### 3. 지표 관리 및 보존 (Retention)

- **이력 관리**: 공식 테스트 결과는 실행 시간, target, users, spawn rate, 시나리오, Locust 요청 통계, 결과 요약을 evidence로 남긴다.
- **보존 경계**: 결과 보존은 관련 Task/Incident 정책을 따른다. 이 정책에서 별도 백업 주기를 단정하지 않는다.

## Security Controls

- **UI 접근 제어**: 현재 Locust/k6 leaf에는 Traefik route가 없다. UI 접근은 승인된 host port 경계에서만 수행한다.
- **데이터 무결성**: 테스트 중 주입되는 가상 데이터가 실제 사용자 데이터와 혼용되지 않도록 프리픽스(e.g., `test_user_`)를 사용해야 함.

## Governance & Compliance

이 정책은 플랫폼의 전체 성능 가용성 기준을 따르며, 모든 테스트 수행 이력은 감사(Audit) 대상이 될 수 있습니다.

## Controls

- **Required**: Preserve the operational contract documented in the linked guide and source configuration.
- **Allowed**: Documentation-only corrections that keep links and verification evidence current.
- **Disallowed**: Secret values, credential dumps, or unapproved runtime changes in this policy document.

## Exceptions

N/A — 현재 승인된 예외 없음.

## Verification

- Review this policy with its matching guide, runbook, and linked infra/config documents before material operations changes.
- Run `bash scripts/validation/check-repo-contracts.sh` after policy or linked operations document updates.
- Run `bash scripts/validation/check-doc-traceability.sh` when execution or operations links change.

## Review Cadence

- Review when linked service configuration, architecture, or runbook behavior changes.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/09-tooling/performance-testing.md)
- [Recovery runbook](../../runbooks/09-tooling/performance-testing.md)
