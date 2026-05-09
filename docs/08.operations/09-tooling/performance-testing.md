<!-- Target: docs/08.operations/09-tooling/performance-testing.md -->

# Performance Testing Operations Policy

> `hy-home.docker` 환경에서 Locust 기반 성능 테스트를 실행하기 위한 운영 지침 및 거버넌스입니다.

---

## Overview (KR)

이 문서는 로드 테스팅 및 벤치마킹 작업 시 시스템의 가용성과 안정성을 유지하기 위한 운영 정책을 정의합니다. 특히, 부하 테스트가 실제 운영 중인 다른 서비스에 미치는 영향을 최소화하고 지표의 무결성을 보장하는 방법을 다룹니다.

## Target Audience

- Operator
- Performance Engineer
- Infrastructure Admin

## Policy Goals

- **재현 가능성**: 모든 부하 테스트는 동일한 조건에서 재현될 수 있도록 관리되어야 함.
- **가용성 보존**: 테스트 중 임계 시스템(Gateway, Identity)의 다운타임을 방지해야 함.
- **데이터 보존**: 테스트 결과 지표(InfluxDB)를 벤치마킹 자산으로 안전하게 보관해야 함.

## Operational Standards

### 1. 테스트 예약 및 사전 공지 (Pre-testing)

- **부하 규모**: 초당 10,000 요청 이상의 대규모 테스트 시 사전에 인프라 팀과 협조해야 함.
- **영향 범위**: 테스트 대상 서비스뿐만 아니라 공유 자원(데이터베이스, 네트워크 대역폭)에 대한 부하를 고려해야 함.

### 2. 환경 격리 (Environment Isolation)

- **네트워크**: `infra_net` 내에서 실행되며, 필요한 경우 부하 생성을 위한 전용 워커 노드를 분리하여 배치함.
- **데이터베이스**: 가능한 경우 실제 운영 DB가 아닌 복제본 또는 테스트 전용 환경을 대상으로 테스트를 수행해야 함.

### 3. 지표 관리 및 보존 (Retention)

- **이력 관리**: 모든 공식 테스트 결과는 InfluxDB에 타임스탬프와 함께 보관하며, Grafana 대시보드를 통해 보고서 형태로 아카이빙함.
- **정기 백업**: InfluxDB의 데이터는 주기적으로 백업되어야 하며, 특히 릴리스 전 공식 벤치마킹 데이터는 삭제되지 않도록 보호해야 함.

## Security Controls

- **UI 접근 제어**: Locust 마스터 UI는 내부 어드민 도메인(`/locust`)을 통해서만 접근 가능하며, 필요시 기본 인증을 적용함.
- **데이터 무결성**: 테스트 중 주입되는 가상 데이터가 실제 사용자 데이터와 혼용되지 않도록 프리픽스(e.g., `test_user_`)를 사용해야 함.

## Governance & Compliance

이 정책은 플랫폼의 전체 성능 가용성 기준을 따르며, 모든 테스트 수행 이력은 감사(Audit) 대상이 될 수 있습니다.

## Related Documents

- **Guide**: [Performance Testing Guide](../../07.guides/09-tooling/performance-testing.md)
- **Runbook**: [Performance Testing Recovery Runbook](../../09.runbooks/09-tooling/performance-testing.md)

---

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.
