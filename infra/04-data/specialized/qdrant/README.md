---
title: "Qdrant"
version: "1.0.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2025-11-12"
---

# Qdrant

> 고성능 벡터 유사도 검색 엔진입니다.

## Overview

`qdrant` 서비스는 AI/ML 애플리케이션을 위한 벡터 데이터베이스 계층을 제공하며 고차원 임베딩의 빠른 의미 검색을 가능하게 합니다. `04-data/specialized` tier 안에 위치하며 Retrieval-Augmented Generation(RAG) 워크플로의 핵심 구성 요소입니다.

## Audience

이 README의 주요 독자:

- AI/ML Engineers(벡터 검색 통합)
- Operators(자원 튜닝과 snapshot)
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Qdrant unprivileged 컨테이너 설정(`docker-compose.yml`)
- REST 6333(SSO 뒤에서 라우팅)과 gRPC 6334(네트워크 내부 전용)
- Snapshot 저장 설정(`/qdrant/storage/snapshots`)
- Telemetry와 서비스 헬스 모니터링

### Out of Scope

- 벡터 임베딩 생성(upstream 모델이 담당)
- collection 수준의 스키마 설계(시스템 가이드 `docs/05.operations/guides/0034-qdrant.md` 참조)
- 운영 통제(운영 정책 `docs/05.operations/policies/0034-qdrant.md` 참조)
- 헬스와 복구 triage(복구 런북 `docs/05.operations/runbooks/0034-qdrant.md` 참조)

## Structure

```text
qdrant/
├── docker-compose.yml    # 서비스 정의
└── README.md            # 이 파일
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `04-data`의 Qdrant 서비스 leaf; services: `qdrant`; [root docker-compose.yml](../../../../docker-compose.yml)을 통해 root include 활성화 -> `infra/04-data/specialized/qdrant/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | 환경 키는 Compose가 소유함; exact profiles: `ai`, `ai-llm`, `qdrant` |
| Compose linkage | [root docker-compose.yml](../../../../docker-compose.yml)을 통해 root include 활성화 -> `infra/04-data/specialized/qdrant/docker-compose.yml` |
| Networks | `ai_net`, `edge_net`, `obs_net` |
| Volumes | `qdrant-data:/qdrant/storage:rw`, `qdrant-data` |
| Ports | `${QDRANT_PORT:-6333}`, `${QDRANT_GRPC_PORT:-6334}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.qdrant.rule`, `traefik.http.routers.qdrant.entrypoints`, `traefik.http.routers.qdrant.tls`, `traefik.http.routers.qdrant.middlewares`, `traefik.http.services.qdrant.loadbalancer.server.port` |
| Secret refs | `qdrant_api_key`, `qdrant_read_only_api_key` |
| Healthcheck | `qdrant`에 Compose healthcheck 선언됨 |
| Operations | Guide (`docs/05.operations/guides/0034-qdrant.md`), Policy (`docs/05.operations/policies/0034-qdrant.md`), Runbook (`docs/05.operations/runbooks/0034-qdrant.md`) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `docker compose config --quiet`부터 시작한 뒤 서비스 로그와 연결된 운영/runbook 증거를 확인함 |

## How to Work in This Area

1. RAG 통합 패턴을 위해 시스템 가이드 (`docs/05.operations/guides/0034-qdrant.md`)를 검토합니다.
2. 배포 시 `ai`나 `qdrant` profile이 활성화되어 있는지 확인합니다.
3. Snapshot은 persistent volume 안에 설정됩니다. owner 승인 백업 작업 전에 경로 매핑을 확인합니다.
4. `/readyz` 엔드포인트로 헬스를 모니터링합니다.

## Tech Stack

| Category   | Technology   | Notes                          |
| ---------- | ------------ | ------------------------------ |
| Engine     | [선언된 runtime 이미지](../../../tech-stack.versions.json) | 단일 unprivileged 서비스 |
| REST API   | HTTP         | 포트 6333                      |
| gRPC API   | gRPC         | 포트 6334                      |
| Persistence | Local Bind  | `${DEFAULT_DATA_DIR}/qdrant/data` |

## Validation

Classification은 `HOME`입니다. Qdrant는 `qdrant_api_key`(AI-008)의 API key가
필요하며 이것이 없으면 health 엔드포인트만 응답합니다. Prometheus는
`qdrant_read_only_api_key`(AI-009)의 read-only key로 스크레이프합니다.
Snapshot 복구는 동일 minor 또는 다음 minor의 새로운 target, 별도로 승인된
force가 아닌 한 존재하지 않는 목적지 collection, snapshot 크기의 약 2배에
해당하는 여유 디스크를 사용합니다. 소유 artifact는 `GDE-0034`, `POL-0034`,
`RUN-0034`입니다.

- Qdrant에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- Qdrant 문서와 운영 링크를 동기화하려면 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.

## Troubleshooting

- `docker compose config --quiet`로 Qdrant volume, 네트워크, label 참조가 정상 렌더링되는지 먼저 확인합니다.
- collection, snapshot, persistence 설정을 변경하기 전에 Qdrant 로그와 연결된 runbook을 확인합니다.

## Related Documents

- Specialized 가이드 (`docs/05.operations/guides/README.md`)
- Qdrant 시스템 가이드 (`docs/05.operations/guides/0034-qdrant.md`)
- Qdrant 운영 정책 (`docs/05.operations/policies/0034-qdrant.md`)
- Qdrant 복구 런북 (`docs/05.operations/runbooks/0034-qdrant.md`)
- [문서 인덱스](../../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../../tech-stack.versions.json)은 drift 검증을 제공합니다.
