<!-- Target: docs/08.operations/04-data/analytics/influxdb.md -->

# InfluxDB Operations Policy

> Operational policy for time-series data storage and retention.

---

## Overview (KR)

이 문서는 InfluxDB 운영 정책을 정의한다. 시계열 데이터의 세분화 수집 주기, 버킷별 보존 정책(Retention Policy), 그리고 인덱싱 및 쿼리 자원 통제를 규정한다.

## Policy Scope

이 정책은 플랫폼 내 모든 InfluxDB 인스턴스와 이에 연결된 데이터 수집(Telegraf) 및 시각화(Grafana) 인터페이스를 관리한다.

## Applies To

- **Systems**: InfluxDB 3.x, InfluxDB 2.x, Telegraf
- **Agents**: AI Metric Analyzers, Automated Scaling Agents
- **Environments**: Production, Staging, Dev

## Controls

- **Required**:
  - 모든 버킷은 최소 7일 이상의 보존 정책을 가져야 함.
  - 모든 쓰기 작업은 유효한 API Token을 필요로 함.
  - 고빈도 데이터(`1s` 미만)는 별도의 고성능 버킷에만 허용됨.
- **Allowed**:
  - 읽기 전용 토큰의 생성 (대시보드 공유용).
  - 특정 기간에 대한 데이터 다운샘플링(Downsampling) 및 집계.
- **Disallowed**:
  - 인증되지 않은 익명 접근 (HTTP 인증 비활성화 금지).
  - 무제한(`INF`) 보존 정책 설정 (승인 없이 금지).

## Exceptions

- 장기 보관 요구사항이 있는 규제 준수 데이터의 경우, 백업 절차를 포함한 별도 승인 후 `INF` 설정 가능.

## Verification

- `influx bucket list`를 통한 보존 정책 정기 점검.
- Prometheus를 통한 InfluxDB 자원 사용량 모니터링.

## Review Cadence

- Quarterly (분기별)

## AI Agent Policy Section

- **Log / Trace Retention**: 수집된 메트릭은 90일 후 자동 다운샘플링 또는 삭제.
- **Safety Incident Thresholds**: 디스크 사용량 80% 초과 시 즉시 알림 및 데이터 정리 태스크 실행.

## Related Documents

- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **Runbook**: [influxdb.md](../../../09.runbooks/04-data/analytics/influxdb.md)
