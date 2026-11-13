---
title: "합성 준비 schema"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# 합성 준비 schema

## Purpose

### Service Role

네 문서는 closed-object JSON Schema 2020-12입니다. consumer-manifest만 기존 registration schema의 메모리 URN을 사용합니다. caller는 허용 URN mapping을 제공하며 외부 $ref는 거절합니다. consumer의 Qdrant RBAC은 project-scoped collection과 non-admin role을 구조화하고, helper가 trusted caller policy와 project scope를 확인합니다. schema는 입력 형식, helper는 hash·선택·generation 등 교차 필드 정합을 검사합니다.

#### Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

#### Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

#### Structure

[consumer](consumer-manifest.schema.json), [source](source-artifact.schema.json), [job](job-outbox-handoff.schema.json), [blog](blog-data-handoff.schema.json)

### Supported Environment

기존 Python·jsonschema와 오프라인 JSON 문서를 사용합니다.

## Interfaces

### Inputs and Outputs

비밀값과 실제 환경 변수는 입력하지 않습니다.

### Security Boundary

없음: 이 디렉터리는 Markdown 문서와 합성 JSON만 두며 Compose 서비스·포트·네트워크·Docker Secret·접근 제어를 정의하지 않는다. 비밀값과 실제 환경 변수는 입력하지 않는다.

## Development

### Local Workflow

총괄의 공통 계약 통합 후 해당 증거를 Task에 연결합니다.

### Checks

저장소 루트에서 활성화한 격리 venv에 `python -m pip install -r scripts/requirements.txt`를 실행한 뒤 `python -m unittest tests.lib.ops.test_wiki_preparation tests.validation.test_wiki_preparation_contracts -v`를 실행합니다. 시스템의 오래된 jsonschema는 검증 환경이 아닙니다. 단위검사는 native 실행 증거가 아닙니다.

## Operations

### Runbook Links

문서 체계는 저장소 docs README 진입점을 통해 확인합니다.

### Observability and Recovery

없음: 실행되는 서비스가 아니므로 헬스체크·지표·로그가 없고, 이 패키지를 대상으로 하는 운영 런북도 `docs/05.operations/runbooks`에 없다. 계약 문서가 어긋나면 위 Checks의 단위 검사 실패로 드러나며, 복구는 Git 이력에서 해당 문서 변경을 되돌리는 것이다.
