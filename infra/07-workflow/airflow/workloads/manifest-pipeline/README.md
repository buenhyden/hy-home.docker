---
title: "Independent Manifest Pipeline"
version: "0.2.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-10"
---

# Independent Manifest Pipeline

## Overview

합성 운영 문서 목록을 S3에서 읽어 검증·readback한 뒤 DEV PostgreSQL에
게시하는 단일 Airflow workload입니다. 입력의 해시 형식은 실제 Git 내용의
인증 증거가 아닙니다. 원문 수집이나 Wiki 구현을 하지 않습니다.

## Scope

DAG `source_manifest_ingest`, pool `manifest_ingest`, DB `opsflow_dev`, schema
`ops_flow`, bucket `opsflow-dev`의 전용 배치입니다. P04가 SQL 단독 작성자이며
P05는 검토 후 고정한 SQL 버전·hash와 함수 계약을 소비합니다. 소스 회귀시험은
실제 권한·배포·복구 수용과 별개이며 이번 P04에서 P05 실제 통지는 NOT_RUN입니다.

## Structure

- [dags/](dags/README.md): 수동·paused DAG.
- [workflow_lib/](workflow_lib/README.md): parser와 전용 adapter.
- [sql/](sql/README.md): migration과 실행 가능한 SQL 검사.
- [fixtures/](fixtures/README.md): 공개 합성 manifest와 값 없는 접속 예시.
- Compose 변경은 [airflow Compose](../../docker-compose.yml)에 합쳐져 있고 별도 override는 없습니다.

## Usage

저장소 root에서 전용 `tests.lib.ops.test_opsflow_manifest`,
`tests.lib.ops.test_opsflow_adapters`, `tests.lib.ops.test_opsflow_provision_contract`,
`tests.validation.test_opsflow_airflow_contract` unittest를 실행합니다.
SDK double·driver double의 PASS는 실제 DAG import나 DEV 실행의 증거가 아닙니다.

### Configuration

SEC01의 호환 이미지·dependencies와 P03의 endpoint·실제 worker UID/GID 계약을
받아야 합니다. 이미지에는 필요한 패키지를 빌드 시 설치하며 startup pip를
사용하지 않습니다. 소스 기본 UID와 관측된 UID가 달라 어느 쪽도 가정하지 않습니다.

overlay 규칙은 [POL-0078](../../../../../docs/05.operations/policies/01-common/0078-compose-profile-vocabulary.md#home-compose-overlay-등록부와-적용-규칙)이 소유하며 이 workload는 overlay를 쓰지 않습니다. Airflow Compose가 apiserver·scheduler·dag-processor·triggerer·worker에
이 폴더의 DAG와 `workflow_lib`를 읽기 전용으로 mount하고, worker에만 DEV/object network와
`OPSFLOW_SECRET_DIR`(없으면 추적된 빈 `secret-placeholder/`)을 `/run/opsflow`로 mount합니다.
`OPSFLOW_SECRET_DIR`에는 worker 전용 보호 디렉터리의 정확한 경로를 지정합니다. 기본 이미지를 그대로 쓰며
n8n 변경은 없습니다.

Worker는 `pg.json`, `s3.json`과 TLS를 선택한 경우 같은 보호 폴더의
`ca.pem`을 읽습니다. [CA 전달](workflow_lib/tls.py)은 보호된 경로·소유자·권한·
단일 regular file·크기·PEM 인증서를 확인하고, 검증한 bytes를 쓰기 금지한
메모리 사본으로 고정해 driver에 전달합니다. Linux memfd·seal·procfs가 없거나
검증에 실패하면 연결을 거부합니다. TLS를 선택한 PostgreSQL은 `verify-full`만 지원하며,
접속을 바꾸는 libpq 환경 변수도 거부합니다. GSS 암호화가 TLS를 대신하지 않도록
`gssencmode=disable`을 명시합니다.

S3 TLS 소스 계약은 명시적 `https://seaweedfs-s3:443`과 고정
`https:seaweedfs-s3:443` token만 허용합니다. Proxy와 redirect를 통한 다른
대상 연결을 막고 DAG의 성공·실패 모두에서 client와 CA 사본을 닫습니다.
현재 SeaweedFS 소스의 내부 listener는 평문 `:8333`이며 이 변경은 TLS listener를
배포하지 않습니다. 실제 `:443` listener·CA/SAN·잘못된 CA·만료 인증서·고정 이미지의
실제 driver·worker UID/GID·재인증·복구는 NOT_RUN입니다. 기존 승인된 내부 평문
경로를 보존하며, P03의 실제 endpoint·인증서 수용 전에 TLS 설정을 활성화하지 않습니다.
Admin·reader·notifier 자격 증명은 이 폴더에 두지 않습니다.
기존 DEV provisioner는 schema version 2의 함수 전용 Opsflow 계약을 지원합니다.
Owner는 NOLOGIN이며 migrator만 명시적 SET ROLE 권한을 갖고 runtime은 승인된
함수/view만 소비합니다. 공개 `pg/provision/opsflow.json`은 로그인 네 개의 secret 이름
(`dev_pg_opsflow_{migrator,ingest,notifier,reader}_password`)을 선언하지만 값 파일 생성과
실제 역할 발급은 owner가 승인한 별도 실행 대상입니다. worker의 S3 identity
`opsflow-worker`는 `seaweedfs/config/s3-identities.conf`에 선언되며 `/run/opsflow`의
`pg.json`·`s3.json`을 만드는 입력(`OPSFLOW_SECRET_DIR`)은 저장소가 정의하지 않는 열린
항목입니다. pool 한 slot 생성도 별도 실행 대상입니다. 기존 generic table-grant 계약을 이 workload에
대입하거나 미지정 자격을 자동 발급하지 않습니다.

### Validation

실제 실행은 고정 이미지의 DAG import, SQL 직접 호출·역할/다른 DB/S3 거부,
Celery worker 게시·재실행·경합·backfill·객체 후 DB 실패 및 빈 대상 복원이
필요합니다. 관련 계약 미확정 상태에서는 이 항목을 NOT_RUN으로 기록합니다.
고정 캐시 이미지·명시 선택자가 없는 기본 시험은 native 실행을 skip합니다.
과거 migration·pg_hba·PutObject 오류는 각 실행 입력과 함께 역사 Task에 보존되어
있습니다. 후속 Task0020(`docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0020-airflow-native-publication.md`)은
generation-1 실제 Celery 게시·제어된 재시도·replay PASS를 기록하지만 generation-2는
UNVERIFIED이고 recovery는 NOT_RUN/BLOCKED입니다. Task0018(`docs/03.specs/0204-service-integration-security-and-operations/tasks/tsk-0018-workflow-lease-and-connect-safety.md`)의
별도 PostgreSQL CONNECT 거부·복원은 같은 범위의 보조 증거입니다. 이를 현재
전체 Worker·S3·실제 Timescale·HOME·P05 종단 인수로 확대하지 않습니다.
이번 P04 Task(`docs/03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0043-opsflow-data-path.md`)는
연결·입력 격리·data_version·객체 메타데이터 복원의 현재 차분과 실제 시험 결과를
별도로 기록합니다. 정제된 명령·결과만 공개하고 원시 payload·자격·운영 로그는
남기지 않습니다. 직렬 lock·소유 자원·cleanup HOLD는 기존 fixture 경계를 따릅니다.
PG/S3는 하나의 원자적 트랜잭션이 아니므로 DB 실패 후 객체는 unpublished로
남고 같은 bytes를 readback한 뒤 재사용합니다. Orphan 삭제는 게시 장부와 별도
보존 정책으로만 판단합니다. Rollback은 이 DAG pause와 검토한 migration 복구이며
MNG reset·공유 volume 초기화·전체 restart를 사용하지 않습니다.

## Related Documents

- [Workloads](../README.md)
- [Airflow](../../README.md)
- [문서 탐색](../../../../../docs/README.md)
- [Task SDK](https://airflow.apache.org/docs/task-sdk/stable/api.html)
- [Compose merge](https://docs.docker.com/reference/compose-file/merge/)
