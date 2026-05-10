<!-- Target: docs/05.operations/04-data/analytics/influxdb.md -->

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

- **ARD**: [0012-data-analytics-architecture.md](../../../../02.architecture/requirements/0012-data-analytics-architecture.md)
- **Procedure**: [influxdb.md](./influxdb.md)

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/04-data/analytics/influxdb.md` during the 2026-05-10 operations taxonomy consolidation.

### InfluxDB (TSDB) Usage

> Comprehensive guide for managing InfluxDB 3.x and 2.x in the hy-home.docker ecosystem.

---

#### Overview (KR)

이 문서는 InfluxDB 시계열 데이터베이스에 대한 가이드다. 시스템의 아키텍처, V3(Core)와 V2(Legacy)의 차이점, 그리고 Telegraf/Grafana와의 연동 방법을 설명한다. 플랫폼 성능 지표 및 비즈니스 매트릭 수집의 핵심 진입점을 다룬다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- Agent-tuner

#### Purpose

이 가이드는 운영자가 인프라 내 InfluxDB 구성을 이해하고, 개발자가 성능 모니터링 및 분석을 위해 데이터베이스와 상호작용하는 방법을 익히도록 돕는다.

#### Prerequisites

- `infra_net` 네트워크 접근 권한.
- Docker 및 Docker Compose 설치 완료.
- `secrets/influxdb_api_token` 내 유효한 API 토큰.

#### Step-by-step Instructions

##### 1. 버전 선택 (Version Selection)

환경은 다음 두 가지 버전을 지원한다:

- **v3 (Core)**: 고성능 및 SQL 지원을 위해 선호됨. `docker-compose.yml` 사용.
- **v2 (Legacy)**: 기존 Flux 스크립트 호환성을 위해 사용. `docker-compose.v2.yml` 사용.

##### 2. 기본 버킷 관리 (Basic Bucket Management)

버킷은 특정 보존 정책을 가진 데이터를 저장하는 단위다.

```bash
### InfluxDB 3.x (via influx3 CLI)
influx3 bucket create --name my-metrics --retention 90d

### InfluxDB 2.x (via influx CLI)
influx bucket create -n my-metrics -r 90d
```

##### 3. 검증 및 상태 확인 (Verification & Health Check)

```bash
### Endpoint: http://influxdb:8181 (v3) or http://influxdb:8086 (v2)
curl -i http://influxdb:8181/health
```

#### Common Pitfalls

- **토큰 불일치 (Token Mismatch)**: Telegraf나 k6에서 사용하는 토큰이 Docker Secrets에 저장된 토큰과 일치하는지 확인한다.
- **포트 충돌 (Port Conflict)**: v3는 `8181`, v2는 `8086`을 기본값으로 사용한다. 애플리케이션 연결 정보를 확인한다.
- **보존 제약 (Retention Limits)**: 보존 정책 없이 대량의 데이터를 수집할 경우 `${DEFAULT_DATA_DIR}`의 디스크 공간이 고갈될 수 있다.

#### Related Documents

- **PRD**: [2026-03-26-04-data-analytics.md](../../../../01.requirements/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../../02.architecture/requirements/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../../02.architecture/decisions/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../../03.specs/04-data-analytics/spec.md)
- **Operation**: [influxdb.md](./influxdb.md)
- **Procedure**: [influxdb.md](./influxdb.md)

## Procedure

> Migrated from `docs/05.operations/04-data/analytics/influxdb.md` during the 2026-05-10 operations taxonomy consolidation.

### InfluxDB Recovery Procedure

: InfluxDB Performance & Ingestion Recovery

---

#### Overview (KR)

이 런북은 InfluxDB의 수집 장애, 성능 저하 및 노드 중단 시의 실행 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 복구 단계와 검증 기준을 제공한다.

#### Purpose

지표 수집 누락을 최소화하고, InfluxDB 서비스의 가용성을 즉각적으로 복구하는 것을 목적으로 한다.

#### Canonical References

- `[../../02.architecture/requirements/0012-data-analytics-architecture.md]`
- `[../../05.operations/04-data/analytics/influxdb.md]`
- `[../../05.operations/04-data/analytics/influxdb.md]`

#### When to Use

- InfluxDB 헬스 체크(`8181/health`) 실패 시.
- Telegraf 또는 애플리케이션에서 `401 Unauthorized` 또는 `503 Service Unavailable` 노출 시.
- 디스크 사용량 임계치(80%) 초과 경보 발생 시.

#### Procedure or Checklist

##### Checklist

- [ ] Docker 컨테이너 상태 확인 (`influxdb`)
- [ ] API Token 유효성 및 Secrets 마운트 확인
- [ ] 볼륨 마운트 지점의 디스크 잔여 용량 확인

##### Procedure

1. **서비스 요상 확인**:

   ```bash
   docker compose ps influxdb
   docker logs influxdb --tail 100
   ```

2. **토큰 검증**:
   토큰 파일 존재와 mount 상태를 확인한다. 토큰 값은 출력하거나 command history에 남기지 않는다.

   ```bash
   docker compose exec influxdb test -r /run/secrets/influxdb_api_token
   curl -i http://influxdb:8181/health
   ```

3. **강제 재시작 (필요 시)**:

   ```bash
   docker compose restart influxdb
   ```

4. **데이터 정리 (디스크 고갈 시)**:
   보존 정책이 짧은 버킷의 데이터를 수동으로 삭제하거나 보존 기간을 조정한다.

#### Verification Steps

- [ ] `curl -i http://influxdb:8181/health` 결과가 `200 OK`인지 확인.
- [ ] Grafana 대시보드에서 최신 데이터가 업데이트되는지 확인.

#### Observability and Evidence Sources

- **Signals**: Prometheus `influxdb_up`, `influxdb_http_request_duration_seconds`.
- **Evidence to Capture**: `docker logs influxdb` 출력 결과, `influx bucket list` 결과.

#### Safe Rollback or Recovery Procedure

- [ ] 설정 변경 전 `docker-compose.yml` 백업.
- [ ] 데이터 유실 우려 시, 기존 데이터를 다른 경로로 복사 후 작업 수행.

#### Related Operational Documents

- **Operations**: [docs/05.operations/04-data/analytics/influxdb.md](./influxdb.md)

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.
