---
title: "워크플로와 자동화 런북"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-12"
layer: "operations"
---

# 워크플로와 자동화 런북

## Overview

워크플로와 자동화의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Airflow Runbook](0050-airflow.md) | `RUN-0050` | 이 런북은 Apache Airflow 서비스 장애 발생 시 운영자가 즉시 수행할 수 있는 복구 절차를 정의한다. 현재 서비스명은 Airflow 3의 `airflow-apiserver`를 기준으로 한다. `dedicated-valkey` profile은 |
| [n8n Runbook](0053-n8n.md) | `RUN-0053` | 이 런북은 n8n 서비스 장애 발생 시 운영자가 신속하게 서비스를 복구하기 위한 단계별 절차를 제공한다. 현재 구현은 `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker`를 기준으로 하며  |
| [07-Workflow Optimization Hardening Runbook](0054-workflow-optimization-hardening.md) | `RUN-0054` | 이 런북은 `07-workflow` 하드닝 항목에서 발생하는 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. gateway/SSO 체인 누락, health dependency 회귀, n8n image/entrypoint drift, CI 게이트 실패 |

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
