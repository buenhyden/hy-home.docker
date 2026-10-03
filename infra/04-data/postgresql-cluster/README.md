---
title: "PostgreSQL HA LAB support"
version: "0.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2026-10-03"
---

# PostgreSQL HA LAB support

## Overview

이 디렉터리는 독립 LAB의 추적된 보조 소스(init-scripts, config, scripts)를 보유합니다. Compose와 실행 안내는 [LAB 문서](../../../labs/postgresql-ha.md)에 함께 있습니다.

## Audience

LAB 소스 관리자와 검토자를 대상으로 합니다.

## Scope

정상 HOME 서비스·상태와 공유하지 않는 보조 파일만 소유합니다.

## Structure

LAB Compose가 이 디렉터리의 스크립트·설정을 참조합니다. 실제 진입점은 `labs/postgresql-ha.yml`입니다.

## How to Work in This Area

LAB의 독립 프로젝트·환경·secret·network·volume 계약과 정적 검증은 co-located LAB 문서를 따릅니다. HOME root Compose로 실행하지 않습니다.

## Related Documents

- [LAB 문서](../../../labs/postgresql-ha.md)
- [데이터 tier](../README.md)
