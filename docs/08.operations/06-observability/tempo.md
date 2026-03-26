# Tempo Operations Policy

> Operational standards for distributed tracing and S3 backend management.

---

## Overview (KR)

이 문서는 Tempo 운영 정책을 정의한다. 분산 추적 데이터의 보관 주기(Retention), 스토리지 백엔드(MinIO) 관리, 그리고 메트릭 생성부(Metrics Generator) 운영 기준을 규정한다.

## Policy Scope

Tempo 서비스의 트레이스 인입, 저장소 처리, 메트릭 원격 쓰기 정책.

## Applies To

- **Systems**: Tempo (v2.10.1-custom)
- **Agents**: Grafana Alloy (OTLP Collectors)
- **Environments**: Production (Observability Tier)

## Controls

- **Required**:
  - 모든 트레이스 데이터는 OTLP 표준을 준수해야 한다.
  - `metrics_generator`를 통한 Span Metrics는 주기적으로 Prometheus로 `remote_write` 되어야 한다.
- **Allowed**:
  - 개발 환경에서의 100% 샘플링 (주의: 부하 모니터링 필수).
  - 특정 이슈 분석을 위한 일시적인 디버그 로그 레벨 상향.
- **Disallowed**:
  - 개인정보(PII)나 비밀번호 등 민감 정보가 트레이스 속성(Attributes)에 포함되지 않도록 마스킹 처리해야 한다.
  - MinIO 관리 권한 없는 사용자의 버킷 직접 수정.

## Storage and Retention

- **Block Retention**: 데이터 블록은 기본 **24시간** 동안 보관한다 (비용 및 성능 최적화).
- **Storage Backend**: MinIO 버킷 `tempo-bucket`을 상시 가용 상태로 유지한다.

## Exceptions

- 장기 추적 분석이나 법적 규제 준수가 필요한 특정 도메인의 경우, 블록 보관 기간을 연장하거나 콜드 스토리지로 이전할 수 있다 (아키텍처 위원회 승인 필요).

## Verification

- **Storage Audit**: `mc ls` 명령을 통해 MinIO 버킷 내 데이터 블록 생성 및 삭제 상태 확인.
- **Integration Test**: Grafana에서 지연 시간이 긴 트레이스 검색 및 시각화 정상 작동 여부 확인.

## Review Cadence

- Semi-annually (스토리지 증가율 및 트레이스 분석 빈도 검토)

## Related Documents

- **Infrastructure**: `[infra/06-observability/tempo/README.md](../../../infra/06-observability/tempo/README.md)`
- **Guide**: `[../../07.guides/06-observability/tempo.md](../../07.guides/06-observability/tempo.md)`
- **Runbook**: `[../09.runbooks/06-observability/tempo.md](../../09.runbooks/06-observability/tempo.md)`
