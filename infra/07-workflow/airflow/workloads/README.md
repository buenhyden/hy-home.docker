---
title: "Airflow Workloads"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
---

# Airflow Workloads

## Overview

기존 Airflow에서 선택하는 개별 배치의 canonical source를 둡니다.
폴더 존재는 HOME 배포나 실행 승인을 뜻하지 않습니다.

## Scope

현재 독립 매니페스트 검증·게시 배치를 소유합니다. Airflow 이미지·관리 DB와
공통 네트워크는 기존 소유자를 따릅니다. Wiki와 학습 앱을 구현하지 않습니다.

## Structure

- [manifest-pipeline/](manifest-pipeline/README.md): DEV 매니페스트 배치.

## Usage

선택 workload의 README와 현재 Task를 읽고 합성시험부터 수행합니다.
실제 대상·권한·복구 경계가 확정되기 전에는 서비스를 시작하지 않습니다.

## Related Documents

- [Airflow](../README.md)
- [문서 탐색](../../../../docs/README.md)
