---
title: "Superset Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0097"
parent_ids:
- "GDE-0097"
created: "2026-09-23"
---

# Superset Runbook

## When to Use

최초 설정, 로그인 실패, 웹 서버가 healthy 상태가 되지 않는 경우, 또는 업그레이드 시 사용한다.

## Procedure

1. 최초 설정(각 단계는 승인을 받으며, 값은 로그나 문서에 절대 남기지 않는다):
   1. Keycloak realm `hy-home.realm`: standard flow만 사용하고 PKCE `S256`,
      redirect URI `https://superset.${DEFAULT_URL}/oauth-authorized/keycloak`,
      web origin `https://superset.${DEFAULT_URL}`을 설정하여 confidential
      client `home-superset`를 생성한다.
   2. 해당 client secret을 `secrets/auth/superset_oidc_client_secret.txt`로
      저장한다(IAM-013, 한 줄, 모드 `0640`).
   3. `bash scripts/operations/gen-secrets.sh --sync-metadata`를 실행한 다음
      `bash scripts/operations/gen-secrets.sh`를 실행하여 PG-028과 AUTO-020을
      생성한다.
   4. `docker compose --profile bi build superset`를 실행한 다음
      `docker compose --profile bi up -d superset`를 실행한다.
   5. 관리자의 첫 로그인 전에 다음을 실행한다:
      `docker compose --profile bi exec superset superset fab create-admin --username <keycloak username> --firstname <first> --lastname <last> --email <email> --password "$(openssl rand -base64 24)"`.
      생성된 비밀번호는 사용할 수 없으며(폼 로그인이 없다) 보관하지 않는다;
      OIDC가 사용자 이름을 매칭한다.
2. 점검: `docker compose --profile bi logs --tail=100 superset-db-provision superset-init superset`.
3. `superset: secret … must be one non-empty line`: 지정된 secret 파일이
   비어 있거나 여러 줄로 되어 있다는 뜻이다.
4. 로그인이 오류와 함께 Superset으로 돌아오는 경우: Keycloak의 redirect URI와
   client secret을 확인한 다음, 컨테이너에서 `keycloak.${DEFAULT_URL}`이
   Traefik로 해석되는지와 `${DEFAULT_CERT_DIR}/rootCA.pem`이 마운트되어
   있는지 확인한다.
5. 로그인한 사용자에게 데이터가 보이지 않는 경우: 해당 사용자가 `Gamma`
   역할이므로 Admin이 역할을 부여한다.
6. 업그레이드: 재빌드한 다음 `docker compose --profile bi run --rm superset-init`을
   실행하고 `superset`을 재생성한다.

## Evidence

client ID, 역할 이름, Admin이 부여된 사용자 이름, exit code, 소스 커밋을
기록한다; secret, token, session cookie는 절대 기록하지 않는다.

## Rollback or Recovery

메타데이터 데이터베이스는 `mng-pg` pgBackRest 세트(RUN-0021)에 포함된다.
업그레이드 전에 백업을 수행한다; 마이그레이션이 실패하면 백업을 복원하고
이전 이미지를 기동하여 복구한다.

## Escalation

폼 로그인 활성화, 등록 시 `Admin` 부여, 호스트 포트 게시, 또는 환경 변수에
credential을 넣으라는 요청이 있으면 중단한다.

## Traceability

- [Guide](../guides/0097-superset.md) (`GDE-0097`)
- [Policy](../policies/0097-superset.md) (`POL-0097`)
- [Keycloak runbook](0014-keycloak.md)

## Related Documents

- [Superset package README](../../../infra/04-data/analytics/superset/README.md)
- [Superset Compose source](../../../infra/04-data/analytics/superset/docker-compose.yml) and [derived version projection](../../../infra/tech-stack.versions.json)
- [Backup and restore runbook](0021-backup-and-restore.md)
