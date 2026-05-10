# Valkey Cluster Operations Policy

> `docs/07.operations/04-data/valkey-cluster.md`에 대한 운영 정책 문서입니다.

---

## Overview (KR)

이 문서는 Valkey Cluster의 운영 표준, 데이터 보호 정책 및 성능 관리 기준을 정의합니다. 시스템의 안정성과 고가용성을 유지하기 위한 통제 항목을 포함합니다.

## Policy Scope

Valkey 6노드 분산 클러스터의 영속성(Persistence), 메모리 관리, 보안 및 모니터링 정책을 관리합니다.

## Applies To

- **Systems**: `valkey-cluster` (node 0-5)
- **Agents**: Data Infrastructure Agents, SRE Agents
- **Environments**: Production, Staging

## Controls

- **Required**:
  - `appendonly yes`: 데이터 영속성을 위해 AOF 활성화 필수
  - `maxmemory-policy allkeys-lru`: 메모리 부족 시 LRU 기반 키 제거 정책 적용
  - Docker Secrets을 통한 패스워드 주입 및 인증 필수
- **Allowed**:
  - 특정 노드에 대한 Read-only 복제본 추가 확장
  - 유지보수 환경에서의 일시적인 `SAVE` 명령 실행
- **Disallowed**:
  - `CONFIG SET`을 통한 런타임 클러스터 비활성화 금지
  - 패스워드 없는 노드 노출 금지
  - 승인되지 않은 외부 네트워크에서의 직접 접속 차단

## Exceptions

- 대량 데이터 마이그레이션 시 초기 속도 향상을 위해 일시적으로 AOF를 끌 수 있으나, 작업 완료 후 즉시 재활성화하고 상태를 검증해야 함 (Infrastructure Lead 승인 필요).

## Verification

- **Metrics**: Grafana 대시보드에서 `cluster_state:ok` 유무를 실시간 감시합니다.
- **Audit**: 정기적으로 `cluster nodes` 명령을 통해 모든 노드의 연결 상태를 확인합니다.

## Review Cadence

- Quarterly (분기별 운영 데이터 및 장애 이력 검토)

## Related Documents

- **PRD**: [2026-03-26-04-data.md](../../01.prd/2026-03-26-04-data.md)
- **ARD**: [0004-data-architecture.md](../../02.ard/0004-data-architecture.md)
- **Spec**: [spec.md](../../04.specs/04-data/spec.md)
- **Procedure**: [valkey-cluster.md](../../07.operations/04-data/valkey-cluster.md)
- **Usage**: [valkey-cluster.md](../../07.operations/04-data/valkey-cluster.md)

---

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Usage

> Migrated from `docs/07.operations/04-data/valkey-cluster.md` during the 2026-05-10 operations taxonomy consolidation.

### Valkey Cluster Usage

> `docs/07.operations/04-data/valkey-cluster.md`에 대한 안내 문서입니다.

---

#### Overview (KR)

이 문서는 Valkey Cluster의 아키텍처, 설정 및 사용 방법에 대한 기술 가이드입니다. 6노드 기반의 고가용성 캐시 클러스터를 이해하고 애플리케이션에 통합하는 데 필요한 정보를 제공합니다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- Agent-tuner

#### Purpose

애플리케이션 개발자와 시스템 운영자가 Valkey Cluster의 구조를 이해하고, 클라이언트를 올바르게 연결하며, 성능 최적화 기법을 적용할 수 있도록 돕습니다.

#### Prerequisites

- `infra/04-data/cache-and-kv/valkey-cluster`에 대한 기본 지식
- Docker 및 Docker Compose 실행 환경
- Redis Cluster 호환 프로토콜 사용 가능 클라이언트 라이브러리

#### Step-by-step Instructions

##### 1. 클러스터 초기화 및 상태 확인

클러스터는 처음 배포 시 `valkey-cluster-init` 컨테이너에 의해 자동으로 구성됩니다.

```bash
### 클러스터 구성 상태 확인
read -rsp "Valkey password: " VALKEY_PASSWORD; echo
docker exec valkey-node-0 valkey-cli -a "$VALKEY_PASSWORD" cluster info
unset VALKEY_PASSWORD
```

##### 2. 클라이언트 연결 설정 (Cluster Mode)

Valkey Cluster는 샤딩된 환경이므로 모든 노드 정보를 클라이언트에 제공해야 합니다.

- **Seed Nodes**: `valkey-node-0:6379`, `valkey-node-1:6380`, `valkey-node-2:6381`, `valkey-node-3:6382`, `valkey-node-4:6383`, `valkey-node-5:6384`
- **Auth**: Docker Secrets에 정의된 패스워드를 사용합니다.
- **Redirection**: 클라이언트는 `MOVED` 또는 `ASK` 응답을 처리할 수 있어야 합니다.

##### 3. 데이터 파티셔닝 이해

총 16,384개의 해시 슬롯이 3개의 마스터 노드에 분산되어 있습니다.

- Node 0: `0 - 5460`
- Node 1: `5461 - 10922`
- Node 2: `10923 - 16383`

#### Common Pitfalls

- **Single Node Access**: 클러스터 지원이 없는 라이브러리로 특정 노드에만 접속할 경우, 슬롯 불일치 시 `MOVED` 오류가 발생하며 작업이 거부됩니다.
- **Large Keys / Operations**: 클러스터 전체 성능 저하를 방지하기 위해 단일 Key에 과도한 데이터를 담거나 `KEYS *` 등의 전체 스캔 명령은 금지합니다.
- **Network Isolation**: 노드 간 통신(6379+10000 포트 등)이 막히면 슬롯 소유권 확인이 불가능해져 클러스터가 `fail` 상태로 전환됩니다.

#### Related Documents

- **PRD**: [2026-03-26-04-data.md](../../01.prd/2026-03-26-04-data.md)
- **ARD**: [0004-data-architecture.md](../../02.ard/0004-data-architecture.md)
- **Spec**: [spec.md](../../04.specs/04-data/spec.md)
- **Operation**: [valkey-cluster.md](../../07.operations/04-data/valkey-cluster.md)
- **Procedure**: [valkey-cluster.md](../../07.operations/04-data/valkey-cluster.md)

## Procedure

> Migrated from `docs/07.operations/04-data/valkey-cluster.md` during the 2026-05-10 operations taxonomy consolidation.

### Valkey Cluster Recovery Procedure

: `valkey-cluster`

---

#### Overview (KR)

이 런북은 Valkey Cluster에서 발생할 수 있는 노드 장애, 슬롯 불일치 및 네트워크 파티션 상황에 대한 긴급 복구 절차를 정의합니다.

#### Purpose

장애 상황에서 클러스터를 정상 상태(`cluster_state:ok`)로 신속히 복구하고 데이터 무결성을 보장합니다.

#### Canonical References

- **PRD**: [2026-03-26-04-data.md](../../01.prd/2026-03-26-04-data.md)
- **ARD**: [0004-data-architecture.md](../../02.ard/0004-data-architecture.md)
- **Spec**: [spec.md](../../04.specs/04-data/spec.md)
- **Operation**: [valkey-cluster.md](../../07.operations/04-data/valkey-cluster.md)
- **Usage**: [valkey-cluster.md](../../07.operations/04-data/valkey-cluster.md)

#### When to Use

- `cluster_state:fail` 상태가 감지될 때
- `cluster_slots_assigned`가 16384 미만일 때
- 프라이머리 노드 다운 후 자동 페일오버가 실패했을 때

#### Procedure or Checklist

##### Checklist

- [ ] 모든 Valkey 노드 컨테이너가 Running 상태인지 확인
- [ ] 노드 간 네트워크 통신이 가능한지 확인
- [ ] 마스터 패스워드 secret(`service_valkey_password`) 파일 존재와 mount 상태 확인. 값은 출력하지 않는다.

##### Procedure

###### 1. 클러스터 상태 진단

```bash
read -rsp "Valkey password: " VALKEY_PASSWORD; echo
docker exec valkey-node-0 valkey-cli -a "$VALKEY_PASSWORD" --cluster check localhost:6379
unset VALKEY_PASSWORD
```

###### 2. 슬롯 자동 복구 (Inconsistent Slots)

슬롯 할당 불일치 시 다음 명령을 통해 자동으로 슬롯을 재할당하거나 수정합니다.

```bash
read -rsp "Valkey password: " VALKEY_PASSWORD; echo
docker exec valkey-node-0 valkey-cli -a "$VALKEY_PASSWORD" --cluster fix localhost:6379
unset VALKEY_PASSWORD
```

###### 3. 실패한 노드 수동 리셋 (Node Recovery)

복구된 노드가 클러스터에 합류하지 못할 경우:

```bash
### 해당 노드에서
read -rsp "Valkey password: " VALKEY_PASSWORD; echo
docker exec [failed-node] valkey-cli -a "$VALKEY_PASSWORD" cluster reset soft
### 마스터 노드에서 다시 추가
docker exec valkey-node-0 valkey-cli -a "$VALKEY_PASSWORD" --cluster add-node [new-ip]:[port] [master-ip]:[port]
unset VALKEY_PASSWORD
```

#### Verification Steps

- [ ] `valkey-cli cluster info | grep cluster_state` 결과가 `ok`인지 확인
- [ ] `valkey-cli cluster nodes` 결과 모든 노드가 `connected` 상태인지 확인

#### Observability and Evidence Sources

- **Signals**: Prometheus Alert `ValkeyClusterDown`
- **Evidence to Capture**: `valkey-cli cluster nodes` 출력 결과, 노드 에러 로그

#### Safe Rollback or Recovery Procedure

- 클러스터 데이터 손상이 심각할 경우, 모든 노드를 중지하고 데이터 볼륨의 백업본(RDB/AOF)을 복원한 후 클러스터를 재구성합니다.

---

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
