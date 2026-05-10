---
tier: 07.operations
component: 06-observability
title: Loki Operational Policy
status: production
updated: 2026-03-26
---

# Loki Operational Policy

> Operational standards for the Loki log aggregation system.

## 1. Data Retention Policy

To balance storage costs and operational needs, the following retention periods are enforced:

- **Standard Application Logs**: 7 Days (168h).
- **Security & Audit Logs**: 30 Days.
- **System Infrastructure Logs**: 7 Days.

> [!IMPORTANT]
> Retention is enforced by the Loki Compactor. Data older than the specified period is permanently deleted from MinIO.

## 2. Label Governance (Cardinality)

High cardinality labels can degrade Loki performance and increase storage costs.

- **Mandatory Labels**: `service_name`, `env`, `stream` (stdout/stderr).
- **Prohibited Labels**: User IDs, IP addresses, Request IDs, or any high-cardinality dynamic data.
- **Best Practice**: Use `LogQL` parsers (e.g., `| json`) to extract dynamic fields at query time instead of using them as labels.

## 3. Performance & Resource Standards

- **Batching**: Alloy must batch log entries (min 1s or 256KB) before pushing to Loki.
- **Ingester Memory**: `infra-loki` container is limited to 2GB RAM. Monitor `loki_ingester_memory_chunks_bytes` to prevent OOM.
- **Compaction**: The compactor runs every 10 minutes to optimize chunk storage in MinIO.

## 4. Backup & Disaster Recovery

- **Config Backup**: `infra/06-observability/loki/config/` is version-controlled.
- **Data Persistence**: MinIO buckets should be backed up using bucket replication or snapshots if long-term audit compliance is required.

---
[System Usage](../../07.operations/06-observability/loki.md) | [Recovery Procedure](../../07.operations/06-observability/loki.md)

---

## Overview (KR)

이 문서는 `docs/07.operations/06-observability/loki.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

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

## Related Documents

- [../README.md](../README.md)
- [../../07.operations/README.md](../../07.operations/README.md)
- [../../07.operations/README.md](../../07.operations/README.md)

## Usage

> Migrated from `docs/07.operations/06-observability/loki.md` during the 2026-05-10 operations taxonomy consolidation.

### Loki System Usage

> Cloud-native log aggregation system for the LGTM stack.

#### Overview (KR)

Loki는 Prometheus에서 영감을 받은 로그 집계 시스템으로, 데이터 본문 전체를 인덱싱하는 대신 레이블(Labels)만 인덱싱하여 높은 효율성을 제공한다. `hy-home.docker` 아키텍처에서 Loki는 모든 서비스의 로그를 중앙 집중화하고, Grafana를 통해 시각화 및 분석을 수행한다.

#### Strategic Boundaries

- **Ingestion (Push/Pull)**: Alloy 콜렉터가 OTLP 또는 Docker 로그 드라이버를 통해 로그를 수집하여 Loki로 전송한다.
- **Storage (MinIO)**: 로그 데이터(Chunks)와 인덱스는 MinIO S3 버킷에 저장되어 데이터 영속성을 보장한다.
- **Querying (LogQL)**: Grafana Explore 메뉴에서 LogQL을 사용하여 로그를 필터링하고 분석한다.

#### Core Workflows

##### 1. Log Ingestion Flow

1. **Alloy Discovery**: Alloy가 Docker 엔진을 스캔하여 컨테이너 로그 소스를 찾는다.
2. **Metadata Enrichment**: 컨테이너 이름, 이미지, 레이블 정보를 로그에 주입한다.
3. **Transmission**: OTLP/HTTP를 통해 Loki 인제스터(`http://loki:3100/loki/api/v1/push`)로 전송한다.

##### 2. Log Analysis (LogQL)

- **Selection**: `{app="my-app"}`
- **Filtering**: `{app="my-app"} |= "error"`
- **Aggregation**: `count_over_time({app="my-app"}[5m])`

#### Step-by-step Instructions

##### 1. Searching Logs in Grafana

1. `https://grafana.${DEFAULT_URL}` 접속 및 로그인.
2. 왼쪽 메뉴에서 **Explore** 선택.
3. Datasource로 **Loki** 선택.
4. `Label browser`를 사용하여 수집된 레이블 확인.

##### 2. Monitoring Loki Health

- **Readiness Check**: `wget -qO- http://loki:3100/ready`
- **Dashboard**: "Loki / Reads" 및 "Loki / Writes" 대시보드를 통해 처리량 확인.

#### Troubleshooting

- **"No logs found"**: 컨테이너가 표준 출력(stdout/stderr)으로 로그를 전달하고 있는지 확인한다.
- **Retention Discrepancy**: `loki-config.yaml`의 `retention_period` 설정을 확인한다.

#### Related Documents

- **Infrastructure README**: `[../../../infra/06-observability/loki/README.md]`
- **Operational Policy**: `[../../07.operations/06-observability/loki.md]`
- **Recovery Procedure**: `[../../07.operations/06-observability/loki.md]`
- **LGTM Usage**: `[./01.lgtm-stack.md]`

---

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- AI Agent

#### Purpose

관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.

#### Prerequisites

- Repository root README 확인
- 관련 `infra/` 서비스 README 확인
- 필요한 경우 대응 operation/runbook 문서 확인

#### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

## Procedure

> Migrated from `docs/07.operations/06-observability/loki.md` during the 2026-05-10 operations taxonomy consolidation.

### Loki Recovery Procedure

> Critical recovery procedures for Loki logging service.

#### 1. Service Health Check

Verify if Loki is healthy and ready to receive logs:

```bash
### Check readiness
wget -qO- http://loki:3100/ready

### Check service status (docker compose)
docker compose ps loki
```

#### 2. Common Scenarios

##### Scenario A: "No logs found" in Grafana

**Symptoms**: Explore shows empty results despite containers running.

1. **Verify Alloy Status**: Check `https://alloy.${DEFAULT_URL}`. Ensure `loki.write` components are healthy.
2. **Check Loki Ingestion**: Look for `entry out of order` or `rate limit exceeded` errors in Loki logs:

   ```bash
   docker compose logs --tail=100 loki
   ```

3. **Verify Labels**: Ensure the LogQL query labels match exactly what Alloy is sending.

##### Scenario B: MinIO Connection Failure

**Symptoms**: Loki logs show `S3 storage: connection refused` or `access denied`.

1. **Check MinIO Status**: `docker compose ps minio`.
2. **Verify Credentials**: Ensure `MINIO_APP_USERNAME` and `minio_app_user_password` secret match the `loki-config.yaml` S3 settings.
3. **Bucket Existence**: Verify `loki-bucket` exists in MinIO UI.

##### Scenario C: Loki Ingester OOM (Out Of Memory)

**Symptoms**: `infra-loki` container restarts frequently with exit code 137.

1. **Temporary Fix**: Increase memory limit in `infra/06-observability/docker-compose.yml` if traffic has surged.

```bash
docker compose -f infra/06-observability/docker-compose.yml restart loki
```

##### 2. Check S3/MinIO Connectivity

1. **Root Cause**: Check for a specific service emitting massive log volume (log spikes).
2. **Mitigation**: Use `limits_config` in `loki-config.yaml` to throttle high-volume streams.

#### 3. Emergency Maintenance

##### Force Compaction

If storage is full and retention cleanup is pending:

```bash
### Compactor runs automatically, but check for errors:
docker compose -f infra/06-observability/docker-compose.yml logs -f loki | grep "compactor"
```

##### Flush Chunks

If Loki needs to be shut down gracefully while ensuring all logs are committed to S3:

- Loki handles this automatically on `SIGTERM`. Ensure `stop_grace_period` is sufficient (min 30s).

---

- [Loki System Usage](../../07.operations/06-observability/loki.md)
 | [Operational Policy](../../07.operations/06-observability/loki.md)

---

#### Overview (KR)

이 런북은 `docs/07.operations/06-observability/loki.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

#### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

#### Canonical References

- [../README.md](../README.md)
- [../../07.operations/README.md](../../07.operations/README.md)
- [../../07.operations/README.md](../../07.operations/README.md)

#### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

#### Procedure or Checklist

##### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

##### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

#### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../README.md)
- [../../07.operations/README.md](../../07.operations/README.md)
- [../../10.incidents/README.md](../../10.incidents/README.md)
