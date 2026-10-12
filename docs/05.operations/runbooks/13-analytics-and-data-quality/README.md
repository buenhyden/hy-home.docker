---
title: "분석과 데이터 품질 런북"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 분석과 데이터 품질 런북

## Overview

분석과 데이터 품질의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [MLflow Recovery Runbook](0088-mlflow.md) | `RUN-0088` | MLflow tracking server의 프로비저닝 실패, 크리덴셜 회전, 복원, 업그레이드를 다루는 복구 런북이다. |
| [JupyterLab Recovery Runbook](0089-jupyterlab.md) | `RUN-0089` | JupyterLab의 시작 실패, 토큰 노출, 커널 정지, 작업 파일 손실, 이미지 업그레이드를 다루는 복구 런북이다. |
| [dbt Recovery Runbook](0090-dbt.md) | `RUN-0090` | dbt 프로비저닝 실패, 연결·권한 오류, 잘못된 모델 실행, 크리덴셜 교체를 다루는 런북이다. |
| [Lakehouse Recovery Runbook](0094-lakehouse.md) | `RUN-0094` | 레이크하우스의 Spark·Trino·Flink·Great Expectations 실패, 카탈로그 오류, 접근 거부, 테이블 롤백을 다루는 런북이다. |
| [Superset Runbook](0097-superset.md) | `RUN-0097` | Superset의 최초 설정, 로그인 실패, 웹 서버 비정상, 업그레이드를 다루는 런북이다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 런북 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
