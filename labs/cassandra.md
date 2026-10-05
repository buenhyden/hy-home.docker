---
title: "Cassandra LAB"
version: "1.0.3"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2025-11-12"
---

# Cassandra LAB

## Overview

이 문서는 root Compose에서 분리된 Cassandra LAB topology의 source 계약을
설명한다. normal HOME 또는 development stack의 상태·network·secret을 공유하지
않으며, LAB 학습과 정적 render에만 사용한다.

## Audience

- 개발자: 이 실습 topology의 연결과 상태 경계를 확인합니다.
- 운영자: 격리된 LAB 렌더링과 복구 전제만 확인합니다.
- Agent: root Compose와 분리된 보조 자산 경로를 추적합니다.

## Scope

### In Scope

- 단일 Cassandra node의 학습·render 계약

### Out of Scope

- HOME 서비스, 관리 DB, root Compose, 운영 데이터와 credential 값
- 실제 기동, 중지, 데이터 이관·삭제, credential rotation

## Tech Stack

| Category | Source of truth | Boundary |
| --- | --- | --- |
| Compose | [cassandra.yml](./cassandra.yml) | 독립 LAB project |
| State | `${LAB_DATA_DIR:?set isolated LAB data root}/cassandra/node1`을 `/var/lib/cassandra`에 mount | HOME 상태와 미공유 |
| Authentication | 공식 Cassandra 이미지 기본값; LAB 내부망 외 노출 없음 | 비밀번호 인증 미구성 |
| Networks | LAB 전용 network declarations | root network와 미공유 |

## Structure

```text
labs/
├── cassandra.yml
└── cassandra.md
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Entry point | [cassandra.yml](./cassandra.yml) |
| Project | `hy-home-lab-cassandra` |
| State | `${LAB_DATA_DIR:?set isolated LAB data root}/cassandra/node1` → `/var/lib/cassandra` |
| Networks | `lab_cassandra_core_net` |
| Secret refs | 없음; 공식 이미지가 이전 Bitnami password-file 입력을 소비하지 않음 |
| Host exposure | host port 없음; LAB network 내부 expose만 선언 |
| Helper assets | 없음 |
| Readiness | Compose healthcheck/one-shot dependency declarations only; runtime result is unverified |

## Usage

1. `LAB_DATA_DIR`을 독립 상태 경로로 지정한다.
2. 실제 기동 없이 `LAB_DATA_DIR=/tmp/hyhome-cassandra-static docker compose --env-file labs/.env.example -f labs/cassandra.yml --profile '*' config --quiet`로 렌더링한다.
3. LAB Compose project, network, volume, port가 HOME 또는 management 경로와 겹치지 않는지 검토한다.
4. 컨테이너 실행·정지·삭제와 실제 복구는 별도 운영 승인을 따른다.

## Available Scripts

| Command | Description |
| --- | --- |
| `LAB_DATA_DIR=/tmp/hyhome-cassandra-static docker compose --env-file labs/.env.example -f labs/cassandra.yml --profile '*' config --quiet` | LAB source render만 검증; 컨테이너를 만들지 않음 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| --- | ---: | --- |
| `LAB_DATA_DIR` | Yes for bind-backed LAB state | isolated LAB data root; unset이면 fail fast |
| LAB-specific port/network keys | No | Compose의 LAB default만 사용하며 root key와 공유하지 않음 |

## Validation

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

## Troubleshooting

- `LAB_DATA_DIR` unset 오류는 안전한 fail-fast 동작이다. HOME data path를 대입하지 않는다.
- 실제 cluster 재초기화·volume 삭제·restore는 별도 승인 없이는 실행하지 않는다.

## Related Documents

- [Architecture index](../docs/02.architecture/README.md)
- [Operations index](../docs/05.operations/README.md)
