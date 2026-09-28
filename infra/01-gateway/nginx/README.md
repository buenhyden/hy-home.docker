---
title: "Nginx Proxy"
version: "1.2.3"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2025-11-29"
---

# Nginx Proxy

> `nginx` profile로 선택되는 전용 경로 기반 프록시이자 hy-home.docker 생태계의 SSO 클라이언트입니다.

## Overview

Nginx 컴포넌트는 `01-gateway` tier의 전용 프록시로, 복잡한 경로 기반 라우팅(예: 읽기 전용 `/cdn/` 버킷 경로, Keycloak)과 OAuth2 Proxy를 통한 SSO 검사를 수행합니다. 루트 [docker-compose.yml](../../../docker-compose.yml)은 이 파일을 무조건 include하며 `nginx` profile이 서비스를 선택합니다. 파일 단독 검증에도 명시적인 root network/dependency context가 필요하고 실행은 승인된 runtime 절차가 있을 때만 다룹니다.

## Audience

이 README의 주요 독자:

- Infrastructure Engineers
- Backend Developers
- AI Agents

## Scope

### In Scope

- 경로 기반 라우팅 규칙(예: `/cdn/`, `/keycloak/`, `/oauth2/`).
- `auth_request`를 통한 SSO 인증 통합.
- 커스텀 헤더 관리와 프록시 최적화.
- 내부 서비스를 위한 보조 SSL/TLS 종료.

### Out of Scope

- 핵심 에지 라우팅과 전역 TLS 조율(Traefik이 담당).
- 여러 클러스터에 걸친 전역 로드 밸런싱.
- 영구 저장소 관리.

## Structure

```text
nginx/
├── config/
│   └── nginx.conf    # 주 설정 파일(upstream, server, location)
├── docker-compose.yml # 서비스 정의와 볼륨
└── README.md          # 이 파일
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `01-gateway`의 Nginx Proxy 서비스 leaf; services: `nginx`; 루트 include는 항상 활성이고 `nginx` profile이 서비스를 선택하며 여전히 루트 네트워크 컨텍스트에 의존함 |
| Config files | `docker-compose.yml`, `config`, `config/nginx.conf` |
| Config values | profiles: `nginx` |
| Compose linkage | 루트 [docker-compose.yml](../../../docker-compose.yml)이 이 파일을 무조건 include하고 `nginx` profile이 서비스를 선택함; 파일 단독 검증에도 루트 네트워크와 백엔드 의존성에 대한 명시적 컨텍스트가 필요함 |
| Networks | `edge_net`, `object_net` |
| Volumes | `./config/nginx.conf:/etc/nginx/nginx.conf:ro`, `${DEFAULT_CERT_DIR}:/etc/nginx/certs:ro` |
| Ports | `${HTTP_HOST_PORT:-80}:${HTTP_PORT:-80}`, `${HTTPS_HOST_PORT:-443}:${HTTPS_PORT:-443}` |
| Labels | 선언되지 않음 |
| Secret refs | 선언되지 않음 |
| Healthcheck | `nginx`에 Compose healthcheck 선언됨 |
| Operations | Guide (`docs/05.operations/guides/0011-nginx.md`), Policy (`docs/05.operations/policies/0011-nginx.md`), Runbook (`docs/05.operations/runbooks/0011-nginx.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 정적 하드닝 검사부터 시작하고 승인된 Nginx runtime 컨텍스트가 이미 실행 중일 때만 서비스 로그를 확인함 |

## How to Work in This Area

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. `config/nginx.conf`를 검토해 현재 `location` 블록과 `upstream` 정의를 이해합니다.
2. 새 경로 기반 라우트를 추가할 때는 `nginx.conf`의 주 `server` 블록에 추가되었는지 확인합니다.
3. 라우트에 SSO가 필요하면 `auth_request /_oauth2_auth_check;` 지시어를 포함합니다.
4. 설정 변경 후에는 `bash scripts/hardening/check-all-hardening.sh 01-gateway`를 실행합니다. `nginx -t`나 reload는 승인된 실행 중 Nginx 컨텍스트에 대해서만 수행합니다.
5. 설정을 reload하기 전에는 승인된 실행 중 컨텍스트에서 항상 `nginx -t`를 먼저 실행합니다.
6. redirect loop를 피하기 위해 upstream에 `X-Forwarded-Proto https`가 설정되어 있는지 확인합니다.
7. 새 라우팅 로직을 추가할 때는 `docs/05.operations/guides/0011-nginx.md`의 관련 경로 가이드를 갱신합니다.

## Configuration

### Core Files

- `config/nginx.conf`: 라우팅 로직, SSO 통합, 버퍼 최적화를 정의합니다.
- `docker-compose.yml`: 인증서와 설정 파일을 컨테이너에 마운트합니다.

### Docker Healthcheck

Nginx의 healthcheck는 포트 80의 `/ping` 엔드포인트 가용성을 확인합니다.

```yaml
healthcheck:
  test: ['CMD-SHELL', 'wget -q --spider http://localhost:${HTTP_PORT:-80}/ping || exit 1']
```

## Validation

| Command | Description |
| --- | --- |
| `bash scripts/hardening/check-all-hardening.sh 01-gateway` | 추적된 Nginx compose/config 하드닝 계약을 검증함 |
| `docker compose exec nginx nginx -t` | 승인된 Nginx compose 컨텍스트가 실행 중일 때만 수행하는 runtime 설정 lint |
| `docker compose exec nginx nginx -s reload` | 승인된 실행 중 컨텍스트에서 `nginx -t`가 통과한 뒤에만 수행하는 runtime reload |

- 이 서비스에 영향을 주는 README, compose, config 변경 후에는 `bash scripts/hardening/check-all-hardening.sh 01-gateway`를 실행합니다.
- 서비스 문서를 준비 완료로 표시하기 전에 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.
- `nginx`는 루트 네트워크와 백엔드 서비스에 의존하므로, 서비스 단독 compose 렌더링만으로는 충분한 증거로 취급하지 않습니다.

## Troubleshooting

- 게이트웨이 하드닝 검사로 추적된 Nginx 계약이 구현과 여전히 일치하는지 먼저 확인합니다.
- 승인된 runtime 컨텍스트가 범위에 있을 때만 `nginx` 컨테이너 로그를 확인하고 라우팅 오류를 연결된 운영 가이드와 비교합니다.

## Related Documents

- [01-gateway 루트 README](../README.md)
- Nginx 가이드 (`docs/05.operations/guides/0011-nginx.md`)
- 게이트웨이 운영 정책 (`docs/05.operations/policies/0011-nginx.md`)
- Nginx 런북 (`docs/05.operations/runbooks/0011-nginx.md`)
- SSO 설정 가이드 (`docs/05.operations/guides/README.md`)
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [curated 버전 투영](../../tech-stack.versions.json)으로 drift를 검증합니다.
