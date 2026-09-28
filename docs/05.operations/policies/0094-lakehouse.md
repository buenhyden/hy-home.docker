---
title: "Lakehouse Operations Policy"
version: "1.3.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0094"
parent_ids:
- "AD-0004"
created: "2026-09-23"
---

# Lakehouse Operations Policy

## Overview

Iceberg 테이블은 내장 REST 카탈로그 뒤의 SeaweedFS 테이블 버킷 하나에 있다.
접근 범위, 파괴적 유지보수, 테스트 데이터의 분리가 통제 대상이다.

## Policy Scope

카탈로그 노출, 엔진 identity, namespace, 테이블 유지보수, 이미지 및 제거.

## Controls

- `lakehouse`를 통해서만 선택한다. HOME에는 절대 추가하지 않는다.
- 카탈로그는 `object_net`에 머물며 라우트도 host 포트도 없다. 엔진은
  `lakehouse` identity로 서명하며, 이 identity의 S3 액션과 테이블 버킷
  정책은 lakehouse 버킷만 다룬다. 정책은 열 개의 namespace 및 테이블 액션을
  나열하며 정책 변경과 버킷 삭제는 제외한다. 새 엔진은 이 identity를 재사용
  하거나 자체 범위의 identity를 받는다. 어떤 엔진도 admin identity를 쓰지
  않는다.
- `dev`와 `test`는 개발용 테이블과 테스트용 테이블을 보관한다. 운영과
  유사한 데이터는 별도로 승인된 namespace가 필요하다.
- Trino의 HTTP API는 인증이 없다. TLS와 인증기를 추가하는 검토된 변경이
  있기 전까지는 loopback host 포트만 열고 라우트는 없다. 기본 시작 상태는
  아무것도 쓰지 않는다.
- Flink의 REST API와 UI도 인증이 없다. loopback host 포트만 열고 라우트는
  없으며, `web.submit.enable=false`로 설정해 이를 통한 JAR 업로드를 막는다.
  job은 JobManager 컨테이너 내부의 SQL client에서 온다. 스트리밍 `INSERT`는
  취소될 때까지 계속 쓴다. job ID와 대상 테이블을 기록한다.
- Great Expectations는 읽기만 한다. suite는 읽기 전용으로 마운트된 추적
  파일이고, context는 ephemeral이며 `GX_ANALYTICS_ENABLED=false`다. 실패한
  suite는 테이블 소유자에게 전달할 발견 사항이지 suite를 바꿀 이유가 아니다.
- Spark의 기본 command는 읽기만 한다. `expire_snapshots`,
  `remove_orphan_files`, `DROP … PURGE`는 파일을 삭제하므로 명시된 테이블과
  기록된 이유가 필요하다. Trino의 `DROP TABLE`과 그 `expire_snapshots`/
  `remove_orphan_files` 테이블 프로시저도 동일하다.
- 엔진 이미지는 base 이미지와 Iceberg jar를 checksum으로 고정한다. Iceberg
  버전은 모든 엔진에서 함께 이동한다.

## Exceptions

없음. 카탈로그 credential vending이나 라우트를 활성화하려면 검토된 변경이
필요하다.

## Verification

Compose 렌더링, 카탈로그 확인, 그리고 범위가 한정된 identity가 테이블을
생성·쓰기·compact·삭제할 수 있고 다른 버킷은 읽을 수 없음을 증명하는
격리된 실행.

## Review Cadence

SeaweedFS, Iceberg, 엔진 업그레이드 시, 새 엔진 추가 시, 새 namespace가
생길 때마다 검토한다.

## Traceability

- [가이드](../guides/0094-lakehouse.md) (`GDE-0094`)
- [런북](../runbooks/0094-lakehouse.md) (`RUN-0094`)
- [SeaweedFS policy](0024-seaweedfs.md)

## Related Documents

- [Spark Compose source](../../../infra/04-data/lakehouse/spark/docker-compose.yml)
- [Trino Compose source](../../../infra/04-data/lakehouse/trino/docker-compose.yml)
- [Flink Compose source](../../../infra/04-data/lakehouse/flink/docker-compose.yml)
- [Great Expectations Compose source](../../../infra/04-data/lakehouse/great-expectations/docker-compose.yml)
- [Compose profile vocabulary](0078-compose-profile-vocabulary.md)
