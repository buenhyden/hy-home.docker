<!-- Target: docs/05.operations/09-tooling/performance-testing.md -->

# Performance Testing Operations Policy

> `hy-home.docker` 환경에서 Locust 기반 성능 테스트를 실행하기 위한 운영 지침 및 거버넌스입니다.

---

## Overview (KR)

이 문서는 로드 테스팅 및 벤치마킹 작업 시 시스템의 가용성과 안정성을 유지하기 위한 운영 정책을 정의합니다. 특히, 부하 테스트가 실제 운영 중인 다른 서비스에 미치는 영향을 최소화하고 지표의 무결성을 보장하는 방법을 다룹니다.

## Target Audience

- Operator
- Performance Engineer
- Infrastructure Admin

## Policy Goals

- **재현 가능성**: 모든 부하 테스트는 동일한 조건에서 재현될 수 있도록 관리되어야 함.
- **가용성 보존**: 테스트 중 임계 시스템(Gateway, Identity)의 다운타임을 방지해야 함.
- **데이터 보존**: 테스트 결과 지표(InfluxDB)를 벤치마킹 자산으로 안전하게 보관해야 함.

## Operational Standards

### 1. 테스트 예약 및 사전 공지 (Pre-testing)

- **부하 규모**: 초당 10,000 요청 이상의 대규모 테스트 시 사전에 인프라 팀과 협조해야 함.
- **영향 범위**: 테스트 대상 서비스뿐만 아니라 공유 자원(데이터베이스, 네트워크 대역폭)에 대한 부하를 고려해야 함.

### 2. 환경 격리 (Environment Isolation)

- **네트워크**: `infra_net` 내에서 실행되며, 필요한 경우 부하 생성을 위한 전용 워커 노드를 분리하여 배치함.
- **데이터베이스**: 가능한 경우 실제 운영 DB가 아닌 복제본 또는 테스트 전용 환경을 대상으로 테스트를 수행해야 함.

### 3. 지표 관리 및 보존 (Retention)

- **이력 관리**: 모든 공식 테스트 결과는 InfluxDB에 타임스탬프와 함께 보관하며, Grafana 대시보드를 통해 보고서 형태로 아카이빙함.
- **정기 백업**: InfluxDB의 데이터는 주기적으로 백업되어야 하며, 특히 릴리스 전 공식 벤치마킹 데이터는 삭제되지 않도록 보호해야 함.

## Security Controls

- **UI 접근 제어**: Locust 마스터 UI는 내부 어드민 도메인(`/locust`)을 통해서만 접근 가능하며, 필요시 기본 인증을 적용함.
- **데이터 무결성**: 테스트 중 주입되는 가상 데이터가 실제 사용자 데이터와 혼용되지 않도록 프리픽스(e.g., `test_user_`)를 사용해야 함.

## Governance & Compliance

이 정책은 플랫폼의 전체 성능 가용성 기준을 따르며, 모든 테스트 수행 이력은 감사(Audit) 대상이 될 수 있습니다.

## Related Documents

- **Usage**: [Performance Testing Usage](./performance-testing.md)
- **Procedure**: [Performance Testing Recovery Procedure](./performance-testing.md)

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

> Migrated from `docs/05.operations/09-tooling/performance-testing.md` during the 2026-05-10 operations taxonomy consolidation.

### Performance Testing Usage

> `hy-home.docker` 환경에서 Locust를 활용한 분산 부하 테스트 및 성능 벤치마킹 통합 가이드입니다.

---

#### Overview (KR)

이 문서는 플랫폼의 엔드포인트를 벤치마킹하고 성능 병목 지점을 식별하기 위한 성능 테스트 워크플로우를 설명합니다. **Locust**(Python 기반)를 사용하여 시나리오를 작성하고, **InfluxDB**와 **Grafana**를 연동하여 지표를 분석하는 방법을 다룹니다.

#### Usage Type

`system-guide | troubleshooting-guide`

#### Target Audience

- Developer
- Operator
- Performance Engineer

#### Purpose

이 가이드는 사용자가 초당 수천 명의 가상 사용자를 시뮬레이션하여 시스템의 임계치를 확인하고, 인프라 최적화의 근거 데이터를 확보할 수 있도록 돕는 것을 목적으로 합니다.

#### Prerequisites

- **Python 지식**: 테스트 시나리오 작성을 위한 기초적인 Python 문법 이해.
- **네트워크 연결**: 테스트 대상 서비스가 `infra_net` 내에서 `locust-master/worker`와 통신 가능해야 함.
- **InfluxDB**: 지표 저장을 위해 InfluxDB 서비스가 실행 중이어야 함.

#### Step-by-step Instructions

##### 1. 테스트 시나리오 작성 (Scripting)

성능 테스트 시나리오는 `locustfile.py`에 정의합니다.

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5) # 초 단위 대기 시간

    @task
    def index_page(self):
        self.client.get("/")
```

##### 2. 분산 환경 실행 (Orchestration)

1. `infra/09-tooling/k6` 디렉토리로 이동합니다.
2. 서비스를 시작합니다: `docker-compose --profile tooling up -d`
3. 부하량에 따라 워커를 확장합니다: `docker-compose up --scale locust-worker=5 -d`

##### 3. 부하 가동 및 모니터링 (Execution)

1. `https://locust.${DEFAULT_URL}` 웹 UI에 접속합니다.
2. **Number of users**(가상 사용자 수)와 **Ramp-up**(초당 증가 수)를 설정하고 `Start swarming`을 클릭합니다.
3. 실시간 통계 및 차트를 확인합니다.

##### 4. 결과 분석 (Analysis)

- Locust UI에서 실시간 데이터를 확인하거나,
- **Grafana**의 `Load Testing Dashboard`를 통해 InfluxDB에 저장된 이력 데이터를 심도 있게 분석합니다.

#### Common Pitfalls

- **Ramp-up 설정 미흡**: 순간적인 대량 요청은 운영 시스템에 서지(Surge)를 발생시켜 의도치 않은 장애를 유발할 수 있습니다. 반드시 서서히 부하를 늘리십시오.
- **Worker 연결 실패**: 마스터 컨테이너 명칭(`locust-master`) 및 Docker 네트워크 가시성을 확인하십시오.
- **마스터 노드 과부하**: 마스터 노드는 데이터 수집 역할만 수행하도록 하고, 실제 부하 발생은 전적으로 워커 노드에서 담당해야 합니다.

#### Related Documents

- **Operation**: [Performance Testing Operations Policy](./performance-testing.md)
- **Procedure**: [Performance Testing Recovery Procedure](./performance-testing.md)

## Procedure

> Migrated from `docs/05.operations/09-tooling/performance-testing.md` during the 2026-05-10 operations taxonomy consolidation.

### Performance Testing Recovery Procedure

> Locust 부하 테스트 인프라 장애 시 대응 및 복구 절차를 정의합니다.

---

#### Overview (KR)

이 문서는 Locust 마스터/워커 노드의 연결 끊김, InfluxDB 지표 수집 장애 또는 성능 테스트로 인한 타 서비스 과부하 발생 시의 긴급 조치 방법을 안내합니다.

#### Target Audience

- Operator
- Performance Engineer
- SRE

#### Alerting & Monitoring

- **Locust UI Error**: 웹 인터페이스에서 `Worker disconnected` 경고 발생 시.
- **Metric Loss**: InfluxDB로의 데이터 전송 실패가 Locust 콘솔에 출력될 때.
- **Target Down**: 부하 테스트 시작 후 대상 서비스의 가용성 지표(SLI)가 급격히 하락할 때.

#### Recovery Procedures

##### 1. 테스트 강제 중단 (Emergency Stop)

가장 우선적으로 부하 생성을 즉시 중단합니다.

- **Locust UI**: UI에서 `Stop` 버튼을 클릭합니다.
- **CLI**: `docker-compose -f infra/09-tooling/k6/docker-compose.yml stop` 명령을 실행합니다.

##### 2. 마스터-워커 연결 복구 (Master-Worker Sync)

워커 노드가 마스터를 찾지 못하는 경우:

1. 마스터 활성 상태 확인: `docker-compose ps locust-master`
2. 환경 변수 확인: 워커의 `LOCUST_MASTER_NODE_HOST`가 올바른지 확인합니다.
3. 서비스 재시작: `docker-compose restart locust-master locust-worker`

##### 3. InfluxDB 데이터 전송 오류 (Data Link Recovery)

1. InfluxDB 서비스 상태 확인: `docker-compose ps influxdb`
2. 네트워크 가시성 확인: `docker-compose exec locust-master ping influxdb`
3. Locust 설정 확인: `locustfile.py` 내의 InfluxDB 엔드포인트 설정을 점검합니다.

##### 4. 타 서비스 영향 복구 (Cascading Failure Clean-up)

부하 테스트로 인해 다른 서비스가 마비된 경우:

- Gateway 캐시를 플러시하거나 서비스를 재시작하여 정상 상태로 돌려놓습니다.
- 테스트 결과 데이터를 분석하여 어느 지점에서 연쇄 장애가 시작되었는지 파악합니다.

#### Post-Mortem Tasks

- 장애 원인이 테스트 시나리오 설계 오류인지, 인프라 용량 부족인지 분석하여 보고서를 작성합니다.
- 재발 방지를 위해 테스트 스케일링 정책을 조정합니다.

#### Related Documents

- **Usage**: [Performance Testing Usage](./performance-testing.md)
- **Operation**: [Performance Testing Operations Policy](./performance-testing.md)

---

#### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

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
