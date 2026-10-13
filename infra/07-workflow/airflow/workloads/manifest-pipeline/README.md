---
title: "Independent Manifest Pipeline"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
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
실제 권한·배포·복구 수용과 별개이며 P05 실제 통지는 NOT_RUN입니다.

## Structure

- [dags/](dags/README.md): 수동·paused DAG.
- [workflow_lib/](workflow_lib/README.md): parser와 전용 adapter.
- [sql/](sql/README.md): migration과 실행 가능한 SQL 검사.
- [fixtures/](fixtures/README.md): 공개 합성 manifest와 값 없는 접속 예시.
- [Compose override](compose.workflow.override.yml): 기존 root 모델 위의 선택 변경.

## Usage

저장소 root에서 전용 `tests.lib.ops.test_opsflow_manifest`,
`tests.lib.ops.test_opsflow_adapters`, `tests.lib.ops.test_opsflow_provision_contract`,
`tests.validation.test_opsflow_airflow_contract` unittest를 실행합니다.
SDK double·driver double의 PASS는 실제 DAG import나 DEV 실행의 증거가 아닙니다.

### Configuration

이 override의 선택형 서비스 확장 분류에는 `x-hyhome-overlay`의 정수 version과
추적된 root include base를 명시해야 합니다. 검토한 root와 override를 순서대로
명시한 `-f` 조합에서 기존 서비스 profile을 상속하며 단독 기동하지 않습니다.
새 서비스·top-level 자원·profile 재정의를 추가하지 않고 기존 Guide와 inventory를
중복 등록하지 않습니다. Marker 분류는 이미지·권한·DEV/HOME 실행 수용이 아닙니다.
관련 정책 문서는 기존 [문서 탐색](../../../../../docs/README.md)에서 찾습니다.
실제 소스 분류 입력은 이 override의 marker와 공통 분류기가 소비합니다.

SEC01의 호환 이미지·dependencies와 P03의 endpoint·실제 worker UID/GID 계약을
받아야 합니다. 이미지에는 필요한 패키지를 빌드 시 설치하며 startup pip를
사용하지 않습니다. 소스 기본 UID와 관측된 UID가 달라 어느 쪽도 가정하지 않습니다.

Override의 `OPSFLOW_AIRFLOW_IMAGE`에는 검토한 로컬 immutable 이미지,
`OPSFLOW_CODE_DIR`에는 이 폴더, `OPSFLOW_SECRET_DIR`에는 worker 전용 보호
디렉터리의 정확한 경로를 지정합니다. 상속된 build를 `!reset`으로 제거하고
자동 pull을 막습니다. 기존 command·user·management network·volume는 유지하며
worker에만 DEV/object network와 `/run/opsflow`를 추가합니다. n8n 변경은 없습니다.

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
기존 DEV provisioner의 넓은 table grant를 실행하지 말고 함수 전용 권한 확장을
총괄이 먼저 통합해야 합니다. Pool 한 slot 생성도 별도 실행 대상입니다.

### Validation

실제 실행은 고정 이미지의 DAG import, SQL 직접 호출·역할/다른 DB/S3 거부,
Celery worker 게시·재실행·경합·backfill·객체 후 DB 실패 및 빈 대상 복원이
필요합니다. 관련 계약 미확정 상태에서는 이 항목을 NOT_RUN으로 기록합니다.
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
