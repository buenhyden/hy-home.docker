---
title: "12 Analytics"
version: "0.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2026-10-01"
---

# 12 Analytics

## Purpose

### Service Role

이 tier에는 현재 root Compose가 include하는 패키지가 없습니다. 데이터 처리·SQL
조회·품질 검증·BI·변환·notebook 패키지는 SPEC-0262에서 독립 LAB entrypoint로
옮겼습니다. ADR-0062 capability tier 이름은 유지합니다.

#### Audience

데이터 엔지니어, 분석 사용자와 패키지 운영자를 위한 안내입니다.

#### Scope

분석 패키지의 현재 위치 안내만 소유합니다. 공유 저장소는 [04 Data](../04-data/README.md),
MLflow는 [08 AI](../08-ai/README.md)에 남습니다.

#### Structure

| LAB | Entry point | 서비스 | Source 자산 |
| --- | --- | --- | --- |
| Lakehouse | [labs/lakehouse/docker-compose.yml](../../labs/lakehouse/docker-compose.yml) | `seaweedfs-table-bucket`, `spark`, `trino`, `great-expectations`, `flink-jobmanager`, `flink-taskmanager` | `labs/lakehouse/` |
| dbt | [labs/dbt/docker-compose.yml](../../labs/dbt/docker-compose.yml) | `dbt-db-provision`, `dbt` | `labs/dbt/` |
| Superset | [labs/superset/docker-compose.yml](../../labs/superset/docker-compose.yml) | `superset-db-provision`, `superset-init`, `superset` | `labs/superset/` |
| JupyterLab | [labs/jupyterlab/docker-compose.yml](../../labs/jupyterlab/docker-compose.yml) | `jupyterlab` | `labs/jupyterlab/` |

### Supported Environment

없음: 이 tier에는 root Compose가 include하는 패키지가 없어 지원 런타임이 없다. 분석 패키지의 런타임은 독립 LAB이 각자 선언한다.

## Interfaces

### Inputs and Outputs

없음: 이 tier는 입출력을 제공하지 않는다. LAB이 쓰는 HOME SeaweedFS·mng-pg·dev-pg·MLflow endpoint는 `labs/.env.example`의 입력으로만 지정한다.

### Security Boundary

이 tier는 secret, 포트, network를 선언하지 않는다. LAB은 HOME network에 연결되지 않으며 도달 가능한 HOME endpoint는 별도 승인 대상이다.

## Development

### Local Workflow

- LAB은 HOME network에 연결되지 않습니다. HOME SeaweedFS·mng-pg·dev-pg·MLflow는
  `labs/.env.example`의 endpoint 입력으로만 지정하며, 도달 가능한 endpoint는 별도 승인 대상입니다.
- tier 정적 점검: `bash scripts/hardening/check-all-hardening.sh 12-analytics`
  (LAB source를 점검합니다).

### Checks

tier 정적 점검은 `bash scripts/hardening/check-all-hardening.sh 12-analytics`이며 통과는 LAB 실행을 증명하지 않는다.

## Operations

### Runbook Links

- [LAB source](../../labs/README.md)
- [인프라 인덱스](../README.md)

### Observability and Recovery

없음: 이 tier에는 실행 서비스가 없다. LAB 운영은 [LAB Runbook 목록](../../docs/05.operations/runbooks/15-labs/README.md)을 따른다.
