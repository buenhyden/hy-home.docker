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
- **Procedure**: `[../07.operations/06-observability/pyroscope.md](../../07.operations/06-observability/pyroscope.md)`

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/07.operations/06-observability/pyroscope.md` during the 2026-05-10 operations taxonomy consolidation.

### Pyroscope System Usage

> Continuous profiling and performance analysis.

---

#### Overview (KR)

이 문서는 Pyroscope에 대한 가이드다. Pyroscope는 애플리케이션의 런타임 성능 데이터(CPU 사용량, 메모리 할당 등)를 지속적으로 수집(Continuous Profiling)하여 시각화한다. 이를 통해 성능 병목 지점, 데드락, 메모리 누수 등을 플레임그래프(Flamegraph)를 통해 직관적으로 분석할 수 있다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- SRE / DevOps
- Agent-tuner

#### Purpose

Pyroscope의 핵심 기능인 지속적 프로파일링의 원리를 이해하고, Grafana와 연동하여 성능 문제를 분석하는 방법을 익힌다.

#### Prerequisites

- [Grafana Alloy](alloy.md) 프로파일링 수집 설정 완료
- [Grafana](grafana.md) Pyroscope 데이터 소스 연결

#### Step-by-step Instructions

##### 1. 프로파일링 데이터 확인 (Exploration)

Grafana의 `Explore` 메뉴에서 `Pyroscope` 데이터 소스를 선택한다. `Application` 레이블을 필터링하여 특정 서비스의 최근 프로파일 데이터를 조회할 수 있다.

##### 2. 플레임그래프(Flamegraph) 분석

- **CPU Profile**: 어떤 함수가 CPU 시간을 가장 많이 점유하고 있는지 확인한다. 넓은 bar는 해당 함수의 자체 실행 시간(Self Time) 또는 하위 호출 시간(Total Time)이 길다는 것을 의미한다.
- **Memory Profile**: 객체 할당(Allocations) 및 현재 점유 중인 메모리(In-use)를 분석하여 메모리 누수를 추적한다.

##### 3. 시간대 비교 (Diff View)

성능 저하가 발생하기 전과 후의 프로파일을 비교하여 변경된 코드 경로를 식별한다.

##### 4. 분산 추적 연동 (Trace-to-Profile)

Tempro와 연동되어 있는 경우, 특정 Trace ID와 관련된 프로파일을 바로 확인하여 요청 단위의 성능 병목을 수직적으로 분석할 수 있다.

#### Common Pitfalls

- **오버헤드 (Overhead)**: 프로파일링 수집 빈도가 너무 높으면 애플리케이션 성능에 영향을 줄 수 있다. 기본 수집 주기를 유지하고 필요한 경우에만 조정하라.
- **레이블 카디널리티 (Label Cardinality)**: 너무 많은 고유 레이블(예: Request ID)을 프로파일에 추가하면 Pyroscope의 인덱싱 부하가 급증한다.
- **언어별 지원 차이**: Go, Java, Python, Rust 등 언어마다 수집 가능한 프로파일 종류(CPU, Mem, Block, Goroutine 등)가 다르므로 지원 범위를 확인하라.

#### Related Documents

- **Infrastructure**: `[infra/06-observability/pyroscope/README.md](../../../infra/06-observability/pyroscope/README.md)`
- **Operation**: `[../07.operations/06-observability/pyroscope.md](../../07.operations/06-observability/pyroscope.md)`
- **Procedure**: `[../07.operations/06-observability/pyroscope.md](../../07.operations/06-observability/pyroscope.md)`

## Procedure

> Migrated from `docs/07.operations/06-observability/pyroscope.md` during the 2026-05-10 operations taxonomy consolidation.

### Pyroscope Recovery Procedure

> Troubleshooting and recovery procedures for continuous profiling.

---

#### Overview (KR)

이 문서는 Pyroscope 서비스 장애 발생 시 복구 절차를 정의한다. 프로파일 데이터 인입 중단, 저장소 공간 부족, 쿼리 성능 저하 등의 일반적인 데브옵스 시나리오를 다룬다.

#### Procedure Type

`recovery-runbook`

#### Potential Issues & Symptoms

##### 1. Ingestion Gaps (데이터 수집 중단)

- **Symptom**: Grafana 플레임그래프에 데이터가 표시되지 않음.
- **Check**: `infra-pyroscope` 컨테이너 로그 및 `infra-alloy` 송신 로그 확인.
- **Resolution**:

  ```bash
  docker compose restart pyroscope
  docker compose restart alloy
  ```

##### 2. Disk Space Pressure (저장소 부족)

- **Symptom**: 컨테이너가 `Read-only` 모드로 전환되거나 비정상 종료됨.
- **Check**: `df -h`로 `/var/lib/pyroscope` 마운트 지점 확인.
- **Resolution**:
  - `pyroscope.yaml`에서 retention 설정 축소.
  - 오래된 데이터 수동 삭제 (주의: 서비스 중단 후 수행 권장).

##### 3. High CPU Usage (수집 부하)

- **Symptom**: 호스트 시스템 CPU 사용률 급증.
- **Check**: `docker stats pyroscope`.
- **Resolution**:
  - `pyroscope.yaml`의 `ingestion_rate_limit` 조정.
  - Alloy에서 수집 대상 서비스 필터링 강화.

#### Recovery Steps

##### Emergency Restart

```bash
### Move to infra directory
cd infra/06-observability

### Restart Pyroscope
docker compose restart pyroscope

### Verify Health
curl -f http://localhost:4040/health
```

##### Configuration Rollback

설정 변경 후 장애 발생 시 `infra/06-observability/pyroscope/config/pyroscope.yaml`을 이전 버전으로 복구하고 재시작한다.

#### Post-Mortem Usagelines

- 장애 발생 시간과 복구 시간을 기록한다.
- `alloy` 레이블 매핑 오류였는지, `pyroscope` 자체 저장소 문제였는지 원인을 규명한다.
- 재발 방지를 위해 알림 임계값(Alert Threshold) 조정을 검토한다.

#### Related Documents

- **Infrastructure**: `[infra/06-observability/pyroscope/README.md](../../../infra/06-observability/pyroscope/README.md)`
- **Usage**: `[../../07.operations/06-observability/pyroscope.md](../../07.operations/06-observability/pyroscope.md)`
- **Operation**: `[../../07.operations/06-observability/pyroscope.md](../../07.operations/06-observability/pyroscope.md)`

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
