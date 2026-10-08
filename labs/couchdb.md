---
title: "CouchDB LAB"
version: "1.0.9"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
created: "2025-11-12"
---

# CouchDB LAB

## Overview

이 문서는 root Compose에서 분리된 CouchDB LAB topology의 source 계약을
설명한다. normal HOME 또는 development stack의 상태·network·secret을 공유하지
않으며, LAB 학습과 정적 render에만 사용한다.

## Audience

- 개발자: 이 실습 topology의 연결과 상태 경계를 확인합니다.
- 운영자: 격리된 LAB 렌더링과 복구 전제만 확인합니다.
- Agent: root Compose와 분리된 보조 자산 경로를 추적합니다.

## Scope

### In Scope

- 3-node CouchDB cluster와 initializer의 학습·render 계약

### Out of Scope

- HOME 서비스, 관리 DB, root Compose, 운영 데이터와 credential 값
- 실제 기동, 중지, 데이터 이관·삭제, credential rotation

## Tech Stack

| Category | Source of truth | Boundary |
| --- | --- | --- |
| Compose | [couchdb.yml](./couchdb.yml) | 독립 LAB project |
| State | `${LAB_DATA_DIR:?set isolated LAB data root}` bind | HOME 상태와 미공유 |
| Secrets | `${LAB_SECRET_DIR:-../secrets/labs}` 아래 LAB 전용 reference | 값은 문서화하지 않음 |
| Networks | LAB 전용 network declarations | root network와 미공유 |

## Structure

```text
labs/
├── couchdb.yml
├── couchdb-cluster-init.sh
└── couchdb.md
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Entry point | [couchdb.yml](./couchdb.yml) |
| Project | `hy-home-lab-couchdb` |
| Services | `couchdb-1`, `couchdb-2`, `couchdb-3`, `couchdb-cluster-init` |
| State | `${LAB_DATA_DIR:?set isolated LAB data root}/couchdb/data-{1..3}` |
| Networks | `lab_couchdb_core_net`, `lab_couchdb_edge_net` |
| Secret refs | `lab_couchdb_password`, `lab_couchdb_cookie` |
| Host exposure | `couchdb-1`만 `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_COUCHDB_HOST_PORT:-35984}`에 게시; HOME Traefik label 없음 (SPEC-0215) |
| Helper assets | [couchdb-cluster-init.sh](./couchdb-cluster-init.sh) |
| Readiness | Compose healthcheck/one-shot dependency declarations only; runtime result is unverified |

## Usage

1. `LAB_DATA_DIR`과 LAB secret reference directory를 독립 경로로 지정한다.
2. 실제 기동 없이 `LAB_DATA_DIR=/tmp/hyhome-couchdb-static docker compose --env-file labs/.env.example -f labs/couchdb.yml --profile '*' config --quiet`로 렌더링한다.
3. LAB Compose project, network, volume, port와 secret reference가 HOME 또는 management 경로와 겹치지 않는지 검토한다.
4. 기동은 `python3 scripts/operations/lab.py up couchdb --purpose "<목적>" --lease <30m|4h>`로만 한다. 이 명령은 다른 LAB·HOME과의 이름·port·data 경로 충돌, 예산과 동시 LAB 수를 먼저 검사하고 `${LAB_DATA_DIR}/.ledger/couchdb.json`에 정리 대상을 기록한다. 종료는 `lab.py down couchdb`이며 volume과 data를 지우지 않는다. 만료 lease는 `lab.py reap`이 정지한다 (정책 `POL-0078`).

## Available Scripts

| Command | Description |
| --- | --- |
| `LAB_DATA_DIR=/tmp/hyhome-couchdb-static docker compose --env-file labs/.env.example -f labs/couchdb.yml --profile '*' config --quiet` | LAB source render만 검증; 컨테이너를 만들지 않음 |

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

CouchDB 3.5.2의 공식 entrypoint가 admin과 Erlang cookie를 설정합니다.
cluster initializer의 curl 인증 및 JSON 본문은 격리된 `/tmp`의 0600 파일에서
읽으며 비밀번호를 명령 인자에 넣지 않습니다. 이미지의 초기 설정 파일 권한과
cluster 결성은 격리 실행 전까지 검증되지 않았습니다. 재실행 시 cluster가 이미
완료되어도 세 system DB의 존재를 다시 확인합니다.

## Troubleshooting

- `LAB_DATA_DIR` unset 오류는 안전한 fail-fast 동작이다. HOME data path를 대입하지 않는다.
- secret file 누락이나 허용되지 않는 credential 문자는 LAB secret reference를 교정해야 하는 상태이며 값의 공개나 root secret 재사용 사유가 아니다.
- 실제 cluster 재초기화·volume 삭제·restore는 별도 승인 없이는 실행하지 않는다.

## Related Documents

- [Architecture index](../docs/02.architecture/README.md)
- [Operations index](../docs/05.operations/README.md)
