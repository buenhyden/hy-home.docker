---
title: "n8n Task Runner 예열"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-09"
---

# n8n Task Runner 예열

## Overview

launcher는 JS Task Runner를 첫 작업이 들어올 때 띄웁니다. 2026-11-09에는 재시작 뒤 첫
작업인 Hermes `devops` 제출에서 runner 등록까지 약 55초가 걸려, 제출 15초 제한과 흐름 30초
제한을 넘겼습니다. 이 흐름은 Hermes 정기 실행 10분 전인 매일 07:50 KST에 아무 일도 하지 않는
Code node를 한 번 실행해 runner를 미리 띄웁니다.

## Scope

비활성 workflow 소스만 포함합니다. 외부 호출, 자격 증명, 저장 데이터는 없습니다.
운영 n8n에 가져오고 게시하는 일은 승인된 절차로만 수행합니다.

## Structure

- [workflow.json](workflow.json): Schedule Trigger와 no-op Code node입니다.

## Usage

`N8N_RUNNERS_AUTO_SHUTDOWN_TIMEOUT: 0`이므로 한 번 뜬 runner는 컨테이너가 재시작될 때까지
유지됩니다. 재시작 뒤 첫 07:50 실행까지는 콜드 스타트가 남을 수 있습니다. 재시작 직후에
보고서를 제출해야 하면 n8n 편집기에서 이 흐름을 먼저 수동으로 실행합니다(미시험). 시작 노드가
스케줄 트리거뿐이라 `n8n execute --id`는 `Missing node to start execution`으로 실패합니다.
CLI로 게시한 변경은 n8n main을 재시작해야 반영됩니다.

## Related Documents

- [n8n 독립 워크로드](../README.md)
- [Hermes 수집 전송](../hermes-blog-ingestion/README.md)
