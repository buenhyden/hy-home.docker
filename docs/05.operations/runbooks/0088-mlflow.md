---
title: "MLflow Recovery Runbook"
version: "1.0.3"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0088"
parent_ids:
- "GDE-0088"
created: "2026-09-21"
---

# MLflow Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

프로비저닝 작업 실패, 서버 시작 또는 헬스 실패, 크리덴셜 교체, 아티팩트 접근
거부, 트래킹 저장소 복원 또는 업그레이드 시 사용한다.

### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../policies/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Procedure

### Procedure

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
   구성한다([SeaweedFS 런북](0024-seaweedfs.md)). 다른 object consumer의 영향과
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

리허설도 DB와 artifact의 일관된 캡처 경계를 요구한다. 모든 작성자를 정지하거나
검증된 공동 복구 시점을 확보하지 않았다면 두 사본의 일관성을 주장하지 않는다.
복원은 격리된 환경에서만 수행한다. 공유 `mng-pg` 전체 복원은 다른 서비스를
덮어쓸 수 있으므로 MLflow 장애의 일반 해결책으로 사용하지 않는다.

### Tracking 데이터와 변경 전 검토

notebook과 job을 위해 `MLFLOW_TRACKING_URI`를 internal URL로 설정한다. 기존
experiment와 artifact URI는 `MLFLOW_ARTIFACT_BUCKET`과 database 이름이
변경되지 않는 동안만 유효하다. 둘 중 하나라도 rename하면 migration이다.

`MLFLOW_DB_NAME`의 `pg_dump`로 tracking database를 backup하고, run이
artifact path를 참조하므로 bucket도 SeaweedFS backup set으로 함께
가져간다. 먼저 격리된 `mng-pg`와 SeaweedFS로 restore해 run과 artifact
수를 비교한다. upgrade 전에는 release note를 읽는다. 현재 선언 버전은 기존 DB의 schema revision이 다르면 시작을 거부한다. 신규 테이블
초기화와 기존 DB 업그레이드는 다르며 자동 migration을 가정하지 않는다. 이 service에서는
backup도 restore도 아직 실행하지 않았다.

### 선언 버전의 동작 근거

선언 버전의 공식 tagged 소스와 비교한 [W6 검토 근거](../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0006-tooling-communication-laboratory.md)에
따르면 기존 schema revision 불일치는 명시적 DB upgrade가 필요하고 run 삭제는
lifecycle 변경이다. 따라서 artifact 자동 제거를 주장하지 않는다. 실행 버전 원본은
[Dockerfile](../../../infra/08-ai/mlflow/Dockerfile)이며 변경 때 근거를 다시 검토한다.
secret 파일 교체·서비스 재생성은 [공통 수명주기 정책](../policies/0006-infrastructure-optimization-governance.md)을
따르고 이전 자격 증명 거부와 새 연결·artifact 조회를 각각 확인한다.

## Verification

### Evidence

명령 종료, 작업 종료 코드, 이미지, 소스 커밋, 개수, 체크섬을 기록한다.
비밀번호, 액세스 키, 아티팩트 내용은 절대 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

설정 롤백은 Git에서 Compose 파일을 복원한다. 업그레이드가 실행한 데이터베이스
마이그레이션은 업그레이드 이전 백업으로만 되돌릴 수 있다. 복원과 업그레이드
리허설은 **계획됨, 미실행**이다.

### Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

다른 소유의 데이터베이스가 거부되거나, superuser나 SeaweedFS 관리자
크리덴셜 부여 요청, 복원 개수 비교 실패, 게이트웨이 SSO 제거 요청이 있으면
중단한다.

### Traceability

- [Guide](../guides/0088-mlflow.md) (`GDE-0088`)
- [Policy](../policies/0088-mlflow.md) (`POL-0088`)
- [MLflow Compose](../../../infra/08-ai/mlflow/docker-compose.yml)

## Related Documents

- [이미지 Dockerfile](../../../infra/08-ai/mlflow/Dockerfile)과
  [파생 버전 프로젝션](../../../infra/tech-stack.versions.json)
- [관리 데이터베이스 런북](0028-management-database.md)
- [SeaweedFS 런북](0024-seaweedfs.md)
