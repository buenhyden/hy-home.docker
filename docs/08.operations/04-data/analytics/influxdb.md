<!-- Target: docs/08.operations/04-data/analytics/influxdb.md -->

# InfluxDB Operations Policy

> Security and data governance standards for time-series persistence.

---

## Overview (KR)

이 문서는 InfluxDB 운영 정책을 정의한다. 데이터 보존 주기, API 토큰 관리 기준, 그리고 스토리지 모니터링 임계치를 규정한다.

## Policy Scope

Governs all time-series data stored in InfluxDB instances within the `data` and `obs` profiles.

## Applies To

- **Systems**: InfluxDB 3.x, InfluxDB 2.x
- **Agents**: Operators, Automated load-testing workers
- **Environments**: Production, Lab

## Controls

- **Required**:
  - API Tokens MUST be stored in Docker Secrets.
  - All buckets MUST have a non-infinite retention period.
  - Periodic volume snapshots for `influxdb-data`.
- **Allowed**:
  - Direct SQL queries (v3) for analytical reporting.
  - Bucket-level access control via scoped tokens.
- **Disallowed**:
  - Using the `admin` token for standard application ingestion.
  - Moving `influxdb-data` outside the `${DEFAULT_DATA_DIR}` hierarchy without ADR approval.

## Retention Standards

| Data Type | Retention Period | Reason |
|-----------|------------------|--------|
| Metrics (Telegraf) | 90 Days | Standard observability history |
| Load Tests (k6/Locust) | 30 Days | Temporary benchmarking data |
| System Audits | 180 Days | Compliance and security tracking |

## Exceptions

- Load testing data meant for long-term "Golden Signal" benchmarking can be retained for up to 1 year with manual tagging.

## Verification

- Compliance check script: `scripts/audit-influxdb-retention.sh` (Planned)
- Alerting: Prometheus alerts if InfluxDB volume exceeds 85% utilization.

## Review Cadence

- Quarterly.

## Related Documents

- **ARD**: `[../../02.ard/04-data/analytics-tier.md]`
- **Runbook**: `[../../../09.runbooks/04-data/analytics/influxdb.md]`
