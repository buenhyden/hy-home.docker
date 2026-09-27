---
title: "Cache & Key-Value Stores (04-data/cache-and-kv)"
version: "1.0.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-03-27"
---

# Cache and key-value data

## Overview

이 영역은 저장소의 캐시 및 키-값 데이터 패키지를 문서화합니다.

## Audience

Valkey 배포의 operator와 maintainer를 대상으로 합니다.

## Scope

선택된 패키지와 cluster/관리용 Valkey 상태 사이의 경계를 다룹니다.

## Structure

### Current package

[`valkey-cluster`](valkey-cluster/README.md)는 이 tier의 유일한 패키지입니다. 6개의
Valkey 노드, init job, exporter는 정확히 `valkey-cluster` profile을 사용하며 LAB로
분류됩니다. `operational/mng-db`가 소유하고 workflow broker/cache 상태를 제공하는
HOME `mng-valkey`와는 별개입니다.

## How to Work in This Area

### Operator boundary

루트 프로젝트를 통해 `valkey-cluster` profile을 렌더링하십시오. 6개의 데이터 경로와
cluster identity를 분리 유지하고 `service_valkey_password`를 보호하며 게시된
client/cluster-bus 포트는 신뢰 네트워크 노출로 취급하십시오. 동일 호스트의
3-primary/3-replica 토폴로지는 host availability가 아닙니다.

백업에는 조율된 RDB checkpoint와 완전한 AOF set/manifest, 그리고 격리된
fresh-identity 복구가 필요합니다.

## Related Documents

[문서 진입점](../../../docs/README.md)에서 Stage 05 subject
`docs/05.operations/guides/0022-valkey-cluster.md`와 백업 정책 POL-0021을 찾으십시오.
