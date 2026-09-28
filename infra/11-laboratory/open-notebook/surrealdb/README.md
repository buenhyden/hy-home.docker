---
title: "SurrealDB Implementation"
version: "0.3.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-27"
---

# SurrealDB Implementation

> Open Notebook용 커스텀 SurrealDB 빌드 컨텍스트 및 저장소 엔진입니다.

## Overview

이 디렉터리에는 SurrealDB의 커스텀 컨테이너 빌드 컨텍스트와 런타임 엔트리포인트가 있습니다. SurrealDB는 Open Notebook의 전용 영속화 데이터베이스 역할을 합니다.

Open Notebook 업스트림은 SurrealDB v2만 엄격하게 지원합니다. SurrealDB v3은 Open Notebook과의 쿼리 및 프로토콜 호환성을 깨뜨리므로 Dockerfile의 기준 이미지는 명시적으로 SurrealDB v2에 고정되어 있습니다.

## Audience

- **Operators**: 데이터베이스 영속화, 버전, 자격 증명 관리.
- **Developers**: 데이터베이스 스키마 확장 또는 쿼리 연결 디버깅.
- **AI Agents**: 이미지 빌드 경계와 버전 호환성 규칙 파악.

## Scope

### In Scope

- `surrealdb/surrealdb:v2` 기준 이미지를 고정하는 다단계 이미지 빌드 컨텍스트(`Dockerfile`).
- Docker Secret에서 `surreal_db_password`를 읽는 시크릿 인식 컨테이너 엔트리포인트(`docker-entrypoint.sh`).
- Open Notebook 저장소 호환성을 위한 버전 경계 강제.

### Out of Scope

- 독립형 SurrealDB 클러스터링이나 고가용성.
- 애플리케이션 수준의 Open Notebook 스키마와 사용자 데이터.

## Structure

```text
surrealdb/
├── Dockerfile            # Multi-stage build pinning surrealdb:v2
├── docker-entrypoint.sh  # Secret-aware entrypoint script
└── README.md             # This file
```

- [Dockerfile](Dockerfile)
- [docker-entrypoint.sh](docker-entrypoint.sh)
- [docker-compose.yml](../docker-compose.yml)

## Tech Stack

런타임 이미지 고정 값은 [Dockerfile](Dockerfile)과 [Compose](../docker-compose.yml)에 선언되어 있습니다. [버전 레지스트리](../../../tech-stack.versions.json)는 파생된 Compose 이미지 프로젝션입니다.

| Component | Source | Target Version | Notes |
| --- | --- | --- | --- |
| `surrealdb` | [Dockerfile](Dockerfile) | SurrealDB v2 | Open Notebook 호환을 위해 기준 이미지를 `surrealdb/surrealdb:v2`에 고정 |

## Configuration

### Version Compatibility

Open Notebook 업스트림은 SurrealDB v2만 지원합니다. Open Notebook이 공식적으로 v3 호환성을 제공하기 전까지는 이 서비스를 SurrealDB v3 이상으로 업그레이드하는 것을 엄격히 금지합니다.

### Authentication & Entrypoint

엔트리포인트 스크립트는 `/run/secrets/surreal_db_password`에서 인증 자격 증명을 직접 읽어 다음 설정으로 SurrealDB를 시작합니다.

- 내부 리슨 엔드포인트: `0.0.0.0:8000`
- 사용자: `${SURREALDB_USERNAME}`
- 저장소 엔진: `surrealkv:/mydata/open_notebook.db`

## How to Work in This Area

1. 이미지 변경을 제안하기 전에 [Dockerfile](Dockerfile)과 [docker-entrypoint.sh](docker-entrypoint.sh)를 검토합니다.
2. `docker compose --profile notebook build surrealdb`로 Compose 빌드를 검증합니다.
3. 업스트림 Open Notebook의 지원이 검증되기 전까지는 기준 이미지를 `v3`으로 올리지 않습니다.
4. 자격 증명은 스크립트나 환경 파일에 절대 하드코딩하지 않습니다.

## Validation

- 커스텀 이미지 빌드: `docker compose -f ../docker-compose.yml build surrealdb`.
- 컨테이너 헬스체크 검증: `/usr/local/bin/surreal is-ready --endpoint http://127.0.0.1:8000`.
- `open_notebook` 컨테이너가 RPC 연결을 성공적으로 수립하는지 확인해 Open Notebook과의 데이터베이스 호환성을 검증합니다.

## Troubleshooting

- **SurrealDB v3 Incompatibility**: 이미지 재빌드 후 `open_notebook`이 연결하거나 쿼리를 실행하지 못하면 기준 이미지가 SurrealDB v3으로 업그레이드되지 않았는지 확인합니다.
- **Secret File Missing**: `surreal_db_password`가 Compose에 선언되어 있고 `/run/secrets/surreal_db_password`에 마운트되어 있는지 확인합니다.

## Related Documents

- [Open Notebook README](../README.md)
- [Documentation index](../../../../docs/README.md)
- [Infrastructure index](../../../README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../../../tech-stack.versions.json)으로 드리프트를 검증합니다.
