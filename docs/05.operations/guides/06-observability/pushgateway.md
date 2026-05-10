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

- **Infrastructure**: `[infra/06-observability/pushgateway/README.md](../../../../infra/06-observability/pushgateway/README.md)`
- **ARD**: `[../../02.architecture/requirements/0006-observability-architecture.md](../../../02.architecture/requirements/0006-observability-architecture.md)`
- **Procedure**: `[../../05.operations/06-observability/pushgateway.md](./pushgateway.md)`

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/05.operations/06-observability/pushgateway.md` during the 2026-05-10 operations taxonomy consolidation.

### Pushgateway Usage

> Metrics buffer for ephemeral and batch jobs.

---

#### Overview (KR)

이 문서는 Pushgateway에 대한 가이드다. Pushgateway는 프로메테우스의 Pull 모델이 직접 적용되기 어려운 단기 실행 작업(Ephemeral jobs)이나 배치 스크립트의 메트릭을 일시적으로 보관하고 프로메테우스가 이를 스크랩할 수 있게 하는 버퍼 역할을 한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- Agent-tuner

#### Purpose

Pushgateway의 역할과 동작 방식을 이해하고, 배치 작업에서 메트릭을 올바르게 전송하고 관리하는 방법을 익힌다.

#### Prerequisites

- [Prometheus](./prometheus.md) 가동 중
- 네트워크 연결 (`infra_net`)
- 메트릭 전송 권한 (Traefik을 통한 외부 노출 시)

#### Step-by-step Instructions

##### 1. 메트릭 전송 (Pushing Metrics)

배치 작업 종료 시 또는 주기적으로 HTTP POST/PUT을 사용하여 메트릭을 Push한다.

```bash
### 단일 메트릭 전송
echo "batch_job_duration_seconds 120" | curl --data-binary @- http://pushgateway.local/metrics/job/my_batch_job

### 레이블과 함께 전송
cat <<EOF | curl --data-binary @- http://pushgateway.local/metrics/job/my_batch_job/instance/worker-01
### HELP batch_process_items Total items processed by batch.
### TYPE batch_process_items counter
batch_process_items 1500
EOF
```

##### 2. 프로메테우스 스크랩 설정

프로메테우스는 Pushgateway의 `/metrics` 엔드포인트를 주기적으로 스크랩한다. 이때 `honor_labels: true` 설정이 권장된다.

##### 3. 메트릭 삭제 (Deleting Metrics)

Pushgateway는 수신된 메트릭을 명시적으로 삭제하기 전까지 계속 보관한다. 작업이 완전히 종료되거나 더 이상 유효하지 않은 인스턴스의 메트릭은 삭제 API를 호출해야 한다.

```bash
curl -X DELETE http://pushgateway.local/metrics/job/my_batch_job
```

#### Common Pitfalls

- **메트릭 잔류 (Stale Metrics)**: Pushgateway는 수신된 마지막 값을 계속 보관한다. 만약 실패한 배치가 메트릭을 업데이트하지 못하면 프로메테우스는 마지막 성공 값을 계속 수집하여 오해를 유발할 수 있다.
- **인스턴스 레이블 충돌**: 여러 인스턴스가 동일한 `job` 레이블로 Push하면 데이터가 덮어씌워진다. `instance` 레이블을 활용하여 구분해야 한다.
- **오남용 (Anti-pattern)**: 일반적인 서비스의 메트릭 수집을 위해 Pushgateway를 사용하지 마라. 이는 프로메테우스의 가용성 감지 기능을 무력화한다.

#### Related Documents

- **Infrastructure**: `[infra/06-observability/pushgateway/README.md](../../../../infra/06-observability/pushgateway/README.md)`
- **Operation**: `[../05.operations/06-observability/pushgateway.md](./pushgateway.md)`
- **Procedure**: `[../05.operations/06-observability/pushgateway.md](./pushgateway.md)`

## Procedure

> Migrated from `docs/05.operations/06-observability/pushgateway.md` during the 2026-05-10 operations taxonomy consolidation.

### Pushgateway Procedure

: Metrics Buffer Management

---

#### Overview (KR)

이 런북은 Pushgateway 운영 중 발생할 수 있는 주요 문제(데이터 오염, 메모리 부하, 전송 실패)에 대한 복구 및 관리 절차를 정의한다.

#### Purpose

Pushgateway의 안정적인 메트릭 버퍼 상태를 유지하고, 비정상적인 메트릭 데이터를 정제하여 가시성 품질을 확보한다.

#### Canonical References

- ARD: `[../../02.architecture/requirements/0006-observability-architecture.md](../../../02.architecture/requirements/0006-observability-architecture.md)`
- Infrastructure: `[infra/06-observability/pushgateway/README.md](../../../../infra/06-observability/pushgateway/README.md)`
- Operation: `[../../05.operations/06-observability/pushgateway.md](./pushgateway.md)`

#### When to Use

- Prometheus에서 Pushgateway 스크랩 실패 발생 시.
- 특정 배치 작업의 메트릭이 업데이트되지 않고 예전 값을 유지할 때 (Stale metrics).
- Pushgateway의 메모리 사용량이 비정상적으로 높을 때.

#### Procedure or Checklist

##### Checklist

- [ ] Pushgateway 컨테이너 상태 (`docker ps | grep pushgateway`)
- [ ] Traefik 라우팅 및 SSL 상태 (`https://pushgateway.local/-/ready`)
- [ ] Prometheus Scrape Target 상태

##### Procedure

###### 1. 비정상 메트릭 그룹 삭제

메트릭이 오염되었거나 오래된 경우 특정 `job` 단위로 데이터를 삭제한다.

```bash
### 특정 job 삭제
curl -X DELETE http://pushgateway.local/metrics/job/stale_batch_job

### 특정 job 및 instance 삭제
curl -X DELETE http://pushgateway.local/metrics/job/stale_batch_job/instance/worker-01
```

###### 2. 서비스 재시작 (In-memory 초기화)

상태가 매우 불안정하거나 메모리 임계치에 도달한 경우 서비스를 재시작하여 버퍼를 완전히 초기화한다. (영구 저장소 설정이 없는 경우 데이터가 소실됨에 주의)

```bash
docker compose -f infra/06-observability/docker-compose.yml restart pushgateway
```

###### 3. 연결 테스트

작업 노드에서 Pushgateway로의 도달 가능성을 확인한다.

```bash
curl -I https://pushgateway.${DEFAULT_URL}/-/ready
```

#### Verification Steps

- [ ] `curl http://pushgateway.local/metrics` 명령으로 현재 보관 중인 메트릭 목록 확인.
- [ ] Prometheus UI (`Targets`)에서 `pushgateway` 스크랩 상태가 `UP`인지 확인.

#### Observability and Evidence Sources

- **Signals**: `pushgateway_http_requests_total`, `process_resident_memory_bytes`
- **Evidence to Capture**: `curl -s http://localhost:9091/metrics | grep <job_name>`

#### Safe Rollback or Recovery Procedure

- 배치 작업의 메트릭 유실이 크리티컬한 경우, 작업 재실행(Retry)을 통해 메트릭을 다시 Push한다.
- Push가 계속 실패할 경우, 배치 작업 로그를 직접 분석하여 작업을 완료한다.

---

Copyright (c) 2026. Licensed under the MIT License.

---

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/incidents/README.md](../../incidents/README.md)
