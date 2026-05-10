# 02-Auth OAuth2 Proxy Operations Policy

## Overview (KR)

이 문서는 `02-auth` OAuth2 Proxy 운영 정책을 정의한다. 시크릿 주입 경로, 세션/쿠키 표준, fail-closed 및 degraded-mode 운영 통제를 명시한다.

## Policy Scope

- `infra/02-auth/oauth2-proxy/docker-compose.yml`
- `infra/02-auth/oauth2-proxy/docker-entrypoint.sh`
- `infra/02-auth/oauth2-proxy/Dockerfile`
- `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg`

## Applies To

- **Systems**: OAuth2 Proxy ForwardAuth gateway
- **Agents**: Infra/DevOps/Ops agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - 서비스는 `template-infra-readonly-med`를 사용해야 한다.
  - 런타임 시크릿 주입은 엔트리포인트 스크립트에서 `/run/secrets` 파일로 처리한다.
  - 이미지 실행 계정은 non-root(`oauth2proxy`)여야 한다.
  - 세션 정책은 `cookie_secure=true`, `cookie_httponly=true`, `cookie_samesite=lax`, `cookie_refresh=1h`, `cookie_expire=12h`를 유지한다.
  - 기본 운영 모드는 fail-closed다.
- **Allowed**:
  - 운영 승인 하에 degraded-mode를 제한적으로 수행(원복 절차 필수)
  - 환경별 도메인 변수(`DEFAULT_URL`) 조정
- **Disallowed**:
  - fail-open 상시 운영
  - 시크릿을 Compose/문서에 평문으로 저장

## Exceptions

- OIDC 공급자 장애가 장기화될 때 한시적 degraded-mode 허용 가능.
- 단, 승인자 기록과 종료 조건(원복 기준)을 사전에 명시해야 한다.

## Verification

- `bash scripts/check-auth-hardening.sh`
- `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml config`
- `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping`

## Review Cadence

- 월 1회 정기 점검
- OAuth2 Proxy/Keycloak 버전 변경 시 수시 점검

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: auth-hardening 스크립트 실패 0건
- **Log / Trace Retention**: 인증 요청/에러 로그는 관측성 보존 정책 준수
- **Safety Incident Thresholds**: 로그인 루프, 콜백 실패 급증, `/ping` 실패 지속 시 런북 수행

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- **Task**: [../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- **Spec**: [../../04.specs/02-auth/spec.md](../../04.specs/02-auth/spec.md)
- **Procedure**: [../../07.operations/02-auth/oauth2-proxy.md](../../07.operations/02-auth/oauth2-proxy.md)
- **Usage**: [../../07.operations/02-auth/oauth2-proxy.md](../../07.operations/02-auth/oauth2-proxy.md)

## Usage

> Migrated from `docs/07.operations/02-auth/oauth2-proxy.md` during the 2026-05-10 operations taxonomy consolidation.

### 02-Auth OAuth2 Proxy Usage

#### Overview (KR)

이 문서는 OAuth2 Proxy를 `ForwardAuth` 표준으로 운영하는 방법을 설명한다. 시크릿 엔트리포인트 주입, non-root 실행, 도메인 파라미터화, 세션 정책 점검 절차를 포함한다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

#### Purpose

- 인증 프록시를 표준 하드닝 상태로 유지한다.
- 신규 서비스의 SSO 연동 시 회귀를 줄인다.

#### Prerequisites

- `infra/02-auth/keycloak` 정상 동작
- `infra/02-auth/oauth2-proxy` 구성 파일 접근
- `mng-valkey` 세션 저장소 준비

#### Step-by-step Instructions

1. Compose 런타임 계약 확인
   - `template-infra-readonly-med` 사용
   - command가 `--config /etc/oauth2-proxy.cfg`인지 확인
   - `OAUTH2_PROXY_OIDC_ISSUER_URL`, `OAUTH2_PROXY_REDIRECT_URL`, `OAUTH2_PROXY_COOKIE_DOMAINS`, `OAUTH2_PROXY_WHITELIST_DOMAINS` 확인
2. 엔트리포인트 시크릿 주입 확인
   - `docker-entrypoint.sh`에서 `oauth2_proxy_cookie_secret`, `oauth2_proxy_client_secret`, `mng_valkey_password`를 읽어 환경 변수에 export하는지 확인
3. 이미지 권한 모델 확인
   - Dockerfile의 `USER oauth2proxy:oauth2proxy` 적용 확인
4. 정적 검증
   - `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml config`
   - `bash scripts/check-auth-hardening.sh`

#### Common Pitfalls

- `DEFAULT_URL`과 Keycloak realm/callback 도메인 불일치
- 세션 비밀 변경 후 기존 쿠키 재사용으로 인한 인증 실패
- `/ping` 헬스체크 통과 전 트래픽 유입

#### Related Documents

- **Spec**: [../../04.specs/02-auth/spec.md](../../04.specs/02-auth/spec.md)
- **Operation**: [../../07.operations/02-auth/oauth2-proxy.md](../../07.operations/02-auth/oauth2-proxy.md)
- **Procedure**: [../../07.operations/02-auth/oauth2-proxy.md](../../07.operations/02-auth/oauth2-proxy.md)
- **Plan**: [../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)

## Procedure

> Migrated from `docs/07.operations/02-auth/oauth2-proxy.md` during the 2026-05-10 operations taxonomy consolidation.

### 02-Auth OAuth2 Proxy Procedure

: OAuth2 Proxy ForwardAuth Recovery

#### Overview (KR)

이 런북은 OAuth2 Proxy 인증 루프, OIDC 장애, readonly/tmpfs 관련 오류, 설정 검증 실패 상황에 대한 복구 절차를 정의한다.

#### Purpose

- 인증 경로 장애를 신속히 복구한다.
- degraded-mode 수행/종료를 통제한다.
- config lint 실패 시 안전하게 롤백한다.

#### Canonical References

- [Operations Policy](../../07.operations/02-auth/oauth2-proxy.md)
- [Plan](../../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)

#### When to Use

- 로그인 루프(무한 redirect)
- OIDC issuer 접근 실패
- `/ping` healthcheck 실패
- readonly/tmpfs 관련 쓰기 오류
- compose/config 변경 후 런타임 부팅 실패

#### Procedure or Checklist

##### Checklist

- [ ] `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml config` 성공
- [ ] `bash scripts/check-auth-hardening.sh` 실행
- [ ] `docker logs oauth2-proxy --tail=200` 오류 패턴 확인

##### Procedure

1. 기본 진단
   - `/ping` 확인: `docker exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping`
   - OIDC issuer 확인: `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`
2. 로그인 루프 대응
   - `OAUTH2_PROXY_COOKIE_DOMAINS`, `OAUTH2_PROXY_WHITELIST_DOMAINS`, `redirect_url` 정합성 확인
   - `cookie_secure=true` 환경에서 HTTPS 진입 여부 확인
3. readonly/tmpfs 장애 복구
   - 쓰기 대상 경로가 `/tmp`, `/run` 내인지 점검
   - 엔트리포인트/인증서 마운트 경로 권한 확인
4. degraded-mode 절차(승인 필요)
   - OIDC 장기 장애 시 운영 승인 후 제한적 degraded-mode 적용
   - 적용 시간/범위/종료 조건을 티켓에 기록
   - Keycloak 정상화 즉시 기본 fail-closed로 복귀
5. config lint 실패 롤백
   - 직전 정상 커밋으로 compose/config 복원
   - 재기동 후 `/ping` 및 인증 플로우 재검증

#### Verification Steps

- [ ] `bash scripts/check-auth-hardening.sh` 통과
- [ ] `docker exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping` 성공
- [ ] 인증 콜백(`/oauth2/callback`) 정상 동작

#### Observability and Evidence Sources

- **Signals**: `/ping`, oauth2-proxy 로그, Keycloak 연결 오류율
- **Evidence to Capture**:
  - `docker logs oauth2-proxy --tail=200`
  - `docker logs keycloak --tail=200`
  - auth-hardening 스크립트 출력

#### Safe Rollback or Recovery Procedure

- [ ] 아래 파일을 직전 정상 커밋으로 복원
  - `infra/02-auth/oauth2-proxy/docker-compose.yml`
  - `infra/02-auth/oauth2-proxy/docker-entrypoint.sh`
  - `infra/02-auth/oauth2-proxy/Dockerfile`
  - `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg`
- [ ] `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml up -d oauth2-proxy`
- [ ] `/ping` + 로그인 시나리오 재검증

#### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: `bash scripts/check-auth-hardening.sh`
- **Trace Capture**: oauth2-proxy/keycloak 로그 + CI job 로그

#### Related Operational Documents

- **Usage**: [../../07.operations/02-auth/oauth2-proxy.md](../../07.operations/02-auth/oauth2-proxy.md)
- **Keycloak Procedure**: [./keycloak.md](./keycloak.md)
