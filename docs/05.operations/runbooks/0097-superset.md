---
title: "Superset Runbook"
version: "1.0.4"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "RUN-0097"
parent_ids:
- "GDE-0097"
created: "2026-09-23"
---

# Superset Runbook

## When to Use

최초 설정, 로그인 실패, 웹 서버가 healthy 상태가 되지 않을 때, 또는 업그레이드할 때 사용한다.

### Execution and stop boundary

대상: `superset-db-provision`, `superset-init`, `superset`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

1. 최초 설정(각 단계는 승인을 받으며, 값은 로그나 문서에 절대 남기지 않는다):
   1. Keycloak realm `hy-home.realm`: standard flow만 사용하고 PKCE `S256`,
      redirect URI `https://superset.${DEFAULT_URL}/oauth-authorized/keycloak`,
      web origin `https://superset.${DEFAULT_URL}`을 설정해 confidential
      client `home-superset`를 생성한다.
   2. 해당 client secret을 `secrets/auth/superset/superset_oidc_client_secret.txt`로
      저장한다(IAM-013, 한 줄, 모드 `0640`).
   3. `bash scripts/operations/gen-secrets.sh --sync-metadata`를 실행한 다음
      `bash scripts/operations/gen-secrets.sh`를 실행해 PG-028과 AUTO-020을
      생성한다.
   4. `docker compose --profile bi build superset`를 실행한 다음
      `docker compose --profile bi up -d superset`를 실행한다.
   5. 최초 Admin은 named OIDC identity와 FAB username mapping을 먼저 확인한다. 비공개 TTY에서 `docker compose --profile bi exec superset superset fab create-admin`의 interactive identity/password/confirmation prompt를 사용한다. 승인된 password manager의 강한 값을 masked prompt에만 입력하고 custody한다. `--password`, shell substitution, 환경 변수, 터미널 출력/녹화·trace, stdin pipe와 `exec -T`는 금지한다. TTY/custody/정확한 identity가 없거나 prompt가 masking되지 않으면 중단한다. 폼 로그인 비활성화는 password hash를 비민감 정보로 만들지 않는다. 생성 후 named 사용자의 OIDC login과 Admin 권한만 별도 승인 검증하고 등록 Gamma 정책을 바꾸지 않는다.

2. 점검: `docker compose --profile bi logs --tail=100 superset-db-provision superset-init superset`.
3. `superset: secret … must be one non-empty line`: 지정된 secret 파일이
   비어 있거나 여러 줄로 되어 있다는 뜻이다.
4. 로그인이 오류와 함께 Superset으로 돌아오는 경우: Keycloak의 redirect URI와
   client secret을 확인한 다음, 컨테이너에서 `keycloak.${DEFAULT_URL}`이
   Traefik로 해석되는지, `${DEFAULT_CERT_DIR}/rootCA.pem`이 마운트되어
   있는지 확인한다.
5. 로그인한 사용자에게 데이터가 보이지 않는 경우: 해당 사용자는 `Gamma`
   역할이므로 Admin이 역할을 부여한다.
6. 업그레이드: 정확한 metadata backup, signing key custody, image/schema 호환성과 rollback을 승인받은 다음 재빌드한다. `docker compose --profile bi run --rm superset-init`을
   실행하고 `superset`을 재생성한다.

## Evidence

client ID, 역할 이름, Admin이 부여된 사용자 이름, exit code, 소스 커밋을
기록한다. secret, token, session cookie는 절대 기록하지 않는다.

## Rollback or Recovery

메타데이터는 공유 mng-pg의 physical pgBackRest set에 포함된다. 전체 set을 live로 복원하면 다른 모든 DB도 되돌리므로 Superset만의 rollback으로 실행하지 않는다. RUN-0021의 새 격리 target에서 호환 image로 복원·검증한 뒤 필요한 metadata DB의 logical extraction/cutover를 별도 승인한다. 암호화 connection을 읽는 원래 signing key를 별도 custody한다. 이전 image를 migrated DB에 즉시 연결하지 않는다. dashboard/dataset/role/연결과 OIDC 검증 전 승격하지 않으며 실패 target은 보존한다.

## Escalation

폼 로그인 활성화, 등록 시 `Admin` 부여, 호스트 포트 게시, 또는 환경 변수에
credential을 넣으라는 요청이 있으면 중단하고 @buenhyden에게 전달한다.

## Traceability

- [Guide](../guides/0097-superset.md) (`GDE-0097`)
- [Policy](../policies/0097-superset.md) (`POL-0097`)
- [Keycloak runbook](0014-keycloak.md)

## Related Documents

- [Superset package README](../../../infra/12-analytics/superset/README.md)
- [Superset Compose source](../../../infra/12-analytics/superset/docker-compose.yml) and [derived version projection](../../../infra/tech-stack.versions.json)
- [Backup and restore runbook](0021-backup-and-restore.md)
