<!-- Target: docs/09.runbooks/11-laboratory-maintenance-runbook.md -->

# Maintenance Runbook - 11-laboratory

## Overview (KR)
이 문서는 `11-laboratory` 티어 유지보수 및 장애 발생 시 조치 절차를 정의한다.

## Routine Maintenance

### 1. 서비스 재시작
```bash
# 전체 관리 도구 재시작
docker compose -f infra/11-laboratory/dashboard/docker-compose.yml restart
docker compose -f infra/11-laboratory/portainer/docker-compose.yml restart
docker compose -f infra/11-laboratory/redisinsight/docker-compose.yml restart
```

### 2. 대시보드 설정 갱신
```bash
# config.yml 수정 후 컨테이너 재시작 없이 반영 (Homer 특성)
cp infra/11-laboratory/dashboard/config/config.yml.new infra/11-laboratory/dashboard/config/config.yml
```

## Emergency Procedures

### Case 1: Portainer 로그인 불가 (SSO 오류)
- **증상**: SSO 인증 후 Portainer 대시보드로 진입하지 못함.
- **조치**:
    1. Keycloak 서버 생존 여부 확인.
    2. Traefik 로그에서 미들웨어 인증 실패 이유 확인.
    3. 필요 시 `env.template`의 SSO 설정 값 재입력.

### Case 2: RedisInsight 연결 실패
- **증상**: 데이터베이스 노드 접근 불가.
- **조치**:
    1. `infra_net` 가상 네트워크에 RedisInsight 컨테이너가 포함되어 있는지 확인.
    2. Redis 노드의 호스트 명칭(예: `redis-node-1`)이 올바른지 확인.

## Backup & Restore
- **Backup**: `docker compose down` 후 볼륨 바인드된 디렉토리를 압축하여 보관.
- **Restore**: 압축 해제 후 `docker compose up -d` 재실행.
