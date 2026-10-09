---
title: "RedisInsight"
version: "1.0.5"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-08"
created: "2026-03-26"
---

# RedisInsight

> Redis 시각화, 분석, 관리 도구입니다.

## Overview

RedisInsight는 Redis 데이터를 시각화, 분석, 관리할 수 있는 강력한 GUI입니다. 키 탐색, 메모리 프로파일링, 실시간 모니터링 같은 기능을 제공합니다.

## Audience

- **Operators**: Redis 상태 및 메모리 사용량 모니터링.
- **Developers**: 데이터 구조 분석 및 애플리케이션 상태 디버깅.
- **Data Engineers**: Redis 성능 프로파일링 및 병목 식별.

## Scope

- **Included**: 웹 UI를 통한 Redis 키 탐색, 스트림 분석, 메모리 프로파일링, CLI 접근.
- **Excluded**: Redis 서버 OS의 직접 관리, 하드웨어 수준 성능 튜닝.

## Structure

```text
.
├── docker-compose.yml       # Service definition
└── README.md                # Entry point
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `04-data`의 RedisInsight 서비스 leaf; 서비스: `redisinsight`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/04-data/redisinsight/docker-compose.yml` 경로로 루트 include가 활성화됨 |
| Config files | `docker-compose.yml` |
| Config values | 프로필: `admin`, `admin-data` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/04-data/redisinsight/docker-compose.yml` 경로로 루트 include가 활성화됨 |
| Networks | `edge_net`(고정 `10.250.1.3`), `mng_data_net`, `dev_data_net` |
| Volumes | `redisinsight-data:/data:rw`, `redisinsight-data` |
| Ports | 선언되지 않음 |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.redisinsight-static.rule`, `traefik.http.routers.redisinsight-static.entrypoints`, `traefik.http.routers.redisinsight-static.tls`, `traefik.http.routers.redisinsight-static.priority`, `traefik.http.routers.redisinsight-static.service`, `traefik.http.routers.redisinsight.rule`, 외 7개 |
| Secret refs | 선언되지 않음 |
| Healthcheck | `/api/health/`의 `{"status":"up"}`(UI 상태만, DB 접속은 별도 확인) |
| Operations | Guide (`docs/05.operations/guides/0076-redisinsight.md`), Policy (`docs/05.operations/policies/0076-redisinsight.md`), Runbook (`docs/05.operations/runbooks/0076-redisinsight.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh) `04-data` tier; [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh) 루트 `admin` 프로필; [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 하드닝 점검부터 시작한 뒤 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## Usage

### 1. Initial Setup

1. `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`로 루트에서 활성화되는 admin 프로필을 검증합니다.
2. 승인된 실행 환경에서만 `https://redisinsight.${DEFAULT_URL}`에 접속합니다.
3. EULA에 동의하고 Redis/Valkey 인스턴스에 대한 초기 연결을 설정합니다.

### 2. Basic Usage

- 호스트명(예: 로컬 컨테이너의 경우 `redis`)과 포트(6379)를 입력해 새 데이터베이스를 추가합니다.
- 'Browser' 탭을 사용해 키와 값을 탐색합니다.
- 'Memory Analysis'를 사용해 메모리를 많이 사용하는 키를 찾습니다.

## Implementation Details

### Service Configuration

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Image | [declared runtime image](../../tech-stack.versions.json) | 현재 compose 태그 |
| Port | `5540` (Internal) | Traefik이 관리 |
| Storage | `redisinsight-data` | 연결 정보용 영속 볼륨 |

### Traefik Integration

게이트웨이 SSO·CIDR 제한은 해당 라우트에 적용된다. RedisInsight에는 자체
로그인이 없으므로 `RI_APP_HOST`로 listener를 `edge_net` 주소에만 열어 데이터 망
peer의 직접 접속을 막는다. 사전 등록 연결 `DEV / dev-valkey`와 `MNG / mng-valkey`는
읽기 전용 inspector 계정을 쓰며, `scripts/start.sh`가 inspector 비밀번호와
`RI_ENCRYPTION_KEY`를 secret에서 읽어 저장 비밀번호를 암호화한다. `/data` 백업은
연결 대상 Redis/Valkey의 데이터 복구를 대신하지 않는다.

```yaml
labels:
  traefik.enable: 'true'
  traefik.http.routers.redisinsight.rule: Host(`redisinsight.${DEFAULT_URL}`)
  traefik.http.routers.redisinsight.middlewares: gateway-standard-chain@file,redisinsight-admin-ip@docker,sso-errors@file,sso-auth@file
```

## Available Scripts

- `bash scripts/hardening/check-all-hardening.sh 04-data`: RedisInsight 라우트, 이미지, 네트워크 소속, 헬스체크를 검증합니다.
- `docker logs --tail 100 redisinsight`: 서비스 실행 중 로그를 확인합니다.

## Validation

- RedisInsight에 영향을 주는 README나 Compose 참조 변경 후에는 `bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 서비스 문서와 운영 링크를 동기화하려면 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.

## Troubleshooting

- RedisInsight 네트워크, 볼륨, 레이블 참조를 확인하려면 하드닝 점검부터 시작합니다.
- admin 라우팅이나 연결 설정을 변경하기 전에 RedisInsight 로그와 연결된 런북을 확인합니다.

## Related Documents

- **Guide**: RedisInsight usage guide (`docs/05.operations/guides/0076-redisinsight.md`)
- **Policy**: RedisInsight operations policy (`docs/05.operations/policies/0076-redisinsight.md`)
- **Runbook**: RedisInsight recovery runbook (`docs/05.operations/runbooks/0076-redisinsight.md`)
- [Documentation index](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.
