---
title: "Supabase Operations Policy"
version: "1.0.7"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0029"
parent_ids:
- "AD-0004"
created: "2026-05-17"
---

# Supabase Operations Policy

## Overview

이 정책은 `infra/04-data/supabase`의 exact `supabase` profile stack 운영 기준을 정의한다. 핵심 통제는 Kong 중심 공개 접근, Docker Secrets, `${DEFAULT_DATA_DIR}/supabase/...` runtime mounts와 database/storage/config를 하나의 recovery unit으로 관리하는 것이다.

## Scope

- **Systems**: `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, `functions`, `analytics`, `db`, `vector`, `supavisor`
- **Configs**: `infra/04-data/supabase/docker-compose.yml`, `${DEFAULT_DATA_DIR}/supabase/api/kong.yml`, storage, functions, logs, database init SQL, pooler config
- **Networks**: `supabase_net`
- **Ports**: Kong `8000`/`8443`, analytics `4000`, Supavisor session `5432`, transaction `6543`, 모두 Compose host-port 변수로 `127.0.0.1`에만 게시한다

## Rules

- **Required**:
  - Supabase secret은 `/run/secrets/`의 Docker Secrets로 공급하고 실제 image가 secret을 소비하는 안전한 방법을 검증해야 한다. 현재 `_FILE` 선언만 있고 generic 변환 wrapper가 없어 전체 수용은 미검증이다. process health나 file mount만으로 통제 충족을 인정하지 않는다.
  - Public API와 dashboard 접근은 compose에 선언된 Kong route와 연결된 stack
    config를 따라야 한다.
  - 문서는 현재 compose 파일에서 Studio가 direct host port를 갖지 않는다고
    명시해야 한다.
  - `${DEFAULT_DATA_DIR}/supabase/...` 아래 runtime mount는 구현 state로
    다루고 infra README 및 운영 문서와 동기화해야 한다.
  - JWT, anon, service-role, dashboard, SMTP, database, vault, crypto key 값은
    문서나 evidence에 절대 기록해서는 안 된다.
  - Backup 세트는 PostgreSQL globals/role, schema, data; Storage metadata와
    객체 파일; mount된 Kong/functions/pooler 구성; 보호된 Auth/JWT/SMTP/provider
    설정을 version, checksum, retention, restore evidence와 함께 포함해야
    한다.
  - Restore rehearsal은 새 isolated stack을 사용해야 한다. 의존성 순서대로
    role/schema/data를 복원하고, Storage 객체를 metadata와 조정하며,
    구성/secret을 별도로 적용하고, Auth, REST, Realtime, Storage, Functions,
    pooler 경로를 검증한다.
  - Update guide의 구성 backup은 database나 Storage backup이 아니다.
    Upgrade/removal은 일관된 restore-tested 세트, 호환성 검토, 용량 확인,
    명시적 승인을 요구한다.
- **Allowed**:
  - `docker compose ... config --quiet`를 사용한 metadata-only compose 검증.
  - Secret 값을 노출하지 않는 read-only 서비스 health/log 확인.
  - Task/incident evidence와 해당 runbook 단계로 뒷받침되는 승인된 JWT나
    dashboard credential rotation.
  - 선언된 `SUPABASE_KONG_HTTP_HOST_PORT`와 `SUPABASE_KONG_HTTPS_HOST_PORT`
    변수를 사용한, `127.0.0.1`로 제한된 Kong host-port 접근.
- **Disallowed**:
  - 게시되지 않은 local host port를 통한 direct Studio 접근을 가정하는 것.
  - 승인된 구현과 문서 갱신 없이 public Supabase API 노출을 위해 Kong을
    우회하는 것.
  - Secret 값이 포함된 생성된 Kong config를 commit하는 것.
  - 문서 전용 조치로 파괴적 database restore, storage 삭제, credential
    rotation을 수행하는 것.

### Accountable lifecycle boundary

적용 identity: `analytics`, `auth`, `db`, `functions`, `imgproxy`, `kong`, `meta`, `realtime`, `rest`, `storage`, `studio`, `supavisor`, `vector`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

### SMTP 원본 소유권

- COMM-002와 공용 SMTP password 파일이 유일한 값 원본입니다. COMM-003은 값·경로
  없는 alias이며 별도 발급, 평문 복사, symlink/hardlink 원본을 유지하지 않습니다.
- Auth mount target은 기존 이름을 유지하며 다른 SMTP 소비자·username·host·account는
  SMTP01에서 변경하지 않습니다. 직접 값과 파일 입력이 겹치거나 파일을 읽지 못하면
  Auth wrapper는 시작을 거부합니다.
- 실행 프로세스 환경에 전달된 비밀번호의 관리자 접근 위험을 명시하며 값·hash·길이,
  private registry, 인증 로그를 공개 output이나 Git에 기록하지 않습니다.
- SEC01이 이미지 최신판·보안 업데이트를, SMTP01이 소비 전환을, CLN01이 폐기 판정과
  실제 삭제를 소유합니다. 공통 source 병합과 HOME 배포는 총괄 통합 순서를 따릅니다.

## Exceptions

예외는 명시적인 owner나 user 승인을 요구하며, scope, command, 영향받는
서비스, secret-safety 고려사항, 검증 output, rollback/escalation state를
관련 task나 incident evidence에 기록해야 한다.

### Verification

- Compose 관련 문서를 변경한 뒤 `docker compose --profile supabase config --quiet`를 실행한다.
- 정책, guide, runbook, README, 링크 갱신 후 `python3 scripts/validation/check-document-links.py --mode all`을 실행한다.
- Commit 전에 갱신된 문서에서 direct Studio host-port 가정, 오래된 Compose CLI
  표기, template copyright 잔여물, secret 자료를 검색한다.

### Review Cadence

Supabase compose 서비스, port, profile, network, secret 참조, runtime mount,
Kong routing, 연결된 운영 문서에 대한 모든 변경 시 검토한다. 그 외에는 정기
Stage 05 운영 audit 동안 검토한다.

### Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](../guides/0029-supabase.md) (`GDE-0029`), [Runbook](../runbooks/0029-supabase.md) (`RUN-0029`)

## Related Documents

- [Compose implementation: infra/04-data/supabase/docker-compose.yml](../../../infra/04-data/supabase/docker-compose.yml)

- [Supabase self-hosted restore guidance](https://supabase.com/docs/guides/self-hosting/restore-from-platform)
- [Supabase self-hosted update guidance](https://supabase.com/docs/guides/self-hosting/updating)
- [Supabase source and licenses](https://github.com/supabase/supabase)

- [Operations index](../README.md)
- [Usage guide](../guides/0029-supabase.md)
- [Recovery runbook](../runbooks/0029-supabase.md)
- [Infrastructure service README](../../../infra/04-data/supabase/README.md)
