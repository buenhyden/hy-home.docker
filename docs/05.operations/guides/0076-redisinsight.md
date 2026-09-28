---
title: "RedisInsight Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0076"
parent_ids:
- "POL-0076"
implementation_services:
  infra/11-laboratory/redisinsight/docker-compose.yml:
  - redisinsight
created: "2026-05-10"
---

# RedisInsight Usage Guide

## Usage

### 목적과 분류

RedisInsight는 `admin`과 `admin-data` 하위의 OPTIONAL admin UI이다. Redis/Valkey
서버가 아니며 대상 데이터베이스를 백업하지 않는다. `/data`에 마운트된
`${DEFAULT_MANAGEMENT_DIR}/redisinsight` 아래에 연결 정의, credential, workbench
history, 로그를 영속화한다.

### 현재 구현과 격차

- [RedisInsight Compose](../../../infra/11-laboratory/redisinsight/docker-compose.yml)가
  profile, 볼륨, 라우트, CIDR, middleware, healthcheck를 정의한다.
- UI에는 admin CIDR와 OAuth2 Proxy ForwardAuth를 갖춘 Traefik을 거쳐야만 도달할 수
  있다. 호스트 포트는 게시되지 않는다.
- 현재 소스는 `RI_ENCRYPTION_KEY`를 선언하지 않는다. 업스트림은 이 키가 로컬에
  저장된 데이터베이스 비밀번호/workbench history를 암호화한다고 명시한다.
  키를 구성하고 마이그레이션하기 전까지 `/data`와 그 백업은 민감한 평문 저장 위험으로
  취급한다.
- 디렉터리 health는 `/data` 가용성만 증명할 뿐 게이트웨이 인증, 대상 credential,
  대상 데이터베이스 인가는 증명하지 않는다.
- 업스트림은 RedisInsight를 SSPL 라이선스로 명시하며 해당 약관 동의를 요구한다.
  이 저장소는 다른 edition/라이선스를 주장하지 않는다.

### 일반적인 사용, 백업, 업그레이드

`docker compose --profile admin-data config --quiet`로 검증한다. 게이트웨이
인증/CIDR를 확인한 다음 최소 권한의 대상 credential만 추가한다. Workbench의
파괴적 명령은 대상 소유자 승인이 필요하다. ForwardAuth는 Redis 권한을 제한하지
않는다.

`/data`를 복사하기 전에 RedisInsight를 중지한다. 백업은 credential을 담은
자료로 보고 보호한다. UI 설정 백업은 대상 데이터베이스 백업이 아니다. 먼저 프로덕션
Redis/Valkey에 접근할 수 없는 격리된 RedisInsight로 복원하고 나중에 암호화
키가 구성되면 같은 키를 사용한다. 업그레이드 전에는 release와 라이선스 약관을
검토하고 저장된 연결/history를 테스트한다. 여기서는 백업/복원을 실행하지 않았다.

## Common Checks

- `docker compose --profile admin-data config --quiet`
- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`

## Runbook Handoff

인증, 설정, credential, 대상, 업그레이드 복구에는
[runbook](../runbooks/0076-redisinsight.md)을 사용한다.

## Traceability

- [Policy](../policies/0076-redisinsight.md) (`POL-0076`)
- [Runbook](../runbooks/0076-redisinsight.md) (`RUN-0076`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [RedisInsight configuration and encryption key](https://redis.io/docs/latest/operate/redisinsight/configuration/)
- [RedisInsight usage, telemetry, logs, and SSPL license](https://redis.io/docs/latest/develop/tools/insight/)
