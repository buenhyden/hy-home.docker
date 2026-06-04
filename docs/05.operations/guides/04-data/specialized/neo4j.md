---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/specialized/neo4j.md -->

# Neo4j Usage Guide

## Usage

### Overview (KR)

이 문서는 root compose에 active include된 `infra/04-data/specialized/neo4j/docker-compose.yml` 기준으로 Neo4j graph database의 사용 맥락과 일반 점검 방법을 설명한다. 현재 구현은 `neo4j:5.26.26-community`, 단일 `neo4j` 서비스, `data`/`graph` 프로파일, `infra_net`, `neo4j_password` Docker Secret, secret-aware entrypoint, Traefik HTTP Browser route를 사용한다.

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
   docker compose --profile data --profile graph config neo4j
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

5. 애플리케이션이 `infra_net` 내부에서 접근할 때는 `bolt://neo4j:${NEO4J_BOLT_PORT:-7687}`를 기준으로 한다. Public Bolt TCP route는 현재 compose에 선언되어 있지 않으므로 별도 gateway 변경 승인 없이는 문서화하지 않는다.

### Common Pitfalls

- 현재 구현은 Community single service다. clustering, multi-database enterprise operations, public Bolt routing을 구현된 기능처럼 설명하지 않는다.
- Neo4j Browser는 Traefik HTTPS route를 통해 `${NEO4J_HTTP_PORT:-7474}`로 전달된다. `${NEO4J_HTTPS_PORT:-7473}` exposed port가 있어도 별도 HTTPS router가 선언된 것은 아니다.
- `neo4j_password` 값은 entrypoint와 healthcheck가 secret mount에서 읽는다. 명령 예시는 secret 값을 출력하지 않아야 한다.

## Common Checks

- `docker compose --profile data --profile graph config neo4j`
- `docker compose ps neo4j`
- `docker exec neo4j sh -lc 'cypher-shell -a bolt://localhost:7687 -u neo4j -p "$(tr -d "\n" < /run/secrets/neo4j_password)" "RETURN 1;"'`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [Neo4j runbook](../../../runbooks/04-data/specialized/neo4j.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/specialized/neo4j.md)
- [Recovery runbook](../../../runbooks/04-data/specialized/neo4j.md)
- [Infra README](../../../../../infra/04-data/specialized/neo4j/README.md)
