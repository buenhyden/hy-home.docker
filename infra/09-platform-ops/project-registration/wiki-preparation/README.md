---
title: "Wiki 준비 패키지"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# Wiki 준비 패키지

## Purpose

### Service Role

실제 Wiki 구현 전의 합성 계약과 미래 수용 기준을 정의합니다. SOURCE·UNIT·STATIC만 검증하며 ISOLATED·HOME·MIGRATION·ROTATION·RECOVERY·DELIVERY는 NOT_RUN입니다. owning Spec은 `SPEC-0204`이고 현재 Task ID는 `SPEC-0204-TSK-0008`입니다.

#### Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

#### Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

#### Structure

[제품 intake](product-intake/README.md), [consumer](consumer-contract/README.md), [원천·artifact](source-artifact-contract/README.md), [job·복구](job-outbox-generation/README.md), [blog 인계](blog-data-handoff/README.md), [미래 흐름](future-flows/README.md), [readiness](readiness/README.md), [준비 계약](contracts/README.md), [schema](schemas/README.md), [fixture](fixtures/README.md), [통합 제안](integration-proposal/README.md)

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

[문서 진입점](../../../../docs/README.md), [project registration 계약](../README.md), 현재 Task ID는 `SPEC-0204-TSK-0008`입니다.

### Observability and Recovery

없음: 실행되는 서비스가 아니므로 헬스체크·지표·로그가 없고, 이 패키지를 대상으로 하는 운영 런북도 `docs/05.operations/runbooks`에 없다. 계약 문서가 어긋나면 위 Checks의 단위 검사 실패로 드러나며, 복구는 Git 이력에서 해당 문서 변경을 되돌리는 것이다.
