---
title: "워크플로와 자동화 가이드"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "operations"
---

# 워크플로와 자동화 가이드

## Overview

워크플로와 자동화의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

## Scope

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Airflow Usage Guide](0050-airflow.md) | `GDE-0050` | 이 문서는 `hy-home.docker` 플랫폼의 Apache Airflow 시스템에 대한 가이드다. 현재 구현은 Airflow, `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`,  |
| [Airflow Dag Basics Operations](0051-airflow-dag-lifecycle.md) | `GDE-0051` | 이 문서는 `hy-home.docker` 환경에서 Airflow DAG를 작성하는 기본 방법과 권장 패턴을 설명합니다. |
| [n8n Usage Guide](0053-n8n.md) | `GDE-0053` | 이 가이드는 `hy-home.docker`의 n8n 로우코드 자동화 환경을 사용하는 방법을 설명한다. 현재 구현은 `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker` queue mode  |
| [07-Workflow Optimization Hardening Usage Guide](0054-workflow-optimization-hardening.md) | `GDE-0054` | 이 문서는 `07-workflow` 계층의 최적화/하드닝 변경을 운영자와 개발자가 재현 가능하게 적용하기 위한 가이드다. compose 보안 경계, health 기반 startup 계약, n8n 이미지 하드닝, 검증 절차를 제공한다. |

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
