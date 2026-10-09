---
title: "RedisInsight Usage Guide"
version: "1.3.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
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
  profile, 볼륨, 라우트, CIDR, middleware, healthcheck, 사전 등록 연결을 정의한다.
- gateway 경로에는 admin CIDR와 OAuth2 Proxy ForwardAuth가 적용되며 호스트
  포트는 없다. RedisInsight에는 자체 로그인이 없으므로 Traefik만 함께 붙는 internal
  망 `redisinsight_ingress_net`의 고정 주소(`10.250.18.3`)에만 listener를 연다.
  이 망은 `gateway_mode_ipv4: isolated`라 호스트 쪽 bridge 주소가 없어 호스트
  프로세스도 닿지 않는다. `edge_net`에 없으므로 JupyterLab·n8n 같은 edge peer도 닿지 않고,
  `mng_data_net`, `dev_data_net` peer가 UI 포트에 직접 붙으면 연결이 거부된다.
  Traefik은 `traefik.docker.network: redisinsight_ingress_net`으로 이 주소를 쓴다.
- 선택형 n8n·Airflow 전용 Valkey(`dedicated-valkey`)는 운영자가 실제로 조회할 때만
  해당 망을 붙인다. 기본 선언에는 `n8n_net`, `airflow_net`이 없다.
- `RI_ENCRYPTION_KEY`(`secrets/data/redisinsight/encryption_key.txt`)로 저장된 연결
  비밀번호를 암호화한다. 이 키는 설정의 `encryption` 동의가 켜져 있을 때만 쓰인다.
  새 `/data`에서는 자동으로 켜지고, 기존 `/data`는 런북 절차로 한 번 켠다.
- healthcheck는 `/api/health/`의 `{"status":"up"}`만 본다. UI가 살아 있다는 뜻이며
  대상 DB 접속 성공은 아래 연결 확인으로 따로 본다.
- 업스트림은 RedisInsight를 SSPL 라이선스로 명시하며 해당 약관 동의를 요구한다.
  이 저장소는 다른 edition/라이선스를 주장하지 않는다.

### 일반적인 사용, 백업, 업그레이드

실행 순서와 실패·복구 판단은 [런북](../runbooks/0076-redisinsight.md)의 `승인된 사용·설정 보존·업그레이드` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Common Checks

- `docker compose --profile admin-data config --quiet`
- `bash scripts/hardening/check-all-hardening.sh 04-data`
- `HYHOME_REDISINSIGHT_REHEARSAL=1 python3 -m unittest tests.validation.test_redisinsight_rehearsal`
  (격리 망에서 접속·거부·중단·회전을 시험한다)

### Runbook Handoff

인증, 설정, credential, 대상, 업그레이드 복구에는
[runbook](../runbooks/0076-redisinsight.md)을 사용한다.

### 정상 사용과 운영 한계

일상 조회는 읽기 전용 inspector 계정의 사전 등록 연결만 쓴다. 쓰기나 삭제가
필요하면 별도 역할과 시험 prefix를 대상 소유자와 정한 뒤 진행하며, inspector에
쓰기 권한을 더하지 않는다. 별도 Compose readiness 의존성은 없으므로 대상
Valkey와 gateway 준비를 각각 확인한다. 기동 직후 첫 DB 요청은 시작 시 외부 조회가
끝나기 전까지 25초 요청 제한을 넘을 수 있으므로, 한 번 실패하면 다시 시도한다.

### 사전 등록 연결

RedisInsight는 시작할 때마다 아래 두 연결을 다시 만든다. 목록에서 빠진 사전 등록
연결은 자동으로 지워지므로 UI에서 고친 값은 다음 시작에 되돌아간다.

| 이름 | Host | Port | DB | Username | 비밀번호 secret |
| --- | --- | --- | --- | --- | --- |
| `DEV / dev-valkey` | `dev-valkey` | `6379` | `0` | `devinspector` | `secrets/db/dev-valkey/inspector_password.txt` |
| `MNG / mng-valkey` | `mng-valkey` | `6379` | `0` | `mnginspector` | `secrets/db/mng-valkey/inspector_password.txt` |

- 두 inspector는 같은 규칙(`~* resetchannels -@all +@read +@connection -@dangerous +info`)을
  쓴다. 키 브라우저, 키 정보, 값 조회, overview는 되고 `SET`·`DEL`·`KEYS`·`CONFIG`·
  `ACL`·`FLUSHALL`·`EVAL`·`PUBLISH`는 거부된다.
- 관리자(`devadmin`, MNG `default`)와 지표 수집(`devmonitor`) 비밀번호는 RedisInsight에
  넣지 않는다. renderer는 두 역할이 같은 비밀을 쓰면 시작을 거부한다.
- 키 브라우저는 `SCAN`으로 해당 DB의 모든 키 이름을 보여 준다. DEV에서는 다른
  프로젝트의 키 이름도 보이므로, `MATCH`나 prefix 필터를 프로젝트 격리로 여기지
  않는다. RedisInsight 접근 자체가 관리자 신뢰 경계다. 앱 계정의 `SCAN` 금지는
  그대로 둔다.
- 비밀번호는 secret 파일에서 `start.sh`가 읽어 환경으로만 넘기며 문서, 채팅, 로그,
  스크린샷에 남기지 않는다.

연결이 실패하면 대상 Valkey 컨테이너 안에서 inspector secret으로 `PING`이 `PONG`을
돌려주는지 확인하고, `ACL LOG`의 `username`으로 어떤 사용자로 시도했는지 본다.

### Traceability

- [Policy](../policies/0076-redisinsight.md) (`POL-0076`)
- [Runbook](../runbooks/0076-redisinsight.md) (`RUN-0076`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [RedisInsight configuration and encryption key](https://redis.io/docs/latest/operate/redisinsight/configuration/)
- [RedisInsight usage, telemetry, logs, and SSPL license](https://redis.io/docs/latest/develop/tools/insight/)
