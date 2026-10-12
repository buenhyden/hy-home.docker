---
title: "분석과 데이터 품질 가이드"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 분석과 데이터 품질 가이드

## Overview

분석과 데이터 품질의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

## Scope

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [MLflow Usage Guide](0088-mlflow.md) | `GDE-0088` | MLflow는 `mlops` 또는 `data-science`가 선택하는 OPTIONAL experiment tracking server이다. HOME에도, 현재 8개 profile 운용 명령에도 들어 있지 않다. 추가하려면 별도로 활성화를 결정해야 한 |
| [JupyterLab Usage Guide](0089-jupyterlab.md) | `GDE-0089` | JupyterLab은 `data-science`만 선택하는 OPTIONAL single-user notebook server이며, 이 profile은 MLflow도 함께 선택한다. HOME에도, 현재 8개 profile 운용 명령에도 들어 있지 않다. |
| [dbt Usage Guide](0090-dbt.md) | `GDE-0090` | dbt는 `analytics-engineering`이 선택하는 OPTIONAL command-line 변환 작업이다. web UI가 없으므로 route나 OIDC client가 없고 필요하지도 않다. |
| [Lakehouse Usage Guide](0094-lakehouse.md) | `GDE-0094` | 레이크하우스는 OPTIONAL이며 `lakehouse`로 선택된다. 테이블은 SeaweedFS `lakehouse` 테이블 버킷 안의 Apache Iceberg이며 SeaweedFS 내장 Iceberg REST 카탈로그가 관리한다. Spark는 배치와 |
| [Superset Usage Guide](0097-superset.md) | `GDE-0097` | Superset은 `bi`로 선택되는 OPTIONAL BI 웹 애플리케이션이다. Trino를 통해 레이크하우스 테이블을 탐색하고 차트로 만든다. Grafana는 운영 관측 도구로 남고, Superset은 데이터 분석용이다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 가이드 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
