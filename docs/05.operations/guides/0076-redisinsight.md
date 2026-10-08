---
title: "RedisInsight Usage Guide"
version: "1.2.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "operations"
artifact_id: "GDE-0076"
parent_ids:
- "POL-0076"
implementation_services:
  infra/04-data/redisinsight/docker-compose.yml:
  - redisinsight
created: "2026-05-10"
---

# RedisInsight Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### 목적과 분류

RedisInsight는 `admin`과 `admin-data` 하위의 OPTIONAL admin UI이다. Redis/Valkey
서버가 아니며 대상 데이터베이스를 백업하지 않는다. `/data`에 마운트된
`${DEFAULT_MANAGEMENT_DIR}/redisinsight` 아래에 연결 정의, credential, workbench
history, 로그를 영속화한다.

### 현재 구현과 격차

- [RedisInsight Compose](../../../infra/04-data/redisinsight/docker-compose.yml)가
  profile, 볼륨, 라우트, CIDR, middleware, healthcheck를 정의한다.
- gateway 경로에는 admin CIDR와 OAuth2 Proxy ForwardAuth가 적용되며 호스트
  포트는 없다. 그러나 `edge_net`, `mng_data_net`, `dev_data_net`,
  `n8n_net`, `airflow_net` peer는 직접 listener에 연결할 수 있다. 네이티브 UI 인증 선언이
  없어 gateway만이 유일한 접근 경로라고 볼 수 없다.
- 현재 소스는 `RI_ENCRYPTION_KEY`를 선언하지 않는다. 업스트림은 이 키가 로컬에
  저장된 데이터베이스 비밀번호/workbench history를 암호화한다고 명시한다.
  키를 구성하고 마이그레이션하기 전까지 `/data`와 그 백업은 민감한 평문 저장 위험으로
  취급한다.
- 디렉터리 health는 `/data` 가용성만 증명할 뿐 게이트웨이 인증, 대상 credential,
  대상 데이터베이스 인가는 증명하지 않는다.
- 업스트림은 RedisInsight를 SSPL 라이선스로 명시하며 해당 약관 동의를 요구한다.
  이 저장소는 다른 edition/라이선스를 주장하지 않는다.

### 일반적인 사용, 백업, 업그레이드

실행 순서와 실패·복구 판단은 [런북](../runbooks/0076-redisinsight.md)의 `승인된 사용·설정 보존·업그레이드` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Common Checks

- `docker compose --profile admin-data config --quiet`
- `bash scripts/hardening/check-all-hardening.sh 04-data`

### Runbook Handoff

인증, 설정, credential, 대상, 업그레이드 복구에는
[runbook](../runbooks/0076-redisinsight.md)을 사용한다.

### 정상 사용과 운영 한계

승인된 최소 권한 연결만 선택하고 Workbench 변경은 대상 소유자의 승인을 받는다.
별도 Compose readiness 의존성은 없으므로 대상 Redis/Valkey와 gateway 준비를 각각
확인한다. 디렉터리 health와 UI 로그인은 대상 권한·모든 Valkey 기능 호환성을
보증하지 않는다. 메모리·연결 수·설정 저장소 사용량은 Compose 자원 제한과 함께
검토한다. 현재 이미지의 실제 저장 형식을 조사하지 않았으므로 암호화 키 미선언만으로
모든 저장값이 평문이라고 단정하지 않지만, 암호화 보장도 주장하지 않는다.

### dev-valkey 연결

RedisInsight는 `dev_data_net`으로 `dev-valkey`에 닿는다. 연결을 추가할 때는
다음 값을 쓴다.

| 항목 | 값 |
| --- | --- |
| Host | `dev-valkey` |
| Port | `6379` |
| Username | `devadmin` |
| Password | `secrets/db/dev-valkey/admin_password.txt`의 내용 |

- Username을 비워 두면 RedisInsight는 `default` 사용자로 인증한다. `dev-valkey`의
  ACL은 `user default off`로 시작하므로 이 경우 `Authentication failed`가 난다.
- 비밀번호는 secret 파일에서 직접 붙여 넣는다. 문서, 채팅, 로그, 스크린샷에
  남기지 않는다.
- `devmonitor`는 지표 수집 전용 계정이라 키를 읽지 못한다. RedisInsight 연결에
  쓰지 않는다.
- 프로젝트 사용자(`projects.tsv`)는 자기 키 prefix만 다룬다. 특정 프로젝트 범위로만
  보려면 그 사용자와 해당 secret으로 연결한다.
- `devadmin`은 모든 키와 명령을 다룰 수 있다. Workbench에서 쓰기나 삭제를 하기
  전에 대상 프로젝트 소유자의 승인을 받는다.
- admin 비밀번호를 바꾸면 RedisInsight에 저장한 연결의 비밀번호도 함께 고친다.
  ACL은 `dev-valkey`를 다시 시작할 때 secret에서 새로 만들어진다.

연결이 실패하면 `dev-valkey` 컨테이너 안에서 secret 파일로 `devadmin` 인증이
`PONG`을 돌려주는지 먼저 확인하고, `ACL LOG`의 `username`으로 어떤 사용자로
시도했는지 본다.

### 소스 검토의 한계

여기서 설명한 네트워크는 선언상 연결 가능한 경로다. 실제 peer 연결·인터넷 공개·
사용자 인증·복구 성공을 이번 문서 작업에서 시험하지 않았다. 현재 선언의 제한을
해소하는 구현 변경은 별도 승인·보안 검토·검증이 필요하다.

### Traceability

- [Policy](../policies/0076-redisinsight.md) (`POL-0076`)
- [Runbook](../runbooks/0076-redisinsight.md) (`RUN-0076`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [RedisInsight configuration and encryption key](https://redis.io/docs/latest/operate/redisinsight/configuration/)
- [RedisInsight usage, telemetry, logs, and SSPL license](https://redis.io/docs/latest/develop/tools/insight/)
