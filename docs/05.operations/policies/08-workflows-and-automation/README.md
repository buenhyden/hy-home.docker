---
title: "워크플로와 자동화 정책"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 워크플로와 자동화 정책

## Overview

워크플로와 자동화의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

## Scope

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Airflow Operations Policy](0050-airflow.md) | `POL-0050` | 이 문서는 `hy-home.docker` 플랫폼의 Apache Airflow 운영 정책을 정의한다. 현재 구현은 Airflow와 `airflow-apiserver` 기반 Airflow 3 서비스 구성을 기준으로 한다. |
| [DAG Deployment Operations Policy](0052-airflow-dag-lifecycle.md) | `POL-0052` | 이 문서는 Airflow DAG의 배포 및 승격 정책을 정의합니다. 소스 코드 관리, 정적 분석 필수 항목 및 운영 환경 반영 절차를 규정합니다. |
| [n8n Operations Policy](0053-n8n.md) | `POL-0053` | 이 문서는 n8n 서비스의 안정적인 운영을 위한 정책과 통제 항목을 정의한다. 현재 구현은 `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker` queue-mode 구성을 기준으로 한다.  |
| [07-Workflow Optimization Hardening Operations Policy](0054-workflow-optimization-hardening.md) | `POL-0054` | 이 문서는 `07-workflow` 계층의 최적화/하드닝 운영 정책을 정의한다. gateway 경계 보안, health 기반 의존성, n8n 컨테이너 하드닝, 카탈로그 기반 확장 승인 기준을 통제한다. |

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
