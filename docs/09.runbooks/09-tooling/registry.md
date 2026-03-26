<!-- Target: docs/09.runbooks/09-tooling/registry.md -->

# Docker Registry Runbook

: Internal Image Distribution Service

---

## Overview (KR)

이 런북은 `hy-home.docker` 도커 레지스트리 서비스의 유지보수 및 장애 복구 실행 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 단계와 검증 기준을 제공한다.

## Purpose

- 레지스트리 서비스의 비정상 종료 시 신속한 복구.
- 저장 공간 부족 시 가비지 컬렉션(GC)을 통한 용량 확보.
- CI/CD 파이프라인의 이미지 푸시/풀 장애 해결.

## Canonical References

- [infra/09-tooling/registry/README.md](../../../infra/09-tooling/registry/README.md)
- [../08.operations/09-tooling/registry.md](../08.operations/09-tooling/registry.md)

## When to Use

- 레지스트리 서비스가 응답하지 않을 때 (503 Service Unavailable).
- 이미지 푸시 중 "no space left on device" 에러 발생 시.
- 권한 문제로 인해 이미지를 업로드하거나 내려받을 수 없을 때.

## Procedure or Checklist

### Checklist

- [ ] 레지스트리 서비스 프로세스(컨테이너) 생존 확인.
- [ ] 호스트 디스크 여유 공간 확인 (`df -h`).
- [ ] Docker 데몬의 `insecure-registries` 설정 확인.

### Procedure

#### 1. Service Restart

레지스트리가 응답하지 않는 경우 컨테이너 상태를 확인하고 재시작한다.

1. **상태 확인**: `docker ps | grep registry`
2. **재시작**: `docker compose -f infra/09-tooling/registry/docker-compose.yml restart`

#### 2. Garbage Collection (GC)

참조되지 않는 레이어를 삭제하여 디스크 공간을 확보한다.

1. **Dry-run (검사)**:

   ```bash
   docker exec registry bin/registry garbage-collect --dry-run /etc/docker/registry/config.yml
   ```

2. **정식 실행**:

   ```bash
   docker exec registry bin/registry garbage-collect /etc/docker/registry/config.yml
   ```

   *주의: 실행 중에는 푸시 작업을 중단하는 것이 권장됨.*

#### 3. Auth/Connectivity Check

인증 또는 연결 문제가 의심되는 경우 다음을 수행한다.

1. **데몬 설정 확인**: `/etc/docker/daemon.json`에 `insecure-registries`가 포함되어 있는지 확인.
2. **로그인 재시도**:

   ```bash
   docker login registry.hy-home.docker:5000
   ```

## Verification Steps

- [ ] `curl -I http://registry.hy-home.docker:5000/v2/` 명령어로 `200 OK` 응답 확인.
- [ ] 테스트 이미지 푸시: `docker push registry.hy-home.docker:5000/test/hello-world:latest`

## Observability and Evidence Sources

- **Signals**: Grafana Alert (Registry Container Down), Storage Alert (>90%).
- **Evidence to Capture**: `docker logs registry`, `df -h ${DEFAULT_REGISTRY_DIR}`.

## Safe Rollback or Recovery Procedure

- 데이터 백업본이 있는 경우 `${DEFAULT_REGISTRY_DIR}` 경로를 복원하고 재시작한다.
- GC 작업 중 문제가 발생한 경우 레지스트리 설정을 원복하고 컨테이너를 재생성한다.

## Related Operational Documents

- **Operations Policy**: [../08.operations/09-tooling/registry.md](../08.operations/09-tooling/registry.md)
