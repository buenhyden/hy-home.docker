# Pushgateway Operations Policy

> Operational standards for metrics buffering and ingestion.

---

## Overview (KR)

이 문서는 Pushgateway 운영 정책을 정의한다. 단기 실행 작업의 메트릭 수집을 위한 가이드라인, 데이터 정리(Cleanup) 기준, 그리고 남용 방지를 위한 통제 항목을 규정한다.

## Policy Scope

Pushgateway 서비스의 메트릭 인입, 보관 기간, 그리고 수동/자동 데이터 정리 작업.

## Applies To

- **Systems**: Pushgateway (v1.11.2)
- **Agents**: CI/CD Workers, Batch Scripts
- **Environments**: Production (Observability Tier)

## Controls

- **Required**:
  - 모든 Push 작업에는 `job` 레이블이 반드시 포함되어야 한다.
  - 고유 인스턴스 구분이 필요한 경우 처리 노드나 작업 ID를 `instance` 레이블로 포함해야 한다.
- **Allowed**:
  - Prometheus가 직접 스크랩할 수 없는 네트워크 환경의 작업에 대한 Push 전송.
  - 임시 디버깅 용도의 수동 메트릭 Push.
- **Disallowed**:
  - 장기 실행 서비스(Long-running services)의 메트릭 수집을 위한 Pushgateway 사용 금지.
  - 고카디널리티(High-cardinality) 데이터(예: 사용자 ID별 메트릭) 전송 금지.

## Exceptions

- 프로토타이핑 단계에서 외부 연동 테스트를 위해 일시적으로 위반하는 경우 운영팀의 사전 승인 필요.

## Verification

- **Compliance Check**: Prometheus에서 `push_time_seconds` 메트릭을 모니터링하여 1시간 이상 업데이트되지 않은 `job` 식별.
- **Audit**: 주기적으로 Pushgateway API를 조회하여 비정상적으로 큰 메트릭 그룹 확인.

## Review Cadence

- Quarterly (분기별 운영 정책 검토 및 최적화)

## Related Documents

- **Infrastructure**: `[infra/06-observability/pushgateway/README.md](../../../infra/06-observability/pushgateway/README.md)`
- **ARD**: `[../../02.ard/0006-observability-architecture.md](../../02.ard/0006-observability-architecture.md)`
- **Runbook**: `[../../09.runbooks/06-observability/pushgateway.md](../../09.runbooks/06-observability/pushgateway.md)`
