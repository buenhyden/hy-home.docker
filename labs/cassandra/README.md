---
title: "Cassandra LAB"
version: "1.0.6"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2025-11-12"
---

# Cassandra LAB

## Purpose

### Service Role

이 문서는 root Compose에서 분리된 Cassandra LAB topology의 source 계약을
설명한다. normal HOME 또는 development stack의 상태·network·secret을 공유하지
않으며, LAB 학습과 정적 render에만 사용한다.

#### Audience

- 개발자: 이 실습 topology의 연결과 상태 경계를 확인합니다.
- 운영자: 격리된 LAB 렌더링과 복구 전제만 확인합니다.
- Agent: root Compose와 분리된 보조 자산 경로를 추적합니다.

#### In Scope

- 단일 Cassandra node의 학습·render 계약

#### Out of Scope

- HOME 서비스, 관리 DB, root Compose, 운영 데이터와 credential 값
- 실제 기동, 중지, 데이터 이관·삭제, credential rotation

#### Structure

```text
labs/cassandra/
├── README.md          # 서비스 README
├── docker-compose.yml # 독립 LAB entrypoint
├── promotion.yaml     # SPEC-0263 승격 manifest
└── dashboards/        # LAB 전용 Grafana 대시보드
```

| Dashboard | UID | Source |
| --- | --- | --- |
| [`cassandra.json`](./dashboards/cassandra.json) | `hyhome-cassandra` | grafana.com dashboard 6400 revision 2 (2018-06-14) |

HOME Grafana는 `infra/06-observability/grafana/dashboards/`만 provisioning하므로
이 대시보드는 HOME에 표시되지 않고, HOME Prometheus는 LAB 서비스를 수집하지
않습니다. LAB 관측을 연결하는 별도 계약이 승인되면 그 LAB의 Prometheus·Grafana가
이 파일을 읽도록 구성하며, HOME provisioning 경로로 옮기지 않습니다.

### Supported Environment

| Category | Source of truth | Boundary |
| --- | --- | --- |
| Compose | [docker-compose.yml](./docker-compose.yml) | 독립 LAB project |
| State | `${LAB_DATA_DIR:?set isolated LAB data root}/cassandra/node1`을 `/var/lib/cassandra`에 mount | HOME 상태와 미공유 |
| Authentication | 공식 Cassandra 이미지 기본값; LAB 내부망 외 노출 없음 | 비밀번호 인증 미구성 |
| Networks | LAB 전용 network declarations | root network와 미공유 |

## Interfaces

### Inputs and Outputs

환경 변수 `LAB_DATA_DIR`이 가리키는 `${LAB_DATA_DIR}/cassandra/node1`을 `/var/lib/cassandra`에 mount하고 network는 `lab_cassandra_core_net`만 사용한다. 환경 변수는 아래 표와 같다.

#### Environment Variables

| Variable | Required | Description |
| --- | ---: | --- |
| `LAB_DATA_DIR` | Yes for bind-backed LAB state | isolated LAB data root; unset이면 fail fast |
| LAB-specific port/network keys | No | Compose의 LAB default만 사용하며 root key와 공유하지 않음 |

### Security Boundary

secret 참조는 없고 host port를 게시하지 않으며 LAB network 내부 expose만 선언한다. 비밀번호 인증은 구성되지 않았다.

## Development

### Local Workflow

1. `LAB_DATA_DIR`을 독립 상태 경로로 지정한다.
2. 실제 기동 없이 `LAB_DATA_DIR=/tmp/hyhome-cassandra-static docker compose --env-file labs/.env.example -f labs/cassandra/docker-compose.yml --profile '*' config --quiet`로 렌더링한다.
3. LAB Compose project, network, volume, port가 HOME 또는 management 경로와 겹치지 않는지 검토한다.
4. 기동은 `python3 scripts/operations/lab.py up cassandra --purpose "<목적>" --lease <30m|4h>`로만 한다. 이 명령은 다른 LAB·HOME과의 이름·port·data 경로 충돌, 예산과 동시 LAB 수를 먼저 검사하고 `${LAB_DATA_DIR}/.ledger/cassandra.json`에 정리 대상을 기록한다. 종료는 `lab.py down cassandra`이며 volume과 data를 지우지 않는다. 만료 lease는 `lab.py reap`이 정지한다 (정책 `POL-0078`).

#### Available Scripts

| Command | Description |
| --- | --- |
| `LAB_DATA_DIR=/tmp/hyhome-cassandra-static docker compose --env-file labs/.env.example -f labs/cassandra/docker-compose.yml --profile '*' config --quiet` | LAB source render만 검증; 컨테이너를 만들지 않음 |

### Checks

Classification은 `LAB`입니다. 이 topology는 독립 Compose project, LAB 전용
network와 state path를 사용합니다. 같은 host의 여러 member는
host-level HA를 증명하지 않습니다. 정적 render 통과는 실행·인증·복구 증거가
아닙니다.

공식 `cassandra:5.0.9`는 `CASSANDRA_USER`, `CASSANDRA_PASSWORD_FILE`,
`CASSANDRA_PASSWORD_SEEDER`를 소비하지 않습니다. 이전 Bitnami exporter 이미지와
`/bitnami/cassandra` 경로도 이 LAB에서 제거했습니다. 현재 단일 노드는
`lab_cassandra_core_net` 외 연결이 없지만 비밀번호 인증은 구성되지 않았습니다.
인증이 필요한 소비자가 생기면 공식 이미지 설정 파일과 계정 provisioning을
별도 승인된 LAB Task에서 추가해야 합니다. 실제 기동·데이터 권한은 미검증입니다.

## Operations

### Runbook Links

- [Architecture index](../../docs/02.architecture/README.md)
- [Operations index](../../docs/05.operations/README.md)

### Observability and Recovery

| Field | Evidence |
| --- | --- |
| Entry point | [docker-compose.yml](./docker-compose.yml) |
| Project | `hy-home-lab-cassandra` |
| Services | `cassandra-node1` |
| State | `${LAB_DATA_DIR:?set isolated LAB data root}/cassandra/node1` → `/var/lib/cassandra` |
| Networks | `lab_cassandra_core_net` |
| Secret refs | 없음; 공식 이미지가 이전 Bitnami password-file 입력을 소비하지 않음 |
| Host exposure | host port 없음; LAB network 내부 expose만 선언 |
| Helper assets | [promotion manifest](./promotion.yaml), [대시보드](./dashboards/cassandra.json) |
| Readiness | Compose healthcheck/one-shot dependency declarations only; runtime result is unverified |

#### Troubleshooting

- `LAB_DATA_DIR` unset 오류는 안전한 fail-fast 동작이다. HOME data path를 대입하지 않는다.
- 실제 cluster 재초기화·volume 삭제·restore는 별도 승인 없이는 실행하지 않는다.
