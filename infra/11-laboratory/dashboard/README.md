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

## How to Work in This Area

1. **링크 추가**: `config/config.yml`의 `services` 섹션에 새로운 그룹이나 아이템을 추가한다.
2. **아이콘 설정**: FontAwesome 아이콘을 사용하여 가시성을 높인다.
3. **볼륨 바인딩**: 로컬 `config` 폴더를 컨테이너의 `/www/assets` 경로에 마운트하여 실시간 반영한다.
4. **대시보드 확인**: 설정 변경 후 `homer.${DEFAULT_URL}`에 접속하여 렌더링 상태를 검증한다.

## Available Scripts

| Tool   | Command                                | Description      |
| ------ | -------------------------------------- | ---------------- |
| Docker | `docker compose up -d`                 | 서비스 시작      |
| Docker | `docker compose down`                  | 서비스 중단      |
| Docker | `docker compose restart homer`         | 설정 재로드      |
| Lint   | `yq eval . config/config.yml`          | YAML 구문 검증   |

## Configuration

### Environment Variables

| Variable            | Required | Description                     |
| ------------------- | :------: | ------------------------------- |
| `DEFAULT_URL`       |   Yes    | 기본 도메인 (homer.xxxx.xxx)    |
| `HOMER_HOST_PORT`   |    No    | 호스트 접속 포트 (기본: 8080)   |
| `HOMER_PORT`        |    No    | 컨테이너 내부 포트 (기본: 8080) |

## Change Impact

- `config.yml`의 구문 오류는 대시보드 전체 로딩 실패를 유발한다.
- 서비스 URL 변경 시 Traefik 라우팅 설정과 동기화되어야 한다.

## Related References

- **Guide**: [Dashboard Management Guide](../../../docs/07.guides/11-laboratory/dashboard.md)
- **Operation**: [Laboratory Operations Policy](../../../docs/08.operations/11-laboratory/dashboard.md)
- **Runbook**: [Dashboard Recovery Runbook](../../../docs/09.runbooks/11-laboratory/dashboard.md)
- **Official**: [Homer Documentation](https://github.com/bastienwirtz/homer)
