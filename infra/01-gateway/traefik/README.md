---
title: "Traefik Edge Router"
version: "1.0.3"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2025-11-12"
---

# Traefik Edge Router

> hy-home.docker 생태계의 주 에지 라우터로, 동적 서비스 탐색과 TLS 조율을 갖췄습니다.

## Overview

Traefik은 `hy-home.docker` 생태계의 주 에지 라우터입니다. Docker 프로바이더를 통한 동적 서비스 탐색과 자동 TLS 종료를 제공합니다. 트래픽 모니터링 및 관리를 위한 대시보드도 있습니다.

---

## Audience

이 README의 주요 독자:

- Infrastructure Engineers
- SREs
- AI Agents

## Scope

### In Scope

- 전역 entrypoint 정의(`web` 80, `websecure` 443, `metrics` 8082).
- Docker Provider를 통한 동적 서비스 탐색과 라우팅 label.
- 미들웨어 조율(RateLimit, BasicAuth, SSO).
- TLS store와 인증서 관리.
- Observability 통합(Prometheus 메트릭, OTLP 추적).

### Out of Scope

- 애플리케이션 수준의 비즈니스 로직.
- 상세한 경로 기반 재작성(일부는 Nginx에 위임).
- 개별 서비스 컨테이너 정의(각자의 infra 폴더에서 관리).

## Structure

```text
traefik/
├── config/
│   └── traefik.yml     # 정적 설정(entrypoint, provider, API)
├── dynamic/
│   ├── middleware.yml  # 공유 미들웨어(SSO, RateLimit, BasicAuth)
│   └── tls.yaml        # TLS 인증서 매핑과 store
├── docker-compose.yml  # 서비스 정의와 배포
└── README.md           # 이 파일
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `01-gateway`의 Traefik 에지 라우터 서비스 leaf; services: `traefik`; [root docker-compose.yml](../../../docker-compose.yml)을 통해 root include가 활성화됨 -> `infra/01-gateway/traefik/docker-compose.yml` |
| Config files | `docker-compose.yml`, `config`, `config/README.md`, `config/traefik.yml` |
| Config values | profiles: `core`, `dev` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)을 통해 root include가 활성화됨 -> `infra/01-gateway/traefik/docker-compose.yml` |
| Networks | `edge_net`, `obs_net` |
| Volumes | `/var/run/docker.sock:/var/run/docker.sock:ro`, `${DEFAULT_CERT_DIR}:/certs:ro`, `./dynamic:/dynamic:ro`, `./config/traefik.yml:/etc/traefik/traefik.yml:ro` |
| Ports | `${HTTP_HOST_PORT:-80}:${HTTP_PORT:-80}`, `${HTTPS_HOST_PORT:-443}:${HTTPS_PORT:-443}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.dashboard.rule`, `traefik.http.routers.dashboard.entrypoints`, `traefik.http.routers.dashboard.tls`, `traefik.http.routers.dashboard.service`, `traefik.http.routers.dashboard.middlewares` |
| Secret refs | names: `traefik_basicauth_password`, `traefik_opensearch_basicauth_password`, `traefik_prometheus_api_htpasswd`; mounts: `/run/secrets/traefik_basicauth_password`, `/run/secrets/traefik_opensearch_basicauth_password`, `/run/secrets/traefik_prometheus_api_htpasswd` |
| Healthcheck | `traefik`에 Compose healthcheck 선언됨 |
| Operations | Guide (`docs/05.operations/guides/0013-traefik.md`), Policy (`docs/05.operations/policies/0013-traefik.md`), Runbook (`docs/05.operations/runbooks/0013-traefik.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 루트 profile 검증과 게이트웨이 하드닝 검사부터 시작하고 Traefik runtime이 이미 승인되어 실행 중일 때만 서비스 로그를 확인함 |

## Usage

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. `config/traefik.yml`을 먼저 검토해 핵심 라우팅 entrypoint를 이해합니다.
2. 새 서비스에 인증이나 rate-limiting을 추가할 때는 `dynamic/middleware.yml`을 확인합니다.
3. 서비스의 `docker-compose.yml`에 label을 사용해 Traefik에 라우트를 등록합니다.
4. 설정 변경 후에는 runtime 대시보드 증거를 사용하기 전에 루트 profile 검증기와 게이트웨이 하드닝 검사를 실행합니다.
5. 전체 클러스터 영향 분석 없이 `traefik.yml`의 entrypoint를 수정하지 않습니다.

- **필수**: 모든 동적 라우팅 변경은 Traefik 대시보드로 검증해야 합니다.
- **검증**: 정적 검증을 먼저 사용하고 승인된 실행 중 스택에 대해서만 Traefik 로그를 확인합니다.

### Environment Variables

| Variable          | Required | Description |
| ----------------- | -------: | ----------- |
| `DEFAULT_URL`     |      Yes | 주 도메인(예: localhost 또는 your-domain.com) |
| `HTTP_HOST_PORT`  |       No | HTTP 호스트 포트(기본값: 80) |
| `HTTPS_HOST_PORT` |       No | HTTPS 호스트 포트(기본값: 443) |

## Configuration

### Core Files

- `config/traefik.yml`: 정적 설정(entrypoint, provider, API).
- `dynamic/middleware.yml`: 공유 미들웨어(SSO/ForwardAuth, RateLimit, BasicAuth).
- `dynamic/tls.yaml`: TLS 인증서 매핑과 store.

### Docker Healthcheck

Traefik의 내장 healthcheck는 내부 ping 엔드포인트를 사용합니다.

```yaml
healthcheck:
  test: ['CMD', 'traefik', 'healthcheck', '--ping']
  interval: 15s
  timeout: 30s
  retries: 5
```

### Keycloak & OAuth2 Proxy Integration

Traefik은 `ForwardAuth` 미들웨어(`sso-auth@file`)를 사용해 인증을 OAuth2 Proxy에 위임합니다.

1. Entrypoint: `websecure`(포트 443).
2. Middleware: `sso-auth@file` -> `http://oauth2-proxy:4180/oauth2/auth`.
3. Error Redirect: `sso-errors@file`이 401/403 리다이렉트를 `/oauth2/sign_in`으로 처리.

## Validation

| Command | Description |
| --- | --- |
| `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh` | root-included Traefik compose 컨텍스트를 검증함 |
| `bash scripts/hardening/check-all-hardening.sh 01-gateway` | 게이트웨이 하드닝 계약을 검증함 |
| `docker compose ps traefik` | 승인된 루트 스택이 실행 중일 때만 수행하는 runtime 상태 확인 |
| `docker compose exec traefik traefik healthcheck --ping` | 승인된 루트 스택이 실행 중일 때만 수행하는 runtime 헬스 체크 |

- Traefik compose나 config 참조 변경 후에는 `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh 01-gateway`를 실행합니다.
- 승인된 루트 runtime이 실행 중일 때만 Traefik 대시보드에서 라우팅 설정을 확인합니다.
- runtime 승인 후에만 정제된 Traefik 로그로 TLS와 미들웨어 동작을 확인합니다.

## Troubleshooting

- 루트 `core` profile 검증기로 라우터, 네트워크, secret, 마운트된 dynamic config 경로가 정상 렌더링되는지 먼저 확인합니다.
- runtime 증거가 범위에 있을 때만 `traefik` 컨테이너 로그를 확인하고 라우터 또는 미들웨어 실패를 연결된 게이트웨이 운영 가이드와 비교합니다.

## Related Documents

- [01-gateway 루트 README](../README.md)
- Traefik 가이드 (`docs/05.operations/guides/0013-traefik.md`)
- 게이트웨이 운영 정책 (`docs/05.operations/policies/0013-traefik.md`)
- Traefik 런북 (`docs/05.operations/runbooks/0013-traefik.md`)
- [Traefik 대시보드](https://dashboard.${DEFAULT_URL:-localhost}) (내부용)
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [curated 버전 투영](../../tech-stack.versions.json)으로 drift를 검증합니다.
