---
title: "Development Database (dev-db)"
version: "0.1.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-02"
created: "2026-10-02"
---

# 개발 데이터베이스

## Overview

이 패키지는 개발 업무용 PostgreSQL과 Valkey의 소스 선언을 소유합니다.
관리 서비스의 `mng-db` 및 별도 LAB 상태와 저장 경로를 공유하지 않습니다.

## Audience

개발 데이터 엔진과 외부 프로젝트 접속 계약을 검토하는 maintainer와 operator를 대상으로 합니다.

## Scope

[`docker-compose.yml`](docker-compose.yml)은 `dev-pg`, `dev-platform-provision`,
`dev-valkey`를 정의합니다. 실제 외부 프로젝트 DB·계정·ACL은 승인된 프로젝트
명세가 있을 때만 등록합니다. HOME 실행과 기존 데이터 이관은 별도 승인 단계입니다.

## Structure

[`pg/`](pg/)는 TimescaleDB 이미지, 백업 설정, 명시적 프로젝트 provision을
소유합니다. [`valkey/`](valkey/)는 설정, ACL 생성, 시작 스크립트를 소유합니다.
엔진별 입력·출력·검증 상태는 각 하위 README에서 확인합니다.

## How to Work in This Area

루트에서 다음 정적 검사를 실행합니다. `config`는 컨테이너를 시작하지 않습니다.

```bash
docker compose --env-file .env.example --profile dev-data config --quiet
python3 -m unittest tests.validation.test_dev_pg_provision tests.validation.test_dev_valkey_acl
```

## Related Documents

[문서 진입점](../../../docs/README.md)에서 개발 데이터 계약을 다루는 현재
SPEC-0202와 Stage 05 운영 문서를 찾으십시오. 엔진 세부 사항은
[PostgreSQL README](pg/README.md) 및 [Valkey README](valkey/README.md)를
참조하십시오.
