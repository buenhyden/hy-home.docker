---
title: "Development PostgreSQL"
version: "0.1.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-02"
created: "2026-10-02"
---

# 개발 PostgreSQL

## Overview

`dev-pg`는 Compose와 Dockerfile에 선언된 TimescaleDB Community/PG 단일 인스턴스의 **소스 선언**입니다. `dev-data` 프로파일은 개발 PostgreSQL과 Valkey만 선택합니다. `dev-platform-provision`은 `analytics-engineering` 또는 `cdc` 프로파일에서만 선택되며 명시된 `hyhome-platform` 기술 fixture의 `platform_dev` 데이터베이스를 만들도록 설계됐습니다. 공무원·언어 학습 앱이나 외부 업무 프로젝트 데이터베이스는 기본 설치에서 생성하지 않습니다.

## Audience

개발 PostgreSQL과 프로젝트별 데이터 권한을 검토하는 maintainer와 operator를 대상으로 합니다.

## Scope

- 입력: `DEFAULT_DATA_DIR`의 새로운 `dev-pg` 디렉터리, 별도의 `${BACKUP_STATE_REPO_DIR}/dev-pgbackrest`, `DEV_PG_HOST_PORT`(기본 25433, localhost), `DEV_PG_ADMIN_USER`(기본 postgres), root의 `dev_data_net`, `dev_pg_admin_password`, `dev_pgbackrest_cipher_pass`, 플랫폼 fixture의 세 역할 비밀번호 secret. 실제 값은 저장소 밖 Docker secret으로 공급합니다.
- 출력: `dev-pg:5432` endpoint와 `platform_dev`의 `platform_owner`(NOLOGIN), `platform_migrator`, `platform_runtime`, `platform_reader` 역할. DB와 schema `app`의 소유자는 `platform_owner`이며 migrator는 migration 때 `SET ROLE platform_owner`를 실행해야 새 객체에 기본 권한이 적용됩니다. Runtime과 reader는 DDL 권한이 없습니다.
- 범위: 별도 `dev` pgBackRest stanza, 새 PGDATA `/var/lib/postgresql/18/docker`, 2 CPU/2 GiB RAM/256 MiB SHM, 100 연결, WAL archive 명령의 비활성 초안. `archive_mode=off`이며 stanza/키/저장소/일정/관측 검증과 별도 재시작 승인 후에만 활성화합니다. `max_wal_size=2GB`는 PostgreSQL WAL 디스크 사용의 강제 상한이 아닙니다. WAL/저장소 여유를 관측해야 합니다.
- 보류: secret 발급, HOME 실행, 백업/복원, extension load, 실권한 거절 검증, RPO/RTO 실측. 이미지 빌드 및 선언된 pgBackRest 패키지의 이 이미지 내 호환성도 미검증입니다. 두 full chain과 5분 RPO/4시간 RTO는 승인 전 제안값입니다. pgBackRest retention/expire 설정은 활성화하지 않았습니다.

## Structure

[`Dockerfile`](Dockerfile)은 TimescaleDB 이미지에 pgBackRest를 추가하고, [`backup/`](backup/)은 비활성 백업 설정을 소유합니다. [`provision/`](provision/)은 승인된 프로젝트의 role/DB 경계를 소유합니다. 루트 [`docker-compose.yml`](../docker-compose.yml)이 서비스를 선언합니다.

`provision/project.py`는 명시적 JSON schema v1과 `environment=development`만 받습니다. 이름·secret 참조를 검증한 뒤 실행 시에만 `/run/secrets/`의 값을 읽습니다. 프로젝트별 이름을 shell에서 조합하지 않습니다. 이미 존재하는 DB/role은 project comment가 일치해야 재사용되며, 기존 LOGIN 역할의 비밀번호는 반복 실행 때 바뀌지 않습니다. 최초 DB 생성과 comment 사이에 중단되어도 표식이 있는 프로젝트 owner가 소유하고 ACL이 기본값이며 사용자 schema·객체가 없는 새 DB일 때만 표식을 복구합니다. 이 조건에 맞지 않는 기존 DB는 소유자 검토가 필요하며 자동 인수하지 않습니다.

`platform_dev`은 승인된 시간 이력 테이블을 만들지 않습니다. 업무 migration은 외부 프로젝트 소유이며 UTC/단위/정밀도/NULL/중복/지연 도착, partition 차원을 포함한 유일키, chunk·index·continuous aggregate·refresh·raw retention과 백필/삭제 승인을 명시해야 합니다. 개발 DB 세부 운영 계약은 [운영 가이드 목록](../../../../docs/05.operations/guides/README.md)에서 확인합니다. 승인된 프로젝트 계약 전에는 hypertable과 retention 정책을 추가하지 않습니다.

## How to Work in This Area

정적 확인: `python3 -m unittest tests.validation.test_dev_pg_provision` 및 `python3 infra/04-data/dev-db/pg/provision/project.py infra/04-data/dev-db/pg/provision/platform.json --validate-only`. 백업 운영 절차는 Stage 05의 기존 백업 정책·런북 소유자가 별도로 갱신합니다.


## Related Documents

[문서 진입점](../../../../docs/README.md)에서 현재 SPEC-0202와 Stage 05 백업 정책·런북을 찾으십시오.
