# Laboratory Dashboard (Homer)

> A static service dashboard for easy navigation across infrastructure tools.

## Overview

Homer는 하이홈 인프라의 다양한 서비스 링크를 한곳에 모아 보여주는 정적 웹 대시보드다. 사용자가 환경 내 도구들에 빠르게 접근할 수 있도록 돕는 중앙 허브 역할을 담당한다.

## Audience

이 README의 주요 독자:

- Operators (대시보드 관리 및 서비스 추가)
- Developers (인프라 도구 접근)
- AI Agents (서비스 엔드포인트 파악)

## Scope

### In Scope

- Homer 서비스 구성 및 실행 설정 (`docker-compose.yml`)
- 서비스 링크 및 그룹 설정 (`config/config.yml`)
- 정적 자산(로고, 아이콘) 관리

### Out of Scope

- 개별 서비스(Portainer, Grafana 등)의 내부 구성 및 정책
- SSO 인증 시스템(SSO-Auth)의 핵심 로직 (Traefik 게이트웨이 담당)

## Structure

```text
dashboard/
├── config/
│   └── config.yml    # Main configuration for links and groups
├── docker-compose.yml # Container orchestration
└── README.md          # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Laboratory Dashboard (Homer) service leaf in `11-laboratory`; services: `homer`; root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-laboratory/dashboard/docker-compose.yml` |
| Config files | `docker-compose.yml`, `config`, `config/config.yml` |
| Config values | env keys: `INIT_ASSETS`; profiles: `admin` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-laboratory/dashboard/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `./config:/www/assets` |
| Ports | No host `ports`; Traefik targets internal `${HOMER_PORT:-8080}` via `expose` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.homer.rule`, `traefik.http.routers.homer.entrypoints`, `traefik.http.routers.homer.tls`, `traefik.http.middlewares.homer-admin-ip.ipallowlist.sourcerange`, `traefik.http.routers.homer.middlewares`, `traefik.http.services.homer.loadbalancer.server.port` |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `homer` |
| Operations | [Guide](../../../docs/05.operations/guides/11-laboratory/dashboard.md), [Policy](../../../docs/05.operations/policies/11-laboratory/dashboard.md), [Runbook](../../../docs/05.operations/runbooks/11-laboratory/dashboard.md) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh) tier `11-laboratory`; [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh) root `admin` profile for active includes; [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with the hardening check, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. **링크 추가**: `config/config.yml`의 `services` 섹션에 새로운 그룹이나 아이템을 추가한다.
2. **아이콘 설정**: FontAwesome 아이콘을 사용하여 가시성을 높인다.
3. **볼륨 바인딩**: 로컬 `config` 폴더를 컨테이너의 `/www/assets` 경로에 마운트하여 실시간 반영한다.
4. **대시보드 확인**: 설정 변경 후 `homer.${DEFAULT_URL}`에 접속하여 렌더링 상태를 검증한다.

## Available Scripts

| Tool   | Command                                | Description      |
| ------ | -------------------------------------- | ---------------- |
| Lint   | `yq eval . config/config.yml`          | YAML 구문 검증   |
| Hardening | `bash scripts/hardening/check-all-hardening.sh 11-laboratory` | 라우터/포트/healthcheck 기준 확인 |

## Configuration

### Environment Variables

| Variable            | Required | Description                     |
| ------------------- | :------: | ------------------------------- |
| `DEFAULT_URL`       |   Yes    | 기본 도메인 (homer.xxxx.xxx)    |
| `HOMER_PORT`        |    No    | 컨테이너 내부 포트 (기본: 8080) |

## Change Impact

- `config.yml`의 구문 오류는 대시보드 전체 로딩 실패를 유발한다.
- 서비스 URL 변경 시 Traefik 라우팅 설정과 동기화되어야 한다.

## Validation

- Run `bash scripts/hardening/check-all-hardening.sh 11-laboratory` after any Compose or config reference changes.
- Run `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh` for root-active laboratory profile validation.
- Verify UI connectivity by accessing the dashboard URL and confirming all service links resolve correctly.
- Confirm service health indicators by checking `docker logs homer --tail 100` after config changes when the optional service is running.
- Verify that all referenced service endpoints are reachable from the dashboard container.

## Troubleshooting

- Start with the hardening check to confirm dashboard network, label, and mounted config references.
- Check dashboard logs and the linked runbook before changing admin routing or service discovery settings.

## Related Documents

- **Guide**: [Dashboard Management Guide](../../../docs/05.operations/guides/11-laboratory/dashboard.md)
- **Policy**: [Laboratory Operations Policy](../../../docs/05.operations/policies/11-laboratory/dashboard.md)
- **Runbook**: [Dashboard Recovery Runbook](../../../docs/05.operations/runbooks/11-laboratory/dashboard.md)
- **Official**: [Homer Documentation](https://github.com/bastienwirtz/homer)
