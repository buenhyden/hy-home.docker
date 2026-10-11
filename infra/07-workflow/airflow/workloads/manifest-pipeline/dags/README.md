---
title: "Manifest Pipeline DAG"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
---

# Manifest Pipeline DAG

## Overview

공개 `airflow.sdk`를 사용하는 단일 수동 배치입니다. 등록 중 workload 파일·DB·S3를 읽지 않습니다.

## Scope

최대 active run/task 각각 하나, pool 한 slot, timeout과 bounded retry를 선언합니다.
실제 pool 생성·Celery worker 실행은 별도 검증 대상입니다.

## Structure

- [source_manifest_ingest.py](source_manifest_ingest.py): 검증·보관·게시 한 task.

## Usage

현재 기본은 paused·schedule None입니다. Task 실행에서만 ingest 설정을 읽고
XCom에는 run ID·status·행수만 전달합니다. 예외는 고정된 실패 코드로 제한합니다.

## Related Documents

- [배치](../README.md)
- [Library](../workflow_lib/README.md)
