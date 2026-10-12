---
title: "분석과 데이터 품질 정책"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 분석과 데이터 품질 정책

## Overview

분석과 데이터 품질의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

## Scope

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [MLflow Operations Policy](0088-mlflow.md) | `POL-0088` | MLflow는 OPTIONAL tracking 서비스다. MLflow의 데이터베이스와 artifact store는 공유 인프라 위의 feature-owned 자원이며 공유 인프라의 권한을 절대 넓혀서는 안 된다. |
| [JupyterLab Operations Policy](0089-jupyterlab.md) | `POL-0089` | JupyterLab은 임의의 코드를 실행한다. kernel이나 terminal에 도달할 수 있는 사람은 누구든 컨테이너와 컨테이너가 읽을 수 있는 모든 credential을 제어한다. |
| [dbt Operations Policy](0090-dbt.md) | `POL-0090` | dbt는 application 데이터베이스에 파생된 relation을 기록한다. 그 권한은 source 읽기와 target schema 소유로 제한해야 한다. |
| [Lakehouse Operations Policy](0094-lakehouse.md) | `POL-0094` | Iceberg 테이블은 내장 REST 카탈로그 뒤의 SeaweedFS 테이블 버킷 하나에 있다. 접근 범위, 파괴적 유지보수, 테스트 데이터의 분리가 통제 대상이다. |
| [Superset Operations Policy](0097-superset.md) | `POL-0097` | Superset는 자체 로그인, 메타데이터 데이터베이스, lakehouse 데이터 접근 권한을 가진 라우팅되는 웹 애플리케이션이다. 인증, role 부여, 자격 증명 처리가 통제 대상이다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 정책 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
