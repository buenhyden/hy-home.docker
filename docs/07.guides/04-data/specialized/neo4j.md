# Neo4j Graph Database Guide

> Technical guide for understanding and using Neo4j within the `04-data/specialized` tier.

## Overview (KR)

이 문서는 Neo4j 그래프 데이터베이스에 대한 기술 가이드다. 관계 중심 데이터 모델을 위한 그래프 저장소의 특성과 로컬 환경에서의 브라우저 UI 및 Bolt 프로토콜 활용 방법을 설명한다.

## Guide Type

`system-guide`

## Target Audience

- Backend Developers
- Data Architects
- Operators
- AI Agents

## Purpose

이 가이드는 Neo4j의 아키텍처를 이해하고, Cypher 쿼리 언어를 사용하며, 로컬 서비스를 효율적으로 관리하는 것을 돕는다.

## Prerequisites

- Docker 및 Docker Compose 설치
- `neo4j` 데이터 프로필 활성화
- 기본 Cypher 쿼리 문법 이해

## Step-by-step Instructions

### 1. Accessing Neo4j Browser

Neo4j Browser는 시각적 쿼리 도구이다.

1. 웹 브라우저에서 `https://neo4j.${DEFAULT_URL}` 접속
2. 인증 정보 입력 (사용자: `neo4j`, 비밀번호: Docker Secret `neo4j_password`)

### 2. Basic Cypher Operations

데이터를 탐색하거나 생성할 때 Cypher를 사용한다.

```cypher
// Node 생성
CREATE (p:Person {name: 'Alice', role: 'Dev'})
RETURN p;

// Relationship 생성
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:COLLEAGUE]->(b);
```

### 3. Connection via Bolt

애플리케이션 드라이버는 Bolt 프로토콜을 사용한다.

- **URL**: `bolt://neo4j.${DEFAULT_URL}:7687`
- **TLS**: 활성화 권장 (Traefik을 통한 암호화)

## Common Pitfalls

- **Memory OOM**: Heap 크기(`NEO4J_server_memory_heap_max__size`)가 너무 작으면 복잡한 그래프 연산 시 장애가 발생할 수 있다.
- **Password Policies**: 초기 비밀번호 변경 필요 시, `cypher-shell`을 통해 수행해야 할 수 있다.

## Related Documents

- **Spec**: `[infra/04-data/specialized/neo4j/README.md](../../../../infra/04-data/specialized/neo4j/README.md)`
- **Operation**: `[../../08.operations/04-data/specialized/neo4j.md](../../../08.operations/04-data/specialized/neo4j.md)`
- **Runbook**: `[../../09.runbooks/04-data/specialized/neo4j.md](../../../09.runbooks/04-data/specialized/neo4j.md)`
