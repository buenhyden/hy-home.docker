---
title: "Neo4j"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2025-11-12"
---

# Neo4j

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

> 연결된 데이터를 위한 native property-graph 데이터베이스입니다.

#### Service

##### Purpose

###### Overview
<!-- core-payload-level:4 -->

`neo4j` 서비스는 관계가 중요한 데이터 모델을 위한 전용 그래프 저장 계층을 제공합니다. Cypher 쿼리 언어로 깊은 계층 구조와 복잡한 네트워크 구조를 효율적으로 조회할 수 있습니다. 이 인프라는 `04-data` tier 안에 위치하며 Community edition에 맞춰 최적화되어 있습니다.

###### Audience
<!-- core-payload-level:4 -->

이 README의 주요 독자:

- Operators(Database Administrator)
- Backend Developers(그래프 모델링)
- Documentation Writers

###### Scope
<!-- core-payload-level:4 -->

###### In Scope
<!-- core-payload-level:5 -->

- Neo4j Community Edition 컨테이너 설정(`docker-compose.yml`)
- 서비스별 보안(secret 기반 인증)
- 그래프 전용 네트워킹(Bolt와 HTTP/S 프로토콜)
- 그래프 워크로드를 위한 JVM 메모리 튜닝

###### Out of Scope
<!-- core-payload-level:5 -->

- 애플리케이션 수준의 그래프 모델링(시스템 가이드 `docs/05.operations/01.guides/05.databases-and-storage/0033-neo4j.md` 참조)
- 운영 통제(운영 정책 `docs/05.operations/02.policies/05.databases-and-storage/0033-neo4j.md` 참조)
- 헬스와 복구 triage(복구 런북 `docs/05.operations/03.runbooks/05.databases-and-storage/0033-neo4j.md` 참조)

###### Structure
<!-- core-payload-level:4 -->

```text
neo4j/
├── scripts/
│   └── neo4j-entrypoint-with-secrets.sh   # secret-aware entrypoint
├── docker-compose.yml                     # 서비스 정의
└── README.md                              # 이 파일
```

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Traefik HTTP route `neo4j.${DEFAULT_URL}` -> `${NEO4J_HTTP_PORT:-7474}` | `neo4j` | Traefik 뒤의 Neo4j Browser 사용자 | Traefik이 HTTP로 Neo4j Browser에 라우팅하며 인증은 `neo4j_password` secret 기반이다 | Compose healthcheck가 선언되어 있으며 복구는 Neo4j 복구 런북(RUN-0033)을 따른다 |
| Bolt `${NEO4J_BOLT_PORT:-7687}` | `neo4j` | 컨테이너 로컬 `cypher-shell` | Cypher 쿼리용 Bolt 프로토콜이며 호스트에 게시하지 않고 `edge_net`에서 내부 노출한다 | Compose healthcheck가 선언되어 있으며 복구는 Neo4j 복구 런북(RUN-0033)을 따른다 |
| HTTPS `${NEO4J_HTTPS_PORT:-7473}` | `neo4j` | 이 README는 소비자를 기록하지 않는다. | 내부적으로 7473으로 노출하는 HTTP/S 프로토콜이다 | 이 README는 실패 처리를 기록하지 않는다. |
| Metrics `${NEO4J_METRICS_PORT:-2004}` | `neo4j` | 이 README는 소비자를 기록하지 않는다. | 이 README는 계약을 따로 기록하지 않는다. | 이 README는 실패 처리를 기록하지 않는다. |

###### Inputs and Outputs
<!-- core-payload-level:4 -->

호스트로 게시하는 포트 선언이 없다. 연결 네트워크는 `edge_net`이다. (출처: `infra/04-data/neo4j/docker-compose.yml`의 `neo4j` 서비스)

###### Security Boundary
<!-- core-payload-level:4 -->

Compose가 참조하는 secret은 `neo4j_password`이며 값은 저장소에 두지 않는다. 호스트로 게시하는 포트 선언은 없다. (출처: `infra/04-data/neo4j/docker-compose.yml`의 `neo4j` 서비스)

#### Usage

##### Prerequisites

###### Tech Stack
<!-- core-payload-level:4 -->

| Category   | Technology        | Notes                     |
| ---------- | ----------------- | ------------------------- |
| Engine     | Compose에 선언된 Neo4j Community 이미지 | 단일 서비스 |
| Protocol   | Bolt / HTTP / S   | 내부적으로 7687 / 7474 / 7473로 노출 |
| Security   | Docker Secrets    | `neo4j_password`          |
| Route      | Traefik HTTP      | `neo4j.${DEFAULT_URL}` -> `${NEO4J_HTTP_PORT:-7474}` |

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

1. 아키텍처 맥락을 위해 시스템 가이드 (`docs/05.operations/01.guides/05.databases-and-storage/0033-neo4j.md`)부터 검토합니다.
2. 서비스 시작 전에 `neo4j_password` secret이 provisioning되었는지 확인합니다.
3. 자원 일관성을 위해 `docker-compose.yml`의 `template-stateful-med` 서비스 확장을 따릅니다.
4. 컨테이너 로컬 `cypher-shell`이나 Traefik 뒤의 Neo4j Browser route로 연결을 확인합니다.

#### Checks

##### Readiness

###### Validation
<!-- core-payload-level:4 -->

Classification은 `OPTIONAL`입니다. Community 복구는 오프라인
`neo4j-admin database dump/load`를 새로운 호환 target에 사용합니다.
Enterprise online-backup이나 cluster 명령은 이 배포 범위 밖입니다.
제약 조건, index, 그래프 개수, 대표 Cypher를 검증하십시오. 소유 artifact는
`GDE-0033`, `POL-0033`, `RUN-0033`입니다.

- Neo4j에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- Neo4j 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.

##### Failure Handling

###### Related Documents
<!-- core-payload-level:4 -->

- Specialized 가이드 (`docs/05.operations/01.guides/README.md`)
- Neo4j 시스템 가이드 (`docs/05.operations/01.guides/05.databases-and-storage/0033-neo4j.md`)
- Neo4j 운영 정책 (`docs/05.operations/02.policies/05.databases-and-storage/0033-neo4j.md`)
- Neo4j 복구 런북 (`docs/05.operations/03.runbooks/05.databases-and-storage/0033-neo4j.md`)
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift 검증을 제공합니다.

###### Service Readiness
<!-- core-payload-level:4 -->

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
| Operations | Guide (`docs/05.operations/01.guides/05.databases-and-storage/0033-neo4j.md`), Policy (`docs/05.operations/02.policies/05.databases-and-storage/0033-neo4j.md`), Runbook (`docs/05.operations/03.runbooks/05.databases-and-storage/0033-neo4j.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `docker compose config --quiet`부터 시작한 뒤 서비스 로그와 연결된 운영/runbook 증거를 확인함 |

###### Troubleshooting
<!-- core-payload-level:4 -->

- `docker compose config --quiet`로 Neo4j volume, 네트워크, secret 참조가 정상 렌더링되는지 먼저 확인합니다.
- 그래프 지속성이나 password 설정을 변경하기 전에 Neo4j 로그와 연결된 runbook을 확인합니다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
