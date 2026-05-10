<!-- Target: docs/05.operations/09-tooling/locust.md -->

# Locust Operations Policy

> Locust 기반 성능 테스트 인프라의 운영 안정성 및 거버넌스 지침입니다.

---

## Overview (KR)

이 문서는 로드 테스팅 수행 시 발생할 수 있는 부작용(운영 서비스 영향 등)을 방지하고, 성능 데이터의 신뢰성을 보장하기 위한 운영 정책을 정의합니다.

## Target Audience

- Operator
- Performance Engineer
- SRE

## Policy Goals

- **가용성 보존**: 대규모 테스트 중 Gateway 등 인프라 코어의 무결성 유지.
- **지표 무결성**: InfluxDB에 전송되는 데이터의 일관성 및 정확성 확보.
- **비용 최적화**: 테스트 미수행 시 워커 노드의 유휴 자원 최소화.

## Operational Standards

### 1. 테스트 실행 거버넌스 (Governance)

- **사전 승인**: 초당 5,000 요청 이상의 부하 테스트는 정기 유지보수 윈도우(02:00 ~ 04:00)에 수행하는 것을 권장함.
- **정의된 시나리오**: 모든 테스트는 Git에 관리되는 `locustfile.py`를 통해서만 수행해야 함.

### 2. 리소스 스케일링 정책 (Scaling)

- 테스트 종료 후 즉시 워커 노드를 기본값(`replicas: 2`)으로 축소해야 함.
- CPU/Memory 임계치(`template-infra-med`) 초과 시, 추가 수직 스케일링을 배포 설정에 반영해야 함.

### 3. 데이터 보존 및 보안 (Data & Security)

- **지표 보존**: InfluxDB 내의 부하 테스트 데이터는 90일간 보존하며, 이후 아카이빙함.
- **접근 통제**: 외부 부하 생성(External Load) 시, 반드시 인증 토큰 및 레이트 리밋 설정을 적용하여 무단 접근을 방지함.

## Security Controls

- **Secret Management**: InfluxDB API 토큰은 Docker Secret으로만 주입하며, 환경 변수에 평문 노출을 금지함.
- **Endpoint Protection**: Locust UI는 내부 어드민 망 또는 VPN 환경에서만 노출되도록 Gateway에서 제어함.

## Related Documents

- **Usage**: [Locust Load Testing Usage](./locust.md)
- **Procedure**: [Locust Recovery Procedure](./locust.md)

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

> Migrated from `docs/05.operations/09-tooling/locust.md` during the 2026-05-10 operations taxonomy consolidation.

### Locust Load Testing Usage

> `hy-home.docker` 환경에서 Locust를 사용한 부하 테스트 시나리오 작성 및 실행 가이드입니다.

---

#### Overview (KR)

이 문서는 Locust를 사용하여 플랫폼의 서비스를 벤치마킹하는 방법을 설명합니다. 특히, `influxdb-client`를 통한 성능 지표의 영구 저장 및 분산 워커 노드 환경 구성에 초점을 맞춥니다.

#### Usage Type

`system-guide | troubleshooting-guide`

#### Target Audience

- QA Engineer
- Performance Engineer
- SRE

#### Purpose

플랫폼 서비스의 가용성 임계치를 식별하고, 인프라 증설 또는 성능 최적화의 정량적 근거를 확보하기 위한 로드 테스팅 절차를 안내합니다.

#### Prerequisites

- **Python 지식**: 테스트 시나리오 작성을 위한 기초적인 Python 문법 이해.
- **네트워크 연결**: `infra_net` 내에서 `locust-master`와 `influxdb` 간의 가시성 확보.
- **Secrets**: InfluxDB 전송을 위한 API 토큰이 `secrets/influxdb_api_token`에 준비되어 있어야 함.

#### Step-by-step Instructions

##### 1. 테스트 시나리오 작성 (Scripting)

`locustfile.py` 파일을 생성하고 테스트 로직을 정의합니다.

```python
from locust import HttpUser, task, between

class BenchmarkUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def test_endpoint(self):
        self.client.get("/api/v1/health")
```

##### 2. 인프라 실행 (Deployment)

1. `infra/09-tooling/locust` 디렉토리로 이동합니다.
2. 서비스 시작: `docker-compose --profile tooling up -d`
3. 워커 확장 (최대 부하 시): `docker compose up --scale locust-worker=5 -d`

##### 3. 테스트 실행 및 UI 관리 (Execution)

1. 브라우저에서 `https://locust.${DEFAULT_URL}` (또는 `18089` 포트)로 접속합니다.
2. **Setup**: 수행할 가상 사용자 수(Users)와 초당 증가율(Spawn rate)을 입력합니다.
3. **Run**: `Start swarming`을 클릭하여 시나리오를 가동합니다.

##### 4. 지표 수집 확인 (Monitoring)

- 지표는 실시간으로 InfluxDB에 전송됩니다.
- Grafana의 `Load Testing Dashboard`를 연동하여 시계열 추이를 확인하십시오.

#### Common Pitfalls

- **Token 인식 실패**: `docker-compose.yml`의 `secrets` 경로 및 `locust-master`의 환경 변수 매핑을 확인하십시오.
- **Worker 미연결**: 워커는 `locust-master` 컨테이너 명칭을 호스트로 인식해야 하므로, 네트워크 설정에 유의하십시오.
- **InfluxDB v2 연동**: `influxdb-client` 라이브러리가 포함된 커스텀 이미지를 사용하는지 확인하십시오.

#### Related Documents

- **Infrastructure**: [Locust Infra Layer](../../../../infra/09-tooling/locust/README.md)
- **Operation**: [Locust Operations Policy](./locust.md)
- **Procedure**: [Locust Recovery Procedure](./locust.md)

## Procedure

> Migrated from `docs/05.operations/09-tooling/locust.md` during the 2026-05-10 operations taxonomy consolidation.

### Locust Recovery Procedure

> Locust 로드 테스팅 인프라의 장애 대응 및 복구 절차입니다.

---

#### Overview (KR)

이 문서는 Locust 마스터-워커 간의 연결 끊김, InfluxDB 전송 실패 또는 테스트 실행 중 발생하는 연쇄 장애 상황에서의 복구 방법을 안내합니다.

#### Target Audience

- Operator
- Performance Engineer
- SRE

#### Alerting & Monitoring

- **Connection Failure**: Locust UI 콘솔에 `Worker X disconnected` 메시지 발생 시.
- **Push Failure**: Docker 로그에 `InfluxDB connection timeout` 또는 `Invalid Token` 발생 시.
- **Performance Degradation**: 부하 테스트 수행 중 타 서비스의 응답 지연 시간이 급격히 증가할 때.

#### Recovery Procedures

##### 1. 즉각 중단 (Emergency Stop)

동작 중인 모든 부하 생성을 중단합니다.

- UI: `Stop` 버튼 클릭.
- CLI: `docker-compose -f infra/09-tooling/locust/docker-compose.yml stop`

##### 2. 워커 노드 재동기화 (Worker Resync)

마스터 노드가 재시작된 후 워커가 연결되지 않는 경우:

1. 마스터 상태 확인: `docker compose ps locust-master`
2. 워커 전체 재시공: `docker compose up --force-recreate -d locust-worker`
3. 로그 확인: `docker compose logs -f locust-worker` 에서 마스터 연결 시도 메시지 확인.

##### 3. InfluxDB 지표 유실 대응 (Data Link Recovery)

1. InfluxDB 가용성 점검: `mng-db` 또는 InfluxDB 컨테이너 헬스체크 확인.
2. 비밀번호/토큰 유효성 검증: `influxdb_api_token` 시크릿이 최신인지 확인.
3. 데이터 수동 플러시: 테스트 스크립트 내의 Buffer 설정을 조정하여 재시도.

##### 4. 테스트 결과 수동 아카이빙 (Manual Archiving)

InfluxDB가 장애일 때 로컬에서 결과를 내려받아야 하는 경우:

- Locust UI의 `Download Data` 메뉴를 사용하여 `Requests`, `Failures`, `Exceptions` CSV를 수동으로 백업함.

#### Post-Mortem Tasks

- 로드 테스트 시나리오가 시스템의 병목을 유도한 것인지, 인프라 동적 할당 실패인지 원인 파악.
- 재발 방지를 위한 `locustfile.py` 로직 최적화 및 타임아웃 설정 조정.

#### Related Documents

- **Usage**: [Locust Load Testing Usage](./locust.md)
- **Operation**: [Locust Operations Policy](./locust.md)

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
