---
title: "Valkey Cluster LAB"
version: "1.0.2"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2025-11-12"
---

# Valkey Cluster LAB

## Overview

이 문서는 root Compose에서 분리된 Valkey Cluster LAB topology의 source 계약을
설명한다. normal HOME 또는 development stack의 상태·network·secret을 공유하지
않으며, LAB 학습과 정적 render에만 사용한다.

## Audience

- 개발자: 이 실습 topology의 연결과 상태 경계를 확인합니다.
- 운영자: 격리된 LAB 렌더링과 복구 전제만 확인합니다.
- Agent: root Compose와 분리된 보조 자산 경로를 추적합니다.

## Scope

### In Scope

- 6-node Valkey cluster, initializer, exporter의 학습·render 계약
- 보조 config/script: `../infra/04-data/valkey-cluster/`

### Out of Scope

- HOME 서비스, 관리 DB, root Compose, 운영 데이터와 credential 값
- 실제 기동, 중지, 데이터 이관·삭제, credential rotation

## Tech Stack

| Category | Source of truth | Boundary |
| --- | --- | --- |
| Compose | [valkey-cluster.yml](./valkey-cluster.yml) | 독립 LAB project |
| State | `${LAB_DATA_DIR:?set isolated LAB data root}` 또는 project-scoped named volume | HOME 상태와 미공유 |
| Secrets | `${LAB_SECRET_DIR:-../secrets/labs}` 아래 LAB 전용 reference | 값은 문서화하지 않음 |
| Networks | LAB 전용 network declarations | root network와 미공유 |

## Structure

```text
labs/
├── valkey-cluster.yml
└── valkey-cluster.md
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Entry point | [valkey-cluster.yml](./valkey-cluster.yml) |
| Project | `hy-home-lab-valkey-cluster` |
| State | `${LAB_DATA_DIR:?set isolated LAB data root}/valkey-cluster/data-{0..5}` |
| Networks | `lab_valkey_core_net`, `lab_valkey_obs_net` |
| Secret refs | `lab_valkey_password` |
| Host exposure | loopback의 `LAB_VALKEY0_HOST_PORT`~`LAB_VALKEY5_HOST_PORT` (default 17379~17384; 내부 6379~6384 고정) |
| Helper assets | `../infra/04-data/valkey-cluster/config/`, `scripts/` |
| Readiness | Compose healthcheck/one-shot dependency declarations only; runtime result is unverified |

## How to Work in This Area

1. `LAB_DATA_DIR`과 LAB secret reference directory를 독립 경로로 지정한다.
2. 실제 기동 없이 `LAB_DATA_DIR=/tmp/hyhome-valkey-cluster-static docker compose --env-file labs/.env.example -f labs/valkey-cluster.yml --profile '*' config --quiet`로 렌더링한다.
3. LAB Compose project, network, volume, port와 secret reference가 HOME 또는 management 경로와 겹치지 않는지 검토한다.
4. 컨테이너 실행·정지·삭제와 실제 복구는 별도 운영 승인을 따른다.

## Available Scripts

| Command | Description |
| --- | --- |
| `LAB_DATA_DIR=/tmp/hyhome-valkey-cluster-static docker compose --env-file labs/.env.example -f labs/valkey-cluster.yml --profile '*' config --quiet` | LAB source render만 검증; 컨테이너를 만들지 않음 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| --- | ---: | --- |
| `LAB_DATA_DIR` | Yes for bind-backed LAB state | isolated LAB data root; unset이면 fail fast |
| `LAB_SECRET_DIR` | No | unset이면 `../secrets/labs` reference path 사용 |
| LAB-specific port/network keys | No | Compose의 LAB default만 사용하며 root key와 공유하지 않음 |

## Validation

Classification은 `LAB`입니다. 이 topology는 독립 Compose project, LAB 전용
network, secret reference, state path를 사용합니다. 같은 host의 여러 member는
host-level HA를 증명하지 않습니다. 정적 render 통과는 실행·인증·복구 증거가
아닙니다.

Valkey node는 `/run` tmpfs의 0600 설정 파일을 사용하고 exporter/CLI는
비밀번호를 runtime 환경 변수로 전달합니다. 실제 인증과 cluster 결성은
격리 실행 전까지 검증되지 않았습니다. 기존 node에 metadata가 남았지만
cluster 상태가 정상이 아니면 init job은 실패하며 자동 재초기화하지 않습니다.

## Troubleshooting

- `LAB_DATA_DIR` unset 오류는 안전한 fail-fast 동작이다. HOME data path를 대입하지 않는다.
- secret file 누락이나 설정에서 허용되지 않는 credential 문자는 LAB secret reference를 교정해야 하는 상태이며 값의 공개나 root secret 재사용 사유가 아니다.
- 실제 cluster 재초기화·volume 삭제·restore는 별도 승인 없이는 실행하지 않는다.

## Related Documents

- [Architecture index](../docs/02.architecture/README.md)
- [Operations index](../docs/05.operations/README.md)
