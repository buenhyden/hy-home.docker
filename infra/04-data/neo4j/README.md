---
title: "Neo4j"
version: "1.0.4"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-12"
---

# Neo4j

> 연결된 데이터를 위한 native property-graph 데이터베이스입니다.

## Overview

`neo4j` 서비스는 관계가 중요한 데이터 모델을 위한 전용 그래프 저장 계층을 제공합니다. Cypher 쿼리 언어로 깊은 계층 구조와 복잡한 네트워크 구조를 효율적으로 조회할 수 있습니다. 이 인프라는 `04-data` tier 안에 위치하며 Community edition에 맞춰 최적화되어 있습니다.

## Audience

이 README의 주요 독자:

- Operators(Database Administrator)
- Backend Developers(그래프 모델링)
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Neo4j Community Edition 컨테이너 설정(`docker-compose.yml`)
- 서비스별 보안(secret 기반 인증)
- 그래프 전용 네트워킹(Bolt와 HTTP/S 프로토콜)
- 그래프 워크로드를 위한 JVM 메모리 튜닝

### Out of Scope

- 애플리케이션 수준의 그래프 모델링(시스템 가이드 `docs/05.operations/guides/0033-neo4j.md` 참조)
- 운영 통제(운영 정책 `docs/05.operations/policies/0033-neo4j.md` 참조)
- 헬스와 복구 triage(복구 런북 `docs/05.operations/runbooks/0033-neo4j.md` 참조)

## Structure

```text
neo4j/
├── scripts/
│   └── neo4j-entrypoint-with-secrets.sh   # secret-aware entrypoint
├── docker-compose.yml                     # 서비스 정의
└── README.md                              # 이 파일
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `04-data`의 Neo4j 서비스 leaf; services: `neo4j`; [root docker-compose.yml](../../../docker-compose.yml)을 통해 root include 활성화 -> `infra/04-data/neo4j/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | 환경 키는 Compose가 소유함; exact profile: `graph` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)을 통해 root include 활성화 -> `infra/04-data/neo4j/docker-compose.yml` |
| Networks | `edge_net` |
| Volumes | `neo4j-data:/data:rw`, `./scripts/neo4j-entrypoint-with-secrets.sh:/startup/neo4j-entrypoint-with-secrets.sh:ro`, `neo4j-data` |
| Ports | `${NEO4J_BOLT_PORT:-7687}`, `${NEO4J_HTTP_PORT:-7474}`, `${NEO4J_HTTPS_PORT:-7473}`, `${NEO4J_METRICS_PORT:-2004}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.neo4j.rule`, `traefik.http.routers.neo4j.entrypoints`, `traefik.http.routers.neo4j.tls`, `traefik.http.services.neo4j.loadbalancer.server.port`, `traefik.http.routers.neo4j.middlewares` |
| Secret refs | names: `neo4j_password`; mounts: `/run/secrets/neo4j_password` |
| Healthcheck | `neo4j`에 Compose healthcheck 선언됨 |
| Operations | Guide (`docs/05.operations/guides/0033-neo4j.md`), Policy (`docs/05.operations/policies/0033-neo4j.md`), Runbook (`docs/05.operations/runbooks/0033-neo4j.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `docker compose config --quiet`부터 시작한 뒤 서비스 로그와 연결된 운영/runbook 증거를 확인함 |

## How to Work in This Area

1. 아키텍처 맥락을 위해 시스템 가이드 (`docs/05.operations/guides/0033-neo4j.md`)부터 검토합니다.
2. 서비스 시작 전에 `neo4j_password` secret이 provisioning되었는지 확인합니다.
3. 자원 일관성을 위해 `docker-compose.yml`의 `template-stateful-med` 서비스 확장을 따릅니다.
4. 컨테이너 로컬 `cypher-shell`이나 Traefik 뒤의 Neo4j Browser route로 연결을 확인합니다.

## Tech Stack

| Category   | Technology        | Notes                     |
| ---------- | ----------------- | ------------------------- |
| Engine     | Compose에 선언된 Neo4j Community 이미지 | 단일 서비스 |
| Protocol   | Bolt / HTTP / S   | 내부적으로 7687 / 7474 / 7473로 노출 |
| Security   | Docker Secrets    | `neo4j_password`          |
| Route      | Traefik HTTP      | `neo4j.${DEFAULT_URL}` -> `${NEO4J_HTTP_PORT:-7474}` |

## Validation

Classification은 `OPTIONAL`입니다. Community 복구는 오프라인
`neo4j-admin database dump/load`를 새로운 호환 target에 사용합니다.
Enterprise online-backup이나 cluster 명령은 이 배포 범위 밖입니다.
제약 조건, index, 그래프 개수, 대표 Cypher를 검증하십시오. 소유 artifact는
`GDE-0033`, `POL-0033`, `RUN-0033`입니다.

- Neo4j에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- Neo4j 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.

## Troubleshooting

- `docker compose config --quiet`로 Neo4j volume, 네트워크, secret 참조가 정상 렌더링되는지 먼저 확인합니다.
- 그래프 지속성이나 password 설정을 변경하기 전에 Neo4j 로그와 연결된 runbook을 확인합니다.

## Related Documents

- Specialized 가이드 (`docs/05.operations/guides/README.md`)
- Neo4j 시스템 가이드 (`docs/05.operations/guides/0033-neo4j.md`)
- Neo4j 운영 정책 (`docs/05.operations/policies/0033-neo4j.md`)
- Neo4j 복구 런북 (`docs/05.operations/runbooks/0033-neo4j.md`)
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift 검증을 제공합니다.
