# Management Database (mng-db) Runbook

: Infrastructure Recovery and Maintenance

---

## Overview (KR)

이 런북은 `mng-db` (Management Database)의 가동, 초기화, 건강 상태 점검 및 긴급 복구 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 명령어와 검증 단계를 제공한다.

## Purpose

`mng-db` 서비스의 부재로 인해 상위 관리 서비스(auth, automation 등)가 기동되지 않을 때의 복구 및 사후 관리를 목적으로 한다.

## Canonical References

- **ARD**: [../02.ard/0004-data-architecture.md](../../../02.ard/0004-data-architecture.md)
- **Spec**: [../04.specs/04-data/spec.md](../../../04.specs/04-data/spec.md)
- **Repo**: `infra/04-data/operational/mng-db/`

## When to Use

- 초기 플랫폼 설치 및 부트스트랩 시
- 관리용 DB 또는 캐시 서비스의 불능(unhealthy) 상태 발생 시
- 신규 플랫폼 서비스 추가로 인한 DB 초기화(`mng-pg-init`)가 필요할 때

## Procedure or Checklist

### Checklist

- [ ] `infra_net` 네트워크가 생성되어 있는가?
- [ ] `/run/secrets/` 하위에 필수 비밀번호 파일들이 존재하는가?
- [ ] `${DEFAULT_MANAGEMENT_DIR}` 데이터 볼륨 경로 권한이 올바른가?

### Procedure

1. **서비스 가동**
   ```bash
   cd infra/04-data/operational/mng-db
   docker-compose up -d
   ```

2. **초기화 작업 강제 실행**
   기존에 생성되지 않은 DB 유저나 스키마를 동기화해야 하는 경우 `mng-pg-init`을 재실행한다.
   ```bash
   docker-compose run --rm mng-pg-init
   ```

3. **서비스 로그 감시**
   ```bash
   docker-compose logs -f mng-pg
   docker-compose logs -f mng-valkey
   ```

## Verification Steps

- [ ] `docker exec mng-pg pg_isready -h 127.0.0.1` 결과가 `accepting connections`인가?
- [ ] `docker exec mng-valkey valkey-cli -a <pass> ping` 결과가 `PONG`인가?
- [ ] Exporter 메트릭이 노출되는가? `curl localhost:9187/metrics`

## Observability and Evidence Sources

- **Signals**: Prometheus Alertmanager (DB Down), Grafana Dashboard (Management Health)
- **Evidence to Capture**: `docker-compose logs`, `pg_log`, `valkey` 스냅샷 상태

## Safe Rollback or Recovery Procedure

- [ ] 데이타 정합성 문제 발생 시 `${DEFAULT_MANAGEMENT_DIR}` 백업 스냅샷을 복원한다.
- [ ] 설정 오류 시 `git checkout`으로 `docker-compose.yml` 원복 후 재배포한다.

## Related Operational Documents

- **Operations Policy**: [../08.operations/04-data/operational/mng-db.md](../../../08.operations/04-data/operational/mng-db.md)
- **Guides**: [../07.guides/04-data/operational/mng-db.md](../../../07.guides/04-data/operational/mng-db.md)
