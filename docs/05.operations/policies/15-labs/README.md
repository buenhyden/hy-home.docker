---
title: "독립 LAB 문서 정책"
version: "0.3.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "operations"
---

# 독립 LAB 문서 정책

## Overview

독립 LAB 문서의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

## Scope

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Valkey Cluster Operations Policy](0022-valkey-cluster.md) | `POL-0022` | 이 정책은 현재 source 구성을 데이터 보호, 보안, 자원, 수명주기 통제와 독립적으로 검증 가능한 운영 통제에 묶는다. 대상은 `labs/valkey-cluster/docker-compose.yml`의 LAB 전용 Valkey Cluster이다. |
| [Cassandra Operations Policy](0025-cassandra.md) | `POL-0025` | 독립 Cassandra LAB의 단일 노드·데이터 보존·인증 경계를 정의한다. HOME 소비자와 공유하지 않는다. |
| [CouchDB Operations Policy](0026-couchdb.md) | `POL-0026` | `labs/couchdb/docker-compose.yml`의 CouchDB 3노드 LAB cluster의 loopback 접근, Docker Secret credential, 백업·복구와 제거 기준을 정의한다. |
| [MongoDB Operations Policy](0027-mongodb.md) | `POL-0027` | `labs/mongodb/docker-compose.yml`의 MongoDB replica set LAB의 `mongodb` profile, Docker Secret credential, 백업·복구와 제거 기준을 정의한다. |
| [PostgreSQL Cluster Operations Policy](0031-postgresql-cluster.md) | `POL-0031` | `labs/postgresql-ha/docker-compose.yml`의 PostgreSQL HA LAB(etcd·Patroni·HAProxy)의 `postgres-ha` profile, 접근 경계, 백업·복구 기준을 정의한다. |
| [Locust Operations Policy](0062-locust.md) | `POL-0062` | Locust는 독립 LAB capability이며, 이 정책은 test target 보호와 검토되지 않은 load·credential 수집·오해를 부르는 성능 증거를 막는다. |
| [SonarQube Operations Policy](0066-sonarqube.md) | `POL-0066` | 이 정책은 독립 LAB `labs/sonarqube/docker-compose.yml`의 SonarQube Community Build 배포를 다룬다. |
| [Stalwart Mail Operations Policy](0070-mail.md) | `POL-0070` | Stalwart는 독립 LAB `labs/stalwart/docker-compose.yml`의 메일 서비스다. |
| [JupyterLab Operations Policy](0089-jupyterlab.md) | `POL-0089` | JupyterLab LAB은 임의의 코드를 실행한다. mandatory token, loopback 게시, 단일 사용자와 work directory 보존을 통제한다. |
| [dbt Operations Policy](0090-dbt.md) | `POL-0090` | dbt LAB의 권한은 source 읽기와 target schema 소유로 제한하며 HOME dev-pg endpoint는 별도 승인으로만 연다. |
| [Lakehouse Operations Policy](0094-lakehouse.md) | `POL-0094` | lakehouse LAB 엔진의 identity 범위, 파괴적 유지보수, 테스트 데이터 분리와 HOME catalog endpoint 승인을 통제한다. |
| [Superset Operations Policy](0097-superset.md) | `POL-0097` | Superset LAB의 native OIDC 로그인, role 부여, 자격 증명 처리와 HOME mng-pg endpoint 승인을 통제한다. |
| [LAB Promotion Policy](0107-lab-promotion.md) | `POL-0107` | LAB 구조, 승격 manifest, secret, 목적지 규칙, readiness 규칙과 host reserve를 정한다. |
| [Kafka Cluster LAB Operations Policy](0108-kafka-cluster.md) | `POL-0108` | Kafka LAB의 cluster ID 분리, internal network, 데이터 경로와 승격 경계를 통제한다. |
| [OpenSearch Cluster LAB Operations Policy](0109-opensearch-cluster.md) | `POL-0109` | OpenSearch LAB의 LAB secret·인증서, internal network, 데이터 경로와 승격 경계를 통제한다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

이동 대상은 LAB 관련 운영 문서다. 서비스 소스는 저장소 루트 `labs/`가 소유한다.
문서 이동은 LAB 서비스 기동, 배포, 비밀번호 변경, 데이터 이동·삭제 또는 복구 실행을 뜻하지 않는다.

## Related Documents

- [상위 정책 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
