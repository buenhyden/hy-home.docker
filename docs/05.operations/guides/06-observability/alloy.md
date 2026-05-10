# Alloy Operational Policy

> Telemetry Pipeline Governance and Performance Standards

---

## Overview (KR)

이 정책은 `hy-home.docker` 가시성 플랫폼의 핵심 수집기인 Grafana Alloy의 운영 기준을 정의한다. 파이프라인 안정성과 데이터 무결성을 유지하기 위한 가이드라인을 제공한다.

## Target Audience

- Operator
- SRE
- AI Agents

## Operational Standards

### 1. Ingestion Protocol Tier

- **Tier 1 (Preferred)**: OTLP gRPC/HTTP. 모든 신규 서비스는 OTLP를 통한 직접 전송을 원칙으로 한다.
- **Tier 2 (Legacy/Infra)**: Docker socket discovery + Scraping. 자동 메타데이터 주입이 필요한 인프라 컴포넌트에 사용한다.

### 2. Data Reliability & Performance

- **Batching Strategy**:
  - `send_batch_size`: 통상 1,000 ~ 2,000 레코드 유지.
  - `timeout`: 1s ~ 5s 유지하여 지연 시간 제어.
- **Memory Management**: Alloy 인프라 메모리 사용량이 80%를 초과할 경우 배치 사이즈를 조정하거나 스케일 업을 검토한다.

### 3. Labeling and Taxonomy

- 모든 텔레메트리에는 다음 필수 레이블이 포함되어야 한다.
  - `service_name`: 서비스 명칭
  - `env`: dev, staging, prod 등 환경 정보
  - `scope`: infra (플랫폼 구성 요소) 또는 app (사용자 서비스)

## Monitoring and Alerting

### Key Metrics to Monitor

- `alloy_component_health`: 컴포넌트의 정상 작동 여부 (UI에서 확인 가능)
- `otelcol_processor_batch_dropped_spans_total`: 배치 처리 중 소실된 트레이스 수
- `loki_write_errors_total`: Loki 전송 에러 발생률

### Alerting Rules

- **P0 (Critical)**: Alloy 프로세스 중단 또는 OTLP 포트 수신 불가.
- **P1 (Warning)**: 전송 에러(`forward_to` failure)가 5분간 지속될 경우.
- **P2 (Info)**: 배치 처리 지연 시간이 설정값을 반복적으로 초과할 경우.

## Configuration Governance

- 모든 설정 변경은 `infra/06-observability/alloy/config/config.alloy`를 통해 관리한다.
- 대규모 변경 시 Alloy UI의 Graph View를 통해 의도하지 않은 파이프라인 단절이 없는지 사전 검증해야 한다.

## Related Documents

- **Usage**: [../../05.operations/06-observability/alloy.md](./alloy.md)
- **Procedure**: [../../05.operations/06-observability/alloy.md](./alloy.md)

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

## Usage

> Migrated from `docs/05.operations/06-observability/alloy.md` during the 2026-05-10 operations taxonomy consolidation.

### Alloy System Usage

> Unified Telemetry Collection and OTLP Pipeline Usage

---

#### Overview (KR)

Alloy는 `hy-home.docker` 플랫폼의 모든 텔레메트리(지표, 로그, 트레이스)를 수집하여 적절한 백엔드로 전달하는 통합 에이전트이다. 이 가이드는 Alloy의 파이프라인 구조와 데이터 흐름을 설명한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- Agent-tuner

#### Purpose

이 가이드는 Alloy를 사용하여 시스템의 통합 가시성을 확보하고, 텔레메트리 파이프라인을 효율적으로 관리하는 방법을 설명한다.

#### Prerequisites

- OTLP 프로토콜에 대한 기본 이해
- `config.alloy` (HCL) 설정 문법 이해
- Docker 및 컨테이너 메타데이터에 대한 지식

#### Step-by-step Instructions

##### 1. Understanding the Pipeline

Alloy의 파이프라인은 다음과 같은 단계로 구성된다.

- **Discovery**: `discovery.docker`를 사용하여 컨테이너 정보를 수집한다.
- **Relabeling**: `discovery.relabel`을 사용하여 메타데이터(service_name, env, scope)를 주입한다.
- **Scraping/Receiving**:
  - Logs: `loki.source.docker`
  - Metrics: `prometheus.scrape`
  - Traces/Metrics: `otelcol.receiver.otlp` (OTLP Ingestion)
- **Processing**: `otelcol.processor.batch` 등을 사용하여 성능을 최적화한다.
- **Exporting**: 각 백엔드(`loki.write`, `prometheus.remote_write`, `otelcol.exporter.otlp`)로 데이터를 전송한다.

##### 2. OTLP Ingestion

애플리케이션은 다음 포트를 통해 데이터를 전송할 수 있다.

- **gRPC**: `alloy:4317`
- **HTTP**: `alloy:4318`

##### 3. Pipeline Debugging (Alloy UI)

- 브라우저에서 `https://alloy.${DEFAULT_URL}`에 접속한다.
- **Graph View**: 컴포넌트 간의 연결 상태를 시각적으로 확인한다.
- **Component Details**: 각 컴포넌트의 상태, 수집된 타겟, 에러 로그를 확인한다.

#### Common Pitfalls

- **Relabeling Regex**: 정규표현식이 틀리면 `service_name`이 잘못 지정되거나 `scope`가 `app`으로 오인될 수 있다.
- **Batch Size Tuning**: 배치가 너무 크면 지연 시간이 증가하고, 너무 작으면 백엔드 부하가 증가한다.
- **Docker Socket permissions**: Alloy 컨테이너가 `/var/run/docker.sock`에 접근할 수 있어야 discovery가 작동한다.

#### Related Documents

- **Documentation**: [infra/06-observability/alloy/README.md](../../../../infra/06-observability/alloy/README.md)
- **Operation**: [../05.operations/06-observability/alloy.md](./alloy.md)
- **Procedure**: [../05.operations/06-observability/alloy.md](./alloy.md)

## Procedure

> Migrated from `docs/05.operations/06-observability/alloy.md` during the 2026-05-10 operations taxonomy consolidation.

### Alloy Recovery Procedure

> Incident Response and Recovery Procedures for the Telemetry Pipeline

---

#### Overview (KR)

이 런북은 `hy-home.docker`의 텔레메트리 수집 엔진인 Grafana Alloy의 장애 복구 절차를 정의한다. 데이터 수집 중단이나 파이프라인 지연 발생 시 신속하게 대응하기 위한 가이드라인이다.

#### Procedure Type

`recovery | troubleshooting`

#### Target Audience

- Operator
- SRE
- On-call Engineer

#### Purpose

Alloy 서비스의 가용성을 유지하고, 텔레메트리 데이터 유실을 최소화하기 위한 복구 절차를 수행한다.

#### Prerequisites

- [Alloy System Usage](./alloy.md) 이해
- [Alloy Operational Policy](./alloy.md) 숙지
- Docker Compose 권한 및 Alloy UI 접근 권한

#### Step-by-step Instructions

##### 1. Service Restoration

Alloy 컨테이너가 중단되었거나 응답하지 않을 경우:

1. `docker compose ps alloy`로 상태 확인.
2. `docker compose restart alloy` 실행.
3. `docker compose logs -f alloy`로 에러 메시지 확인.

##### 2. Pipeline Debugging (Alloy UI)

데이터 수집은 되지만 특정 레이블이 탈락하거나 전송되지 않을 경우:

1. `https://alloy.${DEFAULT_URL}`에 접속.
2. **Graph View**에서 빨간색으로 표시된 컴포넌트 식별.
3. 해당 컴포넌트를 클릭하여 구체적인 에러 메시지(예: `connection refused to loki`) 확인.

##### 3. Memory Exhaustion Mitigation

Alloy가 메모리 부족으로 재시작을 반복할 경우:

1. `config.alloy`에서 `otelcol.processor.batch`의 `send_batch_size`를 일시적으로 축소.
2. 사용량이 많은 `discovery.relabel` 규칙이 있는지 검토 및 최적화.

##### 4. OTLP Connectivity Fix

앱이 데이터를 전송하지 못할 경우:

1. `nc -zv alloy 4317` (gRPC) 또는 `nc -zv alloy 4318` (HTTP)로 포트 오픈 여부 확인.
2. Alloy 컨테이너 로그에서 `otelcol.receiver.otlp` 초기화 에러 확인.

#### Common Pitfalls

- **Stale Configuration**: `config.alloy` 수정 후 `restart`하지 않으면 변경 사항이 반영되지 않는다.
- **Docker Socket Disconnect**: 호스트의 `/var/run/docker.sock` 권한 문제로 discovery가 중단될 수 있다.

#### Related Documents

- **Usage**: [../../05.operations/06-observability/alloy.md](./alloy.md)
- **Operation**: [../../05.operations/06-observability/alloy.md](./alloy.md)
- **Infrastructure**: [../../../infra/06-observability/alloy/README.md](../../../../infra/06-observability/alloy/README.md)

---

#### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

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

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/incidents/README.md](../../incidents/README.md)
