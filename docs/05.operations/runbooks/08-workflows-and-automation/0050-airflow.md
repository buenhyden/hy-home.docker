---
title: "Airflow Runbook"
version: "1.4.3"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-09"
layer: "operations"
artifact_id: "RUN-0050"
parent_ids:
- "GDE-0050"
created: "2026-05-17"
---

# Airflow Runbook

## Overview

이 런북은 Apache Airflow 서비스 장애 발생 시 운영자가 즉시 수행할 수 있는 복구 절차를 정의한다. 현재 서비스명은 Airflow 3의 `airflow-apiserver`를 기준으로 한다. broker는 공유 `mng-valkey`다(앱별 전용 Valkey는 ADR-0062 결정 10으로 제거됨).

> Scope: Apache Airflow (07-workflow)

- Airflow 서비스 가용성 즉각 복구
- 파이프라인 중단 시간 최소화
- 시스템 상태 검증 및 정상화 확인

## Trigger

- 태스크가 `Queued` 상태에서 장시간 머물러 있을 때.
- Web UI 접근 시 DB 연결 에러 또는 50x 에러가 발생할 때.
- 워커(Worker) 프로세스가 비정상 종료되거나 리소스 부족으로 경고가 발생할 때.
- Airflow UI 로그인, Keycloak token exchange, 또는 TLS verification이 실패할 때.
- Airflow token 또는 session이 노출되어 폐기해야 할 때.

## Prerequisites

### Service lifecycle prerequisites

처음 기동하거나 이미지를 바꾸기 전에 DB·broker, CA, DAG/plugin/config/log host 경로와 비root 쓰기 권한을 확인한다. `airflow-init`은 migration 가능한 root 일회성 작업이므로 DB backup·schema 계획 승인 뒤에만 실행한다. init은 chown이나 사용자 역할 배정을 하지 않는다. init 완료 뒤 API·scheduler·processor·triggerer, API 준비 뒤 worker·Flower가 요구하는 조건을 각각 검증한다. StatsD exporter도 init 완료에 의존하며 healthcheck는 `:9102/metrics` 응답만 확인하므로 이벤트가 생긴 뒤 metric을 확인한다. 전용 Valkey·exporter를 선택하면 RUN-0028의 broker backup·인증 절차를 적용하되 workflow 이력 복원으로 간주하지 않는다. 중지는 예약·입력을 먼저 차단하고 실행 작업의 외부 효과를 대조한 뒤 한다.

## Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](../01-common/0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](../10-platform-and-backup/0021-backup-and-restore.md), [image 변경](../10-platform-and-backup/0086-dependency-version-management.md), [시크릿](../04-security-and-secrets/0085-openbao.md), [계정](../03-identity-and-access/0014-keycloak.md), [gateway·인증서](../02-gateway-and-networking/0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### 사전 점검

- [ ] `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`가 통과하는가?
- [ ] `AIRFLOW_VALKEY_HOST`/`AIRFLOW_VALKEY_SECRET`의 선택 이름과 일치 여부를 확인했는가? Profile만으로 broker를 추정하지 않는다.
- [ ] 메타데이터 DB(PostgreSQL)가 정상 동작 중인가?
- [ ] `apache-airflow-providers-keycloak` 버전이 바뀌었다면
  [Authorization bootstrap](../../guides/03-identity-and-access/0079-application-auth-integration.md#authorization-bootstrap)의
  `create-permissions`를 다시 실행하고, 로그인한 사용자로 Pools, DAGs, Assets,
  HITL 화면이 `403` 없이 열리는지 확인했는가? (inc-2026-0002)

### 연결 주소와 Secret reader 계약

현재 소스의 metadata DB·Celery result backend·broker `_CMD`는 이미지 안의
`/opt/airflow/bin/connection_uri.py`를 호출한다. 비밀번호는 보호된 regular
file에서 최대 4096바이트로 읽으며 경로 symlink·불안정한 파일·허용하지 않는
권한·빈값을 거부한다. 단일행 UTF-8의 종단 LF 한 개만 파일 구분자로 제거하고
앞뒤 공백·리터럴 `%`·DB의 CR/TAB은 값으로 보존해 비밀번호 부분을 한 번만
인코딩한다. 중간 LF·NUL·잘못된 UTF-8은 거부하고 broker는 기존 ACL 계약대로
제어문자도 거부한다. 종단 LF를 실제 값으로 사용하는 자격은 이 reader의 지원
대상이 아니며 임의 trim이나 비밀 재발급으로 맞추지 않는다.

MNG PG는 `POSTGRES_PORT`, broker는 `VALKEY_PORT`를 사용한다. 지원되는
broker 쌍은 `mng-valkey`/`mng_valkey_password`뿐이며 다른 host와 secret을
조합하면 helper가 거부한다. DEV의 내부 listener `5432`와
호스트 공개 포트는 이 관리 연결과 별개다.

Helper의 성공 출력은 `_CMD` 소비용 연결 주소다. 단독 출력, 전체 config 목록,
연결값 조회나 디버그 출력을 증거로 수집하지 않는다. 실패 시 고정 오류와 종료
상태만 남기고 파일 참조·권한·선택 쌍·포트의 구조를 값 없이 확인한다. 소스의
회귀는 `python3 -m unittest tests.validation.test_airflow_connection_uri`로
합성 입력만 사용해 확인한다. 실제 mount 권한·새 이미지 빌드·운영 연결은 이
시험의 PASS와 별도다. 공급자 reader와 자격 계약 변경은 P02/P06에 인계한다.

이 소스 변경을 되돌릴 때에는 helper와 세 `_CMD` 설정을 같은 차분으로 되돌린다.
실제 이미지 교체·컨테이너 재생성은 drain·backup·복구 조건을 갖춘 별도 승인
대상이다. 로컬 revert가 운영 DB·자격·queue 상태를 복구한 것으로 기록하지 않는다.

### 시나리오 0: Keycloak 인증 또는 TLS 실패

1. `airflow-apiserver` 로그에서 auth manager, `401`, `403`, certificate 오류를
   확인한다. Secret 값 자체는 출력하지 않는다.
2. `KEYCLOAK_URL`, `KEYCLOAK_REALM`, `AIRFLOW_KEYCLOAK_CLIENT_ID`가 현재
   환경의 Keycloak client 설정과 일치하는지 값 노출 없이 확인한다.
3. `/run/secrets/airflow_keycloak_client_secret`(또는 `AIRFLOW_CLIENT_SECRET_FILE`이 가리키는 `/run/openbao/airflow` 아래 파일)와
   `/run/secrets/airflow_api_jwt_secret`가 컨테이너에 연결되어 있는지 경로만
   확인한다.
4. `${DEFAULT_CERT_DIR}/rootCA.pem` bind mount가 존재하고 API server가 임시
   CA bundle을 생성했는지 로그와 파일 존재 여부로 확인한다.
5. 이미지가 최신 Dockerfile 변경을 포함해야 하면 승인된 Compose build를
   수행하고, 이후 `airflow db check`와 UI 로그인 검증을 다시 실행한다.

### 시나리오 1: 태스크 지연 (Task stuck in Queued)

1. 증거 캡처:
   - `docker compose logs --tail=100 airflow-worker airflow-scheduler airflow-apiserver`
   - `docker compose exec airflow-worker df -h /opt/airflow/logs`
2. host/secret pair가 `mng-valkey`/`mng_valkey_password`인지 확인하고 [Valkey Runbook](../05-databases-and-storage/0028-management-database.md)의 값 비노출 인증 점검을 따른다. DB/broker가 준비되지 않으면 중단한다.
3. Celery worker 응답 확인: `docker compose exec airflow-apiserver celery --app airflow.providers.celery.executors.celery_executor.app inspect ping`. Remote control이 허용된 worker의 응답이 없으면 실패로 기록하고 원인을 먼저 진단한다.
4. 스케줄을 pause하고 실행/예약 태스크와 외부 부작용을 조정한 뒤 승인된 worker 재시작만 수행한다: `docker compose restart airflow-worker`. 자동 재실행이나 task clear를 복구 전제로 삼지 않는다.

5. Flower(`flower.${DEFAULT_URL}`) 또는 worker 로그에서 heartbeat 회복 여부를 확인한다.

### 시나리오 2: 메타데이터 DB 오류

1. DB 연결 정보 확인: `docker compose exec airflow-apiserver airflow db check`
2. 비밀번호/시크릿 로드 여부 확인: `/run/secrets/airflow_db_password` 파일 존재 여부 확인.
3. DB/secret 준비 문제가 남아 있으면 중단하고 소유자에게 넘긴다. 해당 준비가 회복되고 실행 작업의 외부 효과와 중단 영향이 승인된 경우에만 기존 설정의 서비스를 재시작한다: `docker compose restart airflow-apiserver airflow-scheduler`. Secret bind·환경변수·image 변경은 restart 대상이 아니며 R0085/R0086의 승인된 재생성 절차로 넘긴다.

### 시나리오 3: 관리자 계정 접근 복구

Native Keycloak Auth Manager의 계정과 역할 소유자는 Keycloak이다.
[RUN-0014](../03-identity-and-access/0014-keycloak.md)의 승인된 계정 복구 절차로 넘긴다.
FAB `airflow users reset-password`나 CLI 인자에 password를 넣는 방식은
이 구현에 적용하지 않는다. 복구 뒤 native login과 필요한 권한을 확인한다.
Permission bootstrap 완료만으로 사용자 역할이 부여되지는 않는다.

### 시나리오 4: 노출된 Airflow token/session 폐기

Keycloak으로 로그인한 UI는 Airflow 자체 JWT(`_token` cookie,
`airflow_api_jwt_secret`으로 서명)와 Keycloak access/refresh/id token cookie를
함께 쓴다. 아래 동작은 설치된 Airflow 3.3.1과 keycloak provider 0.9.0의 <!-- runtime-version-exception: history — SPEC-0193의 2026-09-30 장애·인증 검증에 적용된 버전 근거를 보존한다. -->
코드에서 확인했다. Keycloak session과 client secret은
[RUN-0014](../03-identity-and-access/0014-keycloak.md)의 "노출된 token/session 폐기" 단계가 다룬다.

1. 노출된 브라우저 session에 접근할 수 있으면 UI에서 Logout한다.
   `/api/v2/auth/logout`이 현재 Airflow JWT의 `jti`를 `revoked_token` table에
   기록한 뒤 Keycloak end-session으로 보내고, callback이 token cookie를 지운다.
   이 JWT는 만료 전이라도 거부된다.
2. token 사본이 따로 노출됐으면 로그아웃만으로는 부족하다. Airflow JWT는
   `[api_auth] jwt_expiration_time`(기본 86400초, 이 저장소는 값을 바꾸지
   않음)까지 유효하다. 모두 끊으려면 `airflow_api_jwt_secret`을 교체한다.
   - 실행 중인 task를 먼저 멈추거나 끝낸다. task execution token도 같은
     key로 서명되므로, 교체하면 실행 중인 task의 API 호출이 실패한다.
   - `secrets/automation/airflow/airflow_api_jwt_secret.txt`를 값 출력 없이 새 난수로
     교체하고 기존 소유자와 mode(`0640`)를 유지한다.
   - 이 secret을 읽는 `airflow-apiserver`, `airflow-scheduler`,
     `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`를 함께
     재생성한다. 파일을 바꾸기만 해서는 실행 중인 컨테이너에 반영되지 않는다.
   - 모든 사용자와 API client가 다시 로그인해야 한다.
3. 확인: 기존 cookie의 요청이 `401`을 받고, 새로 로그인하면 DAGs, Pools,
   Assets, HITL이 `403` 없이 열린다. 증거는 경로와 상태 코드만 남긴다.

### 시나리오 5: Opsflow 첫 HOME 설치 (D12)

상태: **계획됨·미실행**. 실행 기록과 미확정 owner 항목(O1–O8)은
[TSK-0051](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0051-opsflow-home-installation.md)이 소유한다.
승인된 운영자와 실행 창이 TSK-0051에 기록되기 전에는 어떤 단계도 시작하지 않는다.
각 단계는 앞 단계 검사가 PASS로 기록된 뒤에만 시작한다. 이미지는 바꾸지 않는다.

값은 placeholder로만 적는다. `<...>`는 운영자가 채우며 secret은 `secrets/` 아래 파일 경로로만
전달하고 argv·환경 변수 출력·로그에 값을 남기지 않는다. 공통 변수:
`W=infra/07-workflow/airflow/workloads/manifest-pipeline`, `REV=<검토한 commit>`,
`BK=<백업 디렉터리, O6>`.

1. **백업** (O6 필요)
   - 명령: 인증은 owner가 지정한 `secrets/` 아래 경로의 `PGPASSFILE`로만 한다(O6). 예:
     `docker exec -e PGPASSFILE=/run/secrets/<O6 파일> dev-pg pg_dump -U <dev-pg admin> -Fc opsflow_dev > "$BK/opsflow_dev.dump"`
     (DB가 없으면 "없음"을 기록하고 건너뛴다),
     `docker exec -e PGPASSFILE=/run/secrets/<O6 파일> mng-pg pg_dump -U <mng-pg admin> -Fc airflow > "$BK/airflow.dump"`,
     승인된 admin 자격으로 `opsflow-dev` 목록을 `"$BK/opsflow-dev.listing"`에 저장(bucket이 없으면 "없음" 기록),
     `(cd "$BK" && find . -maxdepth 1 -type f ! -name SHA256SUMS -exec sha256sum {} + > SHA256SUMS)`.
   - 기대 결과: 파일 크기가 0이 아니고 `SHA256SUMS`에 자기 자신을 뺀 모든 백업 파일이 기록된다.
   - 중단 조건: dump 실패, 크기 0, 디스크 부족.
   - Rollback: 없음(읽기 전용). 백업은 삭제하지 않는다.
2. **SQL 001·003·004·005·007 적용과 008 검사** (O1, O2, O8 필요)
   - HOME에서 실행하는 파일은 migration `001`, `003`, `004`, `005`, `007`과 검사 `008`뿐이다.
     `002_checks.sql`은 합성 행을 쓰고 rollback되지 않는 identity sequence를 증가시키며
     owner와 각 client로 SET ROLE하는 격리 감사 superuser를 요구하므로 폐기 가능한 격리 DB 전용이다.
     `006_checks.sql`도 격리 DB 전용이며 version 4 검사라 version 5의 최종 검사가 아니다.
     두 검사는 격리 rehearsal에 속하며 이 단계에서 실행하지 않는다.
   - 실행 위치: 아래 `psql -h dev-pg` 명령은 `dev-pg` 이름이 해석되는 Docker network 안(그 network에 붙인 일회성 psql 컨테이너 등)에서 실행한다. 호스트 셸에서는 해석되지 않는다.
   - Migration 명령: 각 파일 header가 요구하는 session_user=`opsflow_migrator`,
     current_user=`opsflow_owner`, DB=`opsflow_dev`로 실행한다. 예:
     `PGPASSFILE=<O1 경로> PGOPTIONS='-c role=opsflow_owner' psql -h dev-pg -d opsflow_dev -U opsflow_migrator -v ON_ERROR_STOP=1 -v migration_sha256=<값> -f <파일>`.
     파일마다 별도 session으로 실행한다.

     | 파일 | 실행 role | `migration_sha256` 값 |
     | --- | --- | --- |
     | `001_opsflow.sql` | migrator → owner | `001` 자신의 SHA-256 |
     | `003_business_date.sql` | migrator → owner | `003` 자신의 SHA-256 |
     | `004_notification_quarantine.sql` | migrator → owner | `004` 자신의 SHA-256 |
     | `005_data_version.sql` | migrator → owner | `005` 자신의 SHA-256 |
     | `007_notification_recovery.sql` | migrator → owner | `007` 자신의 SHA-256 |
     | `008_checks.sql` | 기존 감사 관리자(O8) | `007`의 SHA-256 |
     | (격리 전용) `002_checks.sql` | 격리 감사 superuser | 마지막 적용 migration: `001` 뒤 `001`, `003` 뒤 `003` |
     | (격리 전용) `006_checks.sql` | 격리 감사 관리자 | `005`의 SHA-256 |

   - 검사 명령: `PGPASSFILE=<O8 경로> psql -h dev-pg -d opsflow_dev -U <O8 감사 관리자> -v ON_ERROR_STOP=1 -v migration_sha256=<007 SHA-256> -f 008_checks.sql`.
     `008` header는 "approved isolated DB"를 요구하므로 HOME 실행은 O8에서 owner가 따로 승인해야 한다.
     `005`·`007` header의 "no HOME apply is authorized"도 O8 승인으로만 넘어선다.
   - 기대 결과: 다섯 migration이 각각 commit되고 `008`이 읽기 전용 transaction을 오류 없이 ROLLBACK으로 끝낸다.
   - 중단 조건: 어떤 파일이든 오류, 기존 receipt/fingerprint 불일치, 역할·ACL 사전 검사 거부.
   - Rollback: commit 전 실패는 transaction이 되돌린다. Commit 뒤에는 schema를 임의로 지우지 않고
     DAG를 pause한 채 1단계 백업을 별도 빈 대상에서 검증한다. 이전부터 있던 객체는 drop하지 않는다.
3. **Bucket·정책·canary** (O3 필요)
   - 명령: 승인된 admin 자격으로 `opsflow-dev` bucket을 만들고 공유 `seaweedfs-s3` 설정에 worker identity
     하나(manifest-input 읽기, manifest-validated·manifest-quarantine 읽기/쓰기)를 추가한다.
     `WorkerCannotDelete` bucket policy는 `tests/validation/_opsflow_airflow_native_data.py`의
     `worker_bucket_policy` 모양을 따르되, 시험용 principal
     `arn:aws:iam::000000000000:user/synthetic-worker`를 O3의 실제 worker identity로 바꾼다.
     설정 reload는 service 동작이므로 별도 승인 뒤에만 한다.
     `manifest-input/permission-canary`에 `synthetic` body를 admin으로 올린 뒤 worker 자격으로 canary를 실행한다.
   - 기대 결과: allowed_read·allowed_write 200, foreign_bucket·foreign_prefix·input_write·foreign_write·delete·list 403.
   - 중단 조건: 기대와 다른 상태 코드 하나라도.
   - Rollback: 이번에 만든 canary 객체와 bucket policy, 공유 설정에서 추가한 worker identity 항목 하나만 제거한다.
     다른 identity는 건드리지 않으며 reload는 다시 승인이 필요하다. 이전부터 있던 bucket은 지우지 않는다.
4. **코드 설치** (O1, O4, O5 필요)
   - 명령: 설치 방식은 O4 결정을 따른다. 복사 방식이면 subtree로 풀어 저장소 상대 경로를 없앤다:
     `git -C <저장소> archive --format=tar "$REV:$W" dags/source_manifest_ingest.py workflow_lib | tar -x -C <임시 디렉터리>`.
     `dags/README.md`는 넣지 않는다. 임시 디렉터리의 `dags/source_manifest_ingest.py`와 `workflow_lib/`를
     `${DEFAULT_WORKFLOW_DIR}/airflow/dags/`(`/opt/airflow/dags`로 bind) 바로 아래에 두고,
     설치한 모든 파일 경로를 `"$BK/installed-files.txt"`에 기록한다. 대상에 같은 이름이 이미 있으면 중단한다.
     각 파일 `sha256sum`을 commit의 blob과 비교한다. `airflow-worker`의 `/run/opsflow`(`pg.json`, `s3.json`)와
     `dev_data_net`·`object_net`은 O4 결정 없이는 붙이지 않는다.
     확인: `docker exec airflow-scheduler airflow dags list-import-errors`,
     `docker exec airflow-scheduler airflow dags details source_manifest_ingest`.
   - 기대 결과: import 오류가 없고 DAG가 paused다.
   - 중단 조건: hash 불일치, 이름 충돌, import 오류, DAG unpaused.
   - Rollback: `"$BK/installed-files.txt"`에 적힌 파일만 제거한다. 디렉터리의 기존 파일은 건드리지 않는다.
5. **Pool·합성 실행** (O7 필요)
   - DAG task는 `/run/opsflow/pg.json`과 `s3.json`을 읽고 DEV DB와 object network가 필요하다.
     이것은 `airflow-worker`만 받으므로 scheduler에서 `airflow dags test`로 실행하지 않는다.
   - 명령: `docker exec airflow-scheduler airflow pools set manifest_ingest 1 "Opsflow manifest ingest"`.
     합성 입력을 `manifest-input/<source>/<business_date>.json`에 올린다. DAG는 `schedule=None`이며
     업무일은 DAG param `business_date`(기본값 `2026-10-10`)와 `source`(기본값 `hy-home.docker`)로 받는다.
     DAG는 paused로 둔 채 Celery가 worker에서 실행하는 단일 run을 만든다:
     `docker exec airflow-scheduler airflow dags trigger source_manifest_ingest --conf '{"source":"<source>","business_date":"<YYYY-MM-DD>"}'`.
     Paused DAG의 run은 queued로 남으므로 이 run 하나만 진행시키는 방법(일시 unpause 후 즉시 pause 등)은 O7에서 owner가 정한다.
     이어서 잘못된 입력 하나로 같은 절차를 반복한다.
   - 기대 결과: `opsflow_dev`에 raw·validated·published·outbox 행이 생기고
     `manifest-validated/<source>/...json` 객체가 남는다. 잘못된 입력은
     `manifest-quarantine/<source>/<business_date>/<digest>.json`에 `ContentType: application/json`으로 격리되고
     게시 행이 생기지 않는다.
   - 중단 조건: 행·객체 누락, quarantine ContentType 불일치, 잘못된 입력의 게시, 계획 밖 run.
   - Rollback: pool과 이번 합성 객체만 제거한다. 게시 장부·outbox 행은 지우지 않고 DAG를 paused로 둔다.
6. **Unpause**
   - 명령: `docker exec airflow-scheduler airflow dags unpause source_manifest_ingest`.
   - 기대 결과: paused=False이며 계획 밖 run이 생기지 않는다(`schedule=None`).
   - 중단 조건: 예상 밖 run.
   - Rollback: `docker exec airflow-scheduler airflow dags pause source_manifest_ingest`.

전체 rollback은 설치한 파일을 제거하고 백업을 보존하며 1단계 이전부터 있던 것은 drop하지 않는다.

## Verification

- [ ] `docker compose exec airflow-apiserver airflow dags list` 명령어로 정상 로드 여부 확인.
- [ ] native Keycloak 로그인과 `/api/v2/monitor/health` JSON의 component status를 확인한다. HTTP 200만으로 정상 판정하지 않는다. Scheduler health, processor/triggerer job check, worker ping과 승인된 canary 결과도 확인한다.

### Observability and Evidence Sources

- **Signals**: Grafana의 worker 중단 alert와 Flower 큐 길이
- **Evidence to Capture**: `docker compose logs --tail=100 airflow-scheduler airflow-worker airflow-apiserver`, broker ping, `celery --app airflow.providers.celery.executors.celery_executor.app inspect ping`, DAG list 결과.
- **Metrics**: statsd exporter mapping은 DAG, task, pool, DAG 파일 이름을 `dag_id`, `task_id`, `pool_name`, `dag_file` label로 옮기고, 규칙에 없는 네 단계 이상 이름은 버린다(SPEC-0193). 이름 템플릿은 `${1}_${2}`로 쓴다. `$1_$2`로 쓰면 exporter가 `1_`이라는 변수로 읽어 이름이 `airflow_` 하나로 뭉개진다(2026-09-30 확인). DAG run·task 메트릭(`airflow_dagrun_*`, `airflow_task_finish_total`)은 DAG가 실행된 뒤에야 생긴다. Grafana `Applications/airflow`(mixin)와 `Applications/airflow-db`(`airflow-db` SQL datasource)가 이를 본다.
- **Traces**: Airflow는 trace를 보내지 않는다. SPEC-0193에서 OTLP tracing을 켰다가 모두 껐다(2026-09-30, owner 결정). Airflow 3.3.1에서 tracing을 켜면 fork하는 프로세스가 멈춘다. Airflow 쪽 신호는 statsd metric, `airflow-db` SQL datasource, 로그로 본다. 업그레이드 뒤 다시 켜려면 scheduler 하나에서 먼저 health와 DAG run을 확인한다. <!-- runtime-version-exception: history — SPEC-0193의 2026-09-30 장애·인증 검증에 적용된 버전 근거를 보존한다. -->
  - scheduler: 8974 health server가 뜨지 않아 unhealthy로 남는다. SIGUSR2 stack dump에 health thread가 없었다.
  - DAG processor: 파일마다 50 s parse timeout을 넘겨 kill되고, 모든 DAG가 `is_stale`이 되어 run이 `queued`에 머문다. 같은 파일을 프로세스 안에서 parse하면 4 s가 걸린다.
  - worker: prefork pool이 task를 reserve만 하고 실행하지 않는다.
  - 증상이 보이면 `airflow dags details <dag_id>`의 `is_stale`과 `celery inspect reserved`를 먼저 본다.

### 증거 기록

- 실행 명령·결과·시각과 운영자 또는 agent 조치를 기록한다.
- 실패 검사, 관찰 증상과 최종 복구·에스컬레이션 상태를 관련 Task/Incident에 남긴다.

## Failure and Recovery

### Rollback or Recovery

- 이 Runbook에 기록된 복구·rollback 절차와 아래의 `Safe Rollback or Recovery Procedure` 하위 절차만 사용한다.
- 아래 격리 복원은 미실행 상태다. 상태를 변경하기 전에 날짜가 있는 출력과 산출물 checksum을 기록한다.
- 관찰한 장애가 문서화된 절차와 다르면 변경을 중지하고 증거를 보존한 뒤 아래 Escalation 절에 따라 보고한다.

#### Safe Rollback or Recovery Procedure

- [ ] 강제 종료 전 schedule을 pause하고 실행/예약 태스크와 외부 부작용을 조정한다. `Clear`는 재실행을 허가하므로 idempotency와 중복 출력 처리의 별도 승인 없이 실행하지 않는다.
- [ ] DB migration 실패 시 중단하고 DB 소유자와 일치하는 schema/image/artifact 복구 계획을 승인받는다. `_AIRFLOW_DB_MIGRATE: 'false'`는 후속 migration만 막으며 이미 바뀐 schema를 되돌리지 않는다.

#### Planned isolated restore rehearsal

**Project 이름만 바꿔서는 실행할 수 없다.** Rehearsal 전에 고정 container name, host port, bind path, external network와 route 충돌을 제거하고 production 통지·workflow egress를 차단한 별도 Compose/storage 정의를 승인한다. 격리와 대상 backup 계약을 검토하기 전에는 NOT_RUN으로 유지한다. 임의 project에 production volume이나 credential을 연결하지 않는다.

상태: **계획됨·미실행**. 이 문서는 Airflow 복원 성공 증거를 주장하지 않는다.

1. 이미지 digest, profile·환경변수 이름(값 제외), Airflow 버전, 마이그레이션 수준, DAG 목록, 실행·대기 작업 목록, 백업 산출물 checksum을 기록한다. 예약과 입력 생산자를 일시 중지한 뒤 작업 완료를 기다리거나 상태를 명시적으로 대조한다.
2. PostgreSQL 소유자에게 `airflow` DB의 일관된 논리 백업을 요청한다. `airflow-dags`, `airflow-plugins`, `airflow-config`, 필요한 `airflow-logs`와 정확히 일치하는 `airflow_fernet_key`, JWT secret, Keycloak client secret, DB secret, `mng_valkey_password` 참조를 승인된 secret 절차로 보존한다. 실행 중인 Valkey 복사본에 정확한 복구를 의존하지 않는다.
3. 운영 경로·예약·webhook·외부 실행기가 없는 별도 Compose 프로젝트와 격리 네트워크에 복원 복사본을 준비한다. PostgreSQL을 먼저 복원하고 같은 Fernet 키와 마운트 산출물을 복원한 뒤 broker 호스트·secret 쌍을 일치시킨다.
4. 의존 서비스를 기동하고 지원되는 Airflow DB 점검·마이그레이션을 수행한 뒤 processor·scheduler·API·worker를 기동한다. DAG 파싱, DB 상태, 값을 출력하지 않는 Connections 복호화, worker ping, Keycloak 네이티브 로그인, 작업 로그 접근, 외부 효과가 없는 canary DAG를 확인한다.
5. 불일치하면 격리 프로젝트를 중지하고 로그·checksum을 보존한 뒤 변경하지 않은 원본 백업으로 돌아간다. 운영 교체나 DNS·경로 변경에는 별도 변경 승인이 필요하다.

### Escalation

검증 실패, secret 노출 위험, 파괴적 변경 필요 또는 예상 절차와 다른 상태이면 중단하고 @buenhyden에게 넘긴다. 정제된 증거, 시도한 단계와 현재 rollback/recovery 상태를 함께 전달한다.

## Related Documents

### Traceability

- Declared parent: [Airflow Usage Guide](../../guides/08-workflows-and-automation/0050-airflow.md) (`GDE-0050`)
- Governing authority: [Workflow Tier (07-workflow) Architecture Description](../../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Guide](../../guides/08-workflows-and-automation/0050-airflow.md) (`GDE-0050`), [Policy](../../policies/08-workflows-and-automation/0050-airflow.md) (`POL-0050`)

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../../README.md)
- [Usage guide](../../guides/08-workflows-and-automation/0050-airflow.md)
- [Operations policy](../../policies/08-workflows-and-automation/0050-airflow.md)
- [Opsflow HOME 설치 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0051-opsflow-home-installation.md)
