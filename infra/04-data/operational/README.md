---
title: "Operational Data Tier (04-data/operational)"
version: "1.0.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-03-27"
---

# Operational data

## Overview

이 영역은 저장소 서비스가 사용하는 운영 데이터 패키지를 문서화합니다.

## Audience

공유 운영 상태의 operator와 maintainer를 대상으로 합니다.

## Scope

HOME 관리 데이터베이스와 별도의 OPTIONAL 애플리케이션 플랫폼을 다룹니다.

## Structure

### Packages and ownership

- [`mng-db`](mng-db/README.md)는 현재 auth, workflow, tooling 소비자를 위한
  HOME 공유 PostgreSQL과 Valkey입니다.
- [`supabase`](supabase/README.md)는 별도의 OPTIONAL 애플리케이션 플랫폼입니다.
  `mng-db`를 대체하거나 확장하지 않으며 디렉터리를 공유하지 않습니다.

## How to Work in This Area

각 패키지는 정확한 루트 profile을 통해 운영하십시오. 두 패키지가 비슷한
database/cache 프로토콜을 노출한다는 이유로 스키마, credential, queue,
volume을 병합하지 마십시오. 승격, 통합, 제거에는 named application,
스키마/데이터 migration, 격리된 복구 증명, rollback이 필요합니다.

## Related Documents

[문서 진입점](../../../docs/README.md)을 사용해 Stage 05 subject
`docs/05.operations/guides/0028-management-database.md`와 백업 정책 POL-0021을
찾으십시오.
