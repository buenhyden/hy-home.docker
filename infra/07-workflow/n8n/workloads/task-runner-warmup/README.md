---
title: "n8n Task Runner 예열"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# n8n Task Runner 예열

## Purpose

### Service Role

launcher는 JS Task Runner를 첫 작업이 들어올 때 띄웁니다. 2026-11-09에는 재시작 뒤 첫
작업인 Hermes `devops` 제출에서 runner 등록까지 약 55초가 걸려, 제출 15초 제한과 흐름 30초
제한을 넘겼습니다. 이 흐름은 Hermes 정기 실행 10분 전인 매일 07:50 KST에 아무 일도 하지 않는
Code node를 한 번 실행해 runner를 미리 띄웁니다.

#### Scope

비활성 workflow 소스만 포함합니다. 외부 호출, 자격 증명, 저장 데이터는 없습니다.
운영 n8n에 가져오고 게시하는 일은 승인된 절차로만 수행합니다.

#### Structure

- [workflow.json](workflow.json): Schedule Trigger와 no-op Code node입니다.

### Supported Environment

n8n의 Schedule Trigger와 no-op Code node, 그리고 `N8N_RUNNERS_AUTO_SHUTDOWN_TIMEOUT: 0`으로 한 번 뜬 runner를 유지하는 n8n 설정을 전제로 합니다.

## Interfaces

### Inputs and Outputs

입력은 매일 07:50 KST의 Schedule Trigger 한 개입니다. no-op Code node라 출력 데이터와 외부 호출이 없습니다.

### Security Boundary

없음: 외부 호출·자격 증명·저장 데이터가 없는 비활성 workflow 소스입니다.

## Development

### Local Workflow

`N8N_RUNNERS_AUTO_SHUTDOWN_TIMEOUT: 0`이므로 한 번 뜬 runner는 컨테이너가 재시작될 때까지
유지됩니다. 재시작 뒤 첫 07:50 실행까지는 콜드 스타트가 남을 수 있습니다. 재시작 직후에
보고서를 제출해야 하면 n8n 편집기에서 이 흐름을 먼저 수동으로 실행합니다(미시험). 시작 노드가
스케줄 트리거뿐이라 `n8n execute --id`는 `Missing node to start execution`으로 실패합니다.
CLI로 게시한 변경은 n8n main을 재시작해야 반영됩니다.

### Checks

`workflow.json`은 `tests/validation/test_p03_runner_consumers.py`의 검사 대상 파일 목록에 들어 있습니다. runner 실제 기동은 Local Workflow의 수동 실행(미시험)으로만 확인할 수 있습니다.

## Operations

### Runbook Links

- [n8n 독립 워크로드](../README.md)
- [Hermes 수집 전송](../hermes-blog-ingestion/README.md)

### Observability and Recovery

없음: 전용 헬스체크·지표가 없습니다. 효과는 재시작 뒤 첫 Hermes 제출의 runner 등록 지연(약 55초)이 줄어드는지로 판단하며, 운영 n8n 반영 절차는 [n8n 독립 워크로드](../README.md)를 따릅니다.
