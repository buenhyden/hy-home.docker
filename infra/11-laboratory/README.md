# 11-laboratory

> Experimental services, management UIs, and administrative dashboards.

## Overview

`11-laboratory` 티어는 시스템 관리, 리소스 모니터링 및 실험적 서비스들을 위한 샌드박스 환경을 제공한다. 이 티어에 배치된 서비스들은 주로 운영자와 개발자를 위한 도구이며, Traefik을 통해 안전하게 노출된다.

## Audience

이 README의 주요 독자:

- Operators (시스템 관리 및 도구 운영)
- Developers (데이터베이스 및 컨테이너 리소스 조회)
- AI Agents (인프라 구조 분석 및 가이드 제공)

## Scope

### In Scope

- 컨테이너 관리 도구 (Portainer)
- 데이터베이스 관리 인터페이스 (RedisInsight)
- 통합 서비스 대시보드 (Homer)
- 해당 서비스들의 Traefik 라우팅 및 볼륨 구성

### Out of Scope

- 프로덕션 비즈니스 로직 서비스
- 핵심 인증 인프라 (02-auth 담당)
- 로그 및 메트릭 수집 파이프라인 (06-observability 담당)

## Structure

```text
11-laboratory/
├── dashboard/       # Homer-based service navigation dashboard
├── portainer/       # Docker & Environment management UI
├── redisinsight/    # Redis GUI and analysis tool
└── README.md        # This file
```

## How to Work in This Area

1. 서비스 배포: 각 하위 폴더의 `docker-compose.yml`을 사용하여 독립적으로 또는 전체를 배포할 수 있다.
2. 대시보드 갱신: 신규 인프라 서비스 추가 시 `dashboard/config/config.yml`을 업데이트하여 접근성을 유지한다.
3. 보안 적용: 모든 서비스는 Traefik의 `sso-auth` 미들웨어를 통해 보호되어야 한다.

## Related References

- **Parent**: [infra/README.md](../README.md)
- **Guide**: [docs/07.guides/11-laboratory/README.md](../../docs/07.guides/11-laboratory/README.md)
- **Operation**: [docs/08.operations/11-laboratory/README.md](../../docs/08.operations/11-laboratory/README.md)
- **Runbook**: [docs/09.runbooks/11-laboratory/README.md](../../docs/09.runbooks/11-laboratory/README.md)
