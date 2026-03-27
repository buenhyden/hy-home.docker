# Relational Database Guides (04-data/relational)

> High-Availability Relational Database (PostgreSQL) 사용 및 최적화 가이드

## Overview

이 디렉터리는 `hy-home.docker` 데이터 티어의 관계형 데이터베이스(RDBMS) 기술 가이드를 포함합니다. Patroni 기반의 고가용성 PostgreSQL 클러스터 연결 방법, 쿼리 최적화, 그리고 클러스터 관리 지침을 제공합니다.

## Audience

이 README의 주요 독자:

- 데이터베이스 연결이 필요한 **Backend Developers**
- 클러스터 아키텍처를 관리하는 **Ops Engineers**
- 문서 구조를 학습하는 **AI Agents**

## Scope

### In Scope

- PostgreSQL HA 클러스터 접속 및 인증 방법
- 읽기/쓰기 분리를 위한 HAProxy 엔드포인트 활용
- 데이터베이스 초기화 및 사용자 계정 관리 절차
- 주요 성능 메트릭 및 모니터링 대시보드 사용법

### Out of Scope

- NoSQL 및 캐시 서비스 가이드 (-> `docs/07.guides/04-data/nosql/` 등)
- 애플리케이션 프레임워크별 ORM 최적화 (별도 가이드 참조)
- 개별 도메인별 ERD 설계 및 비즈니스 모델 정의

## Structure

```text
relational/
├── postgresql-cluster.md # PostgreSQL HA Cluster Guide
└── README.md             # This file
```

## How to Work in This Area

1. 전반적인 데이터 아키텍처는 [Data Spec](../../../../docs/04.specs/04-data/spec.md) 문서를 먼저 확인합니다.
2. 각 서비스의 배포 및 실행 방법은 `infra/04-data/relational/` 경로를 참조합니다.
3. 새로운 가이드 추가 시 `docs/99.templates/guide.template.md`를 사용합니다.

## Documentation Standards

이 영역의 모든 문서는 다음 기준을 따릅니다:

- 리포지토리 표준 8개 섹션 스켈레톤 준수
- 한글(KR) 개요 및 영문(EN) 상세 내용 병기 (Bilingual Policy)
- Single Source of Truth(SSoT) 유지 및 중복 방지

## Related References

- **Operations**: [Relational Operations](../../../../docs/08.operations/04-data/relational/README.md)
- **Runbooks**: [Relational Runbooks](../../../../docs/09.runbooks/04-data/relational/README.md)
- **Source**: [Infrastructure README](../../../../infra/04-data/relational/README.md)

---
Copyright (c) 2026. Licensed under the MIT License.
