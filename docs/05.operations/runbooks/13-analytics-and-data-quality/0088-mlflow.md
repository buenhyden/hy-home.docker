---
title: "MLflow Recovery Runbook"
version: "1.0.8"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-30"
layer: "operations"
artifact_id: "RUN-0088"
parent_ids:
- "GDE-0088"
created: "2026-09-21"
---

# MLflow Recovery Runbook

## Overview

MLflow tracking server의 프로비저닝 실패, 크리덴셜 회전, 복원, 업그레이드를 다루는 복구 런북이다.

## Trigger

프로비저닝 작업 실패, 서버 시작 또는 헬스 실패, 크리덴셜 교체, 아티팩트 접근
거부, 트래킹 저장소 복원 또는 업그레이드 시 사용한다.

## Prerequisites

### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](../10-platform-and-backup/0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../../policies/01-common/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Procedure

1. 저장소 루트에서 검증하고 점검한다.

   ```bash
   docker compose --profile core --profile mlops config --quiet
   docker compose --profile core --profile mlops ps -a mlflow mlflow-db-provision
   docker compose --profile core --profile mlops logs --tail=100 mlflow-db-provision seaweedfs-buckets mlflow
   ```

2. 작업과 실패 단계를 먼저 구분한다. PostgreSQL helper의 `64`는 secret·이름
   검증 실패뿐 아니라 readiness 대기 만료에서도 나온다. psql 단계 오류는 제한된
   로그에서 소유권·권한·연결 원인을 확인한다. 코드만으로 DB 변경 전 실패라고
   단정하거나 SeaweedFS 작업에도 같은 의미를 적용하지 않는다.
3. `ON_ERROR_STOP`은 첫 오류에서 멈추지만 이미 커밋된 문장을 되돌리지 않는다.
   역할·비밀번호·database·grant의 적용 범위를 확인한 뒤
   재실행을 승인받는다. 아래 명령은 새 컨테이너에서 변경 작업을 수행하며 dependencies를
   시작하지 않으므로 PG/init/object 준비를 먼저 확인한다. 버킷 작업은 설정된 전체
   버킷 집합을 점검·생성할 수 있어 MLflow만의 변경이 아니다.

   ```bash
   docker compose --profile core --profile mlops run --rm --no-deps mlflow-db-provision
   docker compose --profile core --profile mlops run --rm --no-deps seaweedfs-buckets
   ```

4. 두 작업이 모두 `0`으로 끝난 뒤에만 서버를 시작하거나 재시작한다.

### Credential rotation

1. 시크릿, 서비스, 재시작을 명시한 승인을 받는다.
2. 등록된 시크릿 워크플로로 시크릿 파일을 교체한다.
3. 데이터베이스 비밀번호의 경우 `mlflow-db-provision`을 재실행한다. 이 작업은
   비밀번호뿐 아니라 역할·database·grant 계약을 다시 적용할 수 있다. `seaweedfs_s3_mlflow_secret_key`의
   경우 `seaweedfs-s3`를 재생성한다. 이 서비스는 시작할 때 자신의 identity를 다시
   구성한다([SeaweedFS 런북](../05-databases-and-storage/0024-seaweedfs.md)). 다른 object consumer의 영향과
   중단 시간을 포함해 승인받는다.
4. `mlflow`를 재생성하고 헬스와 아티팩트 읽기 한 건을 확인한다.

### Restore and upgrade

1. `mlflow`를 정지한다. `MLFLOW_DB_NAME`을 덤프하고 버킷을 미러링한다. 소스
   커밋, 이미지, 행 개수, 객체 개수를 기록한다.
2. 프로덕션 복원 전에 둘 다 격리된 환경으로 복원하고 개수를 비교한다. 일치하는
   버킷 없이 데이터베이스만 복원하면 유효하지 않은 아티팩트 URI가 남는다.
3. 기존 DB upgrade는 서버 시작과 분리한다. 선택한 버전의 공식 migration 근거,
   백업·복원 증거, DB writer 정지와 secret 비노출 실행 방식을 확인하고 별도 승인된
   `mlflow db upgrade` 계획을 검토한다. 현재 Compose에는 migration 작업이 없으므로
   단순히 새 서버를 시작하는 절차로 대체하지 않는다. 근거가 없으면 진행을 중단한다.
   실행 절차는 아래 `Tracking DB schema upgrade`를 따른다.

### Tracking DB schema upgrade

[Dockerfile](../../../../infra/08-ai/mlflow/Dockerfile)의 MLflow 버전을 올린 뒤 기존
tracking DB로 서버를 처음 시작하기 전에 소유자가 실행한다. 저장소 루트의 같은 shell에서
순서대로 실행하며, 명령은 비밀번호를 출력하거나 argv에 넣지 않는다. 각 단계의 출력은
작업 기록에 남긴다.

1. **준비.** Compose 함수 `c`와 새 이미지 `I`를 정하고, `mng-pg`가 healthy이고
   `mlflow`가 정지 상태인지 확인한 뒤 새 이미지를 빌드한다. `mlflow`가 실행 중이면
   `c stop mlflow`로 먼저 멈춘다.

   ```bash
   c() { docker compose --profile core --profile mlops "$@"; }
   I=$(c config --images | grep '^hy-home/mlflow:')
   c ps -a mng-pg mlflow
   c build mlflow
   ```

2. **현재 상태 기록.** DB revision과 행 개수, 새 이미지가 요구하는 revision을 기록한다.
   두 revision이 같으면 upgrade가 필요 없으므로 6단계로 간다.

   ```bash
   docker exec mng-pg sh -c 'for q in "select version_num from alembic_version" "select count(*) from experiments" "select count(*) from runs"; do psql -U "$POSTGRES_USER" -d mlflow -Atc "$q"; done'
   docker run --rm --entrypoint python "$I" -c 'import os, mlflow.store.db_migrations as m; from alembic.config import Config; from alembic.script import ScriptDirectory; c = Config(); c.set_main_option("script_location", os.path.dirname(m.__file__)); print(ScriptDirectory.from_config(c).get_current_head())'
   ```

3. **백업.** 소유자 전용 경로에 custom-format dump를 만들고 목록과 checksum을 확인한다.
   migration은 되돌릴 수 없으므로 이 dump가 유일한 rollback 원본이다. schema upgrade는
   artifact를 바꾸지 않으므로 이 단계에서 bucket은 복사하지 않는다.

   ```bash
   B=/home/hyunyoun/storage/ops-snapshots/mlflow-$(date +%Y%m%d-%H%M%S)
   install -d -m 0700 "$B"
   docker exec mng-pg sh -c 'pg_dump -U "$POSTGRES_USER" -Fc mlflow' >"$B/mlflow.dump"
   chmod 0600 "$B/mlflow.dump"
   docker exec -i mng-pg pg_restore --list <"$B/mlflow.dump" | grep -c 'TABLE DATA'
   sha256sum "$B/mlflow.dump" | tee "$B/mlflow.dump.sha256"
   ```

4. **격리 리허설.** 공개 port 없는 internal network에 임시 PostgreSQL을 만들고 HOME과
   같은 owner role(`mlflow`)로 dump를 복원한 뒤, 그 role로 새 이미지 upgrade와 아래
   rollback을 차례로 시험한다. 같은 PostgreSQL 이미지를 쓰되 pgBackRest secret을 요구하는
   HOME entrypoint 대신 기본 entrypoint로 시작하고, 초기화 중 임시 서버와 구분하려고
   TCP로 준비 상태를 확인한다. 출력은 upgrade 뒤 새 revision과 2단계와 같은 행 개수,
   rollback 뒤 이전 revision과 같은 행 개수여야 한다. 마지막 줄은 이 단계가 만든 자원만 지운다.

   ```bash
   N=mlflow-upgrade-rehearsal
   docker network create --internal "$N"
   docker run -d --name "$N" --network "$N" -e POSTGRES_HOST_AUTH_METHOD=trust --entrypoint docker-entrypoint.sh "$(docker inspect -f '{{.Config.Image}}' mng-pg)" postgres
   for i in {1..60}; do docker exec "$N" pg_isready -q -h 127.0.0.1 -U postgres && break; sleep 1; done
   docker exec "$N" psql -q -U postgres -c 'create role mlflow login'
   docker exec -i "$N" pg_restore -U postgres -d postgres --create --exit-on-error <"$B/mlflow.dump"
   docker run --rm --network "$N" --entrypoint mlflow "$I" db upgrade "postgresql+psycopg2://mlflow@$N:5432/mlflow"
   for q in "select version_num from alembic_version" "select count(*) from experiments" "select count(*) from runs"; do docker exec "$N" psql -U postgres -d mlflow -Atc "$q"; done
   docker exec "$N" dropdb -U postgres mlflow
   docker exec -i "$N" pg_restore -U postgres -d postgres --create --exit-on-error <"$B/mlflow.dump"
   for q in "select version_num from alembic_version" "select count(*) from experiments" "select count(*) from runs"; do docker exec "$N" psql -U postgres -d mlflow -Atc "$q"; done
   docker rm -f "$N" && docker network rm "$N"
   ```

5. **HOME upgrade.** 리허설이 성공했을 때만 실행한다. 비밀번호는 container 안에서 secret
   파일로만 읽는다. 끝나면 2단계의 첫 명령을 다시 실행해 revision이 새 revision이고
   행 개수가 같은지 확인한다.

   ```bash
   c run --rm --no-deps --entrypoint sh mlflow -ec 'PGPASSWORD="$(tr -d "\r\n" </run/secrets/mlflow_db_password)"; export PGPASSWORD; exec mlflow db upgrade "postgresql+psycopg2://${MLFLOW_DB_USER}@${MLFLOW_DB_HOST}:${MLFLOW_DB_PORT}/${MLFLOW_DB_NAME}"'
   ```

6. **시작과 확인.** `--no-deps`로 `mlflow`만 시작하고 healthy, `/health`, experiment 수를
   확인한다. experiment 수는 2단계와 같아야 한다. 의존성까지 올리면 설정이 바뀐 공유
   `mng-pg`가 재생성될 수 있으므로, 먼저 `c up -d --no-deps --dry-run mlflow`의 대상이
   `mlflow`뿐인지 확인한다.

   ```bash
   c up -d --no-deps --dry-run mlflow
   c up -d --no-deps mlflow
   c ps mlflow
   docker exec mlflow python -c 'import json, os, urllib.request as u; p = os.environ["MLFLOW_PORT"]; print(u.urlopen(f"http://127.0.0.1:{p}/health", timeout=5).read().decode()); r = u.Request(f"http://127.0.0.1:{p}/api/2.0/mlflow/experiments/search", data=b"{\"max_results\": 1000}", headers={"Content-Type": "application/json"}); print(len(json.load(u.urlopen(r, timeout=5)).get("experiments", [])))'
   ```

**중단 조건.** 백업 목록이 비었거나, 리허설 revision·개수가 다르거나, HOME upgrade가
0이 아닌 코드로 끝나면 서버를 시작하지 않고 멈춘다. upgrade 도중 실패하면 DB가
중간 상태일 수 있으므로 아래 rollback으로 백업을 복원한다.

**Rollback.** `mlflow`를 멈추고 `mlflow` database만 지운 뒤 백업으로 다시 만든다.
`pg_restore --clean`은 upgrade가 추가한 테이블의 외래 키 때문에 실패하므로 쓰지 않는다.
`--create`는 dump에 기록된 owner와 database 설정으로 다시 만든다. 공유 `mng-pg`의 다른
database는 건드리지 않으며, 다른 연결 때문에 `dropdb`가 실패하면 강제로 끊지 말고 멈춘다.
그 다음 Git에서 이전 Dockerfile과 Compose 태그로 되돌리고 이전 이미지로 시작한다.

```bash
c stop mlflow
docker exec mng-pg sh -c 'dropdb -U "$POSTGRES_USER" mlflow'
docker exec -i mng-pg sh -c 'pg_restore -U "$POSTGRES_USER" -d postgres --create --exit-on-error' <"$B/mlflow.dump"
```

### Tracking 데이터와 변경 전 검토

notebook과 job을 위해 `MLFLOW_TRACKING_URI`를 internal URL로 설정한다. 기존
experiment와 artifact URI는 `MLFLOW_ARTIFACT_BUCKET`과 database 이름이
변경되지 않는 동안만 유효하다. 둘 중 하나라도 rename하면 migration이다.

`MLFLOW_DB_NAME`의 `pg_dump`로 tracking database를 backup하고, run이
artifact path를 참조하므로 bucket도 SeaweedFS backup set으로 함께
가져간다. 먼저 격리된 `mng-pg`와 SeaweedFS로 restore해 run과 artifact
수를 비교한다. upgrade 전에는 release note를 읽는다. 현재 선언 버전은 기존 DB의 schema revision이 다르면 시작을 거부한다. 신규 테이블
초기화와 기존 DB 업그레이드는 다르며 자동 migration을 가정하지 않는다. HOME DB의
backup·restore·upgrade는 아직 실행하지 않았다. HOME DB dump를 격리된 임시 PostgreSQL에서
upgrade하고 새 서버로 조회한 리허설은 SEC01 Task에 기록되어 있다.

### 선언 버전의 동작 근거

선언 버전의 공식 tagged 소스와 비교한 [W6 검토 근거](../../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0006-tooling-communication-laboratory.md)에
따르면 기존 schema revision 불일치는 명시적 DB upgrade가 필요하고 run 삭제는
lifecycle 변경이다. 따라서 artifact 자동 제거를 주장하지 않는다. 실행 버전 원본은
[Dockerfile](../../../../infra/08-ai/mlflow/Dockerfile)이며 변경 때 근거를 다시 검토한다.
secret 파일 교체·서비스 재생성은 [공통 수명주기 정책](../../policies/01-common/0006-infrastructure-optimization-governance.md)을
따르고 이전 자격 증명 거부와 새 연결·artifact 조회를 각각 확인한다.

### 격리 복원 증거(SPEC-0182 기준 7)

2026-10-30 owner 결정으로 MLflow 격리 복원은 두 부분이다. tracking DB는 [RUN-0021](../10-platform-and-backup/0021-backup-and-restore.md) step 5의 time-target PITR clone에서 `mlflow.public` 표 5개의 count로 확인한다. artifact는 아래 명령이 운영 `mlflow-artifacts` bucket을 읽기 전용으로 새 scratch에 내려받고, 객체마다 ETag와 local MD5를 비교한다. 운영 `mlflow`는 멈추지 않으며 bucket에는 쓰지 않는다. 실행은 owner가 하며 승인 전에는 **NOT_RUN**이다.

artifact 부분은 SeaweedFS/Restic backup에서의 복원이 아니다. 이것이 증명하는 것은 두 가지다. 운영 객체를 mlflow key로 읽을 수 있고, 내려받은 byte가 SeaweedFS에 저장된 MD5와 같다. recovery point는 복사 시각이고 PITR clone의 target 시각과 짝을 이루지 않으며, artifact RPO를 주장하지 않는다. `runs_with_objects`는 clone이 아니라 운영 `runs`와 대조한다.

```bash
cd ~/data/hy-home.docker   # main checkout 루트(worktree에는 git-ignored secrets/가 없다)
SCR=~/storage/backups/mlflow-artifacts-20261030   # 새 경로, data disk
[ -z "$(ls -A "$SCR" 2>/dev/null)" ] || { echo "result=FAIL scratch_not_empty"; exit 1; }
install -d -m 0700 "$SCR" "$SCR/meta" "$SCR/objects"
start=$(date +%s)
admin=$(docker inspect mng-pg --format '{{range .Config.Env}}{{println .}}{{end}}' | sed -n 's/^POSTGRES_USER=//p')
docker exec --user 70 mng-pg psql -U "$admin" -d mlflow -Atc \
  "SELECT experiment_id || '/' || run_uuid FROM runs ORDER BY 1" > "$SCR/meta/runs.txt"
docker run --rm --pull=never --network object_net \
  --user "$(id -u):$(id -g)" --read-only --tmpfs /tmp -e HOME=/tmp \
  --cap-drop ALL --security-opt no-new-privileges \
  --mount "type=bind,src=$PWD/secrets/storage/seaweedfs/seaweedfs_s3_mlflow_secret_key.txt,dst=/run/secrets/k,readonly" \
  --mount "type=bind,src=$SCR/meta,dst=/meta" \
  --mount "type=bind,src=$SCR/objects,dst=/objects" \
  --entrypoint sh \
  amazon/aws-cli@sha256:ce44b800602264c12298bbf3399055a4cefdb9ed4a098abe564afe26e7071bce -ec '
    AWS_SECRET_ACCESS_KEY="$(tr -d "\r\n" </run/secrets/k)"
    export AWS_SECRET_ACCESS_KEY AWS_ACCESS_KEY_ID=mlflow AWS_DEFAULT_REGION=us-east-1
    e=http://seaweedfs-s3:8333
    aws --endpoint-url "$e" s3api list-objects-v2 --bucket mlflow-artifacts --output json >/meta/listing.json
    aws --endpoint-url "$e" s3 sync --only-show-errors s3://mlflow-artifacts /objects'
echo "copy_rc=$?"
python3 - "$SCR" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
listed = json.loads((root / "meta" / "listing.json").read_text()).get("Contents", [])
match = multipart = unsafe = 0
for obj in listed:
    key, tag = obj["Key"], obj["ETag"].strip('"')
    if key.startswith("/") or key.endswith("/") or ".." in pathlib.PurePosixPath(key).parts:
        unsafe += 1
        continue
    local = root / "objects" / key
    if "-" in tag:
        multipart += 1
    elif local.is_file() and hashlib.md5(local.read_bytes()).hexdigest() == tag:
        match += 1
local_files = sum(1 for f in (root / "objects").rglob("*") if f.is_file())
runs = (root / "meta" / "runs.txt").read_text().split()
keys = [o["Key"] for o in listed]
with_objects = sum(1 for r in runs if any(k.startswith(r + "/") for k in keys))
ok = len(listed) >= 1 and len(listed) == local_files == match and not (multipart or unsafe)
print(f"objects_listed={len(listed)}\nobjects_local={local_files}\nmd5_match={match}")
print(f"multipart_unchecked={multipart}\nunsafe_keys={unsafe}")
print(f"runs_with_objects={with_objects}/{len(runs)}\nresult={'PASS' if ok else 'FAIL'}")
PY
echo "elapsed_seconds=$(( $(date +%s) - start ))"
```

`copy_rc=0`이고 `result=PASS`여야 한다. PASS는 객체가 1개 이상이고 `objects_listed`, `objects_local`, `md5_match`가 모두 같으며 `multipart_unchecked`와 `unsafe_keys`가 0이라는 뜻이다. 2026-09-25 기록은 객체 2개였으므로 다른 값이면 원인을 기록한다. `copy_rc`가 0이 아니면 listing이 비었거나 일부일 수 있으므로 python 결과와 무관하게 FAIL이다. multipart 객체는 ETag가 MD5가 아니어서 이 방식으로는 PASS가 될 수 없다. 8 MB를 넘는 artifact가 생기면 backup 복원본과의 SHA-256 비교 같은 다른 확인이 필요하다. `/` 시작, `/` 끝, `..` 포함 key는 `unsafe_keys`로 세고 FAIL이며, sync 대상은 `objects/` bind뿐이라 그런 key도 `meta/`를 덮어쓸 수 없다. `runs_with_objects`는 artifact가 있는 run 수의 관측값이며 artifact가 없는 run도 정상일 수 있다. 출력에는 key 이름, 객체 내용, 비밀값이 없다. `meta/`와 `objects/`는 scratch(0700)에만 남고 artifact 내용은 민감할 수 있는 data로 취급한다. scratch 삭제는 별도 owner 승인이다.

## Verification

명령 종료, 작업 종료 코드, 이미지, 소스 커밋, 개수, 체크섬을 기록한다.
비밀번호, 액세스 키, 아티팩트 내용은 절대 기록하지 않는다.

## Failure and Recovery

### Rollback or Recovery

설정 롤백은 Git에서 Compose 파일을 복원한다. 업그레이드가 실행한 데이터베이스
마이그레이션은 업그레이드 이전 백업으로만 되돌릴 수 있으며 절차는 `Tracking DB schema
upgrade`의 Rollback이다. HOME 복원과 업그레이드는 **미실행**이다.

### Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

다른 소유의 데이터베이스가 거부되거나, superuser나 SeaweedFS 관리자
크리덴셜 부여 요청, 복원 개수 비교 실패, 게이트웨이 SSO 제거 요청이 있으면
중단한다.

## Related Documents

### Traceability

- [Guide](../../guides/13-analytics-and-data-quality/0088-mlflow.md) (`GDE-0088`)
- [Policy](../../policies/13-analytics-and-data-quality/0088-mlflow.md) (`POL-0088`)
- [MLflow Compose](../../../../infra/08-ai/mlflow/docker-compose.yml)

- [이미지 Dockerfile](../../../../infra/08-ai/mlflow/Dockerfile)과
  [파생 버전 프로젝션](../../../../infra/tech-stack.versions.json)
- [관리 데이터베이스 런북](../05-databases-and-storage/0028-management-database.md)
- [SeaweedFS 런북](../05-databases-and-storage/0024-seaweedfs.md)
