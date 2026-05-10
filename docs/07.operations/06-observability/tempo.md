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
- **Usage**: `[../../07.operations/06-observability/tempo.md](../../07.operations/06-observability/tempo.md)`
- **Procedure**: `[../07.operations/06-observability/tempo.md](../../07.operations/06-observability/tempo.md)`

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/07.operations/06-observability/tempo.md` during the 2026-05-10 operations taxonomy consolidation.

### Tempo System Usage

> Distributed tracing and trace-to-metrics correlation.

---

#### Overview (KR)

이 문서는 Tempo에 대한 가이드다. Tempo는 분산 추적(Distributed Tracing) 데이터를 수집, 저장, 쿼리하는 시스템으로, 마이크로서비스 환경에서 요청의 흐름과 지연 시간(Latency)을 시각화한다. 특히 Span Metrics와 Service Graphs를 자동으로 생성하여 서비스 간의 의존성 지도를 제공한다.

#### Usage Type

`system-guide`

#### Target Audience

- Backend Developer
- SRE / DevOps
- Architect

#### Purpose

분산 추적의 기본 개념을 이해하고, TraceQL을 사용하여 성능 병목을 추적하며, 메트릭 및 로그와 연동하여 장애 원인을 파악하는 방법을 익힌다.

#### Prerequisites

- [Grafana Alloy](alloy.md) OTLP 수집 설정 완료
- [MinIO](../../../infra/04-data/lake-and-object/minio/README.md) `tempo-bucket` 생성을 통한 스토리지 확보
- [Grafana](grafana.md) Tempo 및 Prometheus 데이터 소스 연결

#### Step-by-step Instructions

##### 1. 분산 추적 데이터 조회 (TraceQL)

Grafana의 `Explore` 메뉴에서 `Tempo` 데이터 소스를 선택한다. `TraceQL` 쿼리 언어를 사용하여 특정 조건의 트레이스를 검색할 수 있다.

- 예: `{ duration > 100ms && resource.service.name = "api-gateway" }`

##### 2. Trace-to-Metrics Correlation

Tempo는 수집된 트레이스를 기반으로 메트릭(Span Metrics)을 생성하여 Prometheus로 전송한다. 트레이스 상세 뷰에서 관련 메트릭 대시보드로 바로 이동할 수 있다.

##### 3. Service Graphs 및 Dependency Map

`Metrics Generator`가 활성화된 경우, 서비스 간의 호출 관계와 에러율, 지연 시간을 시각화한 서비스 그래프를 확인할 수 있다.

##### 4. 로그와 연동 (Trace ID Correlation)

Loki 로그와 연동되어 있는 경우, 특정 로그 라인에 포함된 Trace ID를 클릭하여 해당 요청의 전체 트레이스 뷰로 전환할 수 있다.

#### Common Pitfalls

- **Instrumentation 누락**: 트레이스 전파(Propagation)가 끊기면 전체 요청 흐름을 볼 수 없다. 공통 라이브러리나 미들웨어에서 Context 전달을 확인하라.
- **WAL 관리**: 로컬 디스크의 WAL(Write-Ahead Log) 공간이 부족하면 트레이스 저장이 중단된다.
- **MinIO 연결**: Tempo와 MinIO 간의 네트워크 지연이나 설정 오류는 트레이스 조회를 불가능하게 만든다.

#### Related Documents

- **Infrastructure**: `[infra/06-observability/tempo/README.md](../../../infra/06-observability/tempo/README.md)`
- **Operation**: `[../07.operations/06-observability/tempo.md](../../07.operations/06-observability/tempo.md)`
- **Procedure**: `[../07.operations/06-observability/tempo.md](../../07.operations/06-observability/tempo.md)`

## Procedure

> Migrated from `docs/07.operations/06-observability/tempo.md` during the 2026-05-10 operations taxonomy consolidation.

### Tempo Recovery Procedure

> Troubleshooting and recovery procedures for distributed tracing.

---

#### Overview (KR)

이 문서는 Tempo 서비스 장애 발생 시 복구 절차를 정의한다. 트레이스 인입 안 됨, MinIO 연결 실패, WAL 손상, 쿼리 엔진 지연 등의 일반적인 시나리오를 다룬다.

#### Procedure Type

`recovery-runbook`

#### Potential Issues & Symptoms

##### 1. Broken Trace Ingestion (트레이스 누락)

- **Symptom**: Grafana에서 최근 트레이스가 검색되지 않음.
- **Check**: `infra-tempo` 로그 및 `distributor` 지표 확인.
- **Resolution**:

  ```bash
  docker compose restart tempo- [Tempo](./tempo.md)
  ```

  Alloy와 Tempo 간의 OTLP 엔드포인트(4317/4318) 도달 가능성 확인.

##### 2. Backend Storage Connection (MinIO 오류)

- **Symptom**: `Failed to write blocks to storage`, `S3 bucket access denied` 오류 로그 발생.
- **Check**: MinIO 버킷 권한 및 네트워크 연결 상태.
- **Resolution**:
  - `MINIO_APP_USERNAME` 및 비밀번호 환경 변수 재확인.
  - MinIO 인터페이스에서 `tempo-bucket` 존재 여부 확인.

##### 3. WAL Corruption (쓰기 버퍼 손상)

- **Symptom**: Tempo 재시작 시 `corrupt WAL` 오류와 함께 기동 실패.
- **Check**: `/var/tempo/wal` 디렉토리 파일 상태.
- **Resolution**:
  - WAL 파일 백업 후 해당 디렉토리 정리 (데이터 유실 주의).

##### 4. Metrics Generator Failure

- **Symptom**: 서비스 그래프나 Span Metrics가 대시보드에서 보이지 않음.
- **Check**: `tempo.yaml` 내 `remote_write` 설정 및 Prometheus 상태.
- **Resolution**:
  - Prometheus 엔드포인트 헬스체크.
  - Tempo 재시작 후 메트릭 생성 로그 모니터링.

#### Recovery Steps

##### Emergency Full Restart

```bash
### Move to infra directory
cd infra/06-observability

### Restart all related services
docker compose restart minio tempo alloy
```

##### Manual Bucket Check

MinIO 클라이언트(`mc`)를 사용하여 스토리지 상태를 점검한다.

#### Post-Mortem Usagelines

- 트레이스 유실 범위 및 시간을 기록한다.
- `alloy`에서 `tempo`로의 데이터 전달 병목이었는지, `tempo` 내부 압축기(Compactor) 문제였는지 분석한다.
- 재발 방지를 위해 저장소 모니터링 알림 임계값을 조정한다.

#### Related Documents

- **Infrastructure**: `[infra/06-observability/tempo/README.md](../../../infra/06-observability/tempo/README.md)`
- **Usage**: `[../../07.operations/06-observability/tempo.md](../../07.operations/06-observability/tempo.md)`
- **Operation**: `[../../07.operations/06-observability/tempo.md](../../07.operations/06-observability/tempo.md)`

---

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
