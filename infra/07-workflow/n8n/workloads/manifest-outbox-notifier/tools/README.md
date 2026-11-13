---
title: "통지 workflow 생성 도구"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# 통지 workflow 생성 도구

## Purpose

### Service Role

공개 import JSON을 결정적으로 생성합니다. module import는 파일을 쓰지 않습니다.

#### Scope

외부 I/O·n8n import·SQL 설치·mail 전송·credential 작업을 수행하지 않습니다.

#### Structure

- [생성기](build_workflow.py): 순수 생성·닫힌 claim 검사·합성 상태 판정입니다.
- [preflight](preflight.py): 계약의 구조적 대기 조건을 보고합니다. 기록 자체로 운영 권한을 부여하지 않습니다.

### Supported Environment

Python 스크립트(`build_workflow.py`, `preflight.py`)이며 표준 라이브러리(`argparse`, `json`, `pathlib`, `datetime`, `re`)만 가져옵니다. 별도 이미지나 서비스는 없습니다.

## Interfaces

### Inputs and Outputs

입력은 `--output` 경로와 `--check` 옵션이고 출력은 `workflows/manifest-outbox-mailpit.json` 파일입니다. 네트워크 입출력은 없습니다.

### Security Boundary

없음: 외부 I/O·SQL 설치·mail 전송·credential 작업을 하지 않으며 생성된 JSON에는 credential placeholder만 들어갑니다.

## Development

### Local Workflow

저장소 루트에서 실행합니다.

```sh
python infra/07-workflow/n8n/workloads/manifest-outbox-notifier/tools/build_workflow.py \
  --output infra/07-workflow/n8n/workloads/manifest-outbox-notifier/workflows/manifest-outbox-mailpit.json
python infra/07-workflow/n8n/workloads/manifest-outbox-notifier/tools/build_workflow.py \
  --output infra/07-workflow/n8n/workloads/manifest-outbox-notifier/workflows/manifest-outbox-mailpit.json --check
```

출력 경로는 명시적으로 지정하며 `--check`는 drift를 보고하고 파일을 수정하지 않습니다.
검증된 P04 SHA·interface version·review 인계는 소비자 계약에 별도로 연결합니다.
workflow의 120초 timeout만으로 socket 취소를 주장하지 않습니다. 제한된 SMTP node가
소유 socket을 취소·정리하며, 실제 DB cancellation과 Worker 동작은 별도 native 증거입니다.
현재 P05는 기본 plain export를 유지하고 인증 capture profile을 fixture에서만 명시 선택합니다.

### Checks

`--check` 옵션이 생성 결과와 `workflows/manifest-outbox-mailpit.json`의 drift를 보고하며 파일은 수정하지 않습니다(위 Local Workflow 명령).

## Operations

### Runbook Links

- [워크로드](../README.md)
- [소비자 계약](../outbox-contract.json)

### Observability and Recovery

없음: 실행 후 종료하는 도구라 헬스체크·지표가 없습니다. `--check`가 drift를 보고하면 같은 명령에서 `--check`를 빼고 다시 생성하거나 Git 변경을 되돌려 복구합니다.
