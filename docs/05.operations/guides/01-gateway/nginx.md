# 01-Gateway Nginx Operations Policy

## Overview (KR)

이 문서는 `01-gateway`의 Nginx 운영 정책을 정의한다. Nginx는 특수 경로(`/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/`) 프록시 역할을 수행하며, `Balanced` 하드닝 기준을 준수한다.

## Policy Scope

- `infra/01-gateway/nginx/docker-compose.yml`
- `infra/01-gateway/nginx/config/nginx.conf`
- Nginx healthcheck/readonly/tmpfs 운영 표준

## Applies To

- **Systems**: Nginx gateway proxy
- **Agents**: Infra/DevOps/Ops agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - Nginx 서비스는 `template-infra-readonly-low`를 사용해야 한다.
  - 필수 `tmpfs`: `/var/cache/nginx`, `/var/log/nginx`, `/var/run`
  - healthcheck는 `/ping` 경로를 사용해야 한다.
  - `server_tokens off;`를 유지해야 한다.
  - `proxy_connect_timeout`, `proxy_send_timeout`, `proxy_read_timeout`을 명시해야 한다.
  - 업스트림 서버는 `max_fails`, `fail_timeout` 정책을 명시해야 한다.
  - `proxy_next_upstream` 정책을 명시해야 한다.
  - 정적 자산 확장자 기반 캐시 정책(`expires`, `Cache-Control`)을 유지해야 한다.
- **Allowed**:
  - 서비스 특성(대용량 업로드/다운로드)에 따른 location 단위 timeout override
- **Disallowed**:
  - `/ping`, `/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/` 기본 흐름 훼손
  - readonly 환경에서 영구 쓰기 경로 의존 설정

## Exceptions

- 장애 대응 중 임시 timeout 완화 가능. 단, 원복 계획과 변경 로그를 남겨야 한다.

## Verification

- `bash scripts/check-gateway-hardening.sh`
- `docker compose -f infra/01-gateway/nginx/docker-compose.yml config`
- `docker compose -f infra/01-gateway/nginx/docker-compose.yml exec nginx nginx -t`

## Review Cadence

- 월 1회 정기 점검
- nginx.conf 변경 시 수시 점검

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: gateway-hardening 스크립트 실패 0건
- **Log / Trace Retention**: nginx access/error 로그는 observability 정책 준수
- **Safety Incident Thresholds**: `/ping` 실패, 반복 5xx 증가, 인증 루프 발생 시 런북 절차 수행

## Related Documents

- **Plan**: [../../04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- **Task**: [../../04.execution/tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)
- **Procedure**: [../../05.operations/01-gateway/nginx.md](./nginx.md)
- **Usage**: [../../05.operations/01-gateway/nginx.md](./nginx.md)

## Usage

> Migrated from `docs/05.operations/01-gateway/nginx.md` during the 2026-05-10 operations taxonomy consolidation.

### 01-Gateway Nginx Usage

#### Overview (KR)

이 문서는 01-gateway의 Nginx 특수 경로 프록시 구성과 하드닝 포인트를 설명한다. readonly/tmpfs 운영, timeout/failover, 정적 캐시 정책의 의도를 중심으로 다룬다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

#### Purpose

- Nginx를 `template-infra-readonly-low` 기반으로 안정적으로 운영한다.
- `/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/` 경로 흐름을 유지하면서 하드닝 변경을 적용한다.

#### Prerequisites

- Docker/Docker Compose 사용 가능
- `infra/01-gateway/nginx` 구성 파일 접근 가능
- `scripts/check-gateway-hardening.sh` 실행 가능

#### Step-by-step Instructions

1. Compose 하드닝 확인
   - `infra/01-gateway/nginx/docker-compose.yml`
   - readonly 템플릿/필수 tmpfs/`/ping` healthcheck 존재 확인
2. Nginx config 하드닝 확인
   - `infra/01-gateway/nginx/config/nginx.conf`
   - `server_tokens off`, timeout 3종, `proxy_next_upstream`, upstream `max_fails/fail_timeout`, 정적 캐시 location 확인
3. 설정 검증
   - `docker compose -f infra/01-gateway/nginx/docker-compose.yml exec nginx nginx -t`
4. 하드닝 검증
   - `bash scripts/check-gateway-hardening.sh`

#### Common Pitfalls

- readonly 전환 후 `/var/cache/nginx`/`/var/log/nginx`/`/var/run` tmpfs 누락
- `proxy_pass` trailing slash 처리 실수로 경로 재작성 오류
- timeout 전역값/특정 location override 충돌

#### Related Documents

- **Spec**: [../../03.specs/01-gateway/spec.md](../../../03.specs/01-gateway/spec.md)
- **Operation**: [../../05.operations/01-gateway/nginx.md](./nginx.md)
- **Procedure**: [../../05.operations/01-gateway/nginx.md](./nginx.md)
- **Plan**: [../../04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md)

## Procedure

> Migrated from `docs/05.operations/01-gateway/nginx.md` during the 2026-05-10 operations taxonomy consolidation.

### 01-Gateway Nginx Procedure

: Nginx Special-path Proxy Recovery

#### Overview (KR)

이 런북은 Nginx readonly/tmpfs 전환 이후 발생 가능한 장애, `nginx -t` 실패, `/ping` 헬스체크 실패 상황의 복구 절차를 정의한다.

#### Purpose

- readonly/tmpfs 운영 안정성 확보
- config lint 실패 시 안전 롤백
- 특수 경로 프록시(`/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/`) 정상성 회복

#### Canonical References

- [Operations Policy](./nginx.md)
- [Plan](../../../04.execution/plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)

#### When to Use

- `nginx -t` 실패
- `/ping` healthcheck 반복 실패
- readonly 전환 후 캐시/로그/PID 쓰기 오류
- 백엔드 장애 전환(failover) 동작 이상

#### Procedure or Checklist

##### Checklist

- [ ] `docker compose -f infra/01-gateway/nginx/docker-compose.yml config` 성공
- [ ] `bash scripts/check-gateway-hardening.sh` 실행
- [ ] `docker compose -f infra/01-gateway/nginx/docker-compose.yml ps` 상태 확인

##### Procedure

1. 설정 검증
   - `bash scripts/check-gateway-hardening.sh`
   - `docker compose -f infra/01-gateway/nginx/docker-compose.yml exec nginx nginx -t`
2. readonly/tmpfs 장애 복구
   - compose에 아래 tmpfs 3개가 있는지 확인:
     - `/var/cache/nginx`
     - `/var/log/nginx`
     - `/var/run`
   - 누락 시 compose 수정 후 재기동:
     - `docker compose -f infra/01-gateway/nginx/docker-compose.yml up -d nginx`
3. config lint 실패 대응
   - 실패 로그에서 오류 지점 수정
   - `nginx -t` 재통과 확인 후 `nginx -s reload` 또는 재기동
4. 특수 경로 정상성 확인
   - `/ping` 200 응답
   - `/oauth2/`, `/keycloak/`, `/minio/`, `/minio-console/` 경로 응답 확인
5. failover 정책 확인
   - `proxy_next_upstream` 정책/업스트림 `max_fails`, `fail_timeout` 존재 확인

#### Verification Steps

- [ ] `docker compose -f infra/01-gateway/nginx/docker-compose.yml exec nginx nginx -t` 통과
- [ ] `/ping` 200
- [ ] 인증 플로우 정상 동작 (`/oauth2/`)
- [ ] 하드닝 검증 스크립트 통과

#### Observability and Evidence Sources

- **Signals**: nginx healthcheck, 4xx/5xx 비율, upstream error 로그
- **Evidence to Capture**:
  - `docker compose -f infra/01-gateway/nginx/docker-compose.yml logs --tail=200 nginx`
  - `nginx -t` 결과

#### Safe Rollback or Recovery Procedure

- [ ] 직전 정상 커밋으로 아래 파일 복원
  - `infra/01-gateway/nginx/docker-compose.yml`
  - `infra/01-gateway/nginx/config/nginx.conf`
- [ ] `docker compose -f infra/01-gateway/nginx/docker-compose.yml up -d nginx`
- [ ] `nginx -t` 및 `/ping` 재검증

#### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: `bash scripts/check-gateway-hardening.sh`
- **Trace Capture**: nginx logs + CI job logs

#### Related Operational Documents

- **Usage**: [../../05.operations/01-gateway/nginx.md](./nginx.md)
- **Traefik Procedure**: [./traefik.md](./traefik.md)
