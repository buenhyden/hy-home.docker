---
title: "독립 LAB 문서 정책"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
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
| [Valkey Cluster Operations Policy](0022-valkey-cluster.md) | `POL-0022` | 이 정책은 현재 source 구성을 데이터 보호, 보안, 자원, 수명주기 통제와 독립적으로 검증 가능한 운영 통제에 묶는다. 대상은 `labs/valkey-cluster.yml`의 LAB 전용 Valkey Cluster이다. |
| [Cassandra Operations Policy](0025-cassandra.md) | `POL-0025` | 독립 Cassandra LAB의 단일 노드·데이터 보존·인증 경계를 정의한다. HOME 소비자와 공유하지 않는다. |
| [CouchDB Operations Policy](0026-couchdb.md) | `POL-0026` | 이 정책은 `hy-home.docker`의 선택 NoSQL 서비스인 CouchDB 3노드 클러스터 운영 기준을 정의한다. 기준은 현재 tracked compose의 couchdb image declaration, curlimages/curl image |
| [MongoDB Operations Policy](0027-mongodb.md) | `POL-0027` | 이 정책은 `hy-home.docker`의 `LAB` MongoDB replica set 운영 기준을 정의한다. runtime image/version은 Compose declaration이 소유하며, 정책 기준은 exact `mongodb` prof |
| [Supabase Operations Policy](0029-supabase.md) | `POL-0029` | 이 정책은 정상 root에서 분리된 `labs/supabase.yml`의 exact `supabase` profile LAB 운영 기준을 정의한다. 핵심 통제는 controller lease, Kong 중심 공개 접근, canonical Docker  |
| [PostgreSQL Cluster Operations Policy](0031-postgresql-cluster.md) | `POL-0031` | 이 정책은 `hy-home.docker`의 독립 LAB인 PostgreSQL HA 실습 cluster 운영 기준을 정의한다. 세 node가 한 host를 공유하므로 host HA가 아니며 HOME·DEV PostgreSQL은 단일 node다. 기준은  |
| [Locust Operations Policy](0062-locust.md) | `POL-0062` | Locust는 독립 LAB capability다. HOME root나 broad tooling startup에는 절대 포함되지 않는다. 이 정책은 test target을 보호하고 검토되지 않은 load, credential capture, 오해를 부르 |

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
