<!-- Target: docs/08.operations/11-laboratory-operational-policy.md -->

# Operational Policy - 11-laboratory

## Overview (KR)
이 문서는 관리 도구(Laboratory Tier)의 안정적인 운영과 보안을 위한 가이드라인 및 정책을 정의한다.

## Access Policy

- **Authentication**: 모든 서비스는 반드시 Traefik `sso-auth` 미들웨어를 경유해야 한다.
- **Role**: 관리 도구 접근 권한은 `admin` 그룹 사용자에게만 제한적으로 부여한다.

## Service Management

- **Homer config**: 신규 서비스 추가 시 `infra/11-laboratory/dashboard/config/config.yml`을 최신화하여 대시보드 정합성을 유지한다.
- **Portainer updates**: 보안 취약점 방지를 위해 Portainer CE 이미지를 주기적으로 최신 STS 버전으로 업데이트한다.
- **RedisInsight**: 대량의 데이터 조회 시 Redis 클러스터 성능에 영향을 주지 않도록 주의하여 사용한다.

## Data Persistence

- **Backup**: `/var/lib/portainer` 및 `/var/lib/redisinsight` 볼륨은 시스템 전체 백업 주기와 동일하게 관리한다.
- **Ephemeral State**: Homer 대시보드는 Stateless하게 설계되었으므로 별도의 백업 없이 설정 파일만 버전 관리한다.
