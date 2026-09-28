---
title: "MLflow Recovery Runbook"
version: "1.0.3"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0088"
parent_ids:
- "GDE-0088"
created: "2026-09-21"
---

# MLflow Recovery Runbook

## When to Use

프로비저닝 작업 실패, 서버 시작 또는 헬스 실패, 크리덴셜 교체, 아티팩트 접근
거부, 트래킹 저장소 복원 또는 업그레이드 시 사용한다.

## Procedure

1. 저장소 루트에서 검증하고 점검한다.

   ```bash
   docker compose --profile core --profile mlops config --quiet
   docker compose --profile core --profile mlops ps -a mlflow mlflow-db-provision
   docker compose --profile core --profile mlops logs --tail=100 mlflow-db-provision seaweedfs-buckets mlflow
   ```

2. 프로비저닝 종료 코드를 확인한다. `64`는 데이터베이스나 SeaweedFS 변경 전에
   발견된 입력 문제다(시크릿 누락/비어 있음/여러 줄, 잘못된 이름). `3`은
   psql 오류이며, 로그에 다른 역할이 소유한 데이터베이스나 관리자 역할 이름
   같은 거부 사유가 명시된다.
3. `ON_ERROR_STOP`은 첫 오류에서 멈추지만 이미 커밋된 문장을 되돌리지 않는다.
   원인을 수정하고 작업을 재실행한다. 모든 문장은 멱등적이다.

   ```bash
   docker compose --profile core --profile mlops up --no-deps mlflow-db-provision
   docker compose --profile core --profile mlops up --no-deps seaweedfs-buckets
   ```

4. 두 작업이 모두 `0`으로 종료된 이후에만 서버를 시작하거나 재시작한다.

### Credential rotation

1. 시크릿, 서비스, 재시작을 명시한 승인을 받는다.
2. 등록된 시크릿 워크플로로 시크릿 파일을 교체한다.
3. 데이터베이스 비밀번호의 경우 `mlflow-db-provision`을 재실행한다. 이는
   MLflow 역할 비밀번호만 재설정한다. `seaweedfs_s3_mlflow_secret_key`의
   경우 `seaweedfs-s3`를 재생성한다. 이는 시작 시 자신의 identity를 다시
   구성한다(RUN-0024).
4. `mlflow`를 재생성하고 헬스와 아티팩트 읽기 한 건을 확인한다.

### Restore and upgrade

1. `mlflow`를 정지한다. `MLFLOW_DB_NAME`을 덤프하고 버킷을 미러링한다. 소스
   커밋, 이미지, 행 개수, 객체 개수를 기록한다.
2. 프로덕션 복원 전에 둘 다 격리된 환경으로 복원하고 개수를 비교한다. 일치하는
   버킷 없이 데이터베이스만 복원하면 유효하지 않은 아티팩트 URI가 남는다.
3. 업그레이드의 경우 먼저 1단계를 수행한 뒤 새 이미지를 시작하고 마이그레이션
   출력을 지켜본다.

리허설은 `mlflow`를 계속 실행 상태로 둔다. 1단계의 정지 대신 읽기 전용 덤프와
읽기 전용 버킷 미러링을 수행하고, 2단계의 격리된 환경으로만 복원한다.

## Evidence

명령 종료, 작업 종료 코드, 이미지, 소스 커밋, 개수, 체크섬을 기록한다.
비밀번호, 액세스 키, 아티팩트 내용은 절대 기록하지 않는다.

## Rollback or Recovery

설정 롤백은 Git에서 Compose 파일을 복원한다. 업그레이드가 실행한 데이터베이스
마이그레이션은 업그레이드 이전 백업으로만 되돌릴 수 있다. 복원과 업그레이드
리허설은 **계획됨, 미실행**이다.

## Escalation

다른 소유의 데이터베이스가 거부되거나, superuser나 SeaweedFS 관리자
크리덴셜 부여 요청, 복원 개수 비교 실패, 게이트웨이 SSO 제거 요청이 있으면
중단한다.

## Traceability

- [Guide](../guides/0088-mlflow.md) (`GDE-0088`)
- [Policy](../policies/0088-mlflow.md) (`POL-0088`)
- [MLflow Compose](../../../infra/11-laboratory/mlflow/docker-compose.yml)

## Related Documents

- [이미지 Dockerfile](../../../infra/11-laboratory/mlflow/Dockerfile)과
  [파생 버전 프로젝션](../../../infra/tech-stack.versions.json)
- [관리 데이터베이스 런북](0028-management-database.md)
- [SeaweedFS 런북](0024-seaweedfs.md)
