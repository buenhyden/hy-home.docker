---
title: "Neo4j Usage Guide"
version: "1.0.2"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0033"
parent_ids:
- "POL-0033"
implementation_services:
  infra/04-data/specialized/neo4j/docker-compose.yml:
  - 'neo4j'
created: "2026-05-10"
---

# Neo4j Usage Guide

## Usage

### Overview

이 문서는 root compose에 active include된 [Neo4j Compose 구현](../../../../../infra/04-data/specialized/neo4j/docker-compose.yml)을 설명한다. 현재 구현은 `OPTIONAL` 단일 Community `neo4j` 서비스, exact `graph` profile, `edge_net`, `neo4j_password` Docker Secret, secret-aware entrypoint와 Traefik Browser route를 사용한다.

### Current implementation

| Field | Repository-specific decision |
| --- | --- |
| Consumer and data rationale | OPTIONAL graph storage for consumers needing Cypher relationships; no cluster requirement is implemented. |
| Source / updater | [Compose](../../../../../infra/04-data/specialized/neo4j/docker-compose.yml) and secret-aware entrypoint own the Community image/process; review edition compatibility on updates. |
| Services / profile | Single `neo4j`; exact `graph`. |
| Flow / exposure | applications use internal Bolt; Browser uses Traefik HTTPS; no public Bolt router. |
| Persistence / secrets | `neo4j-data:/data`; `neo4j_password` Docker Secret. |
| Health / resources | secret-backed `cypher-shell RETURN 1`; `template-stateful-med` plus Compose heap/page-cache controls. |
| Security | Community authentication, secret-aware entrypoint, Browser gateway boundary. |
| Backup / upgrade | Community offline dump/load only; Enterprise online backup is unavailable. Restore-test before store-format upgrade/removal. |
| License / edition | Neo4j Community is GPLv3; Enterprise backup/clustering commands and rights are not implied. |

### Usage Type

`system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

Neo4j를 graph storage로 사용할 때 현재 repository의 service name, route, Bolt boundary, secret mount, healthcheck 기준을 오해하지 않도록 한다.

### Prerequisites

- 루트 [docker-compose.yml](../../../../../docker-compose.yml)에 `infra/04-data/specialized/neo4j/docker-compose.yml`가 active include인지 확인한다.
- `DEFAULT_DATA_DIR`, `DEFAULT_URL`, `NEO4J_BOLT_PORT`, `NEO4J_HTTP_PORT`, `neo4j_password` secret 파일이 준비되어 있어야 한다.
- secret 값은 `/run/secrets/neo4j_password`에서 container 내부로만 읽고 문서나 로그에 남기지 않는다.

### Step-by-step Instructions

1. root-active compose 구성을 렌더링한다.

   ```bash
   docker compose --profile graph config --quiet
   ```

2. 서비스 상태를 확인한다.

   ```bash
   docker compose ps neo4j
   ```

3. Browser route는 Traefik HTTP router 기준으로 접근한다.

   ```text
   https://neo4j.${DEFAULT_URL}
   ```

4. 내부 Bolt 확인은 container-local secret mount를 사용한다.

   ```bash
   docker exec neo4j sh -lc 'cypher-shell -a bolt://localhost:7687 -u neo4j -p "$(tr -d "\n" < /run/secrets/neo4j_password)" "RETURN 1;"'
   ```

5. 애플리케이션이 `edge_net` 내부에서 접근할 때는 `bolt://neo4j:${NEO4J_BOLT_PORT:-7687}`를 기준으로 한다. Public Bolt TCP route는 현재 compose에 선언되어 있지 않으므로 별도 gateway 변경 승인 없이는 문서화하지 않는다.

### Common Pitfalls

- 현재 구현은 Community single service다. clustering, multi-database enterprise operations, public Bolt routing을 구현된 기능처럼 설명하지 않는다.
- Neo4j Browser는 Traefik HTTPS route를 통해 `${NEO4J_HTTP_PORT:-7474}`로 전달된다. `${NEO4J_HTTPS_PORT:-7473}` exposed port가 있어도 별도 HTTPS router가 선언된 것은 아니다.
- `neo4j_password` 값은 entrypoint와 healthcheck가 secret mount에서 읽는다. 명령 예시는 secret 값을 출력하지 않아야 한다.
- Community edition recovery uses an offline `neo4j-admin database dump/load` workflow. Online backup features documented for Enterprise must not be presented as available here.

## Common Checks

- `docker compose --profile graph config --quiet`
- `docker compose ps neo4j`
- `docker exec neo4j sh -lc 'cypher-shell -a bolt://localhost:7687 -u neo4j -p "$(tr -d "\n" < /run/secrets/neo4j_password)" "RETURN 1;"'`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [Neo4j runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [Neo4j Operations Policy](policy.md) (`POL-0033`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](policy.md) (`POL-0033`), [Runbook](runbook.md) (`RUN-0033`)

## Related Documents

- [Neo4j backup and restore](https://neo4j.com/docs/operations-manual/current/backup-restore/)
- [Neo4j backup planning and edition scope](https://neo4j.com/docs/operations-manual/current/backup-restore/planning/)
- [Neo4j open-source licensing](https://neo4j.com/open-source-project/)

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/specialized/neo4j/README.md)
