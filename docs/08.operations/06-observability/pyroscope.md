# Pyroscope Operations Policy

> Operational standards for continuous profiling and data retention.

---

## Overview (KR)

이 문서는 Pyroscope 운영 정책을 정의한다. 지속적 프로파일링 데이터의 보관 주기(Retention), 수집 오버헤드 관리, 그리고 분석 권한 및 보안 기준을 규정한다.

## Policy Scope

Pyroscope 서비스의 프로파일 데이터 인입, 저장소 관리, 보관 기간 정책.

## Applies To

- **Systems**: Pyroscope (v1.18.1)
- **Agents**: Grafana Alloy (Collectors)
- **Environments**: Production (Observability Tier)

## Controls

- **Required**:
  - 모든 프로파일 데이터에는 `application` 레이블이 반드시 포함되어야 한다.
  - 데이터 보관 기간은 기본 **7일**로 유지한다.
- **Allowed**:
  - 개발 및 스테이징 환경에서의 고빈도(High-frequency) 프로파일링.
  - 성능 장애 분석을 위한 임시 프로파일링 세션 활성화.
- **Disallowed**:
  - 개인정보(PII)나 민감한 데이터가 함수 인자 등을 통해 프로파일에 포함되지 않도록 소스 코드 수준에서 관리해야 한다.
  - 운영 환경에서의 무분별한 `Block` 또는 `Mutex` 프로파일링 상시 활성화 (심각한 성능 저하 유발 가능).

## Exceptions

- 장기 성능 트렌드 분석이 필요한 특정 프로젝트의 경우, 별도의 외부 스토리지 백엔드(S3 등) 구성을 통해 보관 기간 연장 가능 (운영팀 승인 필요).

## Verification

- **Compliance Check**: `/var/lib/pyroscope` 디렉토리의 용량 및 데이터 파일 생성 날짜 확인.
- **Audit**: Grafana에서 Pyroscope 데이터 소스의 쿼리 응답 시간 및 스토리지 부하 모니터링.

## Review Cadence

- Quarterly (데이터 보관 비용 및 분석 효용성 검토)

## Related Documents

- **Infrastructure**: `[infra/06-observability/pyroscope/README.md](../../../infra/06-observability/pyroscope/README.md)`
- **ARD**: `[../../02.ard/0006-observability-architecture.md](../../02.ard/0006-observability-architecture.md)`
- **Runbook**: `[../09.runbooks/06-observability/pyroscope.md](../../09.runbooks/06-observability/pyroscope.md)`

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.
