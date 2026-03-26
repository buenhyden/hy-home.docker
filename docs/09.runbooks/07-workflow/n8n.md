# n8n Recovery Runbook

: Apache n8n (07-workflow)

---

## Overview (KR)

이 런북은 n8n 서비스 장애 발생 시 운영자가 신속하게 서비스를 복구하기 위한 단계별 절차를 제공한다. 워커 중단, 데이터베이스 연결 오류, 암호화 키 분실 등 주요 장애 시나리오에 대응한다.

## Purpose

- n8n 서비스의 가용성 조기 회복
- 자동화 워크플로우 중단 시간 최소화
- 시스템 정상 작동 여부 검증

## Canonical References

- ARD: [07-workflow Architecture](../../02.ard/0007-workflow-architecture.md)
- Guide: [n8n System Guide](../../07.guides/07-workflow/n8n.md)
- Policy: [n8n Operations Policy](../../08.operations/07-workflow/n8n.md)

## When to Use

- n8n UI 접근 시 "Connection lost" 또는 50x 에러가 발생할 때.
- 워크플로우가 실행되지 않고 `Pending` 또는 `Waiting` 상태에 멈춰 있을 때.
- 워커 컨테이너가 반복적으로 재시작(`Restarting`)될 때.

## Procedure or Checklist

### Checklist

- [ ] [ ] `docker compose ps` 결과 모든 n8n 서비스가 `Up` 인가?
- [ ] [ ] `n8n-valkey` 서비스가 정상이며 워커가 연결되어 있는가?
- [ ] [ ] `n8n_db_password` 시크릿이 올바르게 로드되었는가?

### Procedure

#### 시나리오 1: 워커 노드 중단 (Worker Down)

1. 워커 로그 확인: `docker compose logs --tail=50 n8n-worker`
2. 워커 재시작: `docker compose restart n8n-worker`
3. Valkey 큐 상태 확인: `docker compose exec n8n-valkey valkey-cli info keyspace`

#### 시나리오 2: 데이터베이스 연결 오류

1. DB 호스트(`POSTGRES_MNG_HOSTNAME`)가 가용한지 확인.
2. n8n 메인 서비스 재시작: `docker compose restart n8n`
3. 시크릿 파일 권한 확인: `docker compose exec n8n ls -l /run/secrets/n8n_db_password`

#### 시나리오 3: 텐서플로우/Task Runner 오류

1. Task Runner 로그 확인: `docker compose logs n8n-task-runner`
2. Task Runner 재시작: `docker compose restart n8n-task-runner`

## Verification Steps

- [ ] `https://n8n.${DEFAULT_URL}/healthz` 호출 시 `200 OK` 응답 확인.
- [ ] UI 로그인 후 `Executions` 탭에서 최근 작업의 성공 여부 확인.

## Observability and Evidence Sources

- **Signals**: Grafana n8n Dashboard (Error Rate), Valkey Queue Depth.
- **Evidence**: `docker compose logs --tail=100 n8n`, `n8n-worker`.

## Safe Rollback or Recovery Procedure

- [ ] 서비스를 재시작하기 전, `database` 볼륨의 데이터 유실 가능성이 낮으므로 안심하고 재시작을 시도하십시오.
- [ ] 만약 `N8N_ENCRYPTION_KEY`가 변경되어 이전 데이터 복호화가 불가능한 경우, 이전 키로 롤백하거나 자격 증명을 재설정해야 합니다.
